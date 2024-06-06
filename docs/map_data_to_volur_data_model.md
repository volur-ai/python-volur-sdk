# Mapping your data to the Völur data model

## What is the Völur data model?
The Völur data model is a general data model for the meat industry. It includes
the sources needed as inputs to the Völur system. It is designed to be flexible,
so it can adapt to the data for a given customer.

Your internal data model was build for your business needs. 
To get most of the data we adopt to your data, we there need to transform your data
into the Völur data model and then AI models can use your data to solve your use case.
This document explains how to do that.

**Note:** this page is a work in progress and if there is
something that is unclear or need to be added, please add an issue.

## Sources
When creating the Völur data model Völur identified the sources that are needed
as inputs to the Völur system. Note, additional sources might be added as we iterate.
A source is often a table from you system. Examples are materials/the supply, or
products/product catalog. Available sources can be found in
[`volur.sdk.v1alpha2.sources`][volur.sdk.v1alpha2.sources].
Using the defined sources allows you to prepare your data so it can be upload to
the Völur system.

## Configuring a source
The different sources have three type of fields:
- ID field: ID field that uniquely identifies each entity/row.
- Other required fields: Which fields are required will differ between sources.
- Non-required fields: This are called characteristics, and there is no limit on the
  number that can be added for a given source.

We can use the `materials` source as an example. In
[upload-materials-data-from-a-csv-with-header][materials-doc] it is illustrated how to
upload materials data from a csv. In this example the column called `Material ID` is
used as the ID field. The material source also have the predefined field that defines the
`quantity`. The column name and unit needs to be specified.
In addition, any other field can be added as a `characteristic`. 
There are different type of characteristics that are supported. You can see which are currently supported [here](https://github.com/volur-ai/python-volur-sdk/blob/4f32272ff234f7741c8d371ee62ae35a63b358f2/src/volur/sdk/v1alpha2/sources/csv/__init__.py#L5). Separate documentation for characteristic will later be created.
For a given field find the correct type and then specify the name of the column in the csv
given by `column_name` and then the name that you want to give this field given by `characteristic_name`. `column_name` and `characteristic_name` can be the same, but for instance
if your column headers are in a language different from English, you can use the same source,
but translate the names by adding a different `characteristic_name`. See example for with the
"Material Name"-column [here](https://github.com/volur-ai/python-volur-sdk/blob/4f32272ff234f7741c8d371ee62ae35a63b358f2/docs/examples/upload-materials-data-from-a-csv-with-header.md?plain=1#L44).


[materials-doc]: upload-materials-data-from-a-csv-with-header.md
