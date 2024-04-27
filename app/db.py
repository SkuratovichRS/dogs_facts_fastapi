import json
import os
import requests
from random import randint
from typing import Any
from datetime import datetime


class NotFoundException(Exception):
    def __init__(self, detail):
        self.detail = detail


class DogsFactsApi:
    def __init__(self, facts_json):
        self.data = facts_json

    def create_database(self) -> None:
        if os.path.exists(self.data):
            return
        data = {'data': []}
        with open(self.data, 'w') as file:
            json.dump(data, file)

    def add_fact(self, fact: dict) -> None:
        with open(self.data, 'r') as file:
            data = json.load(file)
            data['data'].append(fact)
        with open(self.data, 'w') as file:
            json.dump(data, file, indent=4)

    def get_facts(self, page: int, page_size: int, sorting: Any) -> tuple[list[dict], int]:
        def sort_(data_):
            if sorting[0] == '-':
                data_.sort(key=lambda x: x[sorting[1:]], reverse=True)
            else:
                data_.sort(key=lambda x: x[sorting])
            return data_

        with open(self.data, 'r') as file:
            data = json.load(file)
        if page_size == 0:
            return [], len(data['data'])
        result = sort_(data['data'])[page_size * page: page_size * page + page_size]
        return result, len(data['data'])

    def get_fact_by_id(self, fact_id: str) -> dict:
        with open(self.data, 'r') as file:
            data = json.load(file)
        for fact in data['data']:
            if fact_id == fact['fact_id']:
                return fact
        raise NotFoundException(f"Fact {fact_id} is not found")

    def delete_fact_by_id(self, fact_id: str) -> None:
        with open(self.data, 'r') as file:
            data = json.load(file)
        id_ = None
        for i, fact in enumerate(data['data']):
            if fact_id == fact['fact_id']:
                id_ = i
                break
        if not id_:
            return
        data['data'].pop(id_)

        with open(self.data, 'w') as file:
            json.dump(data, file, indent=4)

    def change_fact_by_id(self, fact_id: str, fact_text: str = None,
                          interest: int = None, likes: int = None) -> dict:
        with open(self.data, 'r') as file:
            data = json.load(file)
        for i, fact in enumerate(data['data']):
            if fact_id == fact['fact_id']:
                if fact_text:
                    data['data'][i]['fact_text'] = fact_text
                if interest is not None:
                    data['data'][i]['interest'] = interest
                if likes is not None:
                    data['data'][i]['likes'] = likes
                resp = data['data'][i]
                with open(self.data, 'w') as file:
                    json.dump(data, file, indent=4)
                return resp
        raise NotFoundException(f"Fact {fact_id} is not found")

    def add_like_by_id(self, fact_id: str) -> dict:
        with open(self.data, 'r') as file:
            data = json.load(file)
        for fact in data['data']:
            if fact_id == fact['fact_id']:
                fact['likes'] += 1
                with open(self.data, 'w') as file:
                    json.dump(data, file, indent=4)
                return fact
        raise NotFoundException(f"Fact {fact_id} is not found")

    def import_facts_from_dogapi(self, amount: int) -> None:
        url = 'https://dogapi.dog/api/v2/facts'
        params = {'limit': amount}
        r = requests.get(url, params=params)
        if r.status_code != 200:
            raise ValueError(f"Docs api respond with status code {r.status_code}")
        dogs_api_resp = r.json()
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


dogs_facts_api = DogsFactsApi('facts.json')
dogs_facts_api.create_database()
