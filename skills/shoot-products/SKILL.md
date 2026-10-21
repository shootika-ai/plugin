---
name: shoot-products
description: Creates on-model product photos for a store with Shootika. Use when someone asks to shoot, photograph or create model photos for their products, find products that have no model photos, check on shoots, or publish (approve) frames to their store. Needs the Shootika connector.
---

# Shoot products with Shootika

Shootika puts a store's garments on AI models and returns the result as a
frame. This skill walks through one round: find the products, choose a scene,
start the shoots, show the frames, and publish only the frames the person
picks.

## Rules that always apply

- **A shoot costs one frame from the store's plan.** Call `get_account` first
  and say how many frames are left. Never start shoots the person did not ask
  for, and confirm the count before starting more than one.
- **Pass a `request_id` to every `start_shoot`** (for example the product id
  plus the scene id). Repeating a call with the same `request_id` within 24
  hours returns the first result instead of charging a second shoot.
- **Publishing is the person's call.** Show each frame and wait for a clear yes
  before `approve_frame`. On Shopify stores approving puts the frame on the
  live product page, where shoppers see it. Ask before `remove_frame` too.
- If a tool says the connection is missing a permission, tell the person which
  one and that they can reconnect Shootika to grant it. Do not retry.

## The round

1. **Check the account.** `get_account` gives the store, its plan and the
   frames left this month.
2. **Find the products.** `list_products` (24 per page; follow `page` while
   more exist). To find products without model photos, compare against
   `list_shoots` filtered by `product_id`, or ask the person which ones.
   - Web app stores can add a missing product with `add_product`, or a photo
     with `add_product_image`, from public image URLs.
   - Shopify stores cannot: their products come from Shopify, so the person
     adds them there.
3. **Choose a scene.** A scene is a model in a style and pose.
   - `list_scenes` with `status` ready shows what the store already has.
   - For something new, `list_models` and `list_styles`, then
     `request_scene`. It is free and safe to repeat. Wait until
     `list_scenes` shows it ready.
   - Offer the person two or three options rather than picking silently.
4. **Pick the photo.** `get_product` lists a product's photos; its id is the
   `source_image_id`. Use the one that shows the whole garment most clearly,
   or ask. If someone is wearing the garment in it, pass
   `garment_photo_type` `model`; the default is `flat-lay`.
5. **Start the shoots** with `start_shoot`, one per product and scene, each
   with its own `request_id`. They return at once with the frame queued.
6. **Wait for results** with `get_shoot`. It waits a few seconds; call it again
   with the same id while the frame is queued or processing. A failed frame
   says why, and its frame was refunded.
7. **Show the frames.** Give the person each preview and its full-size link,
   and ask which to publish.
8. **Publish** the chosen frames with `approve_frame`, then confirm what was
   published and how many frames remain.

## Good to know

- `list_shoots` filtered by `approved` shows what is already live.
- A removed frame is kept and can be approved again until it expires.
- To shoot a frame again, pass its id as `regenerate_of` to `start_shoot`. That
  is a new shoot and costs a frame.
