# Configure CSV source for given source without header

This example will guide you through the process of configuring a headerless CSV source for a given source using the Völur SDK.
In the example we will use uploading materials as the example, but it works the same way for any source. For how to upload
materials CSV with a header and read more about sources see [upload-materials-data-from-a-csv-with-header][materials-doc].

[materials-doc]: upload-materials-data-from-a-csv-with-header.md

## Configuring a source

Let us say we have a file `materials.csv` with the following content:

| <!-- --> |<!-- --> |<!-- --> |<!-- --> |<!-- --> |
|-- |---------------|-----------|--------|---|
| 1 | material-id-1 | False     | 0.5    | A |
| 2 | material-id-2 | False     | 1.5    | A |
| 3 | material-id-3 | True      | 2.5    | A |
| 4 | material-id-4 | True      | 3.5    | A |
| 5 | material-id-5 | False     | 4.5    | A |

To configure a source for this file, you can build a `MaterialsCSVFileSource`.
Instead of specifying the column name of the of each field you will specify the column number.
For the characteristic columns the characteristic_name is the new name for the uploaded data.

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
    has_header=False,
    material_id_column=Column(column_name=0),
    quantity_column=QuantityColumn(
        column_name=3,
        unit="kilogram",
    ),
    characteristics_columns=[
        CharacteristicColumnString(
            column_name=1,
            characteristic_name="name",
        ),
        CharacteristicColumnString(
            column_name=4,
            characteristic_name="quality_category",
        ),
        CharacteristicColumnBool(
            column_name=2,
            characteristic_name="is_frozen,
        ),
    ],
)
```

Let's break down the configuration:

- `path`: the path to the CSV file,
- `has_header`: the default is `True`, if set to `False` lik in the example above the
  column names should be specified as column numbers instead.
- `material_id_column`: the column number that containing material IDs (we need to
   uniquely identify each material available in the CSV file),
- `quantity_column`: the column number containing the quantity of the material,
  in this case, the weight of the material in kilograms,
- `characteristics_columns`: all the columns of the CSV file that contain
  characteristics of the material. In this case, we have three columns:

    - Column id 1/the second column as we count from 0 is mapped to the `name` characteristic,
    - Column id 4 is mapped to the `quality_category` characteristic,
    - Column id 2 is mapped to the `is_frozen` characteristic.

# Use a source with a Völur SDK client

To use the source with a Völur SDK client, you can use the following code:

```python linenums="1"
from volur.sdk.v1alpha2 import VolurClient

# Your MaterialCSVFileSource configuration

client = VolurClient()
client.upload_materials_information(source)
```

That's it! You have successfully configured a CSV source for materials using Völur SDK.
