# Configure CSV source for Materials

This example will guide you through the process of configuring a CSV source for materials using Völur SDK.

## What are sources?

A source is a way to prepare your data to upload it to the Völur.

Available sources can be found in
[`volur.sdk.v1alpha2.sources`][volur.sdk.v1alpha2.sources]. For this specific
example we will use
[`MaterialsCSVFileSource`][volur.sdk.v1alpha2.sources.csv.MaterialsCSVFileSource].

## Configuring a source

Let us say we have a file `materials.csv` with the following content:

| Material ID | Material Name         | Is Frozen | Weight | Quality Category |
|-------------|-----------------------|-----------|--------|------------------|
| 1           | material-id-1         | False     | 0.5    | A                |
| 2           | material-id-2         | False     | 1.5    | A                |
| 3           | material-id-3         | True      | 2.5    | A                |
| 4           | material-id-4         | True      | 3.5    | A                |
| 5           | material-id-5         | False     | 4.5    | A                |

To configure a source for this file, you can build a `MaterialsCSVFileSource`:

```python linenums="1"
from volur.sdk.v1alpha2.sources.csv import (
    CharacteristicColumnString,
    CharacteristicColumnBool,
    Column,
    MaterialsCSVFileSource,
    QuantityColumn,
)

source = MaterialsCSVFileSource(
    path="materials.csv",
    material_id_column=Column(column_name="Material ID"),
    quantity_column=QuantityColumn(
        column_name="Weight",
        unit="kilogram",
    ),
    characteristics_columns=[
        CharacteristicColumnString(
            column_name="Material Name",
            characteristic_name="name",
        ),
        CharacteristicColumnString(
            column_name="Quality Category",
            characteristic_name="quality_category",
        ),
        CharacteristicColumnBool(
            column_name="Is Frozen",
            characteristic_name="is_frozen",
        ),
    ],
)
```

Let's break down the configuration:

- `path`: the path to the CSV file,
- `material_id_column`: the column containing material IDs (we need to
   uniquely identify each material available in the CSV file),
- `quantity_column`: the column containing the quantity of the material,
  in this case, the weight of the material in kilograms,
- `characteristics_columns`: all the columns of the CSV file that contain
  characteristics of the material. In this case, we have three columns:

    - `Material Name` is mapped to the `name` characteristic,
    - `Quality Category` is mapped to the `quality_category` characteristic,
    - `Is Frozen` is mapped to the `is_frozen` characteristic.

# Use a source with a Völur SDK client

To use the source with a Völur SDK client, you can use the following code:

```python linenums="1"
from volur.sdk.v1alpha2 import VolurClient

# Your MaterialCSVFileSource configuration

client = VolurClient()
client.upload_materials_information(source)
```

That's it! You have successfully configured a CSV source for materials using Völur SDK.
