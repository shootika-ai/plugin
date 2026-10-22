# Shootika for AI assistants

[Shootika](https://shootika.com) turns the flat-lay photos a clothing store
already has into on-model product photos, for a Shopify store or any other
online store. This plugin connects Shootika to your AI assistant, so you can
ask it to shoot your products, show you the results and publish the ones you
like, in the same conversation where you do the rest of your work.

## What you can ask

- "Which of my products have no model photos yet?"
- "Shoot my newest product on a model and show me the frames."
- "Show me the frames from today and publish the second one."
- "How many frames do I have left this month?"

The plugin adds four skills that walk the assistant through those jobs:
`shoot-products` (find products, pick a photo and a scene, start shoots and
wait for the frames), `review-frames` (show frames, publish or take back the
ones you choose), `cast-models` (pick the model, pose and style, or set up one
house model for the whole catalog) and `connect` (what the connection asks for
and how to change it).

## How it treats your store

- **Every shoot uses one frame from your plan.** The assistant checks how many
  you have left and asks before starting shoots you did not ask for.
- **Nothing is published until you say so.** The assistant shows you each
  frame and waits for a clear yes. On a Shopify store, an approved frame goes
  on the live product page, where shoppers see it. On a web app store it is
  saved to the product in Shootika.
- **It only adds and removes its own frames.** It cannot change prices or
  other product details, and Shootika has no customer or order data.

## Connecting

You need a Shootika account: the
[Shopify app](https://apps.shopify.com/shootika), or the web app at
[panel.shootika.com](https://panel.shootika.com/signup).

The first time the assistant uses Shootika, it opens a Shootika page where you
approve the connection. Shopify stores approve inside their Shopify admin; web
app stores approve in the Shootika web app. You choose what the assistant may
do:

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

The full guides are at [docs.shootika.com/ai-assistants](https://docs.shootika.com/ai-assistants/).

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

**Cursor and other assistants** that take a remote MCP server by URL: add
`https://mcp.shootika.com`.

## What this plugin sends and fetches

The plugin runs no code on your computer. It is one remote MCP server
reference and four skills written in plain text.

- Your assistant talks to three Shootika addresses, all over HTTPS: the tools
  at `https://mcp.shootika.com`; sign-in and tokens at
  `https://api.shootika.com`; and, in your own browser, the approval page at
  `https://panel.shootika.com` or inside your Shopify admin. It authenticates
  with an OAuth token issued when you approve, which stops working as soon as
  you disconnect.
- With the Read permission, the assistant reads your Shootika account, your
  products and their photos, the model, style and scene library, and your
  shoots and frames. With Catalog it adds products and photos; with Shoot it
  requests scenes and starts shoots; with Publish it approves frames onto your
  products and takes them off.
- Product photos you add by URL are fetched by Shootika's servers, not by the
  plugin or your assistant.
- Frame previews come back to your assistant as small images, with a link to
  the full-size image on Shootika's servers.
- The plugin stores nothing itself and sends nothing to any other service.

## Privacy

Shootika's privacy policy: <https://shootika.com/legal/privacy/>.
Terms of service: <https://shootika.com/legal/terms/>.
Support: support@shootika.com.

Shootika is built by [Dimenso](https://dimenso.io), DIMENSO L.L.C-FZ.

## License

MIT. See [LICENSE](LICENSE).
