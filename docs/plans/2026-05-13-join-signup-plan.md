# Team Crafties Join Signup Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Add a real “Join Team Crafties” signup flow so Nath can see who arrived from Instagram/Facebook and gently grow an email-first member list.

**Architecture:** Reuse the site’s current static Netlify setup and existing Netlify Forms workflow instead of jumping straight to full accounts. Phase 1 creates a real join-interest/member-waitlist form, a thank-you page, and source tracking fields so Nath can see who joined. Phase 2 optionally upgrades that waitlist into password-free magic-link accounts later, after moderation and notifications are ready.

**Tech Stack:** Static HTML/CSS/vanilla JS, Netlify Forms, Netlify dashboard submissions, existing bilingual homepage patterns, optional future Supabase auth.

---

## Why this is the right next step

The current site already has:
- a real Netlify form for `gallery-submission` in `index.html`
- a real thank-you page at `thanks.html`
- demo-only account UI in `index.html` around the `#account` section

The simplest way to start seeing who joined is **not** full authentication yet.
The simplest, safest fit is:
1. real join form
2. real submission inbox
3. visible “found us on Instagram/Facebook” tracking
4. optional mailing-list export later

This keeps the gentle Team Crafties tone and avoids account-management complexity before moderation, comments, and notifications are ready.

---

## Success criteria

After this feature is live:
- visitors can submit a real join form
- submissions appear in Netlify Forms with timestamped entries
- Nath can tell whether a join came from Instagram, Facebook, or another source
- the homepage no longer claims the join flow is demo-only
- the form remains low-pressure, beginner-safe, and bilingual-friendly
- no public profile or comment account is created yet

---

## Files to inspect before implementation

- `index.html`
- `thanks.html`
- `README.md`
- `TEAM_CRAFTIES_NEXT_STEPS.md`
- `netlify.toml`

---

## Task 1: Replace the demo-only account concept with a real join waitlist concept

**Objective:** Decide that the first real membership step is a real join/signup list, not full account auth.

**Files:**
- Modify: `index.html` (account section copy only)
- Modify: `README.md`
- Modify: `TEAM_CRAFTIES_NEXT_STEPS.md`

**Step 1: Update product language**

Change copy in the `#account` section so it describes a real “join the cozy list” / “join Team Crafties” flow rather than promising a magic-link account that does not exist yet.

**Suggested content direction:**
- heading: `Join Team Crafties` / `Join the cozy list`
- explanation: maker name + email + craft interests + where you found us
- promise: gentle updates, first invitations, no spam, no password yet

**Step 2: Keep scope explicitly small**

Do **not** promise any of these in Phase 1:
- working login
- notification bell
- member dashboard
- public profile creation
- comments
- direct chat posting

**Step 3: Verification**

Read the updated section and confirm there is no remaining “demo only” or “magic sign-in link” wording in the visible account/signup area.

---

## Task 2: Convert the account demo form into a real Netlify form

**Objective:** Make the existing join form submit real data into Netlify Forms.

**Files:**
- Modify: `index.html` in the `#account` section/form block
- Create: `join-thanks.html`

**Step 1: Find the existing form elements**

Current code references to inspect in `index.html`:
- section `#account`
- form `#joinAccountForm`
- success message `#accountSuccess`
- JS preview handler near lines ~1492–1514

**Step 2: Replace the demo form markup with a real form**

Use the same pattern as the real gallery submission form already on the homepage:

Required attributes:
```html
<form
  class="craft-form"
  id="joinAccountForm"
  name="join-team-crafties"
  method="POST"
  action="/join-thanks.html"
  data-netlify="true"
  data-netlify-honeypot="bot-field"
>
  <input type="hidden" name="form-name" value="join-team-crafties">
  <p class="sr-only">
    <label>Do not fill this in if you are human: <input name="bot-field"></label>
  </p>
</form>
```

**Step 3: Include real fields**

Required fields:
- `maker-name`
- `email`
- `craft-interest` (single select or checkboxes)
- `found-us-from` (Instagram / Facebook / Friend / Search / Other)
- `kindness-rules-agree` (required checkbox)

Optional fields:
- `instagram-handle`
- `wants-gallery-invite`
- `wants-email-updates`
- `notes`

Recommended hidden fields:
- `join-page` = `homepage-account-section`
- `campaign-source` = value from URL query param `?from=instagram` etc when available
- `submitted-lang` = current page language (`en` or `fr`)

**Step 4: Add a true noscript-safe submit button**

Use a normal submit button so the form works even if JavaScript fails.

**Step 5: Create the thank-you page**

Create `join-thanks.html` with the same visual family as `thanks.html`, but wording focused on joining:
- “Thank you for joining Team Crafties”
- “You’re on the cozy list”
- “Nath can now see your join request privately”
- explain that this is not yet a full account login

**Step 6: Verification**

Run a local preview and manually submit a test form. Confirm the browser goes to `/join-thanks.html`.

---

## Task 3: Remove the demo-only JavaScript interception

**Objective:** Stop JS from preventing real form submission.

**Files:**
- Modify: `index.html` script block near lines ~1492–1514

**Step 1: Delete the current fake submit handler**

Remove the code that does all of the following:
- `event.preventDefault()` on `joinAccountForm`
- writes “Demo only…” into `#accountSuccess`
- resets the form without submitting anything

**Step 2: Replace it with lightweight enhancement only**

Allowed JS behavior:
- auto-fill hidden `campaign-source` from URL params
- auto-fill hidden `submitted-lang`
- optionally show inline validation help before submit

Not allowed JS behavior:
- blocking the native form submit
- pretending an email was sent

