import logging

from tortoise import Tortoise


async def init(path: str = "Database/database.db"):

    logging.info("Connecting to database...")

    await Tortoise.init(
        db_url=f"sqlite://{path}",
        modules={
            "models": [
                "Database.Models.user",
                "Database.Models.node",
            ]
        },
    )
    await Tortoise.generate_schemas()
