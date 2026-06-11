# Zapier Automation Configurations

> All Zap configurations for Pinky's Property Management operations automation.

---

## Zap 1: New Lead Notification

**Trigger**: New row added to Notion Lead Tracker database  
**Actions**:
1. Send Slack notification to `#leads` channel with lead details
2. Send SMS alert to market manager (based on Market field)
3. Create follow-up task in Notion with 1-hour deadline
4. Log lead source to analytics spreadsheet

**Filter**: Only triggers when Status = "New"

---

## Zap 2: Content Calendar to Buffer

**Trigger**: Notion Content Calendar entry status changes to "Scheduled"  
**Actions**:
1. Retrieve image from linked asset library
2. Format caption with market-specific hashtags
3. Create Buffer post for specified channel
4. Set publish time based on channel optimal schedule
5. Update Notion entry with Buffer post URL

**Filter**: Only triggers when Date is within next 7 days

---

## Zap 3: Bid Deadline Reminder

**Trigger**: Schedule — Daily at 8:00 AM EST  
**Actions**:
1. Search Notion Bid Pipeline for entries with Deadline within 48 hours
2. Filter for Status = "Estimating" or "Reviewing"
3. Send email digest to operations team
4. Send Slack alert to `#bids` channel
5. Create urgent task if deadline is within 24 hours

---

## Zap 4: Lead Follow-Up Automation

**Trigger**: Schedule — Every 4 hours  
**Actions**:
1. Search Lead Tracker for Status = "Contacted" with no activity in 48 hours
2. Send follow-up email template (market-specific)
3. Update Next Action field with "Automated follow-up sent"
4. If no response after 3 follow-ups, move to "Nurturing" status

---

## Zap 5: Social Media Lead Capture

**Trigger**: New DM or comment mention on Instagram/Facebook  
**Actions**:
1. Extract contact information from message
2. Create new Lead Tracker entry with Source = "Social Media"
3. Set Market based on geo-tags or message content
4. Send auto-reply with service information
5. Notify market manager via Slack

---

## Zap 6: ConstructConnect New Project Alert

**Trigger**: New project matching criteria on ConstructConnect  
**Actions**:
1. Create new Bid Pipeline entry with Platform = "ConstructConnect"
2. Set Status to "Identified"
3. Extract project details (name, GC, value, deadline)
4. Send notification to estimating team
5. Create assessment task with 24-hour deadline

---

## Zap 7: SmartBid Invitation Handler

**Trigger**: New bid invitation received on SmartBid  
**Actions**:
1. Create Bid Pipeline entry with Platform = "SmartBid"
2. Download bid documents
3. Send notification to operations manager
4. Create review task in Notion
5. Set initial deadline from invitation

---

## Zap 8: Weekly Content Performance Report

**Trigger**: Schedule — Every Monday at 9:00 AM EST  
**Actions**:
1. Pull Buffer analytics for past 7 days
2. Calculate engagement rates by channel and market
3. Identify top 3 performing posts
4. Generate summary report
5. Send to Chris Pegnia and marketing team via email
6. Post summary to `#content-performance` Slack channel

---

## Zap 9: Equipment Maintenance Reminder

**Trigger**: Schedule — First Monday of each month  
**Actions**:
1. Check Equipment Registry for vehicles approaching service intervals
2. Generate maintenance schedule for the month
3. Send to fleet manager
4. Create maintenance tasks in Notion
5. Alert if any vehicle is overdue

---

## Zap 10: Won Bid Celebration and Onboarding

**Trigger**: Bid Pipeline Status changes to "Won"  
**Actions**:
1. Send celebration notification to `#wins` Slack channel
2. Create project setup checklist in Notion
3. Assign project manager based on market
4. Generate client welcome email
5. Update Lead Tracker if client exists
6. Schedule kickoff meeting (3 business days out)

---

## Zap 11: Content Approval Workflow

**Trigger**: Content Calendar Status changes to "Needs Review"  
**Actions**:
1. Send approval request to Chris Pegnia via email
2. Include content preview (image + caption)
3. Provide approve/reject buttons
4. On approve: Change status to "Scheduled"
5. On reject: Change status to "Draft" and notify content creator

---

## Zap 12: Daily Operations Digest

**Trigger**: Schedule — Daily at 6:00 AM EST  
**Actions**:
1. Compile: New leads (last 24h), Bid deadlines (next 48h), Content scheduled today
2. Pull weather alerts for all 3 markets (snow ops trigger for Buffalo)
3. Format daily briefing email
4. Send to operations leadership team
5. Post to `#daily-ops` Slack channel

---

## Environment Variables Required

| Variable | Description |
|----------|-------------|
| `NOTION_API_KEY` | Notion integration token |
| `BUFFER_ACCESS_TOKEN` | Buffer API access |
| `SLACK_WEBHOOK_URL` | Slack incoming webhook |
| `CONSTRUCTCONNECT_API` | ConstructConnect credentials |
| `SMARTBID_API` | SmartBid integration |
| `GMAIL_OAUTH` | Gmail sending credentials |

---

## Zap Naming Convention

Format: `[Category] - [Trigger Source] → [Primary Action] (v[version])`

Examples:
- `[Leads] - Notion New Entry → Slack + SMS Alert (v2.1)`
- `[Content] - Calendar Scheduled → Buffer Post (v1.3)`
- `[Bids] - ConstructConnect New → Pipeline Entry (v1.0)`
