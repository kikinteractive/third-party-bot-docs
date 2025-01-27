# Third Party Bot Docs

This repository contains technical documentation to help bot creators get started with Kik.

# Authentication Overhaul

Kik is migrating to a modernized authentication backend. This involves two major changes:

- Registration and login are now handled by the login service instead of XMPP
- [JWTs](https://auth0.com/docs/secure/tokens/json-web-tokens) are used to authenticate an XMPP connection

This document explains the technical details of these changes and how bot creators can adopt these new authentication
mechanisms.

## Whitelisting

For a bot account to log in and to request JWTs, it must first be whitelisted. This process involves contacting
Kik with a list of account `JID`s. After validation by Kik, the accounts will be whitelisted and ready for use.

## Authentication Flow

To successfully authenticate with Kik, the following flows can be used:

### Login Flow

Use this flow if the `access-token`, `refresh-token` and `JID` have not yet been obtained for the account.

1. Call login service to obtain and store an `access-token`, `refresh-token` and the account's `JID`.

2. Create an XMPP connection, but add `access-token` to the connection payload `<k ...>`

### Access Token Flow

Use this flow when a valid `access-token` is available.

1. Create an XMPP connection, but add `access-token` to the connection payload <k ...>

### Refresh Token Flow

Use this flow if the `access-token` is expired or invalid, and a `refresh-token` is available.

1. Call JWT service with `refresh-token` to obtain and store a new `access-token` and `refresh-token`

2. Create an XMPP connection, but add `access-token` to the connection payload `<k ...>`

## Technology

Interacting with the login and JWT services involves using [GRPC](https://grpc.io/). Client code is generated from
`.proto` files in a chosen programming language. This document supplies the `.proto` files and
endpoint information required to use the login and JWT services.

## Login Service

The login service takes a username and password, along with device information, and, on success, returns a
`refresh-token`, `access-token` and `JID`. Refer to the `.proto` files for a full schema of what to send, and what data
is returned.

> [!NOTE]
> `LoginResponse`’s `session-token` is the `refresh-token`

An example of how to structure a login request for a whitelisted account can be found in [login.py](login.py).

## JWT Service

The JWT service is used to exchange a `refresh-token` for an `access-token` and a new `refresh-token`. Ensure both
tokens are stored, so the new `refresh-token` can be used when the `access-token` expires again.

A token exchange can be done like this:

An example of how to structure a refresh token request can be found in [jwt.py](jwt.py).

## Authenticating an XMPP Connection

When an `access-token` is obtained, the account can authenticate an XMPP connection. Note that the `access-token` is an
**additional requirement**. An equivalent of `EstablishAuthenticatedSessionRequest`
at https://github.com/tomer8007/kik-bot-api-unofficial/blob/new/kik_unofficial/datatypes/xmpp/login.py#L141  must still
be used. The only change is that `access-token` needs to be added to the connection payload (i.e. add an entry to
`the_map` resulting in `<k from="..." to="..." access-token="..." ...>`). Supplying an `access-token` to authenticate
will become mandatory in the future.

## Proto Files

The required `.proto` files are located in this repository's `proto/` folder.

An example shell script to compile the proto files into Python code using BetterProto is provided in
[compile-proto.sh](compile-proto.sh).
