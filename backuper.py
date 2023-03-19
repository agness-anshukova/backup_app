import requests
import json
import os, glob

class BackUper:
    def __init__(self, token: str, vk_id: str):
        self.token = token
        self.vk_id = vk_id

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
        headers = self.get_headers()
        params = {"path":disk_file_path, "overwrite":"true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return json.loads(response.text)
    
    def upload(self, disk_file_path, filename):
        result = self._get_upload_link(disk_file_path=disk_file_path)  
        print(result.get("href"))
        url = result.get("href")
        response = requests.put(url,data=open(filename, 'rb'))
        response.raise_for_status()

        if response.status_code == 201:
            print('Success')

    def upload_VK_PH(self):
        access_token = 'vk1.a.FQZTmZBPACHBGRf-IY7w8VCYHQghG-s5r1RnojlB5BfEnbGY16uFs45vseevAO-PKRKnQfVTWiYN0huLCW_gA3wSPGkPY_sSqCjVZVI0NEn79c4QlS1oT4xicSIifYThh0Zed_WS7990De7ozyHN7DBkODUnK5c3o4zwkrgRZf5Wu8bANi9TQAtkpg8SzK4IqWQBvkGYd6EY4qEF0gVZRQ'
        user_id = '520147283'
        vk = VK(access_token, user_id)
        js = vk.users_photo()
        # данные для json-файла 
        data = []        
        for item in js['response']['items']:
            photo_it = {}
            photo_it['file_name'] = str(item['likes']['count'])+"_"+str(item['date'])+".jpg"
            for photo in item['sizes']:
                if photo['type'] =='s':
                    photo_it['url'] = photo['url']
                    photo_it['size'] = 's'
                elif photo['type'] =='m':
                    photo_it['url'] = photo['url']
                    photo_it['size'] = 'm'
                elif photo['type'] =='x':
                    photo_it['url'] = photo['url']
                    photo_it['size'] = 'x'
                elif photo['type'] =='o':
                    photo_it['url'] = photo['url']
                    photo_it['size'] = 'o'
                elif photo['type'] =='p':
                    photo_it['url'] = photo['url']
                    photo_it['size'] = 'p'
                elif photo['type'] =='q':
                    photo_it['url'] = photo['url']
                    photo_it['size'] = 'q'
                elif photo['type'] =='r':
                    photo_it['url'] = photo['url']
                    photo_it['size'] = 'r'
                elif photo['type'] =='y':
                    photo_it['url'] = photo['url']
                    photo_it['size'] = 'y' 
                elif photo['type'] =='z':
                    photo_it['url'] = photo['url']
                    photo_it['size'] = 'z'
                elif photo['type'] =='w':
                    photo_it['url'] = photo['url']
                    photo_it['size'] = 'w' 
            # загрузка фото на диск
            filename=photo_it['file_name']
            response=requests.get(photo_it['url'])
            if response.status_code==200:
                with open(filename,'wb') as imgfile:
                    imgfile.write(response.content)
            data.append(photo_it)

        # загрузка фото на Яндекс Диск
        for photo in data:
            self.upload(disk_file_path = "netology/"+photo['file_name'], filename = photo['file_name'])

        # создание json-файла с описанием фото
        with open("data_file.json", "w") as write_file:
            json.dump(data, write_file)
        # загрузка json-файла с описанием фото
        self.upload(disk_file_path = "netology/data_file.json", filename = "data_file.json")
        
        # удаление фото с диска
        for file in glob.glob('*.jpg'):
            os.remove(file)
        # удаление data_file.json с диска
        os.remove("data_file.json")

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
       return response.json()
   
   def users_photo(self):
       url = 'https://api.vk.com/method/photos.get?extended=1'
       params = {'owner_id': self.id, 'album_id': 'profile'}
       response = requests.get(url, params={**self.params, **params}) 
       return response.json()