**Step 3: Verification**

Search `index.html` for these phrases and confirm they are gone from the join flow:
- `Demo only:`
- `future magic sign-in link`
- `event.preventDefault()` attached to `joinAccountForm`

---

## Task 4: Add source tracking for Instagram and Facebook traffic

**Objective:** Let Nath tell where joiners came from.

**Files:**
- Modify: `index.html`
- Modify: `README.md`

**Step 1: Add URL-source capture**

Use a tiny JS helper to read URL parameters such as:
- `?from=instagram`
- `?from=facebook`
- `?from=linkinbio`

Write that value into a hidden input like:
```html
<input type="hidden" id="campaignSource" name="campaign-source" value="direct">
```

**Step 2: Add a visible fallback field**

Keep a visible “How did you find us?” select, because many visitors will arrive without a tagged URL.

**Step 3: Update social links later**

When Nath posts in bios/captions, prefer links like:
- `https://teamcrafties.com/?from=instagram`
- `https://teamcrafties.com/?from=facebook`

**Step 4: Verification**

Open the homepage with tagged URLs and inspect the hidden field value before submit.

---

## Task 5: Keep the join area bilingual-friendly

**Objective:** Match the site’s EN/FR approach without overbuilding.

**Files:**
- Modify: `index.html`
- Modify: `join-thanks.html`

**Step 1: Follow the existing homepage translation pattern**

Mirror the current `data-fr` / language-toggle pattern already used in `index.html`.

**Step 2: Translate all new visible strings**

At minimum translate:
- heading
- body copy
- field labels
- placeholder text
- thank-you page body
- consent checkbox
- source labels

**Step 3: Verification**

Toggle EN/FR on the homepage and confirm all new join strings switch cleanly.

---

## Task 6: Update docs so Nath knows where to look for joiners

**Objective:** Make the workflow easy to remember later.

**Files:**
- Modify: `README.md`
- Create: `docs/join-signup-workflow.md`
- Modify: `TEAM_CRAFTIES_NEXT_STEPS.md`

**Step 1: Update README feature status**

Add a new status section such as:
- ✅ Real private gallery intake
- ✅ Real join signup / cozy list intake
- 🚧 Full member accounts still not live

**Step 2: Create workflow doc**

Create `docs/join-signup-workflow.md` covering:
- form name: `join-team-crafties`
- where submissions arrive: Netlify Forms
- how to filter by `campaign-source` and `found-us-from`
- which fields are safe to export into a future mailing list
- reminder that joiners are not yet public members

**Step 3: Update next-steps doc**

Change the build order so “real join signup” is checked off once implemented and “full password-free accounts” stays as a later phase.

**Step 4: Verification**

Read the docs and confirm a future helper could find the join submissions without guessing.

---

## Task 7: Local verification pass

**Objective:** Confirm the join feature works before deploy.

**Files:**
- Modify if needed: `index.html`, `join-thanks.html`, docs

**Step 1: Start a local server**

Run from repo root:
```bash
python3 -m http.server 8000
```

**Step 2: Open the site**

Run:
```bash
open http://localhost:8000
```

**Step 3: Manual checks**

Confirm all are true:
- the join section no longer says demo-only
- the form has a normal submit button
- required fields block empty submission
- EN/FR strings render correctly
- the thank-you page loads cleanly
- the query-param source field is populated when visiting a tagged URL

**Step 4: Optional HTML sanity check**

Run:
```bash
python3 - <<'PY'
from pathlib import Path
for p in [Path('index.html'), Path('join-thanks.html'), Path('thanks.html')]:
    print(p, 'exists=', p.exists(), 'bytes=', p.stat().st_size if p.exists() else 0)
PY
```

Expected: all files exist.

---

## Task 8: Deploy and verify on Netlify

**Objective:** Publish the working join flow.

**Files:**
- No code changes expected unless verification fails

**Step 1: Deploy**

Run from repo root:
```bash
netlify deploy --prod --dir .
```

**Step 2: Smoke test production**

Verify on live site:
- homepage join section copy is updated
- form posts to Netlify successfully
- redirect goes to `/join-thanks.html`
- a test submission appears in Netlify Forms under `join-team-crafties`

**Step 3: Clean up test data**

If needed, mark the test submission clearly in Netlify Forms or delete it after checking.

---

## Future Phase 2: Real password-free accounts (only after the join list works)

Do this later, not now.

**Recommended stack:** Supabase Auth with magic links.

Future files likely needed:
- `index.html` (real auth CTA)
- `app.js` or extracted JS module
- `auth/callback.html` or equivalent
- `netlify.toml` redirects if needed
- a protected moderation/admin surface later

Future capabilities:
- real sign-in link email
- saved maker profile
- notification preferences
- approved comments/help-room identity

But **do not start here**. Get the real join list working first.

---

## Acceptance checklist

Implementation is complete when:
- [ ] `#account` is no longer demo-only
- [ ] `join-team-crafties` Netlify form exists in the source
- [ ] `join-thanks.html` exists and is styled
- [ ] no fake join submit JS remains
- [ ] source tracking exists for Instagram/Facebook/direct
- [ ] README/docs explain the workflow
- [ ] live production test succeeds
- [ ] Nath can open Netlify Forms and see who joined

---

## Notes for the implementer

- Reuse existing Team Crafties styling classes where possible.
- Keep the tone warm and beginner-safe.
- Avoid building a login system in this pass.
- Treat this as a real **community interest / member waitlist** feature, not full membership.
- The key business outcome is simple: **Nath can finally see who arrived from social posts.**
