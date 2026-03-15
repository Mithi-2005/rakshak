# 🛡️ RAKSHAK — Income Shield for India's Delivery Warriors

> **Team · Code Warriors** from SRM University AP

```
"Rakshak" (रक्षक) = Protector in Sanskrit.
When the rain stops your ride — Rakshak pays you.
Automatically. Fairly. Based on income actually lost.
```

## 📋 Table of Contents

## 📋 Table of Contents

1. [The Problem](#1-the-problem)
2. [Our Solution](#2-our-solution)
3. [Persona — Who We Protect](#3-persona--who-we-protect)
4. [Complete Platform Workflow](#4-complete-platform-workflow)
5. [System Architecture](#5-system-architecture)
6. [Parametric Triggers](#6-parametric-triggers)
7. [Weekly Premium Model](#7-weekly-premium-model)
8. [AI / ML Integration](#8-ai--ml-integration)
9. [Fraud Detection Architecture](#9-fraud-detection-architecture)
10. [Platform Choice](#10-platform-choice)
11. [Tech Stack](#11-tech-stack)
12. [System Scalability](#12-system-scalability)
13. [Business Viability](#13-business-viability)
14. [What Rakshak Does NOT Cover](#14-what-rakshak-does-not-cover)
15. [Team](#15-team)


---

## 1. The Problem

India has *12+ million active food delivery partners* on Zomato and Swiggy.

| Reality | Impact |
|--------|--------|
| Average daily earnings | ₹600 – ₹900 |
| Income lost during disruptions | 20 – 30% per month |
| Disruption days per year (avg) | 18 – 22 days |
| Existing safety net | ❌ None |

When a Red Alert rainstorm hits Hyderabad, or AQI crosses 300 in Delhi, or a sudden bandh shuts down Mumbai — delivery partners *lose their entire day's income* with zero recourse. No employer, no union, no insurance was built for them.

---
## 2. Our Solution

Rakshak is an AI-enabled parametric income insurance platform built exclusively
for food delivery partners on Zomato, Swiggy, and similar platforms.

| Core Feature     | What It Means                                               |
|------------------|-------------------------------------------------------------|
| Mobile App + Web | Single backend supporting two frontends                     |
| Parametric       | Payout triggered by data, not claim forms                   |
| AI-powered       | **1)** Premium pricing + claim amount calculation           |
|                  | **2)** Disruption monitoring + claim initiation             |
|                  | **3)** Fraud detection                                      |
| Weekly pricing   | Multiple plans · dynamic prices aligned to gig pay cycles   |
| Instant payout   | UPI transfer immediately on claim approval                  |


---

## 3. Persona — Who We Protect

*Segment:* Food Delivery Partners — Zomato & Swiggy


Name:         Ravi/Suresh/Farhan(composite persona) 
Age:          22 – 38 years
Education:    10th – 12th pass
Weekly earn:  ₹3,000 – ₹6,000
City:         Hyderabad , Bengaluru , Mumbai(pilot zones)
Pain point:   "Kal barish thi, ek bhi order nahi mila."
              (It rained yesterday, I got zero orders.)


### Real-World Persona Scenarios

*Scenario A — Ravi, Swiggy Partner, Hyderabad*
> IMD declares Red Alert. Rainfall exceeds 55mm/hr. Ravi cannot ride out.
> *Rakshak:* Weather trigger fires → claim auto-created → ₹600 UPI transfer in 6 minutes.
> Ravi receives  "Heavy rain confirmed in your zone. ₹600 credited. Stay safe."

*Scenario B — Suresh, Zomato Partner, Bengaluru (BTM Layout)*
> AQI hits 340 at 9 AM. Order volume in BTM drops 62% (platform crash trigger also fires).
> *Rakshak:*   AQI trigger or Platform demand drop trigger  → ₹1,062 payout processed.

*Scenario C — Farhan, Swiggy Partner, Mumbai*
> State-wide transport strike called. NewsAPI NLP detects "bandh Mumbai" with 91% confidence.
> *Rakshak:* Band Trigger → GPS confirms Farhan is in covered zone → ₹750 credited.


---
## 4. Complete Platform Workflow

> **The key design principle:** The trigger monitoring (Step 4) only detects *that* a disruption happened and *how long* it lasted. No money is decided there. All payout logic runs at **11:50 PM** when actual platform delivery data is available for cross-checking.

---

### STEP 1 — Worker Onboarding

```
Login/Signup

Worker provides:
  ├─ Name · City · Pincode · Platform (Zomato/Swiggy) etc
  ├─ Registered shift hours  (e.g. 10 AM – 9 PM) (can also be fetched from platform)
  └─ UPI ID

System verifies:
  ├─ OTP 
  ├─ Delivery partner ID cross-check (mock platform API)
  

Stored in DB:
  ├─ Worker profile + zone mapping (pincode → weather station)


CRITICAL — Shift window registration:
  Triggers only fire during the worker's registered shift hours.
  Rain at 3 AM when worker is asleep → no timer starts → no claim.
```

---

### STEP 2 — AI Risk Profiling *(ML )*

```
Runs immediately after onboarding. Background, instant.

ML Model
Inputs:   Pincode flood index · 3-yr AQI average · disruption frequency
          · current season · 7-day forecast · worker tenure etc
Output:   Zone Risk Score (0–100) + Risk Tier (Low/Med/High/Extreme)
          Respective Premium Plans(dynamic prices)&
          Recommended weekly tier



```

---

### STEP 3 — Weekly Policy Purchase

```
 presents 3 AI-recommended tiers:
                                                example prices
  Bachao   ₹P1/wk  — Rain + Heat only         — Max ₹800/wk
  Suraksha ₹P2/wk  — +AQI +Curfew  ★ AI pick  — Max ₹1,500/wk
  Kavach   ₹P3/wk  — All 5 triggers            — Max ₹2,500/wk

Worker replies "2" (or tier name)
→ Razorpay UPI collect request sent via WhatsApp
→ Worker pays with GPay / PhonePe / Paytm
→ Policy activated: 7-day coverage window begins

On activation:
  ├─ Policy record created (ID · start · end · cap · triggers enabled)
  ├─ Monitoring job registered for worker's pincode zone
  └─ Sunday renewal nudge scheduled
```

---

### STEP 4 — Real-Time Disruption Monitoring *(24/7)*

> **This step ONLY detects disruptions and records their duration. No payout amount is calculated here.**

```
Architecture: BullMQ job queue polls 5 sources every 15 minutes
              Redis caches latest readings per zone

For each active zone per trigger:

  IF threshold crossed AND current time is within worker's shift window:
    → Log disruption START: timestamp · API reading · zone
    → Mark event: ACTIVE

  Continue polling every 15 min...

  IF threshold drops below limit:
    → Log disruption END: timestamp
    → Calculate duration = end − start (in hours, decimal)
    → Event stored: { type, start, end, duration_hrs, peak_reading, zone }

  IF threshold never drops (e.g. all-day bandh):
    → End timer at 11:45 PM (5 min before reconciliation)
    → Duration = full shift window overlap

The 5 triggers:

  T1  Rain          OpenWeatherMap API   > 35mm/hr OR IMD Red Alert
  T2  Extreme heat  OpenWeatherMap API   Feels-like > 44°C, 10AM–4PM window only
  T3  Hazardous AQI WAQI API             AQI > 300 for 2+ hrs
  T4  Curfew/bandh  NewsAPI + NLP        "bandh/curfew/strike", confidence > 80%
  T5  Platform drop Mock platform API    Order volume drop > 60% vs 4-week baseline


```

---
### STEP 5 — 11:50 PM Nightly Income Reconciliation

> **This is where payouts are actually calculated.**
> Runs once per day at **11:50 PM** after all disruption windows for the day are finalized.

```
For every worker with:
  ├─ Active policy
  └─ ≥1 disruption event recorded today

System processes each disruption event individually.

──────────────────────────────────────────────────────────────
A. Pull actual delivery data
──────────────────────────────────────────────────────────────

Fetch from mock platform API:

Worker's orders completed per hour slot today.

Example:
  { 10AM:3, 11AM:4, 12PM:2, 1PM:3, 2PM:1, 3PM:0, 4PM:1 }

──────────────────────────────────────────────────────────────
B. Load worker baseline
──────────────────────────────────────────────────────────────

IF worker has ≥4 weeks of history:

  Use personal 4-week average for same:
    ├─ Day-of-week
    └─ Hour slots

Example baseline:
  { 2PM:3.2, 3PM:3.5, 4PM:2.8 }

IF worker history insufficient (new worker / shift change):

  ML baseline estimation predicts expected orders using:
    ├─ Zone-level patterns
    ├─ Day-of-week
    ├─ Time slot
    └─ Event calendar

Formula remains identical — only baseline source changes.

──────────────────────────────────────────────────────────────
C. Intersect with disruption window
──────────────────────────────────────────────────────────────

Example disruption window:
  2:15 PM – 4:30 PM  (2.25 hours)

Only hour slots INSIDE this window are evaluated.
All other hours ignored.

──────────────────────────────────────────────────────────────
D. Calculate actual income loss
──────────────────────────────────────────────────────────────

orders_lost = Σ (baseline[hr] − actual[hr]) for hrs in window

income_lost = orders_lost × avg_earning_per_order

avg_earning_per_order is taken from worker's historical earnings
average stored during onboarding.

──────────────────────────────────────────────────────────────
E. Prorated cap calculation
──────────────────────────────────────────────────────────────

hourly_rate = tier_daily_max ÷ 8 working hours

event_cap   = hourly_rate × disruption_duration_hours

Example (Suraksha tier):

  hourly_rate = ₹600 ÷ 8 = ₹75/hr
  event_cap   = ₹75 × 2.25 = ₹168.75

──────────────────────────────────────────────────────────────
F. Final payout rule
──────────────────────────────────────────────────────────────

payout = MIN(income_lost, event_cap)

Guarantees:
  ├─ Never pays more than actual income loss
  ├─ Never exceeds tier payout cap
  └─ Worker must actually lose orders to qualify

──────────────────────────────────────────────────────────────
G. Claim decision
──────────────────────────────────────────────────────────────

IF payout > ₹20
  → Create claim record → Step 6

IF payout ≤ ₹20
  → Dismiss silently

IF worker performed above baseline
  → Dismiss silently

IF disruption outside shift window
  → Event never logged (blocked in Step 4)

```

---

### STEP 6 — Claim Pathways

> Claims are created only after reconciliation confirms **real income loss**.

```
Two claim types exist:

  PATH A — Automatic Claim
  PATH B — Worker Self-Report

Both eventually enter the fraud verification pipeline.
```

---

#### PATH A — Automatic Claim (~80%)

```
Triggered by:
  Reconciliation job detecting payout > ₹20

Worker action required:
  None

System auto-creates claim with evidence bundle:

  ├─ Trigger type           (e.g. HEAVY_RAIN)
  ├─ API reading value      (e.g. 52mm/hr at 14:30)
  ├─ Source URL snapshot
  ├─ Disruption window
  ├─ Duration
  ├─ Zone confirmation
  ├─ Baseline orders
  ├─ Actual orders
  └─ Calculated payout

Worker notification (after fraud check passes):

  "Disruption detected in your zone.
   Claim #XXXXX created.
   Verifying — payout in ~10 minutes."

Fraud signals checked for Path A:

  ├─ GPS zone match
  ├─ Device activity during shift
  ├─ Platform API data authenticity
  ├─ Duplicate claim detection
  └─ Claim frequency anomaly
```

---

#### PATH B — Worker Self-Report (~20%)

```
Used when:
  Real disruption occurred but API trigger was missed.

Example:
  Hyper-local flash flood not detected by weather API.
```

Worker flow:

```
Worker texts:  CLAIM
       │
       ▼
Website asks disruption type:

  1 Heavy rain / flood
  2 Extreme heat
  3 Poor air quality
  4 Curfew / bandh
  5 App not working / no orders

Worker selects option
       │
       ▼
Bot asks for ONE proof:

  ├─ Photo of disruption
  ├─ News alert screenshot
  └─ Delivery app screenshot showing 0 orders

Worker uploads image
       │
       ▼
Website response:

  "Claim submitted.
   Verification in progress (~30 minutes)"
```

Extra **Media Verification layer** runs first:

```
Checks performed:

  ├─ EXIF timestamp (photo within last 6 hrs)
  ├─ GPS metadata match
  ├─ Duplicate image hash detection
  ├─ NewsAPI corroboration
  └─ Platform order volume cross-check

Path B uses stricter approval threshold:
  Auto-approve only if fraud score < 0.60
```

---

### STEP 7 — 3-Layer Fraud Verification

```
All claims (Path A + Path B) pass through:

  LAYER 1 — Rule-Based Filter
  LAYER 2 — GPS Location Validation
  LAYER 3 — Isolation Forest ML Model
```

---

Layer 1 — Rules (<1 sec)

```
Reject if:

  ├─ Duplicate UPI across accounts
  ├─ Claim before API trigger threshold
  ├─ Weekly payout cap exhausted
  ├─ Policy expired or unpaid
  └─ Same trigger already paid today
```

---

Layer 2 — GPS Validation (<5 sec)

```
Zone mismatch > 15km        → +0.30 fraud score
Impossible GPS velocity     → AUTO-REJECT
No location pings in 4 hrs  → +0.20 fraud score
Zone switched < 48 hrs      → +0.15 fraud score
```

---

Layer 3 — Isolation Forest ML (<10 sec)

```
Features used:

  ├─ Claim frequency vs zone norm
  ├─ Earnings ratio
  ├─ Time-of-day claim distribution
  ├─ Claim-to-disruption correlation
  └─ Device fingerprint uniqueness

Output:
  Fraud score between 0.00 – 1.00
```

Decision routing:

```
0.00 – 0.74   → AUTO APPROVE (Path A)
0.00 – 0.60   → AUTO APPROVE (Path B)
0.75 – 0.89   → HOLD (admin review)
0.90 – 1.00   → AUTO REJECT
```

---

### STEP 8 — Instant UPI Payout

```
Triggered when:
  Claim passes fraud verification.

Payment flow:

  Razorpay Payout API
        │
        ▼
  Worker UPI ID

Transfer time:
  < 6 minutes
```

Worker receives WhatsApp confirmation:

```
"₹169 transferred successfully.

 Trigger: Heavy Rain
 Window: 2:15 PM – 4:30 PM
 Claim ID: XXXXX"
```

System ledger updates:

```
  ├─ Weekly payout cap reduced
  ├─ Claim marked SETTLED
  └─ Analytics event fired for insurer dashboard
```


---

## 5. System Architecture
![Rakshak Architecture](./architecture.jpg) 

Rakshak uses a modular microservice-style architecture consisting of: 
- API Gateway (Django REST) 
- Core Platform Services 
- AI/ML Models for pricing, fraud detection, and loss estimation 
- External disruption data APIs 
- Instant payout integration via Razorpay

### Architecture Highlights 
• Trigger Monitoring continuously polls weather, AQI, and news APIs using Celery jobs. 
• When disruptions occur, the Claims & Reconciliation Engine calculates income loss. 
• AI/ML models assist with premium pricing, risk scoring, and fraud detection. 
• Verified claims trigger instant payouts through Razorpay UPI. 
• PostgreSQL stores policies and claims while Redis handles caching.

---



## 6. Parametric Triggers (**Estimated)

| # | Trigger | Source | Threshold | Payout Rate | Notes |
|---|---------|--------|-----------|-------------|-------|
| T1 | Heavy rain | OpenWeatherMap | > 35mm/hr OR IMD Red Alert | ₹600/day base | Real free API |
| T2 | Extreme heat | OpenWeatherMap | Feels-like > 44°C · 10AM–4PM | ₹400/day base | Peak hours only |
| T3 | Hazardous AQI | WAQI API | AQI > 300 for 2+ hrs | ₹500/day base | Real free API |
| T4 | Curfew / bandh | NewsAPI + NLP | Keywords + confidence > 80% | ₹750/day base | NLP-scored |
| T5 | Platform crash | Mock platform API | Order volume drop > 60% vs baseline | ₹350/day base | Unique to food delivery |

**"Payout rate" is a ceiling, not a flat amount.** Actual payout = MIN(prorated hourly rate × disruption hours, actual income loss calculated).


---

## 7. Weekly Premium Model

### Why weekly?

Gig workers earn daily and budget weekly. Monthly feels unaffordable. Weekly feels like skipping two chai breaks.

### Tiers

```
**Example plans**
┌──────────────────┬──────────┬──────────────────┬──────────────────────────┐
│ Tier             │ Price/wk │ Max Payout/week  │ Triggers                 │
├──────────────────┼──────────┼──────────────────┼──────────────────────────┤
│ Bachao (Basic)   │ ₹29      │ ₹800             │ T1 + T2                  │
│ Suraksha (Std) ★ │ ₹49      │ ₹1,500           │ T1 + T2 + T3 + T4        │
│ Kavach (Premium) │ ₹79      │ ₹2,500           │ All 5 + composite bonus  │
└──────────────────┴──────────┴──────────────────┴──────────────────────────┘
  ★ AI-recommended default for most workers
```

### Dynamic pricing (using ML model)


---

## 8. AI / ML Integration

Rakshak uses **4 distinct ML modules**, each at a different stage of the pipeline.

### Module 1 — Dynamic Premium Engine *(Step 2)*
```
Purpose:    Personalize weekly premium per worker per zone
Features:   Pincode flood index · season · 7-day forecast ·
            disruption frequency · worker tenure · claim history
Output:     Weekly price + zone risk tier
Update:     Every Sunday 11 PM
```

### Module 2 — Zone Risk Profiler *(Step 2)*
```
Algorithm:  K-Means Clustering on pincode-level disruption data
Purpose:    Cluster zones into risk tiers for heat-map + pricing input
Input:      IMD flood maps · WAQI records · curfew history per pincode
Output:     Risk Score 0–100 + Tier (Low/Medium/High/Extreme)
Visual:     Live heat-map on insurer admin dashboard
```

### Module 3 — Income Loss Calculator *(Step 5)*
```

Purpose:    Calculate actual income lost during disruption window
Inputs:     Worker's actual orders (platform API) · 4-week baseline ·
            disruption duration · avg earnings per order
Output:     Payout amount = MIN(actual loss, prorated cap)
Key logic:  Never pays more than actual loss. Never pays for time
            outside shift window. Never pays if worker performed above baseline.
```

### Module 4 — Isolation Forest Fraud Detector *(Step 7)*
```
Framework:  scikit-learn via Python FastAPI microservice
Features:   Claim frequency vs zone norm · earnings ratio ·
            device fingerprint uniqueness · time distribution ·
            claim-to-disruption correlation
Output:     Fraud Score 0.00–1.00
Routing:    < 0.74 auto-approve (Path A) · < 0.60 auto-approve (Path B)
            0.75–0.89 hold · > 0.90 reject
```


---

## 9. Fraud Detection Architecture

```
PATH A (auto claims):
  Pre-check:  Evidence bundle integrity (API snapshot timestamp,
              zone match, platform data authenticity)
  → L1 Rule filter → L2 GPS validation → L3 Isolation Forest
  Auto-approve if score < 0.74

PATH B (self-report claims):
  Pre-check:  MEDIA VERIFICATION first
              EXIF timestamp (within 6 hrs) · Duplicate image hash ·
              GPS metadata · NewsAPI corroboration · Platform cross-check
  → L1 Rule filter → L2 GPS validation → L3 Isolation Forest
  Auto-approve only if score < 0.60  (stricter)

LAYER 1 — Rules (instant):
  Duplicate UPI · claim before threshold · cap exceeded ·
  policy inactive · same event already paid

LAYER 2 — GPS (< 5 sec):
  Zone mismatch > 15km +0.30 · velocity impossible → reject ·
  no pings in 4 hrs +0.20 · zone switched < 48hr +0.15

LAYER 3 — ML based Isolation Forest (< 10 sec):
  5-feature anomaly model → score 0.00–1.00

Score routing:(**Estimated)
  0.00–0.74 (A) / 0.00–0.60 (B)  → AUTO-APPROVE → payout
  0.75–0.89                        → HOLD 2 hrs → admin review
  0.90–1.00                        → AUTO-REJECT → appeal offered
```

---
## 10. Platform Choice

**Decision: Mobile App + Web App for workers · Web Dashboard for admin · Single shared backend**

| Layer            | Platform          | Users          | Reason                                          |
|------------------|-------------------|----------------|-------------------------------------------------|
| Worker frontend  | Mobile App(primary) | Delivery partners | Native GPS · push notifications · camera upload · UPI deep-links |
| Worker frontend  | Web App (PWA)     | Delivery partners | Access from any browser · no install needed · same features as app |
| Admin frontend   | Web Dashboard     | Insurer / ops team | Large screen for heat-maps · fraud queue · analytics · bulk actions |
| Backend          | Single REST API   | Both frontends | One codebase serves all — no duplication        |

### Why both Mobile + Web for workers?

- **Mobile App** — best experience for active delivery partners.
  Native GPS tracking, camera for proof upload, UPI deep-links,
  push notifications for instant payout alerts. Works offline for
  claim drafting, syncs when reconnected.

- **Web App** — fallback for workers without storage space or those
  on older devices. Same features, accessible from any browser.
  No install friction. Shareable via WhatsApp link.

- **Single backend** — both frontends hit the same REST API.
  Claim logic, fraud detection, payout rules all live in one place.
  One change propagates to both platforms instantly.


---

## 11. Tech Stack

### Backend
| Component | Technology |
|-----------|----------- |
| API server | Django     |
| ML service | Python    |
| ML models | scikit-learn |
| Database | PostgreSQL  |
| Cache | Redis — real-time trigger readings per zone |
| Job queue | Celery + Redis — 15-min trigger polling + 11:50 PM reconciliation batch |

### Frontend
| Component | Technology |
|-----------|----------- |
| web dashboard(admin + user) | React.js + Tailwind CSS  |
| mobile app | Flutter |

### Integrations (Subjected to change)
| Service | Tool | Mode |
|---------|------|------| |
| Weather (T1, T2) | OpenWeatherMap API | Free tier |
| AQI (T3) | WAQI API | Free tier |
| Curfew (T4) | NewsAPI + custom NLP | Free tier |
| Platform data (T5 + reconciliation) | Custom mock API | Simulated JSON |
| Payments | Razorpay | Test mode |
| Maps / zone boundaries | Google Maps JS API | Free tier |

### Infrastructure
| Component | Service |
|-----------|---------|
| Hosting | Railway.app / AWS EC2 t2.micro |
| Database | Supabase (PostgreSQL free tier) |
| CI/CD | GitHub Actions |

---

## 12. System Scalability

Rakshak is designed to scale across millions of workers using a **zone-based
trigger monitoring model**.

Instead of running trigger checks individually for every worker:

• Disruption triggers are monitored **once per geographic zone**  
• Workers are mapped to zones using their registered pincode  
• A single disruption event is applied to all workers in that zone  

Example:

Heavy rain detected in **Hyderabad Zone 3**

→ Trigger recorded once  
→ Applied to all workers mapped to that zone  
→ Nightly reconciliation calculates income loss per worker

This architecture ensures the system can support **millions of workers
without linear infrastructure growth**.
---

---

## 13. Business Viability

| Metric | Estimate |
|--------|---------|
| Food delivery partners in India | ~12 million |
| Pilot cities (Hyderabad + Bengaluru + Mumbai) | ~900,000 |
| Average weekly premium | ₹49 |
| Annual revenue at 1% penetration | ₹22.8 Cr/year |
| Expected claim ratio | 35–45% of premium pool |
| Expected disruption days per partner/year | 18–22 |
| Target payout settlement time | < 12 min (reconciliation + transfer) |

**Why the hybrid model improves unit economics:**
Traditional parametric pays full daily rate whenever a trigger fires. Rakshak's reconciliation model pays only actual loss, bounded by a prorated cap. This reduces expected payout per event by an estimated 35–50% compared to flat-rate parametric — making the pool sustainable at lower premiums while still being meaningful to workers.

---

## 14. What Rakshak Does NOT Cover

Per the Guidewire DEVTrails Golden Rules:

```
❌  Health or medical expenses
❌  Accident injuries or hospitalization
❌  Vehicle repair or maintenance costs
❌  Life insurance
❌  Theft of personal property
❌  Vehicle EMI support

✅  Rakshak covers ONE thing only:
    INCOME LOST due to external, uncontrollable disruptions —
    verified against actual delivery data, not just weather readings.
```

---

## 15. Team (Flexible Roles)

| Name | Role(Primary) |
|------|------|
| *K V Mithilesh* | Team Lead/AIML Engineer |
| *SK Mohammad* | Backend/AIML |
| *T Suman yadav* | Backend/AIML |
| *Praveen Ramisetty* | Frontend/Backend |
| *Ch Yaswitha* | Frontend/Database |

**University:** SRM University AP
**Hackathon:** Guidewire DEVTrails 2026

---

```
╔══════════════════════════════════════════════════════════════╗
║  The difference between Rakshak and every other parametric   ║
║  insurance product:                                          ║
║                                                              ║
║  We don't pay because it rained.                             ║
║  We pay because YOU lost income when it rained.              ║
║  And we prove it with data before transferring a rupee.      ║
╚══════════════════════════════════════════════════════════════╝

Guidewire DEVTrails 2026 · Phase 1 Submission · March 20, 2026
```