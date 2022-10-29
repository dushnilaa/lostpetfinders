import json
import time
from datetime import datetime

import requests
import yaml
from fake_useragent import UserAgent
from lxml import html

from db.methods import MethodsMySQL
from db.schemes import User


class Parser:
    def __init__(self):
        self.my_sql = MethodsMySQL()
        self.sleep_sec = self.read_yaml()[1]['sleep_sec']
        self.start_date_unix = self.read_yaml()[1]['start_date']
        self.proxies = self.read_yaml()[1]['proxies']

    def read_yaml(self):
        # with open('/home/work/projects/work/lostpetfinders/parser_files/config.yaml') as fh:
        with open('config.yaml') as fh:
            return yaml.safe_load(fh)

    @classmethod
    def create_dict(cls, raw_dict):
        dict_insert = {'status': raw_dict.get('status'),
                       'website': raw_dict.get('website'),
                       'ws_id': raw_dict.get('item_id'),
                       'phone': raw_dict.get('phone'),
                       'email': raw_dict.get('email'),
                       'author': raw_dict.get('author'),
                       'descr': raw_dict.get('description')
                       }

        if raw_dict.get('item_date_created'):
            time_create = raw_dict.get('item_date_created')
            date = datetime.strptime(time_create, "%Y-%m-%d %H:%M:%S")
            time_stamp = datetime.timestamp(date)
            dict_insert['created_at'] = int(time_stamp)

        try:
            if raw_dict.get('item_datefound'):
                time_found = raw_dict.get('item_datefound')
                date = datetime.strptime(time_found, "%Y-%m-%d")
                time_stamp = datetime.timestamp(date)
                dict_insert['happened_at'] = int(time_stamp)
        except:
            pass

        if raw_dict.get('item_state') and raw_dict.get('item_suburb'):
            state = raw_dict.get('item_state')
            suburb = raw_dict.get('item_suburb')
            address = f'{state}, {suburb}'
            dict_insert['address'] = address

        if raw_dict.get('images'):
            list_pics = []
            for pic in raw_dict.get('images'):
                list_pics.append(pic.get('image'))
            dict_insert['pics'] = list_pics

        if raw_dict.get('animal') == 'Dog':
            dict_insert['animal'] = 1
        elif raw_dict.get('animal') == 'Cat':
            dict_insert['animal'] = 2
        else:
            dict_insert['animal'] = 3

        if raw_dict.get('item_flag') == 'found':
            dict_insert['type'] = 2
        elif raw_dict.get('item_flag') == 'lost':
            dict_insert['type'] = 1

        if raw_dict.get('item_gender') == 'Male':
            dict_insert['sex'] = 2
        elif raw_dict.get('item_gender') == 'Female':
            dict_insert['sex'] = 3
        else:
            dict_insert['sex'] = 0

        return dict_insert

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
            animal = {'joined': False, 'write_mysql': False, 'status': 0, 'website': 1}
            for key in keys:
                value = animal_dict.get(key)
                animal.update({key: value})
            all_animal.append(animal)
        return all_animal

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

    def download_json(self, headers=True, proxies=None):
        count = 0
        while True:

            unixtime = datetime.now().timestamp() - self.start_date_unix
            start_date = datetime.fromtimestamp(unixtime).strftime("%d/%m/%Y")

            start_url = f'https://lostpetfinders.com.au/pets/map_bound_items?status=all&address=&pet_type=' \
                        f'&radius=20&pet_id=&gender=&breed=&color=&listed_after={start_date}&micro_chip=' \
                        f'&lat=-24.9899066&lng=115.2063346&offset={count}&expand_radius=0'

            if headers:
                headers = {'User-Agent': UserAgent().chrome}
            if proxies:
                proxies = self.proxies
            request = requests.get(url=start_url, headers=headers, proxies=proxies).text

            data = json.loads(request)
            list_animal = data['items']['items']
            if not list_animal:
                print(start_url)
                break

            result_dicts = self.parser_search_result(list_animal)
            for dict_animal in result_dicts:
                id_animal = dict_animal.get('item_id')
                url = f'https://lostpetfinders.com.au/pets/{id_animal}'
                result = self.parser_page(url, headers, proxies)
                new_dict = self.create_dict(dict_animal | result)
                self.my_sql.insert(new_dict, User)
                time.sleep(self.sleep_sec)

            time.sleep(self.sleep_sec)
            count += 9
