#!/usr/bin/python3
import os
import copy
import json
import hashlib

BUF_SIZE = 65536

def sha256file(file):
    sha256 = hashlib.sha256()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def replace_in_file(file_path, old_text, new_text):
    with open(file_path, 'r') as file:
        file_data = file.read()

    file_data = file_data.replace(old_text, new_text)

    with open(file_path, 'w') as file:
        file.write(file_data)

def process_files(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            process_files(item_path)
        elif item.endswith('.json'):
            replace_in_file(item_path, 'http://dl.liteloader.com/versions', 'https://bmclapi.bangbang93.com/maven/com/mumfrey/liteloader')

            replace_in_file(item_path, 'http://repo.maven.apache.org/maven2', 'https://mirrors.cloud.tencent.com/nexus/repository/maven-public')

            replace_in_file(item_path, 'https://maven.fabricmc.net', 'https://bmclapi2.bangbang93.com/maven')
            replace_in_file(item_path, 'https://maven.modmuss50.me', 'https://bmclapi2.bangbang93.com/maven')

            replace_in_file(item_path, 'https://piston-meta.mojang.com', 'https://bmclapi2.bangbang93.com')
            replace_in_file(item_path, 'https://launchermeta.mojang.com', 'https://bmclapi2.bangbang93.com')
            replace_in_file(item_path, 'https://launcher.mojang.com', 'https://bmclapi2.bangbang93.com')
            replace_in_file(item_path, 'https://piston-data.mojang.com', 'https://bmclapi2.bangbang93.com')
            replace_in_file(item_path, 'https://libraries.minecraft.net', 'https://bmclapi2.bangbang93.com/maven')

            replace_in_file(item_path, 'https://maven.minecraftforge.net', 'https://bmclapi2.bangbang93.com/maven')
            replace_in_file(item_path, 'https://files.minecraftforge.net/maven', 'https://bmclapi2.bangbang93.com/maven')

            replace_in_file(item_path, 'https://maven.neoforged.net/releases', 'https://bmclapi2.bangbang93.com/maven')

            # replace_in_file(item_path, 'https://maven.quiltmc.org/repository/release', 'https://bmclapi2.bangbang93.com/maven')

def fix_sha256(directory):
    has_index = ""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            fix_sha256(item_path)
        elif item.endswith('index.json'):
            has_index = item
    if has_index != "":
        plain = ""
        need_change = False
        with open(os.path.join(directory, has_index), 'r+', encoding="utf-8") as f:
            data = json.load(f)
            fix_data = fix_sha256_internal(copy.deepcopy(data), directory)
            plain = json.dumps(fix_data)
            if plain != f.read():
                need_change = True
        if need_change:
            with open(os.path.join(directory, has_index), 'w') as f:
                f.write(plain)

def fix_sha256_internal(data, directory):
    for obj in data:
        if isinstance(data, dict):
            obj = data[obj]
        if isinstance(obj, dict):
            if 'sha256' in obj:
                item = ''
                uid = ''
                if 'version' in obj:
                    item = obj['version']
                    obj['sha256'] = sha256file(os.path.join(directory, item + '.json'))
                    print("fix sha256 for {}", os.path.join(directory, item + ".json"))
                if 'uid' in obj:
                    uid = obj['uid']
                    obj['sha256'] = sha256file(os.path.join(*[directory, uid, 'index.json']))
                    print("fix sha256 for {}", os.path.join(*[directory, uid, 'index.json']))
            else:
                fix_sha256_internal(obj, directory)
        elif isinstance(obj, list):
            fix_sha256_internal(obj, directory)
    return data

if __name__ == '__main__':
    os.system("rm -rf meta-launcher")
    os.system("git clone https://github.com/PrismLauncher/meta-launcher")
    current_directory = os.path.join(os.getcwd(), 'meta-launcher')
    process_files(current_directory)
    fix_sha256(current_directory)
    os.system("rm -rf meta")
    os.system("mv meta-launcher meta")
    os.system("chmod -R 777 meta")
    os.system("rm -rf meta/.git")


