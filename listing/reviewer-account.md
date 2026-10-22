# The reviewer account

Both directories' reviewers run every tool against a real store. One
production web app store serves both.

## What the store contains

- A name that says what it is for, such as "Shootika Review Store".
- About twelve products with real flat-lay photos, so `list_products`,
  `get_product` and `add_product_image` have something to work with.
- Two or three scenes saved in the Studio and ready, so `start_shoot` can run
  without waiting on `request_scene`.
- A few finished frames, at least one approved, so `list_shoots` filtered by
  `approved` is not empty.
- Goodwill credits granted by Shootika, enough for two reviews that run every
  tool several times, with an expiry about a year out. The amount and expiry
  are recorded below when granted. Re-grant before a scheduled review if the
  balance is low.

## How reviewers sign in

`https://panel.shootika.com/login`, with the email address and password
provided in the portal's review form. The account is an admin of the store,
its email is verified, and it has no second factor, sign-in code or
magic-link-only login.

## Where the credentials live

In the company password manager, under "Shootika directory reviewers". Never
in this repository, the ZIP, or a chat.

## Grants

| Date | Amount | Expires | Note |
|---|---|---|---|
| | | | |
