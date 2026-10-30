# Sign-in protocols for the ticket assistant: OIDC and SAML

Reference for [F03 Section 9](../README.md#9-signing-the-user-in-oidc-and-saml). Carried verbatim from the chapter on 30 October 2026 so the main text stays scannable; the choosing table lives in the chapter.

## OpenID Connect: signing the user into the agent application

**OpenID Connect (OIDC) is an authentication protocol built on OAuth 2.0.** It lets your application establish who signed in. Entra acts as the **identity provider / OpenID Provider**; your complaints application is the **client / relying party** that trusts its sign-in result.

Register the application with Entra, configure its redirect URI (the approved address for returning the sign-in response), and use a supported authentication library. Request the `openid` scope to request OIDC authentication.

```text
Employee → Application → Entra sign-in
                           ↓
Application validates the returned ID token
                           ↓
Application establishes the employee's signed-in session
```

The **ID token** tells the application about the authenticated user. It is intended for that application, not for calling an MCP API. Libraries validate its signature, issuer, audience, expiry and applicable request-binding checks.

Subsequent Foundry/MCP calls need **access tokens** for their respective APIs and the required permissions. User sign-in does not automatically grant downstream access. A background agent acting under its own identity does not need an interactive OIDC user sign-in for every tool call.

Source: [OpenID Connect on the Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc). The diagram summarises sign-in, not the individual browser redirects or token exchanges.

### When and how to use OIDC

Use OIDC when building an interactive web, desktop or mobile application where employees sign in with Entra. For the complaints assistant, this is the employee-facing application login, not the agent's background identity.

A typical authorization-code flow with PKCE works as follows:

1. Configure the app registration, tenant, client ID, redirect URI and required API permissions. Use a supported authentication library.
2. The application redirects the browser to Entra, requesting `openid` and any required API scopes. PKCE binds code redemption to the client that started the request.
3. Entra authenticates the employee and applies applicable sign-in policy; consent is obtained where required.
4. Entra returns a short-lived authorization code to the registered redirect URI.
5. The client redeems the code with its PKCE verifier and, for a confidential client, its configured client authentication. It receives the requested, authorised tokens.
6. The application validates the ID token for sign-in; an access token is presented only to its intended API. Browser/public clients must not hold a client secret.

Source: [Authorization code flow with OIDC and PKCE](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow).

## SAML: enterprise single sign-on into an application

**SAML 2.0 is another protocol for federated sign-in**, where an application trusts an identity provider to authenticate users. Single sign-on (SSO) means users can access participating applications using an existing sign-in session. SAML remains common in enterprise applications.

Entra acts as the **identity provider (IdP)**. The application is the **service provider (SP)**—this protocol term is not the same as an Entra service principal.

```text
Employee → Enterprise application → Entra sign-in
                                      ↓
Application receives and validates a signed SAML assertion
                                      ↓
Application establishes the employee's signed-in session
```

Administrators configure trust through identifiers, reply/recipient URLs, signing certificates and metadata. The SAML assertion is an XML security statement about the authenticated user; the application validates it before accepting sign-in.

In our Foundry/MCP design, SAML may authenticate the employee into an enterprise front end. It does not replace the OAuth access tokens used for subsequent API calls. Do not send a SAML assertion as the MCP bearer access token. Any transition to delegated API access requires an explicitly supported authentication flow.

Source: [Microsoft identity platform SAML protocol](https://learn.microsoft.com/en-us/entra/identity-platform/saml-protocol-reference).

### When and how to use SAML

Use SAML when integrating an enterprise application whose supported SSO interface is SAML, or when maintaining an existing SAML federation. For example, a bank's existing case-management portal might use SAML while its agent integration separately uses OAuth API access.

1. Add/select the enterprise application in Entra and configure SAML single sign-on.
2. Configure the application's Entity ID (its SAML identifier), Reply/ACS URL (where it receives the response), and required user claims.
3. Configure the application to trust Entra's issuer, sign-in endpoint and signing certificate/metadata. Assign the intended users or groups as required by the application's access configuration.
4. In an application-initiated flow, the browser goes from the application to Entra for sign-in and returns with a SAML response. The application validates it and establishes a session.
5. Test sign-in and denied access, and plan signing-certificate renewal. Follow the application's integration guide; user provisioning and sign-in are separate concerns.

Source: [Configure enterprise application SAML SSO](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso).
