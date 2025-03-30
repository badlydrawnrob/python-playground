# Auth

## Methods

> You should make sure when a user logs out their session expires. It's nice to have QR codes or 6 number codes for double auth but involves quite a bit of setup.

**Basic HTTP authentication**

User credentials sent via Authorization HTTP header. The request returns a WWW-Authenticate header containg a `Basic` value and optional realm parameter, which indicates the authentication request is made to.

**Cookies**

Cookies are used when data is stored on the client side, like a web browser. [Elm Lang Guide to Cookies] these can be retrieved by the server for authentication purposes but in general cookies are discouraged by Elm. You can use LocalStorage to set your session cookies and consume these in the client side app.

**Bearer token authentication**

Uses security tokens called bearer tokens. These are sent alongside the `Bearer` keyword in the Authorization header request. The most used token is JWT which is usually a dictionary comprising the user ID and the tokens expiry time.

**Summary**

All these have their pros and cons, and you'll likely need a security expert to set this thing up properly when scaling up. There's many ways you could get hacked so better to be safe than sorry — it's not something I feel comfortable handling myself.
