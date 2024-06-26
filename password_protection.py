import os
SVTD_path = __file__[:-22] #includes the / at the end
os.system(f'pip3 install -r "{SVTD_path}requirements.txt" ' + ("> NUL" if os.name == "nt" else "> /dev/null"))
from cryptography.fernet import Fernet
import hashlib

def commands(cmd):
    options       = ("clear","rename","rmdir")
    nt_commands   = ("cls"  ,"rename","rmdir /s /q")
    lx_commands   = ("clear", "mv"   ,"rm -Rf")
    return nt_commands[options.index(cmd)] if os.name == "nt" else lx_commands[options.index(cmd)]

if __name__ == "__main__":
    os.system(f'{commands("rmdir")} ' + os.path.abspath(".git"))
    wrong = False
    key = input("Enter password: ")
    for i in range(4096):
        key = hashlib.sha256(key.encode("utf-8")).hexdigest()

    key = Fernet(key[:43].encode("utf-8")+b"=")
                
    def list_files(directory_path):
        files = []
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name) 
            if os.path.isfile(file_path):
                files.append(os.path.abspath(file_path))
            elif os.path.isdir(file_path):
                    files.extend(list_files(file_path))
        return files

    files = list_files(os.path.abspath("."))
    files.remove(os.path.abspath("password_protection.py"))
    files.remove(os.path.abspath("README.md"))
    files.remove(os.path.abspath("requirements.txt"))
    files.remove(os.path.abspath(".gitignore"))
    files.remove(os.path.abspath(".gitattributes"))

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
        with open("file_config.txt") as e:
            exec(e.read())
        os.remove("file_config.txt") # remove this line to make changes to file_config.txt
        os.remove(__file__)