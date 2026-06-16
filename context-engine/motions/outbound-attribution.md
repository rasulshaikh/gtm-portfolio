# Motion: Outbound Attribution 2026

**Source:** [ Outbound Attribution Playbook](https://www./workflows/outbound-attribution-playbook)  
**Production anchor:** `gtm-omnibound-clay-workflow` (HubSpot sync + send logging)  
**Rasul:** `multi-signal` (north-star: positive reply rate, not reply rate alone)

## When to use

Outbound touches Smartlead/HeyReach but CRM shows "Direct" or "Organic" signups. You need every touch logged in HubSpot, outbound-influenced signups tagged, and pipeline attributed to channel.

## Rasul stack note

 uses **OutboundSync + Instantly**. This implementation maps to **n8n clay-push + Smartlead/HeyReach** with the same HubSpot property model.

## 7 steps (implemented)

| # | Step |  | Rasul implementation |
|---|------|--------------|----------------------|
| 1 | Connect outreach to CRM | OutboundSync + Instantly/HeyReach | n8n clay-push-pipeline.json |
| 2 | Core HubSpot properties | Outbound Campaign + Sign Up checkboxes | HubSpot custom props via n8n |
| 3 | Auto-tag contacts | Contact + company level | Clay col + HubSpot upsert |
| 4 | Track signups | Outbound Influenced Signups | product-signup webhook + Slack |
| 5 | Deal stages + reporting | Outbound Influenced to Closed Won | HubSpot deal automation |
| 6 | Hidden impact | Silent visits, LinkedIn effect, delayed | gtm-founder-led-loop capture |
| 7 | Revenue engine | Full-funnel influence metric | 1.5%+ positive reply north star |

## HubSpot properties

| Property | Type | Set when |
|----------|------|----------|
| `outbound_campaign` | Checkbox | Any Smartlead/HeyReach touch fires |
| `sign_up` | Checkbox | Product form or trial signup |
| `outbound_influenced_signup` | Checkbox | Sign up = TRUE AND outbound_campaign = TRUE |
| `outbound_channel` | Dropdown | email, linkedin, mixed |
| `first_outbound_touch_date` | Date | First logged touch |

## Deal stage model

```
Outbound Influenced -> Signed Up -> Activated -> Closed Won
```

Build HubSpot dashboard: **Outbound -> Signup -> Revenue** by channel.

## Hidden impact capture

| Type | Detection | Repo |
|------|-----------|------|
| Silent website conversion | RB2B/Warmly visitor after email | gtm-founder-led-loop |
| LinkedIn effect | Profile views, content engagement | gtm-founder-led-loop/01 |
| Off-channel | Manual Slack tag from rep | HubSpot note |
| Delayed conversion | Signup 14-30d after sequence | HubSpot workflow delay |

## Success metric shift

| Old metric | New metric |
|------------|------------|
| Reply rate only | Positive reply rate (north star) |
| CRM source = Direct | Outbound Influenced Signup flag |
| Channel guesswork | Smartlead vs HeyReach dashboard |

## Run

```bash
python3 context-engine/engine/route.py --motion outbound-attribution
```

Import n8n: `gtm-omnibound-clay-workflow/n8n/clay-push-pipeline.json`