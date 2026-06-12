#!/usr/bin/env python3
"""
Generate Gemini captions for all 10 Pinky's Content images
and save to a state file for the next Buffer posting run.
"""

import json
import os
import requests
from datetime import datetime, timezone

GEMINI_KEY = "os.environ.get("GEMINI_KEY", "")"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"

PHONE_MAP = {
    "buffalo": "716-289-0764",
    "sarasota": "941-961-8070",
    "tampa": "813-417-8038",
}

# All 10 images with their Drive file IDs
IMAGES = [
    {"file_id": "1oIPeDeTr0KVWPrqdqK8X8I1bUGlqnkXf", "filename": "Pinkys_Fencing_Painting_Tampa_813-417-8038.png",        "service": "Fencing & Painting",    "location": "Tampa",    "phone": "813-417-8038"},
    {"file_id": "145fZCmXC5a7jCOlYtvRGrgCubdDE0DDd", "filename": "Pinkys_Fencing_Painting_Buffalo_716-289-0764.png",     "service": "Fencing & Painting",    "location": "Buffalo",  "phone": "716-289-0764"},
    {"file_id": "1o2W22vrZ8cU-30v4YQVqCU_2sF8U8ZrP", "filename": "Pinkys_Outdoor_Kitchens_Tampa_813-417-8038.png",       "service": "Outdoor Kitchens",      "location": "Tampa",    "phone": "813-417-8038"},
    {"file_id": "1fS7CBVr-J3rlVX36zLvo_4UKQxUu1bcw", "filename": "Pinkys_Outdoor_Kitchens_Sarasota_941-961-8070.png",    "service": "Outdoor Kitchens",      "location": "Sarasota", "phone": "941-961-8070"},
    {"file_id": "1pCVpYHNcS_LEke0CJXh_vawxTvL0XRHI", "filename": "Pinkys_Snow_Removal_Buffalo_716-289-0764.png",         "service": "Snow Removal",          "location": "Buffalo",  "phone": "716-289-0764"},
    {"file_id": "1U7uN0BrNU9huYTL6H0GeymH80-QI-8v5", "filename": "Pinkys_Landscaping_Tampa_813-417-8038.png",            "service": "Landscaping",           "location": "Tampa",    "phone": "813-417-8038"},
    {"file_id": "1Fr0BDJyKjoWMv1KShT3fUK7nfwiZwdKD", "filename": "Pinkys_Retaining_Walls_Sarasota_941-961-8070.png",    "service": "Retaining Walls",       "location": "Sarasota", "phone": "941-961-8070"},
    {"file_id": "142soQ6IIkpb_iKQQMYMWxs3SffzvuDfr", "filename": "Pinkys_Retaining_Walls_Buffalo_716-289-0764.png",     "service": "Retaining Walls",       "location": "Buffalo",  "phone": "716-289-0764"},
    {"file_id": "1RDFMXDbaEUEAWIq5Kni287Mg6zZLM5wd", "filename": "Pinkys_Concrete_Paving_Sarasota_941-961-8070.png",    "service": "Concrete & Paving",     "location": "Sarasota", "phone": "941-961-8070"},
    {"file_id": "1ckp_SICD-e2mbxyo-C73Fd4VJdsDc9LC", "filename": "Pinkys_Concrete_Paving_Buffalo_716-289-0764.png",     "service": "Concrete & Paving",     "location": "Buffalo",  "phone": "716-289-0764"},
]

def build_prompt(service, location, phone):
    return (
        f"Write a bold, confident social media caption for Pinky's Property Management advertising their "
        f"{service} service in {location}. "
        f"The caption must be under 150 words. "
        f"It should be punchy, professional, and speak directly to homeowners or property managers. "
        f"Include the phone number {phone} naturally in the copy. "
        f"End the caption with the website pinkyspropertymanagement.com on its own line, "
        f"followed by 3 to 5 relevant hashtags on the next line. "
        f"Do NOT use quotation marks around the caption. Output only the caption text."
    )

def call_gemini(prompt):
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    resp = requests.post(GEMINI_URL, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()

def main():
    state_path = "/home/ubuntu/pinkys_buffer_state.json"

    # Load existing state if present
    if os.path.exists(state_path):
        with open(state_path) as f:
            state = json.load(f)
    else:
        state = {"processed_file_ids": [], "pending_posts": []}

    already_processed = set(state.get("processed_file_ids", []))
    pending = state.get("pending_posts", [])
    pending_ids = {p["file_id"] for p in pending}

    generated = 0
    for img in IMAGES:
        fid = img["file_id"]
        if fid in already_processed:
            print(f"  SKIP (already posted): {img['filename']}")
            continue
        if fid in pending_ids:
            print(f"  SKIP (already queued): {img['filename']}")
            continue

        print(f"  Generating caption for: {img['filename']} ...", end=" ", flush=True)
        prompt = build_prompt(img["service"], img["location"], img["phone"])
        caption = call_gemini(prompt)
        print("done.")

        pending.append({
            "file_id": fid,
            "filename": img["filename"],
            "service": img["service"],
            "location": img["location"],
            "phone": img["phone"],
            "caption": caption,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "posted": False,
        })
        generated += 1

    state["pending_posts"] = pending
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    print(f"\n✅ {generated} new captions generated.")
    print(f"📋 {len(pending)} total posts pending in state file: {state_path}")

    # Print a preview of each caption
    for post in pending:
        print(f"\n{'='*60}")
        print(f"📸 {post['filename']}")
        print(f"{'='*60}")
        print(post["caption"])

if __name__ == "__main__":
    main()
