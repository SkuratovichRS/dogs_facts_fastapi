import json
import os
from typing import Any


class DogsFactsApi:
    def __init__(self):
        self.data = 'facts.json'

    def create_database(self) -> None:
        data = {'data': []}
        with open(self.data, 'w') as file:
            json.dump(data, file)

    def total(self) -> int:
        if not os.path.exists(self.data):
            self.create_database()
        with open(self.data, 'r') as file:
            data = json.load(file)
        return len(data['data'])

    def add_fact(self, fact: dict) -> None:
        if not os.path.exists(self.data):
            self.create_database()
        with open(self.data, 'r') as file:
            data = json.load(file)
            data['data'].append(fact)
        with open(self.data, 'w') as file:
            json.dump(data, file, indent=4)

    def get_facts(self, page: int, page_size: int, sorting: Any) -> list[dict]:
        def sort_(data_):
            if sorting[0] == '-':
                data_.sort(key=lambda x: x[sorting[1:]], reverse=True)
            else:
                data_.sort(key=lambda x: x[sorting])
            return data_

        with open(self.data, 'r') as file:
            data = json.load(file)
        if page_size == 0:
            return []
        chosen_facts = []
        pagination = []
        i = 1
        for fact in data['data']:
            if i == page_size + 1:
                chosen_facts.append(pagination)
                pagination = []
                i = 1
            pagination.append(fact)
            i += 1
        chosen_facts.append(pagination)
        resp = chosen_facts[page]
        return sort_(resp)

    def get_fact_by_id(self, fact_id: str) -> dict | bool:
        with open(self.data, 'r') as file:
            data = json.load(file)
        for fact in data['data']:
            if fact_id == fact['fact_id']:
                return fact
        return False


dogs_facts_api = DogsFactsApi()
print(dogs_facts_api.get_fact_by_id("829769cd-189b-4748-ba51-b55f37025dc6"))
