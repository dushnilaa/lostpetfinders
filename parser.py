import json
import time

import requests
from fake_useragent import UserAgent
from lxml import html

from db import MethodsMongo


class Parser:

    @classmethod
    def write_db(cls, data, *args):
        mongo = MethodsMongo()
        for dict_ins in data:
            dict_ins["_id"] = int(dict_ins.get('item_id'))
            mongo.insert(dict_ins, *args)

    @classmethod
    def parser_search_result(cls, list_animal):
        keys = [
            'item_id',
            'item_name',
            'pet_type',
            'item_gender',
            'item_flag',
            'item_datefound',
            'item_date_created',
            'item_listingType',
            'item_suburb',
            'item_state',
            'images',
        ]

        all_animal = []
        for animal_dict in list_animal:
            animal = {'joined': False, 'write_mysql': False}
            for key in keys:
                value = animal_dict.get(key)
                animal.update({key: value})
            all_animal.append(animal)
        return all_animal

    def download_json(self, headers=True, proxies=None):
        start_date = '27/09/2022'
        count = 0
        while True:
            start_url = f'https://lostpetfinders.com.au/pets/map_bound_items?status=all&address=&pet_type=' \
                        f'&radius=20&pet_id=&gender=&breed=&color=&listed_after={start_date}&micro_chip=' \
                        f'&lat=-24.9899066&lng=115.2063346&offset={count}&expand_radius=0'

            if headers:
                headers = {'User-Agent': UserAgent().chrome}
            request = requests.get(url=start_url, headers=headers, proxies=proxies).text

            data = json.loads(request)
            list_animal = data['items']['items']
            if not list_animal:
                print(start_url)
                break

            result = self.parser_search_result(list_animal)
            self.write_db(result)

            time.sleep(5)
            count += 9

    @classmethod
    def parser_page(cls, url, headers=None, proxy=None):
        if headers:
            headers = {'User-Agent': UserAgent().chrome}
        request = requests.get(url=url, headers=headers, proxies=proxy).text

        tree = html.fromstring(request)
        item_id = tree.xpath('//div[@class="id pull-left"]//h3//text()')[0].lstrip("'ID: ")
        desc = tree.xpath('//div[@class="description"]//text()')
        descriptiion_list = [i.strip() for i in desc]
        descriptiion = ' '.join(descriptiion_list).strip()

        result = {
            'item_id': int(item_id),
            'description': descriptiion
        }

        return result

    def update_pages(self):
        mongo = MethodsMongo()
        dicts = mongo.find_all({'joined': False})

        for dict_animal in dicts:
            id_animal = dict_animal.get('_id')
            url = f'https://lostpetfinders.com.au/pets/{id_animal}'
            result = self.parser_page(url)
            self.write_db([result], {'joined': True})
            time.sleep(5)
