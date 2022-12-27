import datetime
from tqdm import tqdm
import requests
from pprint import pprint
import json


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        response_json = response.json()['response']
        for info_data in response_json:
            name_user = (info_data['first_name'] + info_data['last_name'])
            user_id = info_data['id']
            return user_id, name_user

    def users_photo(self, user_id, number_photo=5):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id[0],
                  'album_id': 'profile',
                  'extended': 'likes'
                  }
        response = requests.get(url, params={**self.params, **params})
        response_json = response.json()['response']['items']
        upload_photo = {}
        json_doc = []
        self.list_json = json_doc
        for photo in response_json:
            date_photo = datetime.datetime.fromtimestamp(photo['date']).strftime('%Y-%m-%d')
            max_like = str(photo['likes']['count'])
            max_photo = photo['sizes'][-1]['url']
            type_photo = photo['sizes'][-1]['type']
            glossary = {max_like: max_photo}
            if max_like in upload_photo.keys():
                upload_photo.update({date_photo: max_photo})
            else:
                upload_photo.update(glossary)
            scroll_data = {"file_name": max_like,
                           'size': type_photo
                           }
            json_doc.append(scroll_data)
            if len(upload_photo) == number_photo:
                break
        return upload_photo

    def get_joson(self):
        with open('file.json', 'w') as file:
            json.dump(self.list_json, file)


class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def creat_folder(self, name_folder):
        self.folder = name_folder[1]
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {'path': f'/{self.folder}'}
        respons = requests.put(url, headers=self.get_headers(), params=params)
        if respons.status_code == 409:
            print('Папка с таким именем уже существует')
        else:
            print(f'Папака {self.folder} создана')

    def get_upload_lint(self, dsik_file_name):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': f'/{self.folder}/{dsik_file_name}'}
        response = requests.get(url,  headers=self.get_headers(), params=params)
        return response.json()['href']

    def upload_photo_disk(self, photo_dict):
        for name, photo in tqdm(photo_dict.items()):
            url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            params = {'path': f'/{self.folder}/{name}.jpg', 'url': photo}
            respons = requests.post(url, headers=self.get_headers(), params=params)
            pprint(respons.status_code)


if __name__ == '__main__':
    access_token = 'vk1.a.e8BGn1pwaHqmuTENLG57HJiTyZ5Eu9n-4sYRCKATTZdDkDKT5Qeui3oTjGt_3rycj5RurXEJOPW5-' \
                   '3fweZazo7Wmdy19sqa9uBd-Xz6q-rV3uj4g5jVhjEofE-' \
                   '4GKKTJJMVsTbVnf_380yCXkdXco7AqsrM2xsTLY7qKl8o5LiLBHOX7nlnL_R92E8B7jihPQ2I7OEVIuUZ9-0ZmP8mTFg'
    user_id = input('Ввидите ID: ')
    number_photo = int(input('Сколько фото вы хотите скачать? '))
    yandex_token =
    vk = VK(access_token, user_id)
    ya = YaUploader(yandex_token)
    ya.creat_folder(vk.users_info())
    ya.upload_photo_disk(vk.users_photo(vk.users_info(), number_photo))

