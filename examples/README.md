# Upload materials information using Völur AI SDK

This folder has the code to upload materials information using Völur AI SDK.

## Prerequisites

- You have configured the workspace as it is described in `README.md`.

## How to run an example

> [!NOTE]
> To run the examples you need to have the following environment variables set:
> - `VOLUR_API_ADDRESS`,
> - `VOLUR_API_TOKEN`.
> To obtain these values, you should contact developers.

1. Create .env file and set the following variables:
   ```text
   VOLUR_API_ADDRESS=<change-me-volur-api-server-address>
   VOLUR_API_TOKEN=<change-me-volur-api-token>
   ```

2. Generate fake data
   ```shell
   poetry run python generate-fake-data.py
   ```

   As a result, you will get a file `data.csv` with 100000 entries and a header.

3. Upload the fake data using an example:
   ```shell
   poetry run python main.py
   ```

  As a result you should see this line in your console:
  ```text
  YYYY-mm-dd HH:MM:SS | INFO     | volur.sdk.client:upload_materials_information:27 - successfully uploaded materials information
  ```
