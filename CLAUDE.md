# Repo rules

Password-protected static site on GitHub Pages. `content.html` is encrypted
into `index.html` at build time; the visitor types the password to decrypt it
in the browser.

## Never leak the content
The repo is public and GitHub Pages serves every committed file as a URL.
Committing `content.html` would publish the private content at
`/content.html` with no password at all. It is gitignored — keep it that way,
and never `git add -f` it.

Trip details go in `content.html` only. Anything typed into `index.html` is
served in plaintext AND is silently wiped by the next build.

**Before every push**, confirm the private content did not reach the generated
file — search it for a phrase that only appears in `content.html`:

    grep -i "<phrase from content.html>" index.html

Any hit means it leaked. Do not push.

## Commits
- The commit message is **always** exactly `Update index.html` — nothing else.
  No body, no description of what changed.
- Never mention the password, the encryption scheme, or the page content in a
  commit message.
- Never write the password into any tracked file, or echo it in output.

## README.md
- Must contain exactly `testing 123` and nothing else. Do not add build
  instructions, usage notes, or any description of the project to it.

## Build
    node build.js <password>        # regenerates index.html from content.html

- `index.html` is generated. Never hand-edit it.
- `template.html` is the page shell and decryption logic; edit layout there.
- Every build makes a fresh salt/IV, so `index.html` changes even when the
  content did not. That diff is expected.
- The page needs https:// or localhost — Web Crypto is unavailable on
  `file://`, so a page that "does not work" locally is usually just that.

## Skills
- `.claude/skills/china-trip-planner/` holds the China travel know-how distilled
  from building this itinerary — verification rules, booking windows, payment
  rails, and two self-testing scripts for Baidu map links and route diagrams.
  Use it rather than re-deriving. A copy also lives at
  `~/.claude/skills/` so it applies outside this repo; treat the repo copy as
  the source of truth.

## Branches
- `main` — the live trip.
- `template` — clean reusable scaffold for the next trip. Branch from it, then
  `cp content.example.html content.html`. Use a different password per trip.
