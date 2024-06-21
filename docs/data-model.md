# Data Model

The Völur SDK and its data model are designed to facilitate the integration and
management of business processes within the meat industry. This documentation
provides an overview of the entities available within the SDK and guides on
mapping your internal data to the Völur data model, ensuring a seamless flow of
information between your systems and the Völur platform.

## Entities Overview
Entities represent the core components of your business processes and are
fundamental to managing the data flow between your systems and the Völur
platform.

!!! info "Custom Characteristics"

    To accommodate the diverse needs of our customers, the SDK allows for the
    inclusion of custom characteristics for some entities. This flexibility
    ensures that you can adapt the predefined entities to fit your specific data
    requirements, enhancing the utility and applicability of the SDK in your
    operations.

    By understanding and utilizing these entities, you can effectively manage
    and streamline your data interactions with the Völur platform. Whether
    you're dealing with materials, inventory, product demands, or bills of
    materials, the SDK provides a structured and efficient way to handle your
    data needs.

### BoM (Bill of Materials)

The **BoM** entity represents a bill of materials for a product, detailing the
input and output of a specific product in a process. It is crucial for
understanding the composition and requirements of products, facilitating
efficient planning and production management.

#### Key Attributes:
- **Process ID**: Unique identifier for the process.
- **Plant**: The plant where the process is located.
- **Machine ID**: The machine that is used in the process.
- **Product ID**: The product that is input/output of the process.
- **Quantity Percent**: The amount input/output of a product in the process,
given in percentage decimals.

### Demand

The **Demand** entity captures the need for individual products or a list of
products, along with their quantities, that need to be delivered from a plant to
a customer on a given date for a given price. This entity helps in forecasting
and meeting customer demands efficiently.

#### Key Attributes:
- **Product**: Reference to a product.
- **Plant**: Identifier of the plant or facility where the demand is shipped
from.
- **Quantity**: Number of units required.
- **Characteristics**: A list of additional characteristics that further
describe the demand (sale) of a product.

### Material

**Material** is an entity representing the various inputs used during
fabrication or production processes. This could include carcasses, sides, primal
cuts, and other forms of material. It provides detailed information about the
available supply of materials, including their quantity and attributes important
for processing.

#### Key Attributes:
- **Material ID**: A unique identifier for the material.
- **Plant**: Identifier of the plant or facility where the material is located.
- **Quantity**: The amount of this material that is available.
- **Type**: The specific type of the material (e.g., side, carcass, primal cut).
- **Characteristics**: A list of additional characteristics that further
describe the material.
- **Arrived at**: The timestamp indicating when the material arrived at the
facility.
- **Expires at**: The timestamp indicating when the material is expected to
expire.


### Product Inventory

**Product Inventory** is an entity representing the set of available products.
It includes comprehensive details about product expiration dates, arrival times,
weight, quantity, and characteristics, ensuring effective inventory management.

#### Key Attributes:
- **Product ID**: Unique identifier for the product.
- **Plant**: Identifier of the plant or facility where the inventory is located.
- **Quantity**: The amount of this products of a given combination of the other
fields that is available.
- **Weight**: The amount of this products of a given combination of the other
fields that is available.
- **Available at**: The timestamp indicating when the product arrived at
inventory and was available to use.
- **Expires at**: The timestamp indicating when the product in the inventory is
expected to expire.
- **Characteristics**: A list of additional characteristics that further
describe the material. For instance the status of the product in inventory
(e.g., in transit, assigned to order, available).

### Product

The **Product** entity represents a generic product type with its
characteristics. Unlike other entities, it does not represent a specific product
instance but rather a type of product. This abstraction allows for more
generalized handling of products within the system.

#### Key Attributes:
- **Product ID**: Unique identifier for the product.
- **Characteristics**: List of characteristics that describe the product.

### Mapping Your Data to the Völur Data Model
The Völur data model serves as a flexible framework designed to adapt to the
data of a given customer within the meat industry. To leverage your data
effectively, it's essential to transform your internal data model into the Völur
data model.

#### Sources
Sources, often tables from your system, are identified as inputs to the Völur
system. Examples include materials/the supply or products/product catalog.
Configuring a source involves specifying ID fields, required fields, and
non-required fields (characteristics).

!!! info "Note"

    Additional sources might be added as we iterate.

!!! Example "Example - Configuring the `materials` Source"
    When uploading materials data from a CSV, the column called `Material ID`
    serves as the ID field. Predefined fields like `quantity` require
    specification of the column name and unit. Any other field can be added as a
    `characteristic`, with support for different types.

For detailed examples and further guidance on configuring sources and uploading
data, refer to the [examples section][examples] of the documentation.

[examples]: examples/index.md

