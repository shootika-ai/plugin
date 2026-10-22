---
name: cast-models
description: Choose or prepare the scene a Shootika shoot uses, which is one model in one style and one pose. Use when someone asks which models or looks are available, wants one house model across the whole catalog, a style other than studio, a particular pose, or two or three options to compare before shooting. Needs the Shootika connector. Not for starting the shoot itself (shoot-products).
---

# Cast models with Shootika

A scene is one style, one model and one pose. The style is the setting, such
as a studio backdrop or a street look; the model is the person shown wearing
the garment; the pose is how they stand or sit. A shoot needs a scene whose
status is `ready`. Preparing scenes is free; only shoots use frames.

## What the store already has

- `list_scenes` with `status` ready shows the scenes the store can shoot with
  now, each with a preview. If one fits what the person asked for, offer it
  first: no waiting, and reusing one scene across many products makes the
  catalog read as one shoot.
- A house model is exactly that: one model, one style, a pose or two, used for
  every product. Ask whether the person wants that before proposing variety.

## Something new

- `list_models` lists the models the store can use, with body type, skin tone
  and the poses each can take.
- `list_styles` lists the scene styles: backdrops and looks, plus the store's
  own reference scenes as `ref:<id>`.
- Offer two or three combinations that match what the person described, with
  the model's name, the style and the pose, rather than picking silently.
  When they describe a brand or audience, choose candidates that fit it and
  say why.
- `request_scene` with `model_id`, `style` and `pose` asks for the scene. It is
  free and safe to repeat: a scene the store already has comes back as it is.
  A new scene takes a little while to prepare; check `list_scenes` until its
  status is `ready`, without narrating each check.

## Then

Hand the ready scene's id to `shoot-products`, which checks the frames left
and starts the shoot.

## What this skill does not claim

How many of the store's own models a plan allows, and how long a scene takes
beyond "a little while", are not stated here. Plans are on
shootika.com/pricing, and the Studio in the Shootika app shows a scene's
progress.
