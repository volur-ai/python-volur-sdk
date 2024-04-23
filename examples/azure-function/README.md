# Use Volur AI SDK with Azure Function App

This example contains code on how to use Volur AI SDK with Azure Function App.

## Prerequisites

> [!NOTE]
> For demonstration purposes we are using Poetry as a package manager and Just
> as a task runner. It is not required to use them. All the commands that you
> require to run are available in this README.md.

### Required prerequisites

- Python (>=3.11, <3.12),
- Docker,
- [GitHub CLI][github-cli] ([docs][github-cli-documentation]),
- [Azure CLI][azure-cli] ([docs][azure-cli-documentation]).

### Optional prerequisites

- [just][just] ([docs][just-documentation]).


[azure-cli]: https://github.com/Azure/azure-cli
[azure-cli-documentation]: https://learn.microsoft.com/en-us/cli/azure/
[just]: https://github.com/casey/just
[just-documentation]: https://just.systems/man/en/
[github-cli]: https://github.com/cli/cli
[github-cli-documentation]: https://cli.github.com/manual/

## Required infrastructure

In order to deploy an Azure Function to upload data using Volur AI SDK, this
infrastructure must be in-place in an Azure Resource Group:

- Azure Storage Container with a blob container,
- Azure Container Registry,
- Azure Function App running in Linux Containers.

> [!NOTE]
> Please follow these Azure Documentation pages to deploy this infrastructure
> or use Infrastructure as Code tooling of your choice:
> - [Create a storage account][create-a-storage-account-azure-docs],
> - [Create a blob container][create-a-blob-container-azure-docs],
> - [Create a container registry][create-a-container-registry-azure-docs],
> - [Create a function app running in Linux Containers][create-a-function-app-azure-docs]

[create-a-storage-account-azure-docs]: https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create
[create-a-blob-container-azure-docs]: https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal
[create-a-container-registry-azure-docs]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal
[create-a-function-app-azure-docs]: https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-custom-container

## Function App

An Azure Function App function can be found in the `function_app.py` and it is
configured to trigger on the uploads in the container `test-container` in the
default storage account of the Azure Function.

> [!TIP]
> For production usage we recommend to use a separate Azure Storage Account.
> You can find more information about best practices and Blob Triggers in
> [Azure Blob storage trigger for Azure Functions][azure-blob-trigger].

[azure-blob-trigger]: https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-blob-trigger

## Deployment

If all your infrastructure is in-place, you can start deploying Azure Function
with Volur AI SDK to your Azure cloud environment. You need to run three steps.

### Build a container image and push it to your Azure Container Registry

To build your container image run the following commands:

> [!NOTE]
> As for now (2024-04-32) Volur AI SDK library is private, and therefore
> requires authentication. Please set `GH_TOKEN` environment variable before
> you build container using GitHub CLI `GH_TOKEN=$(gh auth token)`.

```shell
docker build \
  --platform linux/amd64 \
  --secret id=GH_TOKEN \
  --target deployment \
  --tag <change-me-azure-container-registry-name>/<change-me-container-image-name>:<change-me-container-image-tag> \
  .
```

or use a target in `Justfile`

```shell
just \
  acr="<change-me-azure-container-registry-name>" \
  container_image_name="<change-me-container-image-name>" \
  build-container-image
```

After you build a container image, you need to push it to Azure Container
Registry.

> [!NOTE]
> Don't forget to configure Docker credentials helper by using
> `az acr login --name <change-me-azure-container-registry-name>`

```shell
docker push <change-me-azure-container-registry-name>/<change-me-container-image-name>:<change-me-container-image-tag>
```

or simply run `deploy-container` target from `Justfile`:

```shell
just \
  acr="<change-me-azure-container-registry-name>" \
  container_image_name="<change-me-container-image-name>" \
  build-container-image
```

### Configuring Azure Functions to use custom container image

> [!NOTE]
> We highly recommend using a custom container image in order to simplify
> triage and investigation if there is a problem with a library. Yet, Azure
> Function App can use Python runtime, but we do not cover it in the scope of
> this example.

Azure Function App is quite flexible and can use a custom container image. To
make it work, you need explicitly configure Azure Function App using Azure CLI.

1. Make sure that **Admin Access** is enabled for Azure Container registry.
   Please follow
   [Publish the container image to a registry][public-container-image-to-a-registry]
   and [Admin account][container-registry-authentication] Azure documentation
   articles for detailed information.

2. Obtain Admin Access credentials for your Azure Container Registry
   ```shell
   az acr credential show -n <change-me-azure-container-registry-name> -o jsonc | jq -r '.username'
   ```
   for username, and
   ```shell
   az acr credential show -n <change-me-azure-container-registry-name> -o jsonc | jq -r '.passwords[0].value'
   ```
   for password.

3. Configure your Azure Function App to use a custom container
   ```shell
    az functionapp config container set \
       --image=<change-me-azure-container-registry-name>/<change-me-container-image-name>:<change-me-container-image-tag> \
       --registry-server=<change-me-azure-container-registry-name> \
       --registry-username=<change-me-azure-container-registry-username> \
       --registry-password=<change-me-azure-container-registry-password> \
       --name=<change-me-azure-function-app-name> \
       --resource-group=<change-me-azure-resource-group-name>
   ```

4. Provide credentials in Azure Function App application settings
   ```shell
    az functionapp config appsettings set \
       --name=<change-me-azure-function-app-name> \
       --resource-group=<change-me-azure-resource-group-name> \
       --settings VOLUR_API_ADDRESS=<change-me-volur-api-address> VOLUR_API_TOKEN=<change-me-volur-api-token>
    ```

[public-container-image-to-a-registry]: https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-container-registry#publish-the-container-image-to-a-registry
[container-registry-authentication]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli#admin-account


Another option is to simply run `deploy-function` target from `Justfile`:

```shell
just \
  acr="<change-me-azure-container-registry-name>" \
  container_image_name="<change-me-container-image-name>" \
  afa="<change-me-azure-function-app-name>" \
  arg="<change-me-azure-resource-group-name>" \
  volur_api_address="<change-me-volur-api-address>" \
  volur_api_token="<change-me-volur-api-token>" \
  deploy-function-app
```

## Testing

As a result of the deployment, you should be able to see an Azure Function App.
To test the function you can use the code from `function_app.py` and use
`examples/generate-fake-data.py` to generate fake data. After uploading a file
to the container, the function must be executed and after some time you should
see a successful execution in the history of a Function App.
