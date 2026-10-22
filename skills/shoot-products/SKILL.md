---
name: shoot-products
description: Shoot a store's products on AI models with Shootika and get frames back. Use when someone asks to shoot, photograph or make on-model photos of their products, to find products that have no model photos yet, or to check on a shoot that is running. Needs the Shootika connector. Not for publishing or removing frames (review-frames), choosing a model, pose or style (cast-models), or connection and permission problems (connect).
---

# Shoot products with Shootika

A shoot puts one product photo on one scene's model and returns one frame.
Every shoot uses one frame from the store's plan, whether or not the person
keeps the result. This skill takes one round from "which products" to "the
frames are ready"; `review-frames` takes over from there.

## Before spending anything

- Call `get_account` first and tell the person how many frames are left.
- Never start a shoot the person did not ask for. When they ask for several,
  say how many frames that uses and confirm the count before starting more
  than one.
- If a shoot is refused because the plan's frames are used up, the message
  says what the person can do. `references/messages.md` lists those messages
  and what to tell them. Do not retry.

## Find the products

- `list_products` lists the catalog newest first, 24 per page. Follow `page`
  while more exist. Each product carries its id, title, garment category and
  photos.
- A product has no model photos when `list_shoots` filtered by its
  `product_id` and `status` ready returns nothing; failed or canceled frames
  are not photos. For a large catalog, ask the person which products they
  mean rather than paging through everything.
- Web app stores can add a missing product with `add_product`, or a photo with
  `add_product_image`, from public image URLs. Shopify stores cannot: their
  products come from Shopify. `references/store-types.md` has the two cases.

## Pick the photo and the scene

- `get_product` lists a product's photos. The photo's id is the
  `source_image_id`. Use the one that shows the whole garment most clearly, or
  ask when two are close. Flat-lay photos work best.
- If someone is wearing the garment in the photo, pass `garment_photo_type`
  `model`. The default, `flat-lay`, is for the garment alone.
- A shoot needs a scene whose status is `ready` in `list_scenes`. If the store
  has one that fits, use it. For a new model, style or pose, or to offer the
  person options, use `cast-models`, then come back with the scene id.

## Start and wait

- `start_shoot` once per product and scene, each call with a fresh
  `request_id`, for example the product id, the scene id and the time joined.
  Reuse an id only to retry that same call after a network error: within 24
  hours it returns the first result instead of starting and charging a second
  shoot. A second shoot the person asks for needs a new id; the same id with
  different arguments is refused.
- `start_shoot` returns at once with the frame queued. `get_shoot` waits a few
  seconds and returns the frame; call it again with the same id while the
  status is `queued` or `processing`. Do not narrate each poll.
- A failed frame says why, and its frame was refunded. Tell the person and
  offer to try again with another photo or scene.

## Then

Hand the ready frames to `review-frames`: each preview, its full-size link,
and the question of which to publish. Finish by saying how many frames remain
on the plan.

## If a tool refuses

A tool that answers that the connection is not allowed to use it names the
permission it needs. Tell the person which permission and that they can
connect Shootika again to grant it; `connect` explains how. Do not retry the
call. `references/messages.md` has every refusal and what each means.
