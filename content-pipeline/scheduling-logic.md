# Content Scheduling Logic

> Core scheduling algorithm for Pinky's Property Management multi-channel content distribution.

---

## Market Rotation Algorithm

The content calendar follows a strict market rotation to ensure equal coverage across all three markets:

| Day of Week | Market | Rationale |
|-------------|--------|-----------|
| Monday | Buffalo | Start of work week, B2B focus |
| Tuesday | Tampa | Mid-week engagement peak |
| Wednesday | Sarasota | HQ market, mid-week |
| Thursday | Buffalo | Second touch, residential focus |
| Friday | Tampa | Weekend prep content |
| Saturday | Sarasota | Weekend engagement |
| Sunday | Buffalo | Week preview content |

**Pattern**: Buffalo → Tampa → Sarasota → Repeat (3-day cycle mapped to 7-day week)

---

## Channel Distribution Per Day

Each day features content across 3 channels (rotating through all 9):

```
Day 1:  TikTok Business, Facebook, Instagram
Day 2:  LinkedIn Company, Threads, Chris Pegnia LinkedIn
Day 3:  Chris Pegnia YouTube, chrispegnia TikTok, Learning with Leaders IG
Day 4:  TikTok Business, Facebook, Instagram
Day 5:  LinkedIn Company, Threads, Chris Pegnia LinkedIn
Day 6:  Chris Pegnia YouTube, chrispegnia TikTok, Learning with Leaders IG
...repeat
```

This ensures every channel gets content every 3 days minimum.

---

## Content Type Rotation

Each channel has 3 content themes that rotate:

### TikTok Business
1. Before/after transformation (Reel)
2. Equipment showcase (Video)
3. Day in the life (Reel)

### Facebook
1. Service spotlight (Photo)
2. Community engagement (Carousel)
3. Customer testimonial (Video)

### Instagram
1. Fleet photo (Photo)
2. Project showcase (Carousel)
3. Crew spotlight (Reel)

### LinkedIn Company
1. Industry insight (Article)
2. Hiring announcement (Photo)
3. Partnership update (Photo)

### Threads
1. Quick tip (Photo)
2. Behind the scenes (Photo)
3. Hot take (Photo)

### Chris Pegnia LinkedIn Personal
1. Leadership lesson (Article)
2. Business growth story (Photo)
3. Industry perspective (Article)

### Chris Pegnia YouTube
1. Vlog - job walkthrough (Video)
2. Business education (Video)
3. Equipment review (Video)

### chrispegnia TikTok Personal
1. Entrepreneur life (Reel)
2. Motivation (Reel)
3. Funny moment (Reel)

### Learning with Leaders Instagram
1. Leadership quote (Photo)
2. Interview clip (Reel)
3. Book recommendation (Carousel)

---

## Scheduling Rules

1. **No duplicate markets on same channel within 3 days** — Each channel should feature a different market each time it posts
2. **No duplicate content types on same channel within 3 days** — Rotate through all 3 themes
3. **Minimum 7-day buffer** — Always have at least 7 days of content scheduled ahead
4. **Holiday override** — Special content for major holidays supersedes rotation
5. **Weather trigger** — Snow events in Buffalo trigger emergency snow content across all channels
6. **Performance override** — Top-performing content types get extra slots (reviewed weekly)

---

## Caption Template Variables

All captions use these template variables filled at generation time:

| Variable | Source | Example |
|----------|--------|---------|
| `{market}` | Day's market rotation | "Buffalo" |
| `{service}` | Rotating service list | "lawn care" |
| `{equip}` | Rotating equipment list | "F250" |
| `{phone}` | Market-specific phone | "(716) PINKYS-1" |
| `{hashtag_market}` | Market hashtag | "#Buffalo" |

---

## 30-Day Content Volume

| Metric | Count |
|--------|-------|
| Total posts in 30 days | 90 |
| Posts per channel (avg) | 10 |
| Markets featured per week | All 3 |
| Unique content themes | 27 (3 per channel × 9 channels) |
| Content types used | 6 (Video, Photo, Carousel, Reel, Story, Article) |
