from volur.sdk.client import VolurClient
from volur.sdk.sources.csv import (
    CharacteristicColumn,
    Column,
    MaterialsCSVFileSource,
    QuantityColumn,
)


def main() -> None:
    client = VolurClient()

    client.upload_materials(
        MaterialsCSVFileSource(
            path="./product_data.csv",
            material_id_column=Column(column_name="PRODUCTID"),
            quantity_column=QuantityColumn(
                column_name="POIDSTHEORIQUE",
                unit="kilogram",
            ),
            characteristics_columns=[
                CharacteristicColumn(
                    column_name="LABEL",
                    characteristic_name="product_label",
                    data_type="string",
                ),
                CharacteristicColumn(
                    column_name="CDC",
                    characteristic_name="quality_category",
                    data_type="string",
                ),
                CharacteristicColumn(
                    column_name="AVECOS",
                    characteristic_name="contains_bonels",
                    data_type="bool",
                ),
                CharacteristicColumn(
                    column_name="DUREEDEVIE",
                    characteristic_name="shelf_life",
                    data_type="integer",
                ),
                CharacteristicColumn(
                    column_name="POIDSTHEORIQUE",
                    characteristic_name="theoretical_weight",
                    data_type="float",
                ),
                CharacteristicColumn(
                    column_name="ISCONGEL",
                    characteristic_name="is_frozen",
                    data_type="bool",
                ),
            ],
        )
    )
    # Upload data


if __name__ == "__main__":
    main()
