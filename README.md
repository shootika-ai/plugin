# Shootika for AI assistants

[![Shootika MCP connector – tool definition quality and endpoint health on Glama](https://glama.ai/mcp/connectors/com.shootika/shootika/badges/score.svg)](https://glama.ai/mcp/connectors/com.shootika/shootika)

[Shootika](https://shootika.com) turns the flat-lay photos a clothing store
already has into on-model product photos, for a Shopify store or any other
online store. The plugin connects Shootika to Claude, ChatGPT, Codex and other
assistants. What it does, what it asks for and how to install it are in
[shootika/README.md](shootika/README.md).

## Install

**Claude.ai and ChatGPT:** find Shootika in your assistant's directory, or add
a custom connector with the URL `https://mcp.shootika.com`.

**Claude Code**

```
/plugin install shootika --marketplace shootika-ai/plugin
```

**Codex**

```
codex plugin marketplace add shootika-ai/plugin
codex plugin add shootika@shootika
```

## This repository

- `shootika/` is the plugin: its two manifests, the MCP server reference, the
  skills and the icon. It holds only Markdown, JSON, YAML and images.
- `.claude-plugin/marketplace.json` lists it, so both install commands above
  work against this repository.
- `scripts/` checks the directory rules (`python3 scripts/check.py`) and builds
  the upload archives (`bash scripts/build-openai-zip.sh`); CI runs both.
- `listing/` is the copy and notes for the Claude and OpenAI directories.

A release: bump `version` in both manifests under `shootika/`, merge to `main`.

## License

MIT. See [LICENSE](LICENSE).
