# Backend: OpenID Connect pieces for OpenAI's directory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the Shootika OAuth server what ChatGPT's workspace domain restriction needs, the `openid` and `email` scopes, an OpenID Connect discovery document and a UserInfo endpoint, without issuing ID tokens or changing consent, permissions or tools, and stand up the demo store both directories' reviewers log in to.

**Architecture:** OIDC scopes are pass-through: parsed at authorize, stored beside the permission scopes on `PendingAuthorization` and `Grant`, echoed in the token response's `scope`, and never placed in `Token.scopes`, so every permission check stays as it is. UserInfo authenticates with the same bearer check the MCP endpoint uses and reads the approver recorded on the grant. The domain-verification view already exists.

**Tech Stack:** Django 5, DRF, the Django test runner (`python manage.py test`), PostgreSQL in production and SQLite locally, Celery untouched.

**Spec:** `docs/superpowers/specs/2026-10-22-directory-listing-design.md` in `shootika-ai/plugin`, Part 2. This plan is executed in `shootika/backend`; its first task copies the plan there. The backend's `CLAUDE.md` governs commands, migrations and test conventions.

## Global Constraints

- Branch `feat/oidc-userinfo` off `origin/develop`. `develop` deploys to staging, `main` to production.
- `python manage.py makemigrations --check --dry-run` is clean before every commit; `python manage.py test --parallel` passes.
- No network call inside `GET /oauth/userinfo`. No change to `selectors.SCOPES`, `canonical_scopes`, `grant_permissions`, `allowed_scopes`, the consent endpoints or any MCP tool.
- `Token.scopes` holds permission scopes only. `authenticate_access_token` is unchanged.
- Error bodies follow the OAuth wire format through `OAuthError`; descriptions carry no em-dash.
- Secrets are never stored raw; nothing here stores a new secret.
- Commits follow Conventional Commits and end with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

## Review Focus

1. A client that sends `scope=openid email` and no permission scope: today an empty permission list means "all four"; that default must survive, so the pending request still carries all four permission scopes. Test in Task 2.
2. A refresh that names `scope=openid read`: the access token narrows to `read`, and the response echoes `read openid`. Test in Task 2.
3. UserInfo presented a refresh token, an expired access token, or a token for a grant whose approver is gone: 401 with `WWW-Authenticate: Bearer error="invalid_token"`, never a 500 and never claims. Test in Task 4.
4. A Shopify approver whose staff row has an email but `email_verified` false: claims carry `email` and `email_verified: false`, not a silent omission. Test in Task 4.
5. The consent page's request detail must not show `openid` or `email` as a permission a merchant can tick: `pending_detail`'s `scopes` stays the permission list. Test in Task 2.

---

### Task 0: Branch and carry the plan

- [ ] **Step 1: Create the branch**

```bash
cd ~/Develop/shootika/backend
git fetch origin
git checkout -b feat/oidc-userinfo origin/develop
```

- [ ] **Step 2: Copy the spec's Part 2 and this plan**

Copy `docs/superpowers/plans/2026-10-22-backend-openai-oidc.md` from the plugin repository to the same path in the backend, and the spec to `docs/superpowers/specs/2026-10-22-directory-listing-design.md`.

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers
git commit -m "docs: plan for the OpenID Connect pieces OpenAI's directory needs"
```

---

### Task 1: Scopes and discovery metadata

**Files:**
- Modify: `oauth_server/selectors.py`
- Modify: `oauth_server/views/metadata.py`
- Modify: `oauth_server/urls.py`
- Test: `oauth_server/tests/test_metadata.py`

**Interfaces:**
- Produces: `selectors.OIDC_SCOPES = ['openid', 'email']`; `selectors.split_scopes(names) -> tuple[list[str], list[str]]` returning `(permission_names, oidc_names)` in request order with OIDC names removed from the first list and only known OIDC names in the second, unknown names left in the first list for the caller to refuse; `selectors.userinfo_endpoint() -> str` = `f'{issuer()}/oauth/userinfo'`; `selectors.jwks_endpoint() -> str` = `f'{issuer()}/oauth/jwks'`; `selectors.oidc_metadata() -> dict`; `as_metadata()` and `prm_metadata()` with `scopes_supported` = `SCOPES + OIDC_SCOPES` and `as_metadata()` with `userinfo_endpoint`; views `openid_configuration` and `jwks` in `views/metadata.py`.

- [ ] **Step 1: Write the failing tests in `test_metadata.py`**

```python
OIDC = ['openid', 'email']

