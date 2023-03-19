import backuper

if __name__ == '__main__':
    # Программа принимает на вход путь до файла на компьютере и сохраняет на Яндекс.Диск с таким же именем
    token = " " # токен Яндекс Диска
    vk_id = " " # идентификатор VK
    backuper_obj = backuper.BackUper(token, vk_id)
    backuper_obj.upload_VK_PH();