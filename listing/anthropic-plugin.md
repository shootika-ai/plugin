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

Recorded by Task 7 of the implementation plan: date, version uploaded, and one
line per check.
