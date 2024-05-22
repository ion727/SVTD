from cryptography.fernet import Fernet
import os
import hashlib

wrong = False
key = input("Enter password: ")
for i in range(1000):
    key = hashlib.sha256(key.encode("utf-8"),usedforsecurity=True).hexdigest()

key = Fernet(key[:43].encode("utf-8")+b"=")

def list_files(directory_path):
    files = []
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
        elif os.path.isdir(file_path):
            files.extend(list_files(file_path))
    return files

files = list_files(".\\")
files.remove(".\\password_protection.py")

for file in files:
    with open(file,"rb") as e:
        file_contents = e.read()
        try:
            decrypted_contents = key.decrypt(file_contents)
        except:
            wrong = True    
            decrypted_contents = None
            print("incorrect password")
            break
    if not wrong:
        with open(file,"wb") as e:
            e.write(decrypted_contents)
if not wrong:
    exec(open("file_config.txt").read())
    os.remove("file_config.txt") # remove this line to make changes to file_config.txt
    os.remove(__file__)
