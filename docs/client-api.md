# Client API Reference

The [`Client`](#sen4cap_client.Client) class provides a synchronous API.
If you want an asynchronous version, use the `AsyncClient` class instead.
It provides the same interface, but using asynchronous server calls.

Both clients return their configuration as a 
[`ClientConfig`](#sen4cap_client.ClientConfig) object.

Methods of the [`Client`](#sen4cap_client.Client) and `AsyncClient` 
may raise a [`ClientError`](#sen4cap_client.ClientError) if a server call fails. 

::: sen4cap_client.Client

::: sen4cap_client.ClientConfig

::: sen4cap_client.ClientError
