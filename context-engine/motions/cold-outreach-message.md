# Motion: Cold Outreach Message Framework

**Owner:** Rasul Shaikh  
**Inspired by:** [ Cold Outreach Messaging Framework](https://www./workflows/the-cold-outreach-message-playbook) (Dan Rosenthal)  
**Schema:** `profile/cold-outreach-message.json`  
**Production anchor:** `gtm-cold-email-personalizer`

## When to use

Writing E1 copy for Smartlead or HeyReach. You have enrichment data and need a repeatable formula: first line, 1-4 body blocks, one CTA, optional P.S., under 80 words.

## Rasul owns the implementation

| Layer | Repo | What it does |
|-------|------|--------------|
| First line | gtm-cold-email-personalizer | Playwright scrape + Claude opener |
| Body blocks | gtm-email-cadences | 23 YAML cadences, persona + signal routing |
| Clay assembly | gtm-clay-formula-library | Opener, body, CTA IIFEs |
| Variant scale | gtm-omnibound-clay-workflow | Cols 52-59, 144 hash-seeded variants |
| Word gate | gtm-omnibound-clay-workflow | Col 60 PASS + spam-word-checker |

 provides the **structure**. Rasul repos provide the **generators, validators, and send pipeline**.

## 5 steps

| # |  | Rasul implementation |
|---|--------------|----------------------|
| 1 | Strong first line (relevancy / observation / recency) | copy-framework.json hooks -> personalizer |
| 2 | Body: 1-4 components | email-cadences YAML + Omnibound cols 52-59 |
| 3 | One CTA (soft / resource / hard / colleague) | clay-formula-library CTA IIFE |
| 4 | Optional P.S. | Signal-led P.S. in cadence library |
| 5 | Under 70-80 words | Col 60 PASS validator |

## First line mapping

|  type | Rasul strategy | Example |
|-------------------|----------------|---------|
| Relevancy | Billboard | Whole-offer, clear ICP fit |
| Observation | Problem Sniffing | "I asked ChatGPT [keyword] and you ranked 15th..." |
| Recency | Signal-Led | "Post-raise, pipeline velocity matters..." |

## Body components (pick 1-4)

problem_statement, dream_outcome, poke_the_bear, case_study, problem_solution, personal_touch, social_proof, value, story, resource, offer

Omnibound production uses **problem_solution + social_proof + value** with live citation proof in cols 14-26.

## CTA by tier

| Tier | CTA type | Channel |
|------|----------|---------|
| Cool/Warm | Soft or Resource | Smartlead sequence |
| Hot | Hard | HeyReach 1:1 |
| Wrong persona | Colleague ask | Either |

## Gates before send

1. Col 60 PASS (word count + purple-safety)
2. List gate B+ (gtm-list-quality-scorecard)
3. Spam-word-checker on subject + body

## Run

```bash
python3 context-engine/engine/route.py --motion cold-outreach-message --signal content-engagement
```

Read schema: `profile/cold-outreach-message.json`