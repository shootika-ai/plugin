# Anthropic directory: the MCP connector submission

The words for the **MCP connector** form at claude.ai/directory/manage, step by
step as the portal asks. Edit here, then paste. Limits are in the headings.

## 1. Connection

Server URL: `https://mcp.shootika.com`. One URL for every user.

## 2. Tools

Synced from the server. Every tool has a `title`, `readOnlyHint`,
`openWorldHint` and, on write tools, `destructiveHint` and `idempotentHint`.
Nothing to enter.

## 3. Listing

**Name (100):** Shootika

**One-liner (200):** On-model product photos from the flat-lays your store
already has: shoot, review and publish from your assistant.

**Description (2,000):**

Shootika puts a store's garments on AI models and returns finished on-model
photos, called frames. Connect it and ask your assistant to find the products
that have no model photos yet, shoot them in a studio or lifestyle look, show
you the frames, and publish the ones you choose.

It works for a Shopify store, where an approved frame goes straight onto the
live product page, and for any other online store through the Shootika web
app, where approved frames are saved to the product for you to download.

Every shoot uses one frame from your Shootika plan. The assistant checks how
many you have left and asks before spending. Nothing is published until you
say so. Shootika only adds and removes its own frames: it cannot change
prices or other product details, and it has no customer or order data.

You approve the connection yourself on a Shootika page and choose what the
assistant may do: read your catalog and frames, add products and photos (web
app stores), start shoots, or publish frames. You can see every connected
assistant and disconnect it at any time.

**Categories (1 to 5):** choose from the portal's list. Prefer the ones that
name e-commerce, design or marketing. Record the final choice here.

**Documentation URL:** `https://docs.shootika.com/ai-assistants/`

**Privacy policy URL:** `https://shootika.com/legal/privacy/`

**Support contact:** `support@shootika.com`

**Icon:** `assets/icon.png` from this repository (512 px PNG).

**URL slug:** `shootika`. Permanent once published.

## 4. Use cases

- Find the products in a catalog that have no model photos yet, and shoot
  them.
- Shoot a new product on a model in a chosen look and review the frames.
- Publish the frames the merchant picks to their products.

**Before connecting, users need:** a Shootika account, either the Shootika
Shopify app or the Shootika web app. A web app account can be created during
connection.

**Reads or writes:** both. Reads the catalog and frames; writes products and
photos (web app stores), shoots, and frame approvals.

## 5. Company

Dimenso, DIMENSO L.L.C-FZ, `https://dimenso.io`. Primary contact for review
updates: `support@shootika.com`.

## 6. Authentication

OAuth 2.1 with PKCE. The server supports dynamic client registration and
Client ID Metadata Documents. No Anthropic-held client credentials. Every tool
requires a signed-in connection; none works before authentication. Metadata at
`https://api.shootika.com/.well-known/oauth-authorization-server`.

## 7. Data handling

The underlying API is Shootika's own. The connector handles no personal health
data and no sponsored content.

## 8. Test and launch

See `reviewer-account.md` for what the test store contains and where its
credentials live. The access instructions to paste: sign in at
`https://panel.shootika.com/login` with the email and password provided; the
store has products with photos, ready scenes, and frames, and enough credits
for the review. Every tool has been run from Claude as a custom connector.

## 9. Compliance

Seven acknowledgements: the directory guidelines, first-party API usage,
financial transactions, AI media generation, prompt injection, conversation
data collection, and public documentation. All seven are required; read each
before ticking.

## 10. Review and submit

Check for quality warnings on short answers before submitting.