def test_split_scopes_separates_oidc_names(self):
    self.assertEqual(selectors.split_scopes(['read', 'openid', 'shoot', 'email']), (['read', 'shoot'], ['openid', 'email']))
    self.assertEqual(selectors.split_scopes(['openid', 'bogus']), (['bogus'], ['openid']))
    self.assertEqual(selectors.split_scopes([]), ([], []))

def test_as_metadata_advertises_oidc_scopes_and_userinfo(self):
    m = selectors.as_metadata()
    self.assertEqual(m['scopes_supported'], SCOPES + OIDC)
    self.assertEqual(m['userinfo_endpoint'], 'https://api.test/oauth/userinfo')

def test_prm_metadata_advertises_oidc_scopes(self):
    self.assertEqual(selectors.prm_metadata()['scopes_supported'], SCOPES + OIDC)

def test_oidc_metadata_is_the_oauth_document_plus_the_oidc_fields(self):
    m = selectors.oidc_metadata()
    for key, value in selectors.as_metadata().items():
        self.assertEqual(m[key], value, key)
    self.assertEqual(m['jwks_uri'], 'https://api.test/oauth/jwks')
    self.assertEqual(m['subject_types_supported'], ['public'])
    self.assertEqual(m['id_token_signing_alg_values_supported'], ['none'])
    self.assertEqual(m['claims_supported'], ['sub', 'email', 'email_verified'])

def test_openid_configuration_and_jwks_endpoints(self):   # in MetadataViewTests
    self.assertEqual(self._get('/.well-known/openid-configuration'), selectors.oidc_metadata())
    self.assertEqual(self._get('/oauth/jwks'), {'keys': []})
```

Update the existing `test_as_metadata` and `test_prm_metadata` expectations from `SCOPES` to `SCOPES + OIDC`.

- [ ] **Step 2: Run them to verify they fail**

Run: `python manage.py test oauth_server.tests.test_metadata -v 2`
Expected: FAIL on `split_scopes`, `oidc_metadata`, `userinfo_endpoint`, and 404s on the two new paths.

- [ ] **Step 3: Implement in `selectors.py`, `views/metadata.py`, `urls.py`**

`oidc_metadata()` is `{**as_metadata(), 'jwks_uri': ..., 'subject_types_supported': ['public'], 'id_token_signing_alg_values_supported': ['none'], 'claims_supported': [...]}`. The `jwks` view answers `{'keys': []}` through `_json` (cached like the other metadata). Routes: `.well-known/openid-configuration` and `oauth/jwks`. Keep `response_types_supported` at `['code']`: no ID token is ever issued, and `id_token_signing_alg_values_supported: ['none']` says so honestly.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python manage.py test oauth_server.tests.test_metadata -v 2`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add oauth_server/selectors.py oauth_server/views/metadata.py oauth_server/urls.py oauth_server/tests/test_metadata.py
git commit -m "feat(oauth): advertise openid and email, serve OpenID Connect discovery and an empty JWKS"
```

---

### Task 2: Accept and echo the OIDC scopes

**Files:**
- Modify: `oauth_server/models.py` (`PendingAuthorization.oidc_scopes`, `Grant.oidc_scopes`)
- Create: `oauth_server/migrations/0002_oidc_scopes.py` (generated)
- Modify: `oauth_server/services/authorize.py` (`start_authorization`, `approve_pending`)
- Modify: `oauth_server/services/tokens.py` (`_issue`, `_narrowed_scopes`)
- Test: `oauth_server/tests/test_authorize.py`, `oauth_server/tests/test_token.py`, `oauth_server/tests/test_panel_consent.py`

**Interfaces:**
- Consumes: `selectors.split_scopes`, `selectors.OIDC_SCOPES` from Task 1.
- Produces: `PendingAuthorization.oidc_scopes: JSONField(default=list)`, `Grant.oidc_scopes: JSONField(default=list)`; the token response `scope` string is `' '.join(scopes + grant.oidc_scopes)`.

- [ ] **Step 1: Write the failing tests**

In `test_authorize.py`:

```python
def test_openid_and_email_are_accepted_and_kept_apart(self):
    r = self.get(self.params(scope='openid read email shoot'))
    pending = PendingAuthorization.objects.get()
    self.assertEqual(pending.scopes, ['read', 'shoot'])
    self.assertEqual(pending.oidc_scopes, ['openid', 'email'])

