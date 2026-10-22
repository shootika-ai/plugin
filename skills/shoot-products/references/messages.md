# Messages a Shootika tool may answer with

Each message is quoted as Shootika sends it, with what to tell the person.
None of them is fixed by retrying the call.

## Permissions

> This connection is not allowed to use *tool*: it needs the "*permission*"
> permission. Connect Shootika again and allow it, or ask a store admin.

The person did not grant that permission when they approved the connection.
Name the permission. They disconnect Shootika, connect it again and tick that
permission. `connect` explains where.

> This connection was approved by someone who can no longer allow this. Ask a
> store admin to reconnect.

The approver's role no longer allows what was tried. A store admin connects
the assistant again.

> Connect Shootika again: this connection is missing, expired or no longer
> valid.

The connection was disconnected, or the store removed the Shopify app. The
person approves it again, after reinstalling the app if that is the cause.

## Frames

> You have used your plan's frames. Your plan can bill extra frames, but this
> connection is not allowed to. A store admin can allow them on the Connected
> assistants page of the Shootika app in Shopify:
> https://admin.shopify.com/store/{handle}/apps/shootika/app/connections. Or
> wait for your plan to refill.

A Shopify store on a monthly plan. A store admin can allow extra frames for
this connection at that address, where `{handle}` is the store's name.

> You have used your plan's frames. Your plan can bill extra frames, but this
> connection is not allowed to. A store admin can allow them under Settings,
> Connected assistants in the web app. Or wait for your plan to refill.

A web app store on a monthly plan. Same switch, under Settings, Connected
assistants.

> You have used your plan's frames and this billing period's limit on extra
> frames.

The plan's cap on extra frames is reached. On a Shopify store the plan refills
next month, or the person changes plans on the Subscription page of the
Shootika app in Shopify. On a web app store the message continues: "Your plan
refills next month, or you can change plans under Billing in the web app."

> You have no frames left. Your plan refills next month, or you can change
> plans on the Subscription page of the Shootika app in Shopify.

A Shopify store on a plan that does not bill extra frames. On a web app store
with a yearly plan the message ends "or you can upgrade under Billing in the
web app."

> You have used your *n* free frames. Choose a plan ... to keep shooting.

The Free plan's one-time frames never refill. The person chooses a plan on
the Subscription page of the Shootika app in Shopify, or under Billing in the
web app.

## Catalog

> Adding products is not available on Shopify stores.

A Shopify store's products and photos come from Shopify. The person adds them
in their Shopify admin.
