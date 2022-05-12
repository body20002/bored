import json
from tortoise import run_async, Tortoise

from app.settings import get_settings

settings = get_settings()
backup_folder = settings.BACKUP_FOLDER / "db"

# files = [
#     "activities.json",
#     "facts.json",
#     "riddles.json",
#     "websites.json",
# ]

# files = list(map(lambda file: f"{backup_folder}{file}", files))

# models = [m.Activity, m.Fact, m.Riddle, m.Website]
# schemas = [s.Activity, s.Fact, s.Riddle, s.Website]


async def import_db(files, models, schemas):
    file_data: list[dict] | None = None

    print("Importing Files")
    for file, model, schema in zip(files, models, schemas):
        with open(file) as f:
            file_data = json.load(f)

        if not file_data is None:
            for entry in file_data:
                data = schema(**entry)
                await model.create(**data.dict())
        print(
            file,
            "\033[42mOk\033[49m",
        )


async def export_db(files, models, schemas):
    class Encoder(json.JSONEncoder):
        """Encoding Enums Fields"""

        def default(self, o):
            return o.value

    print("Exporting Files")
    for file, model, schema in zip(files, models, schemas):
        objs = await model.all()
        objs_list = []
        for obj in objs:
            data = schema.parse_obj(obj)
            objs_list.append(data.dict())

        with open(file, "w") as f:
            json.dump(objs_list, f, cls=Encoder)

        print(
            file,
            "\033[42mOk\033[49m",
        )


async def run():
    import os

    await Tortoise.init(
        db_url=os.environ.get("DB_URL", "sqlite://../local.db"),
        modules={"models": ["models"]},
    )
    await Tortoise.generate_schemas()

    # await import_db()
    # await export_db()


if __name__ == "__main__":
    run_async(run())
