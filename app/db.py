import json


class DogsFactsApi:
    def __init__(self):
        self.data = 'facts.json'

    def create_database(self) -> None:
        data = {'data': []}
        with open(self.data, 'w') as file:
            json.dump(data, file)

    def add_fact(self, fact: dict) -> None:
        with open(self.data, 'r') as file:
            data = json.load(file)
            data['data'].append(fact)
        with open(self.data, 'w') as file:
            json.dump(data, file)

    def get_facts(self):
        pass


dogs_facts_api = DogsFactsApi()
dogs_facts_api.create_database()
