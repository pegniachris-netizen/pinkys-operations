#!/usr/bin/env python3
"""
Pinky's Content Engine — Buffer Posting Script
Reads pending_posts from state file and posts each image + caption
to all 5 Pinky's Buffer channels. Run after Buffer daily limit resets.

Buffer daily limit resets at: 1781268400 (unix) = ~12:46 PM EDT Jun 12 2026
"""

import json
import os
import sys
import time
import subprocess
import tempfile
import requests
from datetime import datetime, timezone

# ── Config ─────────────────────────────────────────────────────────────────
BUFFER_TOKEN   = "os.environ.get("BUFFER_TOKEN", "")"
GEMINI_KEY     = "os.environ.get("GEMINI_KEY", "")"
GEMINI_URL     = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
STATE_FILE     = "/home/ubuntu/pinkys_buffer_state.json"
DRIVE_FOLDER   = "1T7jNmdv2kgBOBJNKh7w68R49jzPuYwfa"
IMG_DIR        = "/home/ubuntu/pinkys_content_prep"
BUFFER_API     = "https://api.buffer.com/1"
BATCH_SIZE     = 10   # posts per batch before pausing
BATCH_PAUSE    = 90   # seconds between batches

# 5 Pinky's channel profile IDs — will be fetched from Buffer on first run
# and cached in the state file under "buffer_profile_ids"
CHANNEL_NAMES  = ["Instagram", "Threads", "TikTok Business", "Facebook", "LinkedIn"]

os.makedirs(IMG_DIR, exist_ok=True)

# ── Helpers ────────────────────────────────────────────────────────────────

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"processed_file_ids": [], "pending_posts": [], "buffer_profile_ids": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    print(f"  💾 State saved → {STATE_FILE}")

def check_buffer_rate_limit():
    """Returns (remaining, reset_ts) from Buffer API headers."""
    r = requests.get(f"{BUFFER_API}/user.json",
                     headers={"Authorization": f"Bearer {BUFFER_TOKEN}"}, timeout=15)
    remaining = int(r.headers.get("x-ratelimit-remaining", -1))
    reset_ts  = int(r.headers.get("x-ratelimit-reset", 0))
    return remaining, reset_ts, r.status_code

def get_buffer_profiles():
    """Fetch all Buffer profile IDs for Pinky's channels."""
    r = requests.get(f"{BUFFER_API}/profiles.json",
                     headers={"Authorization": f"Bearer {BUFFER_TOKEN}"}, timeout=15)
    if r.status_code == 429:
        raise RuntimeError("Buffer rate limited — cannot fetch profiles yet.")
    r.raise_for_status()
    profiles = r.json()
    # Filter to Pinky's channels only (exclude personal accounts)
    pinkys = []
    for p in profiles:
        username = (p.get("formatted_username") or p.get("service_username") or "").lower()
        service  = p.get("service", "").lower()
        # Include all profiles that belong to Pinky's (not chrispegnia personal)
        if "chrispegnia" not in username and "learningwithleaders" not in username:
            pinkys.append({
                "id":       p["id"],
                "service":  p.get("service"),
                "username": p.get("formatted_username") or p.get("service_username"),
            })
    return pinkys

def download_image(file_id, dest_path):
    """Download a Drive image using gws CLI."""
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        return True
    result = subprocess.run(
        ["gws", "drive", "files", "get",
         "--params", json.dumps({"fileId": file_id}),
         "--output", dest_path],
        capture_output=True, text=True
    )
    return result.returncode == 0 and os.path.exists(dest_path)