def test_only_oidc_scopes_still_means_every_permission(self):      # Review Focus 1
    self.get(self.params(scope='openid email'))
    pending = PendingAuthorization.objects.get()
    self.assertEqual(pending.scopes, ['read', 'catalog', 'shoot', 'publish'])
    self.assertEqual(pending.oidc_scopes, ['openid', 'email'])

def test_an_unknown_scope_beside_openid_is_still_refused(self):
    r = self.get(self.params(scope='openid profile'))
    self.assertEqual(r.status_code, 400)
    self.assertIn('profile', r.content.decode())
```

In `test_token.py` (`issue_code` gains an `oidc=()` parameter that sets `oidc_scopes` on the pending it creates):

```python
def test_the_scope_string_echoes_the_oidc_scopes_after_the_permissions(self):
    body = self.connect(oidc=['openid', 'email'])
    self.assertEqual(body['scope'], 'read catalog shoot publish openid email')
    self.assertEqual(Grant.objects.get().oidc_scopes, ['openid', 'email'])
    for t in Token.objects.all():
        self.assertEqual(t.scopes, ALL)                                  # never in Token.scopes

def test_refresh_may_name_oidc_scopes_and_narrows_only_permissions(self):   # Review Focus 2
    body = self.connect(oidc=['openid', 'email'])
    r = self.refresh(body['refresh_token'], scope='openid read')
    self.assertEqual(r.status_code, 200, r.content)
    self.assertEqual(r.json()['scope'], 'read openid email')
    self.assertEqual(Token.objects.filter(kind=Token.KIND_ACCESS).latest('created_at').scopes, ['read'])

def test_refresh_with_an_unknown_scope_is_still_invalid_scope(self):
    body = self.connect()
    self.assert_oauth_error(self.refresh(body['refresh_token'], scope='openid profile'), 'invalid_scope')
```

In `test_panel_consent.py`, Review Focus 5: a pending with `oidc_scopes=['openid', 'email']` whose request detail `scopes` and `allowed_scopes` contain neither name.

- [ ] **Step 2: Run them to verify they fail**

Run: `python manage.py test oauth_server.tests.test_authorize oauth_server.tests.test_token oauth_server.tests.test_panel_consent -v 2`
Expected: FAIL with `TypeError` on `oidc_scopes`, `invalid_scope` on `openid`, and scope-string mismatches.

- [ ] **Step 3: Add the fields and generate the migration**

`oidc_scopes = models.JSONField(default=list)` on both models, then `python manage.py makemigrations oauth_server -n oidc_scopes`.

- [ ] **Step 4: Implement the scope handling**

In `start_authorization`: `requested, oidc = selectors.split_scopes((single('scope') or '').split())`; the unknown check and the `canonical_scopes(requested or SCOPES)` default operate on `requested`; `PendingAuthorization.objects.create(..., oidc_scopes=oidc)`. In `approve_pending`: `Grant.objects.create(..., oidc_scopes=list(pending.oidc_scopes))`. In `_issue`: `'scope': ' '.join(scopes + list(grant.oidc_scopes))`. In `_narrowed_scopes`: split with `split_scopes` first and run the unknown and beyond checks on the permission names only; the OIDC names a refresh sends are discarded, the grant's own are echoed.

- [ ] **Step 5: Run the tests, the migration check and the whole suite**

Run: `python manage.py makemigrations --check --dry-run && python manage.py test --parallel`
Expected: no changes detected; all tests pass, including the existing `test_the_happy_path_issues_a_bearer_access_token_and_a_refresh_token`, whose `scope` stays `read catalog shoot publish` because that pending has no OIDC scopes.

- [ ] **Step 6: Commit**

```bash
git add oauth_server
git commit -m "feat(oauth): accept openid and email as pass-through scopes and echo them"
```

---

### Task 3: `ShopifyStaffMember.email_verified`

**Files:**
- Modify: `shops/models.py` (`ShopifyStaffMember`)
- Create: `shops/migrations/0006_shopifystaffmember_email_verified.py` (generated)
- Modify: `shops/staff.py` (`resolve_staff_member`)
- Test: `shops/tests/test_staff.py`

**Interfaces:**
- Produces: `ShopifyStaffMember.email_verified: BooleanField(default=False)`, filled from `associated_user.email_verified` on every successful lookup.

- [ ] **Step 1: Write the failing test in `test_staff.py`**

Following the file's existing pattern for mocking `exchange_id_token_for_user`:

```python
def test_a_lookup_records_whether_shopify_verified_the_email(self):
    # associated_user has email 'ada@acme.test' and email_verified True
    member = resolve_staff_member(self.shop, '42', 'idt')
    self.assertEqual(member.email, 'ada@acme.test')
    self.assertTrue(member.email_verified)

