# Plugin Repository for Directory Listing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `shootika-ai/plugin` into the artifact Anthropic's and OpenAI's directories review and display: four skills, a README that is the listing, synced manifests, versioned listing copy, and a check that keeps every release inside both portals' rules.

**Architecture:** Markdown and JSON only, no build step. `scripts/check.py` is the one place the directories' rules are encoded; CI runs it beside `claude plugin validate --strict`. Skills are split by merchant moment and draw every fact from the docs site and the MCP tool descriptions. The OpenAI ZIP is built by a script from the same files.

**Tech Stack:** Markdown, JSON, Python 3 standard library (`unittest`), bash, GitHub Actions, the Claude Code CLI.

**Spec:** `docs/superpowers/specs/2026-10-22-directory-listing-design.md`. Read it first; this plan argues from it. The companion backend plan is `docs/superpowers/plans/2026-10-22-backend-openai-oidc.md`.

## Global Constraints

- No em-dash (U+2014) anywhere in README, skills, manifests or listing copy.
- No number, price, plan name or duration that the backend or docs site does not state. Unknown values are a visible `[N]`.
- Skill front matter uses only `name` and `description`. No `metadata`, no Claude Code-only fields.
- Provider-neutral wording in skills: "the assistant", never "Claude" or "ChatGPT", except in `connect` where a product's own install path is named.
- Every non-image file under 256 KiB; only text, SVG, PNG, JPEG, GIF, WebP and fonts in the repository; no `.DS_Store`, `Thumbs.db`, `__MACOSX`, symlinks.
- `.mcp.json` keeps `type: "http"` and `url: "https://mcp.shootika.com"`.
- OpenAI final-submission limits: `displayName` 30, `shortDescription` 30, `longDescription` 4,000, `developerName` 80, at most 3 `defaultPrompt` entries of 128 characters without `@`; exactly 5 positive and 3 negative test cases; `category` from OpenAI's list.
- `VERSION`, `.claude-plugin/plugin.json` `version` and `.codex-plugin/plugin.json` `version` agree. This release is `0.2.0`.
- Plugin `name` stays `shootika`; skill `shoot-products` keeps its name.
- Commit after every task with a Conventional Commits message, on `main` as this repository does, each ending with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

## Review Focus

1. A README whose 40 words are mostly inside code blocks: the directory counts only prose, so `check.py` must count only prose. Test in Task 1.
2. An em-dash in a manifest description rather than in README or a skill: it would reach the directory card. `check.py` scans manifests too. Test in Task 1.
3. A reference file mentioned from `SKILL.md` with a path that differs in case from the file on disk: works on macOS, breaks on the portal's Linux scanner. `check.py` compares exact paths. Test in Task 1.
4. The ZIP script run on a working tree with an untracked `.DS_Store` or `dist/` left from an earlier run: the archive must contain neither. Test in Task 6.
5. A starter prompt in the Codex manifest with no matching line under "What you can ask" in the README: the two listings would promise different things. `check.py` requires every starter prompt to appear in the README. Test in Task 1.

---

### Task 1: `VERSION` and `scripts/check.py`

**Files:**
- Create: `VERSION`
- Create: `scripts/check.py`
- Create: `scripts/test_check.py`
- Modify: `.gitignore` (add `dist/`, `__pycache__/`)

**Interfaces:**
- Produces: `check.run(root: pathlib.Path) -> list[str]`, one human-readable problem per entry, empty when the plugin passes; `check.main() -> int` prints each problem on its own line and returns 1 when there are any, else 0. `README_WORDS = 40`, `OPENAI_CATEGORIES` (the thirteen names from the spec), `OPENAI_LIMITS = {'displayName': 30, 'shortDescription': 30, 'longDescription': 4000, 'developerName': 80, 'defaultPrompt': 128}`.

- [ ] **Step 1: Write `VERSION`**

Contents: `0.2.0` and a newline.

- [ ] **Step 2: Write the failing tests**

