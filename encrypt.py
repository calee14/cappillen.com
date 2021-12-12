from cryptography.fernet import Fernet
import os 
from os import listdir
from os.path import isfile, join
from datetime import datetime
from pathlib import Path

def gen_key():
    key = Fernet.generate_key()

    with open('secretkey.key', 'wb') as filekey:
        filekey.write(key)

def encrypt_files(dir_unencrypted, dir_encrypted):
    try:
        with open('secretkey.key', 'rb') as filekey:
            key = filekey.read()
    except:
        key = os.environ['ENCRYPTIONKEY']
    
    Path(dir_encrypted).mkdir(parents=True, exist_ok=True)

    fernet = Fernet(key)

    all_story_files = [f for f in listdir(dir_unencrypted) if isfile(join(dir_unencrypted, f) and f[0] != '.')]
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

def encrypt_dir(dir_unencrypted, dir_encrypted):
    dir_sorted = [x[0][x[0].rfind('/')+1:] for x in os.walk(dir_unencrypted)][1:] # get all directories and remove the root dir that we're recursively walking. also just get the quarter director name
    dir_sorted.sort(reverse=False) # sort dir
    print(dir_sorted)
    for quarter_dir in dir_sorted:
        encrypt_files(join(dir_unencrypted, quarter_dir), join(dir_encrypted, quarter_dir))



dir_path = os.path.dirname(os.path.realpath(__file__))
blog_unencrypted_path = join(dir_path, 'personalsite/blogs_unencrypted')
blog_encrypted_path = join(dir_path, 'personalsite/blogs')
encrypt_files(blog_unencrypted_path, blog_encrypted_path)
encrypt_dir(blog_unencrypted_path, blog_encrypted_path)