def test_a_missing_email_verified_flag_is_false(self):
    # associated_user without the key
    self.assertFalse(resolve_staff_member(self.shop, '42', 'idt').email_verified)
```

- [ ] **Step 2: Run to verify they fail**

Run: `python manage.py test shops.tests.test_staff -v 2`
Expected: FAIL, `AttributeError: email_verified`.

- [ ] **Step 3: Add the field, generate the migration, store the flag**

`email_verified = models.BooleanField(default=False)` after `email`; `python manage.py makemigrations shops -n shopifystaffmember_email_verified`; in `resolve_staff_member`'s `defaults`, `'email_verified': bool(user.get('email_verified'))`.

- [ ] **Step 4: Run the tests and the migration check**

Run: `python manage.py makemigrations --check --dry-run && python manage.py test shops.tests.test_staff -v 2`
Expected: clean; PASS.

- [ ] **Step 5: Commit**

```bash
git add shops
git commit -m "feat(shops): record whether Shopify verified a staff member's email"
```

---

### Task 4: UserInfo endpoint

**Files:**
- Create: `oauth_server/views/userinfo.py`
- Modify: `oauth_server/selectors.py` (`userinfo_claims`)
- Modify: `oauth_server/urls.py`
- Create: `oauth_server/tests/test_userinfo.py`

**Interfaces:**
- Consumes: `tokens.authenticate_access_token(raw, *, audience)`, `selectors.mcp_resource()`, `Grant.panel_user`, `Grant.shopify_staff`, `ShopifyStaffMember.email_verified` from Task 3.
- Produces: `selectors.userinfo_claims(grant) -> dict` and `GET /oauth/userinfo`.

- [ ] **Step 1: Write the failing tests in `test_userinfo.py`**

Setup like `test_access_tokens.py`: `make_panel_shop(role='admin')`, a DCR client, a grant, `issue_tokens(grant, audience='https://mcp.test', scopes=['read'])`. A helper `get(raw)` sends `GET /oauth/userinfo` with `HTTP_AUTHORIZATION=f'Bearer {raw}'`.

```python
def test_a_panel_grant_returns_sub_email_and_verified(self):
    r = self.get(self.raw)
    self.assertEqual(r.status_code, 200)
    self.assertEqual(r['Cache-Control'], 'no-store')
    self.assertEqual(r.json(), {'sub': str(self.grant.pk), 'email': self.admin.email, 'email_verified': True})

def test_a_shopify_grant_uses_the_staff_members_email_and_flag(self):
    staff = ShopifyStaffMember.objects.create(shop=shop, shopify_user_id='7', email='s@acme.test',
                                              email_verified=False, synced_at=timezone.now())
    # grant with shopify_staff=staff, panel_user=None
    self.assertEqual(self.get(raw).json(), {'sub': str(grant.pk), 'email': 's@acme.test', 'email_verified': False})   # Review Focus 4

def test_a_shopify_grant_without_an_email_returns_sub_alone(self):
    # staff email '' -> {'sub': str(grant.pk)}

def test_no_token_a_refresh_token_an_expired_token_and_a_gone_approver_are_401(self):  # Review Focus 3
    for raw in ('', refresh_token, expired_access, access_for_grant_whose_panel_user_was_deleted):
        r = self.get(raw)
        self.assertEqual(r.status_code, 401, raw[:12])
        self.assertEqual(r['WWW-Authenticate'], 'Bearer error="invalid_token"')
        self.assertEqual(r.json()['error'], 'invalid_token')

def test_post_is_not_allowed(self):
    self.assertEqual(self.client.post('/oauth/userinfo').status_code, 405)

def test_userinfo_makes_no_network_call(self):
    with patch('shops.shopify_token.exchange_id_token_for_user') as exchange:
        self.get(raw_for_shopify_grant)
    exchange.assert_not_called()

def test_the_middleware_skip_lists_cover_userinfo_and_jwks(self):
    # as MiddlewareSkipTests in test_metadata.py does for /oauth/authorize, for '/oauth/userinfo' and '/oauth/jwks'
