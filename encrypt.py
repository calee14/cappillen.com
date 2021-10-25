from cryptography.fernet import Fernet
import os 
from os import listdir
from os.path import isfile, join
from datetime import datetime

def gen_key():
    key = Fernet.generate_key()

    with open('secretkey.key', 'wb') as filekey:
        filekey.write(key)

def encrypt_files(dir_unencrypted, dir_encrypted):
    with open('secretkey.key', 'rb') as filekey:
        key = filekey.read()
    
    fernet = Fernet(key)

    all_story_files = [f for f in listdir(dir_unencrypted) if isfile(join(dir_unencrypted, f))]
    all_story_files.sort(key = lambda date: datetime.strptime(date[0:8], '%m-%d-%y'), reverse=True) # sort stories

    previously_encrypted_files = [f for f in listdir(dir_encrypted) if isfile(join(dir_encrypted, f))]
    
    all_story_files = set(all_story_files) - set(previously_encrypted_files)

    for fileName in all_story_files:
        file_dir = join(dir_unencrypted, fileName)
        with open(file_dir, 'rb') as file:
            original = file.read()
    
        encrypted = fernet.encrypt(original)

        encryped_file_dir = join(dir_encrypted, fileName)
        with open(encryped_file_dir, 'wb') as encyrpted_file:
            encyrpted_file.write(encrypted)

dir_path = os.path.dirname(os.path.realpath(__file__))
blog_unencrypted_path = join(dir_path, 'personalsite/blogs_unencrypted')
blog_encrypted_path = join(dir_path, 'personalsite/blogs')
encrypt_files(blog_unencrypted_path, blog_encrypted_path)