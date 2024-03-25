import json
import os
import requests
from random import randint
from typing import Any
from datetime import datetime


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

    def delete_fact_by_id(self, fact_id: str) -> None:
        with open(self.data, 'r') as file:
            data = json.load(file)
        for i, fact in enumerate(data['data']):
            if fact_id == fact['fact_id']:
                data['data'].pop(i)
        with open(self.data, 'w') as file:
            json.dump(data, file, indent=4)

    def change_fact_by_id(self, fact_id: str, fact_text: str = None,
                          interest: int = None, likes: int = None) -> dict | bool:
        with open(self.data, 'r') as file:
            data = json.load(file)
        for i, fact in enumerate(data['data']):
            if fact_id == fact['fact_id']:
                if fact_text:
                    data['data'][i]['fact_text'] = fact_text
                if interest:
                    data['data'][i]['interest'] = interest
                if likes:
                    data['data'][i]['likes'] = likes
                resp = data['data'][i]
                with open(self.data, 'w') as file:
                    json.dump(data, file, indent=4)
                return resp
        return False

    def add_like_by_id(self, fact_id: str) -> dict | bool:
        with open(self.data, 'r') as file:
            data = json.load(file)
        for i, fact in enumerate(data['data']):
            if fact_id == fact['fact_id']:
                data['data'][i]['likes'] += 1
                resp = data['data'][i]
                with open(self.data, 'w') as file:
                    json.dump(data, file, indent=4)
                return resp
        return False

    def import_facts_from_dogapi(self, amount: int) -> None:
        url = 'https://dogapi.dog/api/v2/facts'
        params = {'limit': amount}
        dogs_api_resp = requests.get(url, params=params).json()
        with open(self.data, 'r') as file:
            data = json.load(file)
        for fact in dogs_api_resp['data']:
            imported_fact = {"fact_id": fact['id'],
                             "fact_text": fact['attributes']['body'],
                             "interest": randint(1, 10),
                             "likes": 0,
                             "created_at": str(datetime.now())}
            data['data'].append(imported_fact)
        with open(self.data, 'w') as file:
            json.dump(data, file, indent=4)


dogs_facts_api = DogsFactsApi()
