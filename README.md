# Shootika for AI assistants

[Shootika](https://shootika.com) turns the flat-lays a store already has into
on-model product photos, for a Shopify store or any other online store. This
plugin connects Shootika to your AI assistant, so you can ask it to shoot your
products, show you the results and publish the ones you like.

It contains no server code. It points your assistant at the hosted Shootika
MCP server, `https://mcp.shootika.com`, and adds one skill, `shoot-products`,
that walks the assistant through a shoot from start to publish.

## What you can ask

- "Which of my products have no model photos yet?"
- "Shoot the new linen dresses on a model in a studio style."
- "Show me the frames from today and publish the second one."
- "How many frames do I have left this month?"

## Install

**Claude Code**

```
/plugin install shootika --marketplace shootika-ai/plugin
```

**Codex**

```
codex plugin marketplace add shootika-ai/plugin
codex plugin add shootika@shootika
```

**Claude.ai, ChatGPT and other assistants** that take a remote MCP server by
URL: add a custom connector with the URL `https://mcp.shootika.com`.

## Connecting

You need a Shootika account: the Shopify app, or the web app at
[panel.shootika.com](https://panel.shootika.com/signup).

The first time the assistant uses Shootika, it opens a Shootika page where you
approve the connection. Shopify stores approve inside their Shopify admin;
web app stores approve in the Shootika web app. You choose what the assistant
may do:

| Permission | Lets the assistant |
|---|---|
| Read | See your account, products, models, styles, scenes and shoots |
| Catalog | Add products and product photos (web app stores only) |
| Shoot | Request scenes and start shoots, which use frames from your plan |
| Publish | Approve frames onto your products, and take them back off |

You can see and disconnect every connected assistant, and disconnecting stops
it at once:

- **Web app stores:** Settings, Connected assistants.
- **Shopify stores:** open
  `https://admin.shopify.com/store/<your-store>/apps/shootika/app/connections`.
  Removing the Shootika app also disconnects every assistant.

## How it treats your store

- Every shoot uses one frame from your plan. The assistant checks how many you
  have left and asks before starting shoots you did not ask for.
- Nothing is published until you say so. On a Shopify store, an approved frame
  goes on the live product page.

## What this plugin sends and fetches

The plugin runs no code on your computer. It adds one remote MCP server and
one skill written in plain text.

- Your assistant connects only to `https://mcp.shootika.com`, over HTTPS, after
  you approve the connection. It authenticates with an OAuth token issued
  when you approve, which stops working as soon as you disconnect.
- Through that connection the assistant reads your Shootika account, products,
  scenes and shoots, and, with your permission, adds products, starts shoots
  and publishes frames. Product photos you add by URL are fetched by
  Shootika's servers, not by the plugin.
- Frame previews come back to your assistant as small images, with a link to
  the full-size image.

## Privacy

Shootika's privacy policy: <https://shootika.com/legal/privacy/>.
Support: support@shootika.com.

Shootika is built by [Dimenso](https://dimenso.io), DIMENSO L.L.C-FZ.

## License

MIT. See [LICENSE](LICENSE).
