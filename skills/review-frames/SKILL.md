---
name: review-frames
description: Show, publish and unpublish Shootika frames. Use when someone asks to see their frames or today's results, to publish, approve or put a frame on a product, to take a frame back off a product, or to shoot a frame again because they do not like it. Needs the Shootika connector. Not for the first shoot of a product (shoot-products).
---

# Review frames with Shootika

A frame is one finished on-model photo. Nothing reaches a product until the
person says so, and on a Shopify store publishing puts the frame in front of
shoppers. This skill shows frames and acts only on a clear yes.

## Show

- `list_shoots` lists frames newest first, 24 per page. Filter by
  `product_id`, by `status`, or by `approved`. The first 4 ready frames come
  with a small preview and a full-size link; the rest carry the link.
- Give the person each frame's preview and its full-size link, and say which
  product and scene it belongs to.
- Ask about one frame at a time: publish it, leave it, or shoot again.

## Publish

- Wait for a clear yes before `approve_frame`. "Looks nice" is not a yes;
  "publish that one" is.
- On a Shopify store, approving publishes the frame to the live product page,
  where shoppers see it. On other stores it is saved to the product in
  Shootika.
- Confirm what was published and where, in the words the tool answers with.

## Take back

- Ask before `remove_frame`. On a Shopify store it takes the frame off the
  live product page; on other stores it removes it from the product in
  Shootika.
- The frame itself is kept and can be approved again until it expires.

## Shoot again

- To redo a frame, call `start_shoot` with `regenerate_of` set to that frame's
  id. That is a new shoot and uses a frame from the plan, so check
  `get_account` and confirm first, as `shoot-products` does.
- For a different model, style or pose, use `cast-models` to prepare the
  scene, then shoot.

## What is live

`list_shoots` filtered by `approved` shows every frame currently on a product.
