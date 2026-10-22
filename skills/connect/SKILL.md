---
name: connect
description: Connect an AI assistant to a Shootika store, or fix a connection. Use when Shootika is not connected yet, a Shootika tool answers that the connection is missing a permission or is no longer valid, or someone asks what the assistant may do with their store, how to allow extra frames, or how to see and disconnect assistants. Explains the Shootika connect page and its four permissions; starts no shoot.
---

# Connect Shootika

Connecting takes one approval in the person's browser. Shootika opens a page,
they sign in or name their store, choose what the assistant may do, and
approve. This skill explains that page so the person knows what they are
agreeing to, and what to do when a connection stops working.

## An account first

Shootika is the Shopify app at apps.shopify.com/shootika, or the web app at
panel.shootika.com. A web app account can be created during connection; a
Shopify store installs the app first, then connects.

## The connect page

1. The page asks "How do you use Shootika?". A web app user signs in with
   their password, a sign-in link sent to their email, or the code from that
   email. A Shopify user types their store's address, such as
   `acme-store.myshopify.com`, and approves inside their Shopify admin.
2. The page names the assistant and the store: "*Assistant* wants to connect
   to *your store*". The person should check that the store in the heading is
   the one they meant, and approve only if they just clicked Connect in their
   own assistant.
3. A connection request lasts 10 minutes. If it runs out, the person starts
   again from the assistant.

## The four permissions

| Permission | Lets the assistant |
|---|---|
| Read | See the account, products, models, styles, scenes and shoots |
| Catalog | Add products and product photos (web app stores only) |
| Shoot | Request scenes and start shoots, which use frames from the plan |
| Publish | Approve frames onto products, and take them back off |

Read is always included. The others start unticked unless Shootika has
verified the assistant, so the person ticks or unticks the ones they want. In the web app, a team member whose role cannot edit products
(a viewer or a billing user) can grant Read only.

## Extra frames

The page may show "Allow extra frames past my plan (billed on monthly
plans)". It starts off. Left off, the assistant cannot start shoots once the
plan's frames are used up. Extra frames are billed on monthly plans, Shopify
or web app; on a yearly plan or the Free plan they are never billed, and
shoots stop when the frames run out. The switch can be changed later for each
connection, where connections are managed.

## Fixing a connection

- **"This connection is not allowed to use *tool*: it needs the
  "*permission*" permission."** The person disconnects the assistant, then
  connects it again and ticks that permission. Permissions are chosen only
  when approving, so there is no other way to add one.
- **"This connection was approved by someone who can no longer allow
  this."** The approver's role changed. A store admin connects the assistant
  again.
- **The assistant asks to connect again.** It was disconnected, or the store
  removed the Shopify app. Approve it again, after reinstalling the app if
  that is the cause.

## Where connections are managed

- **Web app stores:** Settings, Connected assistants. Each row shows who
  connected the assistant, what it can do and when it was last used. Admins
  can disconnect it and, on a monthly plan, allow extra frames. Other members
  see the list.
- **Shopify stores:**
  `https://admin.shopify.com/store/<your-store>/apps/shootika/app/connections`,
  with the store's name in place of `<your-store>`. The page is not in the
  Shootika app's menu. Each connection can be disconnected or allowed extra
  frames there. Removing the Shootika app disconnects every assistant, and
  reinstalling does not bring them back.

Disconnecting stops the assistant at once.

## Adding Shootika to an assistant

- **Claude.ai and ChatGPT:** find Shootika in the directory, or add a custom
  connector with the URL `https://mcp.shootika.com`.
- **Claude Code:** `/plugin install shootika --marketplace shootika-ai/plugin`,
  then `/mcp`, Shootika, Authenticate.
- **Codex:** `codex plugin marketplace add shootika-ai/plugin`, then
  `codex plugin add shootika@shootika`.
- **Cursor and other editors:** add an MCP server with the URL
  `https://mcp.shootika.com`.

The full guides are at docs.shootika.com/ai-assistants/.
