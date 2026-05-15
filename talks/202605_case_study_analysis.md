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

### Option A — Launch the notification push

**The decision:** Build an aggressive onboarding prompt. Get as many users as possible to enable push notifications.

**Why this is wrong:**

The 17-point gap is real. But it's not caused by notifications. It's caused by user type.

Power users — people who are genuinely invested in the product — do two things: they enable notifications (because they want to stay up to date) and they return over 30 days (because the product matters to them). Casual users do neither.

The notification opt-in rate and the retention rate are both *symptoms* of the same underlying condition: how invested a user is. They move together because a common cause drives both of them, not because one causes the other.

**Concrete example:**

- **User A** (power user): downloads the app, completes onboarding, enables notifications, uses the app 4x per week, still active at day 30.
- **User B** (casual user): downloads the app, skips notifications, opens the app twice, churns by day 10.

Now you build an aggressive notification prompt. User B, who was going to churn anyway, sees the prompt and enables notifications. What happens?

User B still churns at day 10. Getting a push notification doesn't change the fact that the product didn't fit their needs. You moved the notification opt-in rate, but you didn't treat the underlying problem.

**The insight:** You forced the symptom without treating the cause. Opt-in predicts retention because invested users do both. Promoting one doesn't create the other.

---

### Option B — A/B test the onboarding prompt

**The decision:** Treatment group sees a notification opt-in prompt during onboarding. Control doesn't. Measure 30-day retention.

**Why this is better, but the experiment design is flawed:**

Testing is the right move. But this test has three simultaneous changes inside the treatment arm, and you can't separate them.

**The three confounds:**

1. **The prompt itself.** Users in treatment see an onboarding screen about notifications. Just having that screen — regardless of whether they tap "allow" — may affect behavior. It signals that the app has real-time features worth staying for. That nudge alone could lift retention slightly.

2. **Actual notification delivery.** Among users who opt in, they now receive push notifications. This is potentially the real intervention — but it only applies to the subset of treatment users who said yes.

3. **Self-selection within treatment.** Users who choose to opt in are already more engaged than those who decline. Their 30-day retention was higher before the experiment started. When you average the treatment group together (opted in + declined), you're mixing two populations with very different baseline retention rates.

**Concrete example:**

You run the test. Treatment retention = 37%. Control retention = 35%. You report a 2-point lift.

But break down the treatment group:
- Treatment users who opted in: 48% retention (mostly power users who would have been retained anyway)
- Treatment users who declined: 31% retention (casual users, same as control)
- Blended treatment average: 37% (looks like a lift, but it's the composition of the group, not the notifications)

The PM wants to scale this. You have a lift you can't explain, driven by a segment you can't control for at scale. If you triple the prompt aggressiveness and bring in more casual users, the blended average drops — and you've mistaken statistical noise for a product insight.

**The insight:** Randomizing the prompt doesn't randomize opt-in. The lift could be from the feature, the friction of seeing the prompt, or the type of user who said yes. You need to know which one before you can scale it.

---

### Option C — Stratify and isolate the causal effect *(Best Practice)*

**The decision:** Segment users by engagement level before running any test. Test notifications only on high-churn-risk users. Separate the notification effect from the power-user effect.

**Why this is the right call:**

The 17-point gap is a confounded correlation. The confounder is user type — specifically, how invested a user is in the product. To measure the causal effect of notifications, you need to hold user type constant.

**The experiment design:**

Stratify your user base into engagement tiers before randomizing:
- **High-engagement users:** frequent sessions, deep feature usage, completed onboarding
- **Low-engagement users:** few sessions, minimal feature usage, dropped off early in onboarding

Run the notification prompt test within each stratum separately. Now you're comparing like-for-like: high-engagement users who got the prompt vs. high-engagement users who didn't; low-engagement users who got the prompt vs. low-engagement users who didn't.

**What the results show:**

- Within low-engagement users: notifications have almost no effect on retention. These users churn because the product doesn't fit their needs, and a push notification doesn't change that.
- Within high-engagement users: notifications are a small convenience. They're already retained — the notification is a marginal quality-of-life improvement, not a retention driver.

When you control for engagement level, the 17-point gap disappears. The gap existed because the two groups in the original cohort analysis (notification enabled vs. not) were not comparable populations. They were power users vs. casual users — and you were measuring the power-user effect, not the notification effect.

**The actual retention problem:**

The data now points clearly at the real issue: onboarding and content quality. Users who make it past the first week stay. Users who don't make it through onboarding churn regardless of notification status.

The right intervention is not a notification prompt. It's fixing the first-session experience and ensuring new users find the content that's relevant to them before they decide the product isn't for them.

**The insight:** When you see a correlation, ask what confounder could explain it. Stratify to control for it. The 17 percentage points weren't a lever — they were a label, and it said "power user," not "notifications work."

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
