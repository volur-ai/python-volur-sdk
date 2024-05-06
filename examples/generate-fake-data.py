import datetime
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from faker import Faker
from loguru import logger


@dataclass
class FakeMaterial:
    material_id: str
    arrived_at: datetime.datetime
    weight: float
    product_label: str
    quality_category: str
    some_dummy_boolean_value: bool


def generate_fake_material(faker: Faker) -> FakeMaterial:
    return FakeMaterial(
        material_id=faker.uuid4(),  # type: ignore[arg-type]
        arrived_at=faker.date_time_this_decade(),
        weight=faker.random_number(digits=2),
        product_label=faker.word(),
        quality_category=faker.word(),
        some_dummy_boolean_value=faker.boolean(),
    )


def generate_and_write(faker: Faker, file: io.BufferedWriter) -> None:
    material = generate_fake_material(faker)
    file.write(
        f"{material.material_id},{material.arrived_at},{material.weight},{material.product_label},{material.quality_category},{material.some_dummy_boolean_value}\n".encode()
    )


def generate() -> None:
    logger.info("generating fake data")
    with open("./data.csv", "wb") as dst:
        dst.write(
            "MATERIAL_ID,ARRIVED_AT,WEIGHT,PRODUCT_LABEL,QUALITY_CATEGORY,SOME_DUMMY_BOOLEAN_VALUE\n".encode()
        )
        faker = Faker()
        Faker.seed(42)
        number_of_entities = 100000
        executor = ThreadPoolExecutor()
        futures = [
            executor.submit(generate_and_write, faker, dst)
            for _ in range(number_of_entities)
        ]
        for _ in as_completed(futures):
            pass
    logger.info("successfully generated fake data")


if __name__ == "__main__":
    generate()
