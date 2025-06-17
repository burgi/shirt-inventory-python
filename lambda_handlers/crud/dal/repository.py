import json
from typing import Dict

from lambda_handlers.crud.dal.schemas.item_schema import ShirtItem


class FileRepository:

    def __init__(self):
        self.db_file_name = 'db/items.db'

    def read(self) -> Dict[int, ShirtItem]:
        with open(self.db_file_name, 'r', encoding='utf-8') as db_file:
            data = json.load(db_file)
            return {int(key): ShirtItem(**value) for key, value in data.items()}

    def write(self, item_id: int, item_entry: ShirtItem):
        with open(self.db_file_name, 'r+', encoding='utf-8') as db_file:
            data = json.load(db_file)
            data[item_id] = item_entry.model_dump()
            db_file.seek(0)
            json.dump(data, db_file, indent=4)
            db_file.truncate()


# load data from DB
with open('db/items.db', 'r', encoding='utf-8') as initial_db_file:
    initial_data = json.load(initial_db_file)
    # save DB data in memory to improve performance
    ITEMS = {int(key): ShirtItem(**value) for key, value in initial_data.items()}
