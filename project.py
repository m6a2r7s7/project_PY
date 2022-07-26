import json
import time
from tqdm import tqdm
from time import sleep
import requests
from pprint import pprint
with open('token.txt', 'r') as f:
    token = f.read().strip()

class VkUser:
    def __init__(self, token, version):
        self.params = {
            "access_token": token,
            'v': 5.131
        }
    URL = 'https://api.vk.com/method'

    def get_photos(self, id):
        url = self.URL + '/photos.get'
        photos_params = {
            'owner_id': f'{id}',
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': 5
        }
        new_params = {**photos_params, **self.params}
        req = requests.get(url, params=new_params).json()
        json_list = req['response']['items']
        photo_info = []
        for photo in json_list:
            name = str(photo['likes']['count']) + '.jpg'
            photo_size = str(photo['sizes'][-1]['type'])
            link = photo['sizes'][-1]['url']
            date = str(photo['date'])
            info = {"file_name": name, "size": photo_size, 'link': link, 'date': date}
            photo_info.append(info)
        return photo_info

    def get_info(self, id):
        url = self.URL + '/photos.get'
        photos_params = {
            'owner_id': f'{id}',
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': 4
        }
        new_params = {**photos_params, **self.params}
        req = requests.get(url, params=new_params).json()
        json_list = req['response']['items']
        photo_info = []
        for photo in json_list:
            name = str(photo['likes']['count']) + '.jpg'
            photo_size = str(photo['sizes'][-1]['type'])
            info = {"file_name": name, "size": photo_size}
            photo_info.append(info)
        return photo_info



class YaDisk:
    URL = "https://cloud-api.yandex.net/v1/disk/"

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        res = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        return res

    def create_folder(self, disk_file_path):
        url = self.URL + 'resources'
        headers = self.get_headers()
        params = {
            'path': disk_file_path,
            'overwrite': 'true'
        }
        res = requests.put(url, headers=headers, params=params)
        return res

    def move_photos(self, name_of_folder, id):
        self.create_folder(name_of_folder)
        self.save_photos_from_vk(id=id)
        url = self.URL + 'resources/move'
        headers = self.get_headers()
        files = vk_client.get_photos(id=id)
        for file in files:
            name = file['file_name']
            params = {
                'from': name,
                'path': f'{name_of_folder}/{name}'
            }
            res = requests.post(url, headers=headers, params=params)
        return res

    def save_photos_from_vk(self, id):
        URL = self.URL + 'resources/upload'
        files = vk_client.get_photos(id)
        headers = self.get_headers()
        for file in files:
            url = file['link']
            path = file['file_name']
            params = {
                'path': path,
                'url': url
            }
            res = requests.post(URL, params=params, headers=headers)
        return res

    def main_programm(self, vk_id, token_yadisk):
        for i in tqdm(range(200)):
            sleep(0.1)
        self.move_photos('py58', vk_id)
        pprint(vk_client.get_info(vk_id))

if __name__ == '__main__':
    vk_client = VkUser(token, '5.131')
    yandex_client = YaDisk("")
    yandex_client.main_programm(1, "")