`scripts/test_check.py` builds a minimal passing plugin in a `tempfile.TemporaryDirectory()` through a helper `make_plugin(root, **overrides)` that writes `VERSION`, both manifests, `.mcp.json`, `README.md` (50 prose words plus a code block, "What you can ask" with the four lines from Task 4), `LICENSE`, a sample PNG under assets (any bytes; images are not size-checked), and one skill `skills/shoot-products/SKILL.md` with valid front matter. Tests, each mutating one thing:

```python
def test_a_complete_plugin_has_no_problems(self): assert run(root) == []
def test_version_mismatch_is_reported(self)                    # plugin.json version 0.1.9
def test_display_name_over_30_is_reported(self)
def test_short_description_over_30_is_reported(self)
def test_long_description_over_4000_is_reported(self)
def test_unknown_category_is_reported(self)                    # "Photography"
def test_four_starter_prompts_are_reported(self)
def test_starter_prompt_with_mention_is_reported(self)         # "Ask @Shootika ..."
def test_starter_prompt_missing_from_readme_is_reported(self)  # Review Focus 5
def test_test_case_counts_other_than_5_and_3_are_reported(self)
def test_positive_case_missing_expected_behavior_is_reported(self)
def test_skill_without_skill_md_is_reported(self)
def test_skill_name_not_matching_folder_is_reported(self)
def test_skill_description_over_1024_is_reported(self)
def test_skill_with_metadata_field_is_reported(self)
def test_combined_skill_name_over_64_is_reported(self)         # folder of 60 chars
def test_orphan_reference_file_is_reported(self)               # references/x.md not mentioned
def test_missing_reference_file_is_reported(self)              # mentioned, absent
def test_reference_path_case_mismatch_is_reported(self)        # Review Focus 3
def test_readme_under_40_prose_words_is_reported(self)         # Review Focus 1: 39 words + 200 in a code block
def test_em_dash_in_readme_skill_or_manifest_is_reported(self) # Review Focus 2: three subtests
def test_stray_system_file_is_reported(self)                   # .DS_Store
def test_non_image_file_over_256_kib_is_reported(self)
def test_mcp_server_without_https_or_type_http_is_reported(self)
def test_main_returns_1_with_problems_and_0_without(self)
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m unittest scripts/test_check.py -v`
Expected: FAIL, `ModuleNotFoundError` or `ImportError` for `check`.

- [ ] **Step 4: Implement `scripts/check.py`**

