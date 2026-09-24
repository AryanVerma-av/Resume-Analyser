# Brand Guidelines — SkillGap (Resume & Gap Analyzer for Students)

## 1. Brand Overview

**Product name:** SkillGap *(working name — swap in your final app name throughout this doc)*

**What it is:** An AI-powered tool that reads a student's resume against a target job description, shows what's missing, and gives a concrete roadmap to close the gap.

**Mission statement:** Turn "am I qualified?" anxiety into a clear, actionable plan.

**Brand personality:** Encouraging mentor, not a harsh recruiter. Think of a career-services advisor who's honest about gaps but always ends the conversation with "here's what to do next," never "you're not ready."

**Target audience:** University students and early-career job seekers, most of whom are applying to their first few internships/jobs and feel uncertain about how their resume stacks up.

---

## 2. Voice & Tone

| Trait | Do | Don't |
|---|---|---|
| **Encouraging** | "You're closer than you think — 3 skills to go." | "You are missing 7 required skills." |
| **Direct** | "This role needs SQL. Your resume doesn't show it." | Vague hedging like "you might want to consider maybe looking into..." |
| **Practical** | Every gap pairs with an action step. | Listing gaps with no next step. |
| **Peer-to-peer, not corporate** | "Let's close this gap." | "Candidates are advised to acquire..." |

**Tone shifts by context:**
- **Empty states / onboarding:** warm, low-pressure ("Drop in your resume and a job post — we'll do the comparing.")
- **Gap results (bad news):** matter-of-fact, never judgmental — state the gap, immediately follow with the fix.
- **Match results (good news):** genuinely celebratory, not generic ("Strong match — your resume already speaks this role's language.")
- **Errors (parsing/API failures):** calm and specific about what to do next, never blame the user's file.

**Words to use:** roadmap, close the gap, strengthen, next step, match, ready
**Words to avoid:** reject, fail, disqualified, unqualified, deficient

---

## 3. Color Palette

Built for a "clarity + encouragement" feel — calm neutrals with one confident accent and clear semantic colors for match/gap states.

| Role | Color | Hex | Usage |
|---|---|---|---|
| Primary | Indigo | `#4F46E5` | Buttons, links, active states, headers |
| Primary Dark | Deep Indigo | `#3730A3` | Hover/pressed states |
| Background | Off-white | `#FAFAF9` | App background |
| Surface | White | `#FFFFFF` | Cards, panels |
| Text — Primary | Charcoal | `#1F2937` | Body copy |
| Text — Secondary | Slate | `#6B7280` | Captions, helper text |
| Success (Match) | Green | `#16A34A` | Matched skills, "is_match: true" |
| Warning (Gap) | Amber | `#D97706` | Missing skills — deliberately amber, not red, to avoid a "wrong answer" feel |
| Error | Red | `#DC2626` | Parsing/API failures only — never for skill gaps |
| Border | Light Gray | `#E5E7EB` | Card borders, dividers |

**Rule:** Red is reserved strictly for system errors (file didn't parse, API failed). Missing skills are always amber — a gap is a to-do, not a failure.

---

## 4. Typography

- **Headings:** `Inter` (Bold/Semibold) — clean, modern, highly legible at small sizes for a data-dense UI.
- **Body:** `Inter` (Regular) — one typeface family keeps the Streamlit UI simple to theme.
- **Monospace (skill tags, extracted text):** `IBM Plex Mono` — signals "this was extracted/parsed," visually distinct from written copy.

| Style | Size | Weight |
|---|---|---|
| Page title | 28px | Bold |
| Section header | 20px | Semibold |
| Body | 15px | Regular |
| Caption / helper text | 13px | Regular |
| Skill tag / badge | 13px | Medium, mono |

---

## 5. UI Components & Patterns

- **Skill tags/chips:** pill-shaped badges — green fill for matched skills, amber outline for missing skills. Never plain red text.
- **Roadmap items:** numbered checklist style, each item starts with a verb ("Build a small project using...", "Take a short course on...").
- **Match score / is_match indicator:** a simple badge ("Strong Match" / "Partial Match" / "Early-Stage Match") instead of a raw pass/fail — avoids binary "you failed" framing.
- **Buttons:** primary action (Analyze) always indigo, filled; secondary actions (upload another, edit JD) outlined, neutral gray.
- **Loading state:** friendly, specific copy — "Reading your resume...", "Comparing against the role..." — never a bare spinner with no label.
- **Non-engineering gate (TypeSafe filter):** if a resume is filtered out before analysis, message it as scope, not rejection — "This role looks outside our current focus (software/engineering roles)," not "invalid resume."

---

## 6. Logo & Iconography Direction

- **Icon concept:** a simple upward arrow or ascending bar-steps inside a rounded square — conveys "closing the gap" / progress, not a magnifying glass (too "surveillance/audit") or a checkmark (too pass/fail).
- **Icon set:** use a single consistent line-icon library (e.g., Lucide/Feather-style) at 1.5–2px stroke weight throughout — matches the `frontend-design` skill's guidance to avoid mixed icon styles.
- **Avoid:** graduation caps, briefcases, or magnifying glasses — overused in career-tech and don't say anything specific about this product.

---

## 7. Accessibility

- Maintain WCAG AA contrast: body text on background ≥ 4.5:1 (charcoal `#1F2937` on off-white `#FAFAF9` passes).
- Never convey match/gap status by color alone — always pair with a label or icon (e.g., "✓ Matched" / "○ Missing"), since amber/green distinctions can be hard to see for color-blind users.
- Loading and error states must be announced as text, not just a visual spinner/icon.

---

## 8. Quick Reference

```
Primary:     #4F46E5
Success:     #16A34A  (matched skills)
Warning:     #D97706  (missing skills — never red)
Error:       #DC2626  (system errors only)
Background:  #FAFAF9
Surface:     #FFFFFF
Text:        #1F2937 / #6B7280
Font:        Inter (UI) + IBM Plex Mono (extracted/tagged content)
```

**One-line brand summary:** Calm, honest, and always ends with a next step — never a verdict.
