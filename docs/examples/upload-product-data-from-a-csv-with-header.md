# Configure CSV source for Products

This example will guide you through the process of configuring a CSV source for products using Völur SDK.

## What are sources?

A source is a way to prepare your data to upload it to the Völur.

Available sources can be found in
[`volur.sdk.v1alpha2.sources`][volur.sdk.v1alpha2.sources]. For this specific
example we will use
[`ProductsCSVFileSource`][volur.sdk.v1alpha2.sources.csv.ProductsCSVFileSource].

## Configuring a source

Let us say we have a file `products.csv` with the following content:

| Product ID  | Product Name  | Product Description            | Is Active | Plant Num  |
|-------------|---------------|--------------------------------|-----------|------------|
| 1           | product-id-1  | Some description 1             | True      | 1000       |
| 2           | product-id-2  | Another description            | True      | 1000       |
| 3           | product-id-3  | This is a different product    | True      | 1001       |
| 4           | product-id-4  | Also a product                 | True      | 1002       |
| 5           | product-id-5  | This product is no longer used | True      | 1002       |

To configure a source for this file, you can build a `ProductsCSVFileSource`:

```python linenums="1"
from volur.sdk.v1alpha2.sources.csv import (
    CharacteristicColumnString,
    CharacteristicColumnBool,
    CharacteristicColumnInteger,
    Column,
    ProductsCSVFileSource,
)

source = ProductsCSVFileSource(
    path="products.csv",
    product_id_column=Column(column_name="Product ID"),
    characteristics_columns=[
        CharacteristicColumnString(
            column_name="Product Name",
            characteristic_name="product_name",
        ),
        CharacteristicColumnString(
            column_name="Product Description",
            characteristic_name="description",
        ),
        CharacteristicColumnBool(
            column_name="Is Active",
            characteristic_name="is_active",
        ),
        CharacteristicColumnInteger(
            column_name="Plant Num",
            characteristic_name="plant_code",
        ),
    ],
)
```

Let's break down the configuration:

- `path`: the path to the CSV file,
- `product_id_column`: the column containing product IDs (we need to
   uniquely identify each product available in the CSV file),
- `characteristics_columns`: all the columns of the CSV file that contain
  characteristics of the product. In this case, we have four columns:

    - `Product Name` is mapped to the `product_name` characteristic,
    - `Product Description` is mapped to the `description` characteristic,
    - `Is Active` is mapped to the `is_active` characteristic.
    - `Plant Num` is mapped to the `plant_code` characteristic.

# Use a source with a Völur SDK client

To use the source with a Völur SDK client, you can use the following code:

```python linenums="1"
from volur.sdk.v1alpha2 import VolurClient

# Your ProductsCSVFileSource configuration

client = VolurClient()
client.upload_products_information(source)
```

That's it! You have successfully configured a CSV source for products using Völur SDK.