One function per rule family returning `list[str]`, composed by `run`. Front matter is parsed by hand: the text between the first two `---` lines, `key: value` per line, which is enough for `name` and `description` and lets the script stay dependency-free. Word counting strips fenced code blocks first. "Mentioned" means the reference's path relative to the skill folder, such as `references/store-types.md`, appears verbatim in that skill's `SKILL.md`. Make the test module import `check` by inserting `scripts/` on `sys.path` at the top of `test_check.py`.

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m unittest scripts/test_check.py -v`
Expected: all PASS.

- [ ] **Step 6: Run the check against the real repository**

Run: `python3 scripts/check.py`
Expected: it reports the problems later tasks fix (version mismatch with `0.1.1`, the starter prompt "Shoot my newest product on a model and show me the frames." absent from the README) and nothing else. If it reports anything else, the repository has a problem this plan did not foresee: fix the repository, not the check.

- [ ] **Step 7: Commit**

```bash
git add VERSION scripts/check.py scripts/test_check.py .gitignore
git commit -m "feat: add VERSION and the directory rules check"
```

---

### Task 2: Skills `shoot-products` and `review-frames`

**Files:**
- Modify: `skills/shoot-products/SKILL.md`
- Create: `skills/shoot-products/references/store-types.md`
- Create: `skills/shoot-products/references/messages.md`
- Create: `skills/shoot-products/agents/openai.yaml`
- Create: `skills/review-frames/SKILL.md`
- Create: `skills/review-frames/agents/openai.yaml`

**Interfaces:**
- Consumes: `check.run` from Task 1.
- Produces: the reference paths `skills/shoot-products/references/store-types.md` and `.../messages.md`, which Task 3's `cast-models` may cite by the same relative path only if it copies them; it does not, so it cites nothing.

Facts come from the docs site, local at `../docs/src/content/docs/ai-assistants/` (`what-it-can-do.md`, `connect.md`, `manage-connections.md`, `troubleshooting.md`) and `../docs/src/content/docs/shopify/shooting.md`, and from the tool descriptions in the backend's `mcp_server/tools/read.py` and `write.py` on `origin/main`. Nothing else is a source.

- [ ] **Step 1: Rewrite `skills/shoot-products/SKILL.md`**

Front matter, exactly:

```yaml
---
name: shoot-products
description: Shoot a store's products on AI models with Shootika and get frames back. Use when someone asks to shoot, photograph or make on-model photos of their products, to find products that have no model photos yet, or to check on a shoot that is running. Needs the Shootika connector. Not for publishing or removing frames (review-frames), choosing a model, pose or style (cast-models), or connection and permission problems (connect).
---
```

Body sections, 60 to 100 lines in all:

1. One paragraph: a shoot puts one product photo on one scene's model and returns one frame; every shoot uses one frame from the store's plan.
2. "Before spending": call `get_account`, say how many frames are left, never start a shoot the person did not ask for, confirm the count before starting more than one. Point to `references/messages.md` for what a refusal about frames means.
3. "Find the products": `list_products` (24 per page, follow `page`); products without model photos are those with no entry in `list_shoots` filtered by `product_id`, or ask the person; adding products is for web app stores only, see `references/store-types.md`.
4. "Pick the photo and the scene": `get_product` gives photos and their ids (`source_image_id`); choose the photo showing the whole garment, `garment_photo_type` `model` when someone wears it, default `flat-lay`; a scene must be `ready` in `list_scenes`; for a new or different scene, hand off to `cast-models`.
5. "Start and wait": `start_shoot` once per product and scene, each with its own `request_id` (product id plus scene id); the same `request_id` within 24 hours returns the first result instead of charging again; `get_shoot` waits a few seconds, call it again while `queued` or `processing`; a failed frame says why and its frame was refunded.
6. "Then": hand the frames to `review-frames`; say how many frames remain.
7. "If a tool refuses": name the permission from the message, say the person can reconnect to grant it, do not retry; `references/messages.md` has the messages.

- [ ] **Step 2: Write `references/store-types.md`**

Two short sections, Shopify store and web app store, each stating: where products come from (Shopify admin vs `add_product` and `add_product_image` from public PNG, JPEG or WebP URLs, up to 10 photos, 15 MB each), what approving a frame does (live product page vs saved to the product in Shootika), and where connected assistants are managed (`https://admin.shopify.com/store/<your-store>/apps/shootika/app/connections`, not in the app's menu, vs Settings, Connected assistants, admins only). Source: `what-it-can-do.md`, `manage-connections.md`.

- [ ] **Step 3: Write `references/messages.md`**

Each message from `troubleshooting.md` under "Messages from your assistant", quoted exactly, with one sentence on what the assistant should tell the person. Include the permission refusal `This connection is not allowed to use *tool*: it needs the "*permission*" permission...`, the four frames-exhausted variants, the Free plan variant, and `This connection was approved by someone who can no longer allow this.`

- [ ] **Step 4: Write `skills/shoot-products/agents/openai.yaml`**

```yaml
interface:
  display_name: "Shoot products"
  short_description: "On-model photos from your flat-lays"
  default_prompt: "Use $shoot-products to shoot my newest product on a model and show me the frames."
```

- [ ] **Step 5: Write `skills/review-frames/SKILL.md`**

Front matter, exactly:

```yaml
---
name: review-frames
description: Show, publish and unpublish Shootika frames. Use when someone asks to see their frames or today's results, to publish, approve or put a frame on a product, to take a frame back off a product, or to shoot a frame again because they do not like it. Needs the Shootika connector. Not for the first shoot of a product (shoot-products).
---
```

Body, 40 to 70 lines:

1. "Show": `list_shoots` newest first, filter by `product_id`, `status` or `approved`; the first 4 ready frames carry a small preview and a full-size link; give each frame its preview and link and ask about one frame at a time.
2. "Publish": a clear yes before `approve_frame`; on a Shopify store the frame goes on the live product page where shoppers see it, on other stores it is saved to the product in Shootika; confirm what was published.
3. "Take back": ask before `remove_frame`; the frame is kept and can be approved again until it expires.
4. "Shoot again": `start_shoot` with `regenerate_of` set to the frame id is a new shoot and uses a frame; check frames left first, as `shoot-products` does.
5. "What is live": `list_shoots` filtered by `approved`.

- [ ] **Step 6: Write `skills/review-frames/agents/openai.yaml`**

`display_name: "Review frames"`, `short_description: "Publish the frames you like"`, `default_prompt: "Use $review-frames to show me today's frames and publish the ones I pick."`

- [ ] **Step 7: Run the check**

Run: `python3 scripts/check.py`
Expected: no skill problems; the two remaining problems are the version mismatch and the README starter prompt, both fixed later.

- [ ] **Step 8: Commit**

```bash
git add skills/shoot-products skills/review-frames
git commit -m "feat(skills): split shooting from reviewing, add references"
```

---

### Task 3: Skills `cast-models` and `connect`

**Files:**
- Create: `skills/cast-models/SKILL.md`, `skills/cast-models/agents/openai.yaml`
- Create: `skills/connect/SKILL.md`, `skills/connect/agents/openai.yaml`

**Interfaces:**
- Produces: `./skills/connect/SKILL.md`, the path Task 4 sets as `onboardingSkill`.

Sources: `web-app/studio.md`, `shopify/shooting.md`, `connect.md`, `manage-connections.md`, `claude.md`, `chatgpt.md`, `cursor-and-code-editors.md`, and the `list_models`, `list_styles`, `list_scenes`, `request_scene` descriptions.

- [ ] **Step 1: Write `skills/cast-models/SKILL.md`**

Front matter, exactly:

```yaml
---
name: cast-models
description: Choose or prepare the scene a Shootika shoot uses, which is one model in one style and one pose. Use when someone asks which models or looks are available, wants one house model across the whole catalog, a style other than studio, a particular pose, or two or three options to compare before shooting. Needs the Shootika connector. Not for starting the shoot itself (shoot-products).
---
```

Body, 40 to 70 lines:

