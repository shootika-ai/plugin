# OpenAI directory: the With MCP submission

The answers for platform.openai.com/plugins. The ZIP is
`dist/shootika-<VERSION>-openai.zip` from `scripts/build-openai-zip.sh`. The
listing fields, starter prompts and the eight review test cases are read from
`.codex-plugin/plugin.json`; edit the manifest, not the form.

## Prerequisites outside this repository

- A verified developer or business identity on the OpenAI organization, with
  Apps Management write access.
- The domain-verification token the portal issues, set as
  `OPENAI_APPS_CHALLENGE` in the production backend configmap, so that
  `https://mcp.shootika.com/.well-known/openai-apps-challenge` returns it.
- The backend's OpenID Connect pieces live: `openid` and `email` scopes,
  `/.well-known/openid-configuration` and `/oauth/userinfo` on
  `api.shootika.com`.
- A current, successful tool scan of the production server.

## MCP server

`https://mcp.shootika.com`, Streamable HTTP, OAuth 2.1 with PKCE. One server.

## Tool annotations and justifications

| Tool | readOnly | destructive | openWorld | Justification |
|---|---|---|---|---|
| `get_account` | true | false | false | Returns the store, plan and frames left; changes nothing. |
| `list_products` | true | false | false | Lists the store's own products; changes nothing. |
| `get_product` | true | false | false | Returns one product and its photos; changes nothing. |
| `list_models` | true | false | false | Lists the model library; changes nothing. |
| `list_styles` | true | false | false | Lists the style library; changes nothing. |
| `list_scenes` | true | false | false | Lists the store's scenes; changes nothing. |
| `list_shoots` | true | false | false | Lists the store's frames; changes nothing. |
| `get_shoot` | true | false | false | Returns one frame, waiting briefly for it to finish; changes nothing. |
| `add_product` | false | false | true | Adds a product to the store's own catalog in Shootika; nothing is deleted or overwritten. Open world: it fetches photos from public image URLs the person gives. |
| `add_product_image` | false | false | true | Adds a photo to a product; nothing is deleted or overwritten. Open world: it fetches the photo from a public image URL. |
| `request_scene` | false | false | false | Asks Shootika to prepare a scene; free, idempotent, nothing deleted. |
| `start_shoot` | false | true | false | Spends one frame from the merchant's paid plan, which cannot be undone; the description tells the assistant to ask first. |
| `approve_frame` | false | true | true | Changes the live product page on Shopify stores, where shoppers see it; the description tells the assistant to show the frame and ask first. Open world: it writes to the merchant's Shopify store. |
| `remove_frame` | false | true | true | Removes a photo from the live product page on Shopify stores; the description tells the assistant to ask first. Open world: it writes to the merchant's Shopify store. |

Every tool sets all three hints explicitly. `openWorldHint` is true on the four
tools that reach a system Shootika does not control (a public image URL, or the
merchant's Shopify store) and false on the rest, which touch only Shootika.

## Frame domains

None. The server returns text and images, no custom UI.

## Release notes

Same sentence as `extensions.com.openai.publication.release_notes` in the
manifest. Update both together.

## Demo recording URL

`[to record]`. It must show the main tools on at least one supported platform:
connecting, listing products, starting a shoot, reviewing the frame, approving
it.

## Reviewer credentials

Entered in the portal's **Review details** form, never in the ZIP or this
repository. The portal rejects `test_credentials` and `reviewer_instructions`
inside the ZIP. See `reviewer-account.md`. The reviewer account signs in with
email and password only: no second factor, code or magic link.
