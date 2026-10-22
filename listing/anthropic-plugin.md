# Anthropic directory: the plugin bundle submission

The answers for the **Plugin bundle** form at claude.ai/directory/manage.
Submit the MCP connector first (`anthropic-connector.md`), from the same
organization, so the two listings can be paired.

## Source

- **Repository:** `shootika-ai/plugin`
- **Plugin path:** empty (the plugin is at the repository root)
- **Tracked branch:** `main`
- **How new versions reach the directory:** GitHub push webhook. Set it up
  after submitting; it needs admin access to the repository.

Run `claude plugin validate --strict .` and `python3 scripts/check.py` before
pressing Validate in the portal. Both must be clean.

## Listing details

Read from `.claude-plugin/plugin.json` and `README.md`. Nothing to type; change
the files and validate again if something reads wrong.

## Data handling

- **Reads or stores personal data:** reads only, through the declared
  connector: the approver's name is shown on the Shootika connect page, and
  the assistant reads the store's products, photos and frames. The plugin
  stores nothing itself.
- **Sends data to services other than its declared connectors:** no.
- **Retention:** Shootika's, per `https://shootika.com/legal/privacy/`. The
  plugin keeps nothing.
- **Intended for people under 18:** no.

## Compliance

Contact email: `support@shootika.com`. Four acknowledgements, all required.

## Review and submit

**Auto-publish passing versions:** on. A reviewer publishes the first version
either way.

## After listing

A release is: edit, bump `VERSION` and both manifests, merge to `main`. The
webhook triggers a scan; the version publishes under whichever setting the
reviewer applied.

## Surface test

2026-10-22, version 0.2.0, `dist/shootika-0.2.0-claude.zip` uploaded to the
Dimenso workspace on claude.ai (Customize, Plugins, Add, Upload plugin):

- Archive accepted; the preview showed the manifest's name and description.
  Pass.
- Plugin page: "Shootika, 0.2.0, 4 skills". The Skills tab lists
  `/shoot-products`, `/review-frames`, `/cast-models` and `/connect` with
  their descriptions verbatim. Pass.
- Connectors tab lists `shootika` from `.mcp.json`. Adding it, claude.ai
  detected "Sign in now" (OAuth) and "Use Claude's published identity"
  (CIMD) from the server's metadata without any manual setting. Pass.
- Connect opened `https://panel.shootika.com/connect?request=...`, titled
  "Connect an AI assistant · Shootika". Pass for the hand-off. The sign-in
  and approval, and the `get_account` question afterwards, were left to the
  owner, since they grant a store permission.
