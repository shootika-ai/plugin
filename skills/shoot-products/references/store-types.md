# Shopify stores and web app stores

`get_account` says which kind of store is connected. Three things differ.

## Shopify store

- **Products and photos** come from Shopify. `add_product` and
  `add_product_image` answer that adding products is not available on Shopify
  stores. The person adds products and photos in their Shopify admin, then
  asks again.
- **Approving a frame** publishes it to the live product page, where shoppers
  see it. Removing it takes it off the live page.
- **Connected assistants** are managed at
  `https://admin.shopify.com/store/<your-store>/apps/shootika/app/connections`,
  with the store's name in place of `<your-store>`. The page is not in the
  Shootika app's menu, so the person opens it by its address. Removing the
  Shootika app from the store disconnects every assistant.

## Web app store

- **Products and photos** live in Shootika. `add_product` adds a product with
  a title, optionally its garment category (tops, bottoms or one-pieces), the
  store's own id, and up to 10 photos from public image URLs (PNG, JPEG or
  WebP). The product is created even when a photo cannot be fetched; the
  answer says which failed. `add_product_image` adds one photo to a product
  from a public URL, at most 15 MB.
- **Approving a frame** saves it to the product in Shootika. Nothing is
  published anywhere else.
- **Connected assistants** are under Settings, Connected assistants in the web
  app. Only an admin can disconnect one or allow extra frames; other team
  members see the list.
