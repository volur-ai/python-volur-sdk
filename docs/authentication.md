# Authentication

In order to be able to use Volur AI SDK you need to have the following
credentials:

- API endpoint,
- API token.

!!! note "Contact your developer at Volur"
    If you don't have these credentials, please contact your developer at
    Volur and they will provide you with the necessary information.

## Configure

Client is obtaining these credentials from the environment variables:

- `VOLUR_AI_ADDRESS`,
- `VOLUR_AI_TOKEN`.

Please set them in your environment where you run your code.

!!! note "Use secret manager in your cloud to keep the token"
    We recommend using a secret manager in your cloud to keep the token
    secure. Depends on the cloud provider you are using, you can use
    Azure Key Vault, Google Cloud Secret Manage, AWS Secrets Manager, etc.

!!! danger "Do not share API token with anyone externally"
    Please do not share your API token with anyone externally. It is a
    sensitive information that should be kept secure.