def generate_caption(service, location, phone):
    """Call Gemini to generate a social media caption."""
    prompt = (
        f"Write a bold, confident social media caption for Pinky's Property Management "
        f"advertising their {service} service in {location}. "
        f"Under 150 words. Punchy, professional, speaks to homeowners or property managers. "
        f"Include the phone number {phone} naturally. "
        f"End with pinkyspropertymanagement.com on its own line, "
        f"then 3-5 relevant hashtags on the next line. "
        f"Output only the caption text, no quotes."
    )
    resp = requests.post(GEMINI_URL, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

def post_to_buffer(profile_id, image_path, caption):
    """Post an image + caption to a single Buffer profile. Returns (success, status_code)."""
    with open(image_path, "rb") as img_file:
        # Step 1: Upload media
        upload_resp = requests.post(
            f"{BUFFER_API}/media/upload.json",
            headers={"Authorization": f"Bearer {BUFFER_TOKEN}"},
            files={"file": (os.path.basename(image_path), img_file, "image/png")},
            timeout=60
        )
    if upload_resp.status_code == 429:
        return False, 429
    if upload_resp.status_code not in (200, 201):
        print(f"    ⚠️  Media upload failed ({upload_resp.status_code}): {upload_resp.text[:200]}")
        return False, upload_resp.status_code

    media_id = upload_resp.json().get("id") or upload_resp.json().get("media_id")

    # Step 2: Create update (post to queue)
    payload = {
        "profile_ids[]": profile_id,
        "text": caption,
        "now": "false",
    }
    if media_id:
        payload["media[photo]"] = media_id

    post_resp = requests.post(
        f"{BUFFER_API}/updates/create.json",
        headers={"Authorization": f"Bearer {BUFFER_TOKEN}"},
        data=payload,
        timeout=30
    )
    if post_resp.status_code == 429:
        return False, 429
    success = post_resp.status_code in (200, 201)
    if not success:
        print(f"    ⚠️  Post failed ({post_resp.status_code}): {post_resp.text[:200]}")
    return success, post_resp.status_code

# ── Scan Drive for new images ───────────────────────────────────────────────

def scan_drive_for_new_images(state):
    """List images in Drive folder, return those not already processed or pending."""
    result = subprocess.run(
        ["gws", "drive", "files", "list",
         "--params", json.dumps({
             "q": f'"{DRIVE_FOLDER}" in parents and mimeType contains "image/" and trashed = false',
             "fields": "files(id,name,mimeType,createdTime)",
             "pageSize": 100,
             "orderBy": "createdTime desc"
         })],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️  Drive scan error: {result.stderr[:200]}")
        return []

    files = json.loads(result.stdout).get("files", [])
    processed_ids = set(state.get("processed_file_ids", []))
    pending_ids   = {p["file_id"] for p in state.get("pending_posts", [])}

    new_files = []
    for f in files:
        if f["id"] not in processed_ids and f["id"] not in pending_ids:
            new_files.append(f)
    return new_files

def parse_filename(filename):
    """Extract service, location, phone from filename like Pinkys_Fencing_Painting_Tampa_813-417-8038.png"""
    name = filename.replace("Pinkys_", "").replace(".png", "").replace(".jpg", "").replace(".jpeg", "")
    phone_map = {"716-289-0764": "Buffalo", "941-961-8070": "Sarasota", "813-417-8038": "Tampa"}
    phone, location = None, None
    for ph, loc in phone_map.items():
        if ph in name:
            phone    = ph
            location = loc
            name     = name.replace(f"_{ph}", "").replace(f"_{loc}", "")
            break
    service = name.replace("_", " ").strip()
    return service, location, phone

# ── Main ───────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*60}")
    print(f"  Pinky's Content Engine — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    state = load_state()

    # ── 1. Check Buffer rate limit ──────────────────────────────────────────
    print("📡 Checking Buffer rate limit...")
    remaining, reset_ts, status = check_buffer_rate_limit()
    if status == 429 or remaining == 0:
        reset_dt = datetime.fromtimestamp(reset_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC") if reset_ts else "unknown"
        print(f"  ⛔ Buffer rate limited. Resets at: {reset_dt}")
        print("  Captions are saved in state file. Will retry on next scheduled run.")
        save_state(state)
        return
    print(f"  ✅ Buffer OK — {remaining} requests remaining today.\n")

    # ── 2. Fetch Buffer profile IDs (cache in state) ────────────────────────
    if not state.get("buffer_profile_ids"):
        print("📋 Fetching Buffer channel IDs...")
        profiles = get_buffer_profiles()
        state["buffer_profile_ids"] = profiles
        save_state(state)
        print(f"  Found {len(profiles)} Pinky's channels:")
        for p in profiles:
            print(f"    • {p['service']:12} | {p['username']:30} | {p['id']}")
    else:
        profiles = state["buffer_profile_ids"]
        print(f"📋 Using {len(profiles)} cached Buffer channel IDs.\n")

    if not profiles:
        print("  ⚠️  No Buffer profiles found. Check token.")
        return

    # ── 3. Scan Drive for new images ────────────────────────────────────────
    print("🔍 Scanning Google Drive for new images...")
    new_images = scan_drive_for_new_images(state)
    if new_images:
        print(f"  Found {len(new_images)} new image(s) — generating captions...")
        for img in new_images:
            service, location, phone = parse_filename(img["name"])
            if not phone:
                print(f"  ⚠️  Could not parse phone from: {img['name']} — skipping")
                continue
            print(f"  ✍️  Caption for: {img['name']} ...", end=" ", flush=True)
            caption = generate_caption(service, location, phone)
            print("done.")
            state["pending_posts"].append({
                "file_id":      img["id"],
                "filename":     img["name"],
                "service":      service,
                "location":     location,
                "phone":        phone,
                "caption":      caption,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "posted":       False,
            })
        save_state(state)
    else:
        print("  No new images found.\n")

    # ── 4. Post pending items to Buffer ────────────────────────────────────
    pending = [p for p in state["pending_posts"] if not p.get("posted")]
    if not pending:
        print("✅ No pending posts. All caught up.")
        return

    print(f"\n🚀 Posting {len(pending)} pending item(s) to {len(profiles)} channels each...\n")
    posted_count  = 0
    skipped_count = 0
    batch_posts   = 0

    for i, post in enumerate(pending):
        fid       = post["file_id"]
        fname     = post["filename"]
        caption   = post["caption"]
        img_path  = os.path.join(IMG_DIR, fname)

        print(f"  [{i+1}/{len(pending)}] {fname}")

        # Download image
        if not download_image(fid, img_path):
            print(f"    ⚠️  Could not download image — skipping")
            skipped_count += 1
            continue

        # Post to each channel
        all_ok = True
        for profile in profiles:
            pid   = profile["id"]
            svc   = profile.get("service", "?")
            uname = profile.get("username", pid)
            print(f"    → {svc:12} | {uname:30}", end=" ", flush=True)
            ok, code = post_to_buffer(pid, img_path, caption)
            if ok:
                print("✅")
                batch_posts += 1
            elif code == 429:
                print("⛔ rate limited")
                print(f"\n  ⛔ Hit rate limit mid-run after {posted_count} posts. Saving state and stopping.")
                save_state(state)
                return
            else:
                print(f"❌ ({code})")
                all_ok = False
            time.sleep(1)  # 1s between channel posts

        if all_ok:
            # Mark as posted
            for p in state["pending_posts"]:
                if p["file_id"] == fid:
                    p["posted"] = True
            state["processed_file_ids"].append(fid)
            posted_count += 1
            save_state(state)

        # Batch pacing
        if batch_posts > 0 and batch_posts % BATCH_SIZE == 0:
            print(f"\n  ⏸  Batch pause ({BATCH_PAUSE}s) to avoid rate limits...\n")
            time.sleep(BATCH_PAUSE)

        time.sleep(2)  # 2s between images

    print(f"\n{'='*60}")
    print(f"  ✅ Done. {posted_count} images posted, {skipped_count} skipped.")
    print(f"  State file: {STATE_FILE}")
    print(f"{'='*60}\n")
    save_state(state)

if __name__ == "__main__":
    main()