```

- [ ] **Step 2: Run to verify they fail**

Run: `python manage.py test oauth_server.tests.test_userinfo -v 2`
Expected: FAIL with 404 on the path and `AttributeError: userinfo_claims`.

- [ ] **Step 3: Implement**

`selectors.userinfo_claims(grant) -> dict`: `{'sub': str(grant.pk)}`; with a `panel_user`, add `email` and `email_verified = user.is_email_verified`; with `shopify_staff` whose `email` is non-empty, add `email` and `email_verified = staff.email_verified`; otherwise `sub` only.

`views/userinfo.py`: `@require_GET def userinfo(request)`: read the bearer as `mcp_server.auth._bearer` does (copy the four lines; do not import from `mcp_server`, which would invert the dependency), `token = authenticate_access_token(raw, audience=selectors.mcp_resource())`, on `None` return `OAuthError('invalid_token', 'The access token is missing, expired or not valid.', 401, headers={'WWW-Authenticate': 'Bearer error="invalid_token"'}).response()`, else `JsonResponse(selectors.userinfo_claims(token.grant))` with `Cache-Control: no-store` and `Pragma: no-cache`. Route `oauth/userinfo`. If the middleware skip lists in `authshop.middleware.ShopifySessionMiddleware` and `accounts.middleware.PanelJWTMiddleware` match `/oauth/` as a prefix, nothing changes there; the test tells you.

- [ ] **Step 4: Run the tests and the whole suite**

Run: `python manage.py test oauth_server.tests.test_userinfo -v 2 && python manage.py test --parallel`
Expected: PASS; whole suite green.

- [ ] **Step 5: Document in `CLAUDE.md`**

In the `oauth_server/` row of the module table and the URL namespaces section, add `/oauth/userinfo`, `/oauth/jwks` and `/.well-known/openid-configuration`, one sentence each, and the rule that `openid` and `email` are pass-through scopes stored in `oidc_scopes`, never in `Token.scopes`.

- [ ] **Step 6: Commit**

```bash
git add oauth_server CLAUDE.md
git commit -m "feat(oauth): UserInfo endpoint for ChatGPT workspace domain restrictions"
```

---

### Task 5: Demo store for reviewers

No code. Done on production by the owner or an admin, after Task 6 is deployed, and recorded in the plugin repository's `listing/reviewer-account.md`.

- [ ] **Step 1: Create the store**

Sign up at `https://panel.shootika.com/signup` with a company-owned mailbox, verify the email, set a password. The store name says what it is for, such as "Shootika Review Store". No second factor or magic-link-only sign-in.

- [ ] **Step 2: Fill it**

Add about twelve products with real flat-lay photos (the website's sample flat-lays in the `shootika` Spaces bucket under `website/source/` are usable), save two or three scenes in the Studio and wait until ready, shoot three or four frames and approve one, so every read tool returns something.

- [ ] **Step 3: Grant credits**

In a production shell, `credits.services.grant_goodwill(shop, amount, expires_at, note='Directory reviewers', source=...)` with an amount that covers two reviews running every tool several times, and an expiry a year out. Record the amount and expiry in `listing/reviewer-account.md`. Re-grant when a review is scheduled if the balance is low.

- [ ] **Step 4: Store the credentials**

In the company password manager under "Shootika directory reviewers". Never in either repository.

---

### Task 6: Verify on staging, then release

- [ ] **Step 1: Open the merge request to `develop`**

Push `feat/oidc-userinfo`, open the MR, let CI run the suite.

- [ ] **Step 2: Check staging after the automatic deploy**

```bash
curl -s https://stg-api.shootika.com/.well-known/openid-configuration | python3 -m json.tool | grep -E 'userinfo_endpoint|jwks_uri|scopes_supported' -A2
curl -s https://stg-api.shootika.com/oauth/jwks
curl -si https://stg-api.shootika.com/oauth/userinfo | head -3
```

Expected: the discovery document lists `openid` and `email` and the two endpoints; `{"keys": []}`; a 401 with `WWW-Authenticate: Bearer error="invalid_token"`. Then connect a staging store from ChatGPT developer mode with `https://stg-mcp.shootika.com`, approve, and confirm the connection completes and a read tool answers. Use the staging API host as the k8s staging overlay names it; the paths above assume `BACKEND_URL` for staging.

- [ ] **Step 3: Release to production**

Merge `develop` to `main` the way the backend releases. Repeat the three `curl` checks against `https://api.shootika.com`. The spec's Part 3 then continues with the OpenAI submission; when the portal issues the domain token, set `OPENAI_APPS_CHALLENGE` in `k8s/overlays/prod/backend-configmap-patch.yaml` and confirm `curl https://mcp.shootika.com/.well-known/openai-apps-challenge` returns it.
