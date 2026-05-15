# Case Study Analysis — Why Your Model Lies
**DataTech 2026 · Sabin K. Pradhan**

---

## Case Study 1: The Feed Ranking Model

### Setup

You're on the ranking team at a content platform. Your ML model predicts engagement (likes, comments, shares) on posts in a feed. Feature importance analysis comes back and the #1 driver is **"time since post creation"** — a recency signal — with an importance score of 0.23.

Your product manager says: *"Boost recent posts. That's what people want."*

The question is: does feature importance tell you what to build?

---

### Option A — Audit the signal before acting *(Good Start)*

**The decision:** Before running any experiment, normalize engagement by impressions in the training data. Check whether recency predicts engagement *rate* — not raw engagement counts — after controlling for post exposure.

**Why this is directionally right, but only a diagnostic:**

The feed was roughly chronological, so recent posts got more impressions, which mechanically produced more raw engagement. Dividing engagement by impressions controls for that exposure bias.

**Concrete example:**

- Post A (1 hour old): shown to 12,000 users, 480 likes → engagement rate = 4.0%
- Post B (3 days old): shown to 3,000 users, 90 likes → engagement rate = 3.0%

Raw engagement says recency matters (480 > 90). Engagement rate still shows a gap — but a much smaller one. Run this across all posts and age buckets. If the recency gradient collapses when you control for impressions, the signal was a feedback loop artifact. If it holds, something real is there.

This is the right first move: question the signal before acting on it. But it only answers *whether* recency is real — not *why* it matters or *what* to build.

**The insight:** Auditing the signal tells you if recency is real. It doesn't tell you what mechanism is driving it — or what intervention will move the needle.

---

### Option B — Run a 2-arm A/B test *(Better)*

**The decision:** Treatment gets a 2x multiplier for posts under 2 hours. Control gets baseline ranking. Measure engagement over 7 days.

**Why this is more complete, but the mechanism stays ambiguous:**

Option A told you the signal survives exposure debiasing. Option B tests whether acting on it moves the product. That's progress — you're now measuring causal impact, not just auditing correlation.

