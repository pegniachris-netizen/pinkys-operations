# Workflow Diagrams

> Visual documentation of all automated workflows in the Pinky's operations system.

---

## Content Pipeline Flow

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  Content Plan   │────▶│  AI Generate │────▶│   Review    │────▶│   Schedule   │
│  (Notion Cal)   │     │  (Images)    │     │  (Approve)  │     │  (Buffer)    │
└─────────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
        │                                           │                      │
        ▼                                           ▼                      ▼
  Market Rotation                            Brand Check              9 Channels
  Mon=Buffalo                                Logo ✓                   Auto-post
  Tue=Tampa                                  Colors ✓                 Analytics
  Wed=Sarasota                               Voice ✓                  Report
```

---

## Lead Generation Flow

```
┌──────────────┐
│   INBOUND    │
├──────────────┤
│ • Website    │
│ • Phone      │──────┐
│ • Social     │      │     ┌──────────────┐     ┌─────────────┐
│ • Email      │      ├────▶│ Lead Tracker │────▶│  Qualify    │
│ • Referral   │      │     │   (Notion)   │     │  (1 hour)   │
└──────────────┘      │     └──────────────┘     └──────┬──────┘
                      │                                   │
┌──────────────┐      │                          ┌───────┴───────┐
│   OUTBOUND   │      │                          │               │
├──────────────┤      │                     ┌────▼────┐    ┌─────▼─────┐
│ • CC         │──────┘                     │Proposal │    │ Nurturing │
│ • SmartBid   │                            │  Sent   │    │  (Auto)   │
│ • Procore    │                            └────┬────┘    └───────────┘
│ • LinkedIn   │                                 │
└──────────────┘                            ┌────▼────┐
                                            │Won/Lost │
                                            └─────────┘
```

---

## Bid Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        BID PIPELINE                                   │
├─────────────┬──────────────┬─────────────┬───────────┬──────────────┤
│ Identified  │  Reviewing   │ Estimating  │ Submitted │   Result     │
│             │              │             │           │              │
│ • CC Alert  │ • Site Visit │ • Materials │ • Package │ • Won → PM   │
│ • SmartBid  │ • Scope Rev  │ • Labor     │ • Submit  │ • Lost → Log │
│ • Procore   │ • Go/No-Go   │ • Equipment │ • Track   │ • No Bid     │
│ • Direct    │              │ • Margin    │           │              │
└─────────────┴──────────────┴─────────────┴───────────┴──────────────┘
      │               │              │            │             │
      ▼               ▼              ▼            ▼             ▼
   24 hours       48 hours      Per scope    By deadline    Notify team
```

---

## Daily Operations Cycle

```
6:00 AM  ─── Daily Digest Email (weather, leads, bids, content)
7:00 AM  ─── First social posts go live (TikTok, chrispegnia)
8:00 AM  ─── Bid deadline check + alerts
9:00 AM  ─── Facebook, LinkedIn, Learning with Leaders posts
10:00 AM ─── Threads posts, YouTube uploads
12:00 PM ─── Midday posts across all channels
1:00 PM  ─── Lead follow-up automation runs
3:00 PM  ─── Threads afternoon post
5:00 PM  ─── LinkedIn, Learning with Leaders evening posts
6:00 PM  ─── Instagram evening post
7:00 PM  ─── TikTok evening posts
8:00 PM  ─── Threads evening post
9:00 PM  ─── chrispegnia TikTok evening post
```

---

## Integration Map

```
                    ┌─────────────────┐
                    │     NOTION      │
                    │  (Central Hub)  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────┐  ┌─────▼─────┐  ┌────▼────────┐
     │   BUFFER    │  │  ZAPIER   │  │    SLACK     │
     │ (Scheduling)│  │  (Glue)   │  │  (Alerts)   │
     └────────┬────┘  └─────┬─────┘  └─────────────┘
              │              │
    ┌─────────┼─────────┐   │
    │         │         │   │
┌───▼──┐ ┌───▼──┐ ┌───▼──┐ │   ┌──────────────┐
│TikTok│ │  FB  │ │  IG  │ │   │ConstructConn │
│      │ │      │ │      │ ├──▶│   SmartBid   │
│ x2   │ │      │ │ x2   │ │   │   Procore    │
└──────┘ └──────┘ └──────┘ │   └──────────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
        ┌─────▼───┐  ┌─────▼───┐  ┌─────▼───┐
        │LinkedIn │  │ YouTube │  │ Threads │
        │   x2    │  │         │  │         │
        └─────────┘  └─────────┘  └─────────┘
```
