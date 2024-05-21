# Use Völur SDK with Azure Function App

This example contains code on how to use Völur SDK with Azure Function App.

## Prerequisites

> [!NOTE]
> For demonstration purposes we are using Poetry as a package manager and Just
> as a task runner. It is not required to use them. All the commands that you
> require to run are available in this README.md.

### Required prerequisites

- Python (>=3.11, <3.12),
- Docker,
- [GitHub CLI][github-cli] ([docs][github-cli-documentation]),
- [Azure CLI][azure-cli] ([docs][azure-cli-documentation]),
- [Azure Functions Core Tools][azure-functions-core-tools] ([docs][azure-functions-core-tools-documentation]).

### Optional prerequisites

- [just][just] ([docs][just-documentation]).


[azure-cli]: https://github.com/Azure/azure-cli
[azure-cli-documentation]: https://learn.microsoft.com/en-us/cli/azure/
[just]: https://github.com/casey/just
[just-documentation]: https://just.systems/man/en/
[github-cli]: https://github.com/cli/cli
[github-cli-documentation]: https://cli.github.com/manual/
[azure-functions-core-tools]: https://github.com/Azure/azure-functions-core-tools
[azure-functions-core-tools-documentation]: https://learn.microsoft.com/en-us/azure/azure-functions/functions-core-tools-reference?tabs=v2

## Required infrastructure

In order to deploy an Azure Function to upload data using Völur SDK, this
infrastructure must be in-place in an Azure Resource Group:

- Azure Storage Container with a blob container,
- Azure Function App running in Linux Containers.

### Optional

For Docker based deployment of Azure Function, you also need:

- Azure Container Registry.

> [!NOTE]
> Please follow these Azure Documentation pages to deploy this infrastructure
> or use Infrastructure as Code tooling of your choice:
> - [Create a storage account][create-a-storage-account-azure-docs],
> - [Create a blob container][create-a-blob-container-azure-docs],
> - [Create a container registry][create-a-container-registry-azure-docs],
> - [Create a function app triggered by blob][create-a-function-app-blob-triggered-azure-docs] for Python Azure Function,
> - [Create a function app running in Linux Containers][create-a-function-app-azure-docs] for Python Azure Function in Docker.

[create-a-storage-account-azure-docs]: https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create
[create-a-blob-container-azure-docs]: https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal
[create-a-container-registry-azure-docs]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal
[create-a-function-app-azure-docs]: https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-custom-container
[create-a-function-app-blob-triggered-azure-docs]: https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-storage-blob-triggered-function

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
with Völur SDK to your Azure cloud environment. We provide two instructions
to deploy your Azure Function to Azure:

- Python Azure Function,
- Python Azure Function in Docker.

> [!NOTE]
> We highly recommend using a custom container image in order to simplify
> triage and investigation if there is a problem with a library.

### Python Azure Function

To deploy Azure Function in Python runtime, run these commands:

1. Export `requirements.txt`
   ```shell
   poetry export --output=requirements.tx --without-hashes
   ```

2. Deploy Azure Function
   ```shell
   func azure functionapp publish <change-me-azure-functions-app-name> --python --build remote
   ```

3. Provide credentials to Volur API in Azure Function App application settings
   ```shell
   az functionapp config appsettings set \
     --name=<change-me-azure-function-app-name> \
     --resource-group=<change-me-azure-resource-group-name> \
     --settings VOLUR_API_ADDRESS=<change-me-volur-api-address> VOLUR_API_TOKEN=<change-me-volur-api-token>
   ```

### Python Azure Function in Docker

> [!NOTE]
> Don't forget to configure Docker credentials helper by using
> `az acr login --name <change-me-azure-container-registry-name>`

As an alternative way to deploy Azure Function, you can use Azure Function in
Docker. The main difference is that you have more flexible control of runtime
environment, because you are in a control of runtime image, where your
functions are running. To deploy Azure Function in Docker, run these commands:

1. Build a container image
   ```shell
   docker build \
     --platform linux/amd64 \
     --target deployment \
     --tag <change-me-azure-container-registry-name>/<change-me-container-image-name>:<change-me-container-image-tag> \
     .
   ```

2. Push a container image to Azure Container Registry
   ```shell
   docker push <change-me-azure-container-registry-name>/<change-me-container-image-name>:<change-me-container-image-tag>
   ```

3. Make sure that **Admin Access** is enabled for Azure Container registry.
   Please follow [Publish the container image to a registry][public-container-image-to-a-registry] and [Admin account][container-registry-authentication] Azure documentation articles
   for detailed information. Obtain Admin Access credentials for your Azure Container Registry:
   - for username
     ```shell
     az acr credential show -n <change-me-azure-container-registry-name> -o jsonc | jq -r '.username'
     ```
   - for password
     ```shell
     az acr credential show -n <change-me-azure-container-registry-name> -o jsonc | jq -r '.passwords[0].value'
     ```

4. Configure your Azure Function App to use a custom container
   ```shell
   az functionapp config container set \
     --image=<change-me-azure-container-registry-name>/<change-me-container-image-name>:<change-me-container-image-tag> \
     --registry-server=<change-me-azure-container-registry-name> \
     --registry-username=<change-me-azure-container-registry-username> \
     --registry-password=<change-me-azure-container-registry-password> \
     --name=<change-me-azure-function-app-name> \
     --resource-group=<change-me-azure-resource-group-name>
   ```

4. Provide credentials to Volur API in Azure Function App application settings
   ```shell
    az functionapp config appsettings set \
       --name=<change-me-azure-function-app-name> \
       --resource-group=<change-me-azure-resource-group-name> \
       --settings VOLUR_API_ADDRESS=<change-me-volur-api-address> VOLUR_API_TOKEN=<change-me-volur-api-token>
   ```

[public-container-image-to-a-registry]: https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-container-registry#publish-the-container-image-to-a-registry
[container-registry-authentication]: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli#admin-account

## Testing

As a result of the deployment, you should be able to see an Azure Function App.
To test the function you can use the code from `function_app.py` and use
`examples/generate-fake-data.py` to generate fake data. After uploading a file
to the container, the function must be executed and after some time you should
see a successful execution in the history of a Function App.