You run the test and see a small lift. But two things changed at once:
1. The ranking signal (recency weight increased)
2. The content shown (recent posts are, by definition, posts users haven't seen yet in this session)

**Concrete example:**

A user opens the app on Tuesday at 6pm.

- **Control:** The feed shows Post X, a well-performing post from Sunday. The user scrolled past it on Monday. They skip it again.
- **Treatment:** Post X gets pushed down. Post Y, posted two hours ago, fills the slot. The user hasn't seen it before. They tap through.

The test records a click. But if you'd surfaced *any* unseen post in that slot — even a 4-day-old post the user had never encountered — you'd likely see the same result. The lift could be from recency preference, or from novelty. You can't tell which, and they lead to completely different product decisions.

**The insight:** The test tells you the metric moved. It doesn't tell you whether recency or novelty moved it — and you need to know before you can scale or generalize the result.

---

### Option C — 3-arm test with longitudinal outcomes *(Best Practice)*

**The decision:** Add a third arm — unseen-content boost (any post this user hasn't seen, regardless of age). Measure D30 retention and session frequency alongside immediate engagement.

**Why this completes the analysis:**

Option B revealed an ambiguity: is the lift from recency or novelty? Option C is designed specifically to answer that question.

**The experiment design:**

- **Arm 1:** Recency boost — posts under 2 hours get a 2x multiplier
- **Arm 2:** Unseen-content boost — surface the highest-quality post this user hasn't seen yet, regardless of age
- **Arm 3:** Baseline

If Arm 1 ≈ Arm 2, the mechanism is novelty, not recency. The real lever is surfacing unseen content — a completely different product decision than a recency boost.

**Why longitudinal metrics matter:**

A short-term engagement bump can mask long-term feed degradation. If the recency boost fills the feed with low-quality new posts that users click once and don't return to, session frequency and D30 retention will decline even as 7-day engagement looks healthy. Measuring both prevents optimizing the wrong outcome.

**What the results show:**

Arm 1 ≈ Arm 2 in immediate engagement. Arm 1 underperforms Arm 2 on D30 retention — low-quality recent posts don't bring users back. The conclusion: recency was a proxy for unseen content, not a cause of engagement. The right product intervention is a freshness filter (don't re-show posts users have already seen), not a recency boost.

**The insight:** The real lever wasn't time — it was unseen content relevant to that user. That's a completely different product decision than a recency boost.

---

## Case Study 2: The Retention Problem

### Setup

You're a data scientist on a mobile app team. Retention is falling. The analytics team runs a cohort analysis comparing 30-day retention across users who did and didn't enable push notifications.

The numbers:

| Group | 30-Day Retention |
|---|---|
| With notifications enabled | 45% |
| Without notifications | 28% |
| **Difference** | **+17 percentage points** |

Your product manager says: *"Get more people to enable notifications. If we move 50% of new users, we'll boost retention by 8–9 points."*

The question is: does enabling notifications cause users to stay, or are we observing something else?

---

### Option A — Segment the data before acting *(Good Start)*

**The decision:** Before running any experiment, break the 17pp gap down by user engagement tier. Check whether the gap holds within high-engagement and low-engagement users separately.

**Why this is directionally right, but still observational:**

The 17pp aggregate gap is suspicious because it conflates two very different populations. Power users — people already invested in the product — both enable notifications and stay retained. Casual users do neither. If user type is the real driver, the gap should shrink dramatically within each tier.

**Concrete example:**

Break the cohort by engagement level before looking at notifications:

- **High-engagement users:** 52% retention with notifications, 48% without — a 4pp gap
- **Low-engagement users:** 22% retention with notifications, 20% without — almost no gap

The 17pp aggregate was almost entirely a composition effect: the notification-enabled group was disproportionately made up of high-engagement users, not a signal that notifications cause retention.

This is the right first move — you've named the likely confounder before spending on an experiment. But it's still observational. You've found correlation within segments, not causation. The confounder explanation could still be incomplete.

**The insight:** Segmenting the data identifies the confounder. It doesn't prove it — and it doesn't tell you what intervention will actually move retention.

---

### Option B — A/B test the onboarding prompt *(Better)*

**The decision:** Treatment sees a notification opt-in prompt during onboarding. Control doesn't. Measure 30-day retention.

**Why this is more complete, but the treatment arm is underspecified:**

Option A gave you a hypothesis about the confounder. Option B moves to causal experimentation — that's progress. But this test bundles three distinct changes into a single treatment arm, and you can't separate them.

**The three confounds in the treatment:**

1. **The prompt itself.** Seeing a screen about notifications may signal that the app has real-time value worth engaging with — regardless of whether the user taps "allow." The nudge alone could affect behavior.
2. **Actual notification delivery.** Only the subset of treatment users who opted in receives push notifications. Their behavior gets averaged into the full treatment group, masking the effect.
3. **Self-selection.** Users who choose to opt in are already more engaged than those who decline. Their retention reflects who they are, not what notifications did.

**Concrete example:**

Treatment retention = 37%, control = 35%. A 2-point lift.

But break down treatment:
- Opted in: 48% retention (mostly power users, retained regardless)
- Declined: 31% retention (casual users, same as control)
- Blended: 37% — a composition artifact, not a notification effect

If you make the prompt more aggressive and bring in more casual users, the blended average drops. You've scaled a finding that wasn't real.

**The insight:** Randomizing the prompt doesn't randomize opt-in. The lift could be the feature, the friction, or the type of user who said yes — and you need to know which before you can scale it.

---

### Option C — Stratified experiment within engagement tiers *(Best Practice)*

**The decision:** Segment users by engagement level first, then randomize the notification prompt within each stratum. Compare like-for-like populations.

**Why this completes the analysis:**

Option A named the confounder. Option B ran a causal test but left the confound inside the treatment arm. Option C controls for the confounder before randomizing, so you're finally comparing equivalent users.

**The experiment design:**

Stratify into engagement tiers before any randomization:
- **High-engagement users:** completed onboarding, multiple sessions in week one, deep feature usage
- **Low-engagement users:** dropped off early, minimal sessions, skipped key onboarding steps

Run the notification prompt test within each tier separately. Now treatment and control within each stratum are comparable populations.

**What the results show:**

- Within low-engagement users: notifications have almost no effect. These users churn because the product didn't fit their needs — a push notification doesn't change that.
- Within high-engagement users: a small convenience, not a meaningful retention driver. They were already coming back.

When you hold user type constant, the 17pp gap disappears entirely. It was never a notification effect — it was a label that said "power user."

**The actual problem:**

The data now points at the real issue: onboarding. Users who don't find value in week one churn regardless of notification status. The right intervention is fixing the first-session experience, not prompting for notifications.

**The insight:** When you see a correlation, ask what confounder could explain it. Stratify to control for it — then the real problem becomes visible.

---

## The Pattern Across Both Cases

Both case studies share the same failure mode: **acting on a correlation as if it were a causal lever.**

| | Case Study 1 | Case Study 2 |
|---|---|---|
| **Observed correlation** | Recency → engagement | Notifications → retention |
| **Assumed mechanism** | Users prefer recent content | Notifications keep users active |
| **Actual mechanism** | Recent posts got more exposure | Invested users do both |
| **The confounder** | Feed design (chronological bias) | User type (power vs. casual) |
| **Wrong fix** | Boost recent posts | Push notification opt-in |
| **Right question** | Does recency cause engagement, or does exposure? | Does notification opt-in cause retention, or are we observing power users? |

The model learned accurately in both cases. Same question each time: is this a causal lever, or just a pattern the data learned?

---

*From the DataTech 2026 talk: "Why Your Model Lies — Causal Reasoning in Product Data Science"*
*Sabin K. Pradhan · linkedin.com/in/sabinkpradhan*
