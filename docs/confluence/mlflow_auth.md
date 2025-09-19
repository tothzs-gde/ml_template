# Authentication for MLflow

By default, MLflow does not provide built-in authentication or access control mechanisms. When exposing MLflow on a public or internal network (e.g., via Azure-hosted VM or container), external authentication and authorization mechanisms must be integrated to secure access.

**Note**: There is an experimental feature in development ([MLflow Authentication](https://mlflow.org/docs/latest/ml/auth/)). Not recommended in production. Currently only supports Databricks backend.

## Azure App Service Authentication (EasyAuth)

This is Azure’s built-in authentication mechanism for Azure App Services (Web Apps, Function Apps, Static Web Apps). It’s also called Easy Auth.

**How it works**:

Deploy MLflow as an Azure App Service (Web App for Containers).

Enable Authentication/Authorization in the Azure Portal.

Azure handles login flows, token validation, and passes identity info to the app via headers.

![](https://learn.microsoft.com/en-us/azure/app-service/media/app-service-authentication-overview/architecture.png#lightbox)

**References**:

- https://learn.microsoft.com/en-us/azure/app-service/overview-authentication-authorization

## Microsoft Entra application proxy

Microsoft Entra Application Proxy is a secure, cloud-based service that allows you to provide remote access to internal web applications hosted on-premises, in virtual machines, or containers. It's part of the Microsoft Entra ID (formerly Azure Active Directory) platform and supports single sign-on (SSO) and pre-authentication via Entra ID.

**How it works**:

1. A user is directed to the Microsoft Entra sign-in page after accessing the application through an endpoint.

2. Microsoft Entra ID sends a token to the user's client device after a successful sign-in.

3. The client sends the token to the application proxy service. The service retrieves the user principal name (UPN) and security principal name (SPN) from the token. Application proxy then sends the request to the connector.

4. The connector performs single sign-on (SSO) authentication required on behalf of the user.

5. The connector sends the request to the on-premises application.

6. The response is sent through the connector and application proxy service to the user.

![](https://learn.microsoft.com/en-us/entra/identity/app-proxy/media/what-is-application-proxy/app-proxy.png)

## Comparison

|   | Microsoft Entra App Proxy | Azure App Service Auth |
|---|---|---|
| Hosting | Anywhere (VM, container, on-prem, etc.) | Azure App Service / Azure Function |
| Auth provider | Entra ID | Any |
| SSO support | Yes | Yes |
| Extra infra needed? | Needs App Proxy Connector | No |
| Conditional access | via Entra ID | via Entra ID |
| VPN needed | No | No |
| Public access | App stays on private IP, only accesible through the proxy | Publicly available by default |