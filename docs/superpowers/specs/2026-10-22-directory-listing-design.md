# Shootika in the Claude and OpenAI directories: design

Date: 2026-10-22. Owner: Sajad. Status: approved in conversation; builder
check done and its findings folded in.

## Why

Merchants and their teams will not clone a GitHub repository or install a CLI.
They will look for Shootika where they already look for things to add to their
assistant: Anthropic's directory (browsed from claude.ai, Cowork and Claude
Code) and OpenAI's directory (shared by ChatGPT and Codex). Both directories
take a plugin that bundles a remote MCP server with skills, which is exactly
what this repository already is. Both also review it, display parts of it
verbatim, and refuse it on specific rules.

This design turns the repository into the artifact those two directories
review and display, and names the backend changes that only OpenAI's directory
requires. The prompt for it was the
[Higgsfield skills repository](https://github.com/higgsfield-ai/skills). What
transfers from it is skill quality, a README that reads like a product page,
versioned manifests and a CI check that keeps a release from failing a portal's
validation. What does not transfer is everything built for developers who
clone a repository: four install paths, a setup script, an agent-driven install
runbook and a CLI bootstrap. The structural template for a directory plugin is
Anthropic's own `knowledge-work-plugins`: a short manifest, an `.mcp.json`, a
few skills, no build step.

## Who it serves

- A store owner or a member of their team, on Shopify or on the Shootika web
  app, who finds Shootika in a directory, adds it, approves the connection on
  the Shootika page, and asks the assistant to shoot, review and publish. They
  use claude.ai or ChatGPT in a browser. Some use Claude Code, Codex or Cowork.
- A Team or Enterprise owner on claude.ai who makes the plugin available to
  the whole organization.
- Anthropic's and OpenAI's reviewers, who read the README, run every tool
  against a test store, and check the listing against their rules.

## Goals

1. Pass Anthropic's portal validation and security scan on the first run, and
   give the human reviewer nothing to hold.
2. Build an OpenAI ZIP that passes the metadata and skill scans, with the
   backend meeting the remote MCP requirements.
3. Make every skill earn its place: a merchant moment it serves that the tool
   descriptions alone do not.
4. Keep the three manifests, the version and the listing copy in sync by a
   check, not by memory.

## Non-goals

- A Shootika CLI. Merchants have no shell, Shopify stores have no API key, and
  the remote MCP server already reaches every assistant that matters.
- Developer distribution: `npx skills add`, `gh skill install`, a `setup`
  script, an agent install runbook, a Cursor manifest. Cursor users paste the
  MCP URL, as the docs site already tells them.
- Anthropic's partner-only `claude-plugins-official` marketplace. The public
  directory is the target.
- Changing the connect flow, the four permissions, the tools or their
  annotations. They already meet both directories' tool rules.
- OpenID Connect ID tokens. OpenAI's workspace domain check needs the
  `openid` and `email` scopes, a UserInfo endpoint and an OpenID Connect
  discovery document, and those are added; ID tokens are optional for it and
  stay out.

## Anti-goals: failures even if it technically works

- A README or skill that states a number, a price or a feature the backend
  does not. The website repo's rule applies here: a number without a source is
  a visible `[N]`, never a guess.
- A skill that starts a shoot, publishes or removes a frame without the
  person's clear yes. The tools say to ask; the skills must never loosen that.
- Skills that repeat the tool descriptions. If a skill only restates what
  `start_shoot`'s description already says, it costs tokens on every turn and
  adds nothing.
- A plugin that behaves differently on claude.ai than in Claude Code because a
  skill relies on a Claude Code-only component.
- Listing copy typed into a portal form that nobody reviewed and no file
  pins.

## Constraints from the directories

Verified against the official documentation on 2026-10-22. Where a rule is
only on a portal page we cannot reach before submitting, it is marked "verify
in the portal".

### Anthropic's directory

Source: claude.com/docs/plugins/submit, /plugins/pre-submission-checklist,
/plugins/platform-support, /plugins/build, /directory/publish,
/connectors/building/submission.

- Submitted from a GitHub repository at claude.ai/directory/manage, from a paid
  claude.ai plan. The repository may be private while validating and must be
  public before the listing goes live. One submission per repository folder;
  the first organization to submit it owns the listing.
- Two submissions: the MCP server as an **MCP connector**, then the plugin as
  a **Plugin bundle** whose `.mcp.json` points at the same URL. Anthropic
  pairs them when both come from the same organization.
- The README is the listing description. At least 40 words outside code
  blocks. It must describe everything the plugin runs, sends and fetches; the
  security scan looks for undisclosed destinations.
- A `LICENSE` file or `license` in `plugin.json`.
- `.mcp.json` entries: `type` `http`, absolute `https://` URL, no
  `${user_config.*}` in the URL (chat ignores such a server), no credentials.
- Files: no `.DS_Store`, `Thumbs.db` or `__MACOSX`; every non-image file under
  256 KiB; at most 512 files; only text, SVG, PNG, JPEG, GIF, WebP and fonts.
  An `.ico`, `.pdf` or `.zip` is held for a reviewer.
- `name`: lowercase letters, digits and hyphens, permanent. `displayName` and
  `author.name` must not resemble another listing or brand.
- `version` raised on every release; the directory follows a branch or tag and
  publishes new commits after they pass.
- On claude.ai chat: skills load; the remote MCP server appears on the
  plugin's **Connectors** tab, where the merchant connects it through our OAuth
  page. Agents, hooks, `bin/` and local servers are Claude Code-only or refused;
  this plugin has none.
- `claude plugin validate --strict` passes today with nothing to report. The
  portal runs more checks than the CLI.
- Connector listing fields, entered in the portal: name up to 100 characters,
  one-liner up to 200, description up to 2,000, one to five categories,
  documentation URL, privacy policy URL, support contact, icon, a permanent
  URL slug, and a test account for reviewers. Every tool needs a `title` and
  `readOnlyHint` or `destructiveHint`, which ours have.

### OpenAI's directory

Source: developers.openai.com/plugins/deploy/submission,
/plugins/deploy/submission-errors, /plugins/build/plugins,
/plugins/guides/submit-claude-plugin.

- A ZIP uploaded at platform.openai.com/plugins by an organization with a
  verified developer or business identity and **Apps Management** write
  access. Remote MCP servers go through the **With MCP** path; the server URL
  is given in the portal, and only one server per plugin.
- Manifest: `.codex-plugin/plugin.json` is accepted as a compatibility format;
  root `plugin.json` is the newer portable one. Required: `name`, `version`,
  `description`, `author.name`, `interface`, `interface.capabilities`,
  `composerIcon`.
- `interface` limits at final submission: `displayName` 30 characters,
  `shortDescription` 30, `longDescription` 4,000, `developerName` 80, up to 3
  `defaultPrompt` entries of 128 characters each with no `@mention`, a
  supported `category`, and all four of `websiteURL`, `supportURL`,
  `privacyPolicyURL`, `termsOfServiceURL` for an MCP plugin. `logo` and
  `composerIcon` square, 48 to 4,096 px, PNG, JPEG, WebP or SVG, 5 MiB max.
- `extensions.com.openai.review.test_cases`: exactly 5 positive cases
  (`description`, `prompt`, `tools_triggered`, `expected_behavior`) and 3
  negative (`description`, `prompt`). `demo_recording_url` required.
  `extensions.com.openai.publication.release_notes` required.
- Skills: each an immediate child of `skills/` with a `SKILL.md` whose front
  matter has `name` and `description` (1,024 characters max);
  `plugin-name:skill-name` at most 64 characters. Optional
  `agents/openai.yaml` per skill with `interface.display_name` and
  `short_description`. `metadata` in front matter is ignored with a warning.
- ZIP: no `apps` or `.app.json`, no hooks. A local MCP configuration is
  excluded unless the organization is allowlisted; the remote server is given
  in the With MCP step. OpenAI's own submission example shows a Codex manifest
  whose `mcpServers` points at an `.mcp.json` with a remote server, which is
  what ours does, so `.mcp.json` stays in the ZIP. If the portal still warns
  `mcp_configuration_excluded`, the warning is accepted; the server comes from
  the With MCP step either way.
- Reviewer credentials go in the portal's **Review details** form, never in
  the ZIP.
- Backend: a domain-verification token served at
  `https://mcp.shootika.com/.well-known/openai-apps-challenge`; OAuth 2.1 with
  PKCE S256 and `authorization_response_iss_parameter_supported` honoured on
  every response; for workspace domain restrictions (ChatGPT Business and
  Enterprise), the `openid` and `email` scopes advertised and enabled, an
  OpenID Connect discovery document, and a UserInfo endpoint returning `email`
  and `email_verified: true`. ChatGPT requests every OIDC scope the metadata
  advertises, so advertising them without accepting them would break every
  connection. Every tool with explicit `readOnlyHint`, `openWorldHint` and
  `destructiveHint` plus a justification entered in the portal; a current tool
  scan of the production server. The reviewer's test account must log in with
  a password alone: no MFA, email or SMS code, or magic link.

### What the repository and backend already satisfy

- Repository: manifest fields including `displayName`, `icon`, `homepage`,
  `repository`, `supportUrl`, `privacyPolicyUrl`, `termsOfServiceUrl`; MIT
  `LICENSE`; a README over 40 words with a disclosure section; `.mcp.json`
  with `type` `http` and a fixed `https://` URL; a 512 px PNG icon; a Codex
  manifest with the four URLs, three starter prompts, a 23-character short
  description, and 5 + 3 review test cases; `claude plugin validate --strict`
  clean; no stray system files tracked.
- Backend (`mcp_server/` and `oauth_server/`, live at `mcp.shootika.com` and
  `api.shootika.com`): every tool has `title`, `readOnlyHint`, `openWorldHint`
  and, on write tools, `destructiveHint` and `idempotentHint`; OAuth 2.1 with
  PKCE S256, resource indicators, dynamic client registration and Client ID
  Metadata Documents; `/.well-known/oauth-authorization-server` and
  `/.well-known/oauth-protected-resource` published; server `instructions` set.
  The OpenAI domain-verification view is already shipped: the
  `OPENAI_APPS_CHALLENGE` setting, read from the configmap, served as plain
  text at `/.well-known/openai-apps-challenge` on the MCP host only, with
  tests. Only the value needs setting when the portal issues it.

## The design

### Part 1: the plugin repository

#### Layout

```
plugin/
├── .claude-plugin/
│   ├── plugin.json              # Anthropic manifest, also read by Claude Code
│   └── marketplace.json         # keeps /plugin install ... --marketplace working
├── .codex-plugin/plugin.json    # OpenAI compatibility manifest
├── .mcp.json                    # the one remote server
├── .github/workflows/check.yml  # CI: validate + sync + limits
├── VERSION                      # single source of the version
├── README.md                    # the Anthropic listing description
├── LICENSE
├── assets/
│   ├── icon.png                 # 512 px, used by both manifests
│   └── icon.svg                 # optional; see "Calls made"
├── listing/
│   ├── anthropic-connector.md   # copy for the connector portal form
│   ├── anthropic-plugin.md      # data-handling answers, tracked branch, notes
│   └── openai.md                # review justifications, demo URL, credentials note
├── scripts/
│   ├── check.py                 # the rules CI enforces, runnable locally
│   └── build-openai-zip.sh      # writes dist/shootika-<version>.zip
├── skills/
│   ├── shoot-products/
│   │   ├── SKILL.md
│   │   ├── agents/openai.yaml
│   │   └── references/
│   │       ├── store-types.md   # Shopify vs web app: catalog, publishing, where to manage
│   │       └── messages.md      # the refusal messages and what each means
│   ├── review-frames/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── cast-models/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   └── connect/
│       ├── SKILL.md
│       └── agents/openai.yaml
└── docs/superpowers/            # this design and its plan; excluded from the ZIP
```

`docs/`, `listing/`, `scripts/`, `.github/` and `.claude/` are not loaded by
any assistant. Anthropic's scanner reads the whole plugin folder, so every
file in them obeys the file rules above (text, under 256 KiB).

#### Skills

Four skills, each named for a merchant moment, each short enough that an
assistant reads it on every relevant turn without cost. Each `description`
names the situations a merchant is in, in their words, and ends with the
boundary ("not for ...") so the assistant picks one skill, not two. Together
they cover every starter prompt in the manifests and every line of "Things you
can ask" on the docs site.

| Skill | Merchant moment | What it adds beyond the tools |
|---|---|---|
| `shoot-products` | "Shoot the new linen dresses on a model." "Which products have no model photos yet?" | The order of the round, the frames-left check and the ask before spending, finding gaps by comparing `list_products` with `list_shoots`, picking the photo, `request_id` discipline, waiting with `get_shoot`, handing off to `review-frames`. |
| `review-frames` | "Show me today's frames and publish the second one." "Take that photo off the product." | How to present frames (preview plus full-size link, one question per frame), the explicit yes before `approve_frame` and `remove_frame`, what publishing means on each store type, regenerating a frame as a new shoot that costs a frame. |
| `cast-models` | "Make a house model for the whole collection." "I want a street look, not studio." "Show me a few options." | Model, pose and style vocabulary, offering two or three options rather than choosing silently, `request_scene` being free and repeatable, waiting for a scene to be ready, reusing one scene across many products. |
| `connect` | First use, "connect Shootika", "it says I need a permission", "how do I disconnect it". | The connect page in plain words, the four permissions and what each unlocks, the extra-frames switch, reconnecting to add a permission, where connected assistants are managed on each store type. Also OpenAI's `onboardingSkill`. |

Rules that apply to all four:

- Front matter uses only the portable fields: `name`, `description`. Nothing
  Claude Code-only, no `metadata` (OpenAI warns and drops it). The combined
  `shootika:<skill>` name stays under 64 characters.
- Provider-neutral wording. Say "the assistant" or nothing, never "Claude".
- Rules about spending and publishing are stated once, in the skill that owns
  the action, and other skills point to it rather than restate it.
- A skill body targets roughly 60 to 120 lines. The current `shoot-products`
  is 90 lines and covers all four moments; splitting it should leave each part
  shorter, not add text.
- Reference files are mentioned by name from the skill that needs them, with
  the sentence that tells the assistant when to read each one. Only
  `shoot-products` has references in version one; the other skills reuse them
  by path only if they turn out to need them, otherwise they stay
  self-contained.
- Facts in skills come from the docs site and the tool descriptions. A skill
  never states a frame count, a price, a plan name or a time that the backend
  does not.
- Each skill's `agents/openai.yaml` has `interface.display_name`,
  `short_description` and a `default_prompt`, the way Higgsfield's do.

#### README

The README is what Anthropic shows as the listing. It is rewritten as a
product page that also carries the disclosure a security reviewer needs:

1. One paragraph: what Shootika does, for whom, and that this plugin connects
   it to your assistant.
2. "What you can ask": the four lines from the docs site, kept in sync with
   the manifests' starter prompts.
3. "How it treats your store": one frame per shoot and the ask before
   spending; nothing published without a yes; what publishing means on
   Shopify versus the web app.
4. "Connecting": the Shootika page, the four permissions table, where to see
   and disconnect assistants. Links to docs.shootika.com for the detail.
5. "Install": claude.ai and ChatGPT by directory; Claude Code and Codex by the
   marketplace commands that already work; any other assistant by the MCP URL.
6. "What this plugin sends and fetches": kept, and made the explicit list the
   scan expects: the one host, HTTPS, OAuth token issued on approval, what is
   read and written with each permission, that product photos by URL are
   fetched by Shootika's servers, that frame previews come back as images.
7. Privacy, support, company, license.

No em-dashes. No number without a source. The website repo's claim rules
apply: Shootika is built by Dimenso, DIMENSO L.L.C-FZ; never present Dimenso's
store count as Shootika's.

#### Manifests and version

- `VERSION` holds the version. `scripts/check.py` fails when
  `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (if it
  carries a version) and `.codex-plugin/plugin.json` disagree with it.
- `.claude-plugin/plugin.json` keeps its current fields and gains
  `documentationUrl: https://docs.shootika.com/ai-assistants/`. Its
  `description` stays the sentence the directory card shows.
- `.codex-plugin/plugin.json`: `interface.capabilities` becomes
  `["Read", "Write"]`; `extensions.com.openai.onboardingSkill` points at
  `./skills/connect/SKILL.md`; `extensions.com.openai.publication.release_notes`
  is set per release; `review.demo_recording_url` is added when the owner has
  recorded it. The five positive and three negative test cases are kept and
  re-read against the final skills so `tools_triggered` and
  `expected_behavior` match what the skills say.
- The starter prompts are identical in the Codex manifest and the README.

#### Listing copy under `listing/`

Portal forms have no history, so the words typed into them live here and the
plan treats them like code: written, reviewed, then pasted.

- `anthropic-connector.md`: name, one-liner (200 characters), description
  (2,000), categories, documentation URL, privacy URL, support contact, the
  use-case answers, the authentication answer (OAuth with dynamic client
  registration and CIMD, no Anthropic-held credentials), the data-handling
  answers, and the test-account instructions for reviewers.
- `anthropic-plugin.md`: the data-handling answers for the plugin bundle, the
  tracked branch (`main`), and the publish setting to choose.
- `openai.md`: the per-tool annotation justifications, the frame-domain
  answer (none), the demo recording URL once it exists, release notes, and a
  note that reviewer credentials go in the portal's Review details form.

#### CI and scripts

`scripts/check.py` is a dependency-free Python script that CI runs and anyone
can run locally. It fails on:

- a version mismatch between `VERSION` and either manifest;
- any `interface` field over the OpenAI final-submission limit, a category not
  in OpenAI's list, more than three starter prompts, a starter prompt over 128
  characters or containing `@`;
- a test-case count other than 5 positive and 3 negative, or a positive case
  missing a required field;
- a skill folder without `SKILL.md`, front matter without `name` and
  `description`, a `name` that does not match the folder, a description over
  1,024 characters, or `shootika:<name>` over 64 characters;
- a `references/` file that no `SKILL.md` in that skill mentions, or a mention
  of a reference file that does not exist;
- a README under 40 words outside code blocks;
- an em-dash anywhere in README or skills;
- a tracked `.DS_Store`, `Thumbs.db`, `__MACOSX`, symlink, or a non-image file
  over 256 KiB;
- an `.mcp.json` server without `type: http` and an absolute `https://` URL;
- starter prompts in the Codex manifest that differ from the README's "What
  you can ask" list.

`.github/workflows/check.yml` installs Claude Code, runs
`claude plugin validate --strict .` and `python3 scripts/check.py`, on every
push and pull request.

`scripts/build-openai-zip.sh` writes `dist/shootika-<VERSION>.zip` containing
`.codex-plugin/`, `.mcp.json`, `skills/`, `assets/`, `README.md` and `LICENSE`
with the plugin at the archive root, excluding `.git`, `.github`, `.claude`,
`docs/`, `listing/`, `scripts/` and `dist/`. `dist/` is gitignored.

### Part 2: the backend, for OpenAI's remote MCP review

All in `shootika/backend`, on a feature branch off `develop`, following the
backend repository's own conventions and CLAUDE.md.

1. **Domain verification.** Already shipped (see above). The plan's only step
   is to put the portal's token into the production configmap as
   `OPENAI_APPS_CHALLENGE` when the OpenAI submission reaches that step.
2. **`openid` and `email` scopes.** Added to `scopes_supported` on the
   authorization server metadata and the protected resource metadata, and
   accepted at `/oauth/authorize`, at `/oauth/token` for the code exchange, and
   on refresh, where today any scope outside the four permission scopes is
   refused as `invalid_scope`. They are pass-through: they grant nothing on
   the MCP server, `canonical_scopes` keeps them out of the permission scopes,
   and the consent page and `Grant` are unchanged. A token records them so the
   `scope` string echoed back includes what was asked for.
3. **OpenID Connect discovery.** `/.well-known/openid-configuration` on the
   issuer, carrying the same fields as the OAuth document plus
   `userinfo_endpoint` and the fields OpenID Connect Discovery marks required,
   with nominal values where no ID token is ever issued. The OAuth document
   gains `userinfo_endpoint` too. OpenAI's auth guide says either discovery
   document is read, and the domain-restriction section says to publish the
   OpenID Connect one, so both are served.
4. **UserInfo.** `GET /oauth/userinfo` on the authorization server, bearer
   access token, audience-checked the same way the MCP endpoint checks it,
   returning `sub` (the grant's public id) and, when known, `email` and
   `email_verified`. For a web app grant the email is the approving
   `PanelUser`'s; it is always verified, because the web app blocks unverified
   users from the consent endpoints. For a Shopify grant it is the approving
   staff member's email as Shopify reported it in the token exchange, with a
   new `email_verified` field on the staff member filled from Shopify's
   `associated_user.email_verified`, by the same exchange that already fills
   the name and email. When the staff row has no email, because Shopify's
   lookup failed when the member was recorded, UserInfo returns `sub` alone:
   no error, and no network call to Shopify inside the request. Such a
   merchant can still connect from ChatGPT; only a workspace with a domain
   restriction will refuse them until the row is filled on their next visit to
   the Shopify app. Nothing in Shootika reads UserInfo.
5. **Demo store for reviewers.** A production web-app store named for its
   purpose, with a dozen products that carry real flat-lay photos, two or
   three ready scenes, a few finished frames, and credits granted with
   `grant_goodwill`. Its admin is a verified user with a password, since both
   portals' reviewers log in without MFA, codes or magic links. That login is
   what both portals get as reviewer credentials. Both directories require
   reviewers to run every tool, which spends frames; the goodwill grant covers
   that.
6. **Tests** for each of the above in the backend's Django test runner, and
   the staging (`stg-mcp.shootika.com`) deploy before production.

Nothing here changes the consent page, the permission model or the tools.

### Part 3: submissions, in order

1. Repository work merged to `main`, CI green, `claude plugin validate
   --strict` clean, the plugin uploaded to a claude.ai account as a ZIP and
   each skill and the Connectors tab checked in chat.
2. Anthropic, MCP connector: from the owner's paid claude.ai organization,
   with `listing/anthropic-connector.md` as the source of every answer and the
   demo store as the test account.
3. Anthropic, plugin bundle: same organization, repository `shootika-ai/plugin`,
   tracked branch `main`, GitHub push webhook on.
4. Backend changes deployed to production; the token served; UserInfo live.
5. OpenAI: identity verified, ZIP built by the script, With MCP path, domain
   verified, test cases imported from the manifest, justifications pasted from
   `listing/openai.md`, demo recording URL, reviewer credentials in the form.

### Releases after listing

A release is: edit, bump `VERSION` and both manifests (the check fails until
they agree), merge to `main`. Anthropic picks the commit up by webhook, scans
it, and publishes it under whichever publish setting the reviewer applied.
OpenAI needs a new ZIP for any change to skills, metadata or assets, each with
its own review; changes to the MCP server itself are rescanned daily without
a ZIP.

## Calls made in this document (owner, please check)

- **Four skills, named `shoot-products`, `review-frames`, `cast-models`,
  `connect`.** The current single skill keeps its name so existing installs
  and the docs site's references to `shoot-products` stay true.
- **`connect` is a skill, not README-only text**, so an assistant can explain
  a permission refusal or a reconnect without the merchant leaving chat, and
  so OpenAI's `onboardingSkill` has something to point at.
- **References only under `shoot-products`** in version one. The other skills
  stay self-contained; adding references later is a release, not a design
  change.
- **No Cursor manifest, no `setup`, no `INSTALL_FOR_AGENTS.md`, no cookbook
  file.** The docs site's "Things you can ask" and the README's examples are
  the cookbook merchants need.
- **The Codex compatibility manifest stays**; the newer root `plugin.json`
  portable format is not adopted yet, because the current manifest is
  accepted and already carries the review object. Revisit if the portal warns.
- **`listing/` lives in the plugin repository**, not the docs repository,
  because it versions with the manifests it must agree with.
- **CI uses Python with no dependencies**, matching the backend's language,
  rather than Node.
- **Icon**: the existing 512 px PNG serves both `logo` and `composerIcon`. An
  SVG is added only if the design team has one; it is not drawn for this.
- **UserInfo returns the approver's email**, not a store email, because that
  is the person who authenticated and what OpenAI's domain restriction is
  about.
- **An OpenID Connect discovery document is served, without ID tokens.**
  OpenAI's guide reads either discovery document but tells domain-restricted
  workspaces to publish the OpenID Connect one. Serving it costs one view;
  guessing wrong costs a failed OpenAI review.
- **`openid` and `email` are accepted everywhere a scope is parsed**, including
  refresh, because ChatGPT requests every OIDC scope the metadata advertises
  and a refused scope ends the connection.
- **A Shopify approver with no recorded email gets `sub` only from
  UserInfo.** No error, no live call to Shopify inside the request. This only
  affects a ChatGPT workspace with a domain restriction, and only until the
  staff row is filled.
- **The demo store is a web-app store, on production**, because reviewers
  connect to the production URL and a web-app login is a plain email and
  password; a Shopify store would need the reviewer inside a Shopify admin.
- **OpenAI last**, because its backend prerequisites and the demo recording
  are the only items with a dependency outside this repository.

## Left to the builder

- The exact wording of each skill, within the rules above and the facts on
  docs.shootika.com and in the tool descriptions.
- The structure of `scripts/check.py` and the CI workflow.
- The ZIP script's exact exclusion list, so long as the archive has the plugin
  at its root and nothing the portal rejects.
- Which `PanelUser` field or Shopify field the backend reads for
  `email_verified`, following the backend's existing models.
- Test design for the backend changes, following the backend's own testing
  conventions.

## Owner's items, outside the build

- A paid claude.ai plan to submit from, with the GitHub account connected and
  push access to `shootika-ai/plugin`. The organization that submits owns the
  listing permanently.
- A verified OpenAI developer or business identity with Apps Management write
  access.
- The demo recording OpenAI requires, covering the main tools on at least one
  supported platform.
- Doing both portals' forms with the `listing/` files as the source.
- Deciding the demo store's name and who holds its credentials.