1. Vocabulary: a scene is one style, one model and one pose; a shoot needs a scene whose status is `ready`.
2. "What the store has": `list_scenes` with `status` ready; reuse one scene across many products so the catalog reads as one shoot.
3. "Something new": `list_models` (body type, skin tone, poses each can take) and `list_styles` (backdrops and looks, plus the store's own reference scenes as `ref:<id>`); offer two or three combinations rather than picking silently; `request_scene` with `model_id`, `style`, `pose` is free and safe to repeat; a new scene takes a little while, check `list_scenes` until ready.
4. "Then": hand off to `shoot-products` with the scene id.
5. What this skill does not claim: nothing about how many models a plan allows or how long a scene takes beyond "a little while"; those are on shootika.com/pricing and in the app.

- [ ] **Step 2: Write `skills/cast-models/agents/openai.yaml`**

`display_name: "Cast models"`, `short_description: "Pick the model, pose and style"`, `default_prompt: "Use $cast-models to show me three looks for a house model for my catalog."`

- [ ] **Step 3: Write `skills/connect/SKILL.md`**

Front matter, exactly:

```yaml
---
name: connect
description: Connect an AI assistant to a Shootika store, or fix a connection. Use when Shootika is not connected yet, a Shootika tool answers that the connection is missing a permission or is no longer valid, or someone asks what the assistant may do with their store, how to allow extra frames, or how to see and disconnect assistants. Explains the Shootika connect page and its four permissions; starts no shoot.
---
```

Body, 50 to 80 lines:

1. Who needs an account: the Shopify app at apps.shopify.com/shootika or the web app at panel.shootika.com; a web app account can be created during connection.
2. The connect page in plain words: "How do you use Shootika?", sign in or type the store address and approve inside the Shopify admin; check the heading names the right store; a request lasts 10 minutes.
3. The four permissions table from `connect.md`, exactly: Read, Catalog (web app stores only), Shoot (each shoot uses one frame), Publish. Read is always included; in the web app a viewer or billing member can grant Read only.
4. Extra frames: the switch starts off; monthly plans only; yearly and Free never bill extra frames.
5. Fixing: a permission refusal means disconnect and connect again with that permission ticked; "approved by someone who can no longer allow this" means a store admin reconnects; where to manage connections on each store type (same two locations as `store-types.md`, restated here because this skill is self-contained).
6. How to add Shootika, one line each: claude.ai and ChatGPT from their directories or as a custom connector with `https://mcp.shootika.com`; Claude Code with `/plugin install shootika --marketplace shootika-ai/plugin`; Codex with `codex plugin marketplace add shootika-ai/plugin` then `codex plugin add shootika@shootika`; Cursor and other editors by the URL.

- [ ] **Step 4: Write `skills/connect/agents/openai.yaml`**

`display_name: "Connect Shootika"`, `short_description: "Approve the connection, pick permissions"`, `default_prompt: "Use $connect to explain what Shootika may do with my store."`

- [ ] **Step 5: Run the check and read all four skills once as a merchant**

Run: `python3 scripts/check.py`
Expected: no skill problems. Then read each skill end to end and confirm no two skills state the same rule in their own words; where they do, keep it in the owning skill and replace the copy with a pointer.

- [ ] **Step 6: Commit**

```bash
git add skills/cast-models skills/connect
git commit -m "feat(skills): add cast-models and connect"
```

---

### Task 4: README and manifests

**Files:**
- Modify: `README.md`
- Modify: `.claude-plugin/plugin.json`
- Modify: `.codex-plugin/plugin.json`

**Interfaces:**
- Consumes: `./skills/connect/SKILL.md` from Task 3.
- Produces: the README's "What you can ask" list, which `check.py` compares starter prompts against; `VERSION` agreement.

- [ ] **Step 1: Rewrite `README.md`**

Sections in this order, following the spec's README section: title and one paragraph; "What you can ask" with exactly these four lines as a bulleted list of quoted sentences:

```
- "Which of my products have no model photos yet?"
- "Shoot my newest product on a model and show me the frames."
- "Show me the frames from today and publish the second one."
- "How many frames do I have left this month?"
```

then "How it treats your store"; "Connecting" with the permissions table and the two management locations; "Install" (claude.ai and ChatGPT: find Shootika in the directory or add `https://mcp.shootika.com` as a custom connector; Claude Code and Codex: the existing commands; other assistants: the URL); "What this plugin sends and fetches" as the explicit list in the spec; "Privacy"; "License". Keep the existing company line verbatim: built by Dimenso, DIMENSO L.L.C-FZ. Link docs.shootika.com/ai-assistants/ once.

- [ ] **Step 2: Update `.claude-plugin/plugin.json`**

`version` to `0.2.0`; add `"documentationUrl": "https://docs.shootika.com/ai-assistants/"`. Nothing else changes.

- [ ] **Step 3: Update `.codex-plugin/plugin.json`**

`version` to `0.2.0`; `interface.capabilities` to `["Read", "Write"]`; `defaultPrompt` unchanged (its three entries are lines 1, 2 and 4 of the README list); add under `extensions.com.openai`:

```json
"onboardingSkill": "./skills/connect/SKILL.md",
"publication": { "release_notes": "Four skills: shoot products, review frames, cast models, connect. README rewritten as the listing." }
```

Re-read the eight test cases against the new skills: `tools_triggered` and `expected_behavior` must describe what the skills now say. The fourth positive case's `expected_behavior` already matches `shoot-products` and `cast-models` together; the fifth matches `review-frames`. Change wording only where a skill contradicts it.

- [ ] **Step 4: Run both checks**

Run: `python3 scripts/check.py && claude plugin validate --strict .`
Expected: `check.py` prints nothing and exits 0; validate prints `✔ Validation passed`.

- [ ] **Step 5: Commit**

```bash
git add README.md .claude-plugin/plugin.json .codex-plugin/plugin.json
git commit -m "feat: README as the listing, manifests at 0.2.0 with onboarding skill"
```

---

### Task 5: Listing copy under `listing/`

**Files:**
- Create: `listing/anthropic-connector.md`
- Create: `listing/anthropic-plugin.md`
- Create: `listing/openai.md`
- Create: `listing/reviewer-account.md`

**Interfaces:**
- Consumes: the tool annotations in the backend's `mcp_server/tools/read.py` and `write.py` on `origin/main` for the justifications.

- [ ] **Step 1: Write `listing/anthropic-connector.md`**

Headed by the portal's step names from the spec. Fields with their limits in the heading: name (100), one-liner (200), description (2,000), one to five categories (choose from what the portal offers; propose "E-commerce" and "Design" and say the final pick happens in the portal), documentation URL `https://docs.shootika.com/ai-assistants/`, privacy `https://shootika.com/legal/privacy/`, support `support@shootika.com`, the URL slug `shootika`. Use cases: three, from the README's list. Setup needed: a Shootika account, Shopify app or web app. Reads and writes: both. Authentication: OAuth with dynamic client registration and Client ID Metadata Documents, no Anthropic-held credentials, every tool requires a signed-in connection. Data handling: own API; no health data; no sponsored content. Test and launch: a pointer to `reviewer-account.md`. Compliance: the seven acknowledgements, listed so the owner knows what they are agreeing to.

- [ ] **Step 2: Write `listing/anthropic-plugin.md`**

Source: `shootika-ai/plugin`, root, tracked branch `main`, GitHub push webhook on. Data handling answers: the plugin reads personal data only through the connector (the approver's name on the connect page, store and product data); sends data to no service other than the declared connector; stores nothing itself; retention is Shootika's, per the privacy policy; not intended for people under 18. Publish setting: auto-publish passing versions on. Contact: `support@shootika.com`.

- [ ] **Step 3: Write `listing/openai.md`**

Per-tool justification table: tool, `readOnlyHint`, `destructiveHint`, `openWorldHint`, one sentence each, matching the annotations on `origin/main` (read tools true/absent/false; `request_scene` false/false/false; `start_shoot` false/true/false "it spends a frame from the plan"; `approve_frame` and `remove_frame` false/true/false "it changes the live product page on Shopify"; `add_product` and `add_product_image` false/false/false). Frame domains: none, the server has no UI. Release notes: the same sentence as the manifest. Demo recording URL: `[to record]`. Reviewer credentials: "entered in the portal's Review details form, see reviewer-account.md; never in this repository".

- [ ] **Step 4: Write `listing/reviewer-account.md`**

What the demo store must contain (from the spec and the backend plan's Task 5), the login URL `https://panel.shootika.com/login`, that the admin signs in with email and password and no second factor, and a sentence that the credentials themselves live in the company password manager under "Shootika directory reviewers". No credential is ever written here.

- [ ] **Step 5: Run the check**

Run: `python3 scripts/check.py`
Expected: exit 0 (the em-dash and file rules cover `listing/` too).

- [ ] **Step 6: Commit**

```bash
git add listing
git commit -m "docs: listing copy for both directories"
```

---

### Task 6: CI workflow and the OpenAI ZIP script

**Files:**
- Create: `.github/workflows/check.yml`
- Create: `scripts/build-openai-zip.sh`
- Create: `scripts/test_build_zip.sh`

**Interfaces:**
- Consumes: `scripts/check.py`, `scripts/test_check.py`, `VERSION`.
- Produces: `dist/shootika-<VERSION>-openai.zip` (with `.codex-plugin/`) and `dist/shootika-<VERSION>-claude.zip` (with `.claude-plugin/`), each with the plugin at the archive root. Task 7 uploads the second to claude.ai.

- [ ] **Step 1: Write the failing ZIP test**

`scripts/test_build_zip.sh`: copies the repository to a temp dir with `git archive`, plants `.DS_Store` at the root and a stale `dist/old.zip` (Review Focus 4), runs `build-openai-zip.sh` there, then asserts with `unzip -Z1` on each archive: `dist/shootika-0.2.0-openai.zip` contains `.codex-plugin/plugin.json` and not `.claude-plugin/`; `dist/shootika-0.2.0-claude.zip` contains `.claude-plugin/plugin.json` and not `.codex-plugin/`; both contain `.mcp.json`, `README.md`, `LICENSE`, the icon under assets and every `skills/*/SKILL.md`; neither contains a path starting with `.git`, `.github`, `.claude/`, `docs/`, `listing/`, `scripts/`, `dist/`, nor any `.DS_Store`; `dist/old.zip` is gone. Exits 1 on any failure with the offending path.

- [ ] **Step 2: Run it to verify it fails**

Run: `bash scripts/test_build_zip.sh`
Expected: FAIL, `build-openai-zip.sh: No such file`.

- [ ] **Step 3: Write `scripts/build-openai-zip.sh`**

`set -euo pipefail`; reads `VERSION`; removes and recreates `dist/`; two `zip -r` runs from the repository root with explicit include lists, `.codex-plugin .mcp.json README.md LICENSE assets skills` for the OpenAI archive and `.claude-plugin .mcp.json README.md LICENSE assets skills` for the claude.ai one, each with `-x '*/.DS_Store' '*/__MACOSX/*' '*/__pycache__/*'`; prints both archive paths and their `unzip -l` summaries.

- [ ] **Step 4: Run the test to verify it passes**

Run: `bash scripts/test_build_zip.sh`
Expected: `ok` and exit 0.

- [ ] **Step 5: Write `.github/workflows/check.yml`**

Triggers: `push` and `pull_request`. One job on `ubuntu-latest`: checkout; `actions/setup-node` with Node 20; `npm install -g @anthropic-ai/claude-code`; `claude plugin validate --strict .`; `actions/setup-python` with 3.12; `python3 -m unittest scripts/test_check.py`; `python3 scripts/check.py`; `bash scripts/test_build_zip.sh`.

- [ ] **Step 6: Run the whole suite locally once**

Run: `python3 -m unittest scripts/test_check.py && python3 scripts/check.py && claude plugin validate --strict . && bash scripts/test_build_zip.sh`
Expected: every command exits 0.

- [ ] **Step 7: Commit and push, then watch the first CI run**

```bash
git add .github scripts/build-openai-zip.sh scripts/test_build_zip.sh
git commit -m "ci: validate the plugin, the directory rules and the OpenAI zip"
git push
```

Confirm the Actions run is green. If `claude plugin validate` needs something CI lacks, fix the workflow in a follow-up commit rather than removing the step.

---

### Task 7: Surface test on claude.ai and hand-off notes

**Files:**
- Modify: `listing/anthropic-plugin.md` (append "Surface test" results)

- [ ] **Step 1: Build the archives**

Run: `bash scripts/build-openai-zip.sh`
Expected: `dist/shootika-0.2.0-openai.zip` and `dist/shootika-0.2.0-claude.zip`.

- [ ] **Step 2: Upload and check in chat**

In claude.ai, Customize, Plugins, Add, Upload plugin, select `dist/shootika-0.2.0-claude.zip`. In a new chat ask which skills it has from plugins; expect the four names. Open the plugin's Connectors tab and connect Shootika; the Shootika connect page must open and approve. Ask "How many frames do I have left this month?" and expect a `get_account` answer.

- [ ] **Step 3: Record the result**

Append to `listing/anthropic-plugin.md` the date, the version uploaded, and one line per check with pass or the exact failure text. A failure here is a defect in a skill or manifest: fix it in the owning task's files, bump nothing, and repeat.

- [ ] **Step 4: Commit**

```bash
git add listing/anthropic-plugin.md
git commit -m "docs: record the claude.ai surface test"
```

The repository is now ready for the owner's two Anthropic submissions, in the order the spec gives. The OpenAI ZIP waits on the backend plan.
