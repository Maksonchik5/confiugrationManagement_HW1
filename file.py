#!/bin/python3
import json
import tarfile
import os
import tempfile


def load_configuration(path):
    with open(path, "r") as f:
        return json.load(f)


class VirtualFileSystem:
    def __init__(self, tar_path):
        self.tar = tarfile.open(tar_path, "r")
        self.current_directory = ''


    def ls(self, path=''):
        path = self.current_directory + path
        files = [filename for filename in self.tar.getnames() if filename.startswith(path)]
        print(' '.join(files))


    def cd(self, path):
        if path == "..":
            self.current_directory = os.path.dirname(self.current_directory)
        elif self._path_exist(path):
            self.current_directory = path
        else:
            print(f"Directory {path} is not found")


    def cp(self, first_file_name, second_file_name):
        if self._path_exist(first_file_name):
            #метаданные исходного файла
            original_file_info = self.tar.getmember(first_file_name)

            #содержимое исходного файла
            original_file = self.tar.extractfile(first_file_name)

            #создание временного файла
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(original_file.read())
                temp_file_name = temp_file.name
            
            with tarfile.open(self.tar.name, "a") as tar:
                #создание объекта TarInfo с именем копии
                temp_file_info = tarfile.TarInfo(name=second_file_name)

                #метаданные исходного файла
                temp_file_info.size = os.path.getsize(temp_file_name)
                temp_file_info.mode = original_file_info.mode
                temp_file_info.mtime = original_file_info.mtime

                with open(temp_file_name, "rb") as temp_file:
                    tar.addfile(temp_file_info, temp_file)


            #self.tar.add(temp_file.name, arcname=second_file_name)
            os.remove(temp_file_name)
        else:
            print(f"File {first_file_name} does not exist")


    def _path_exist(self, path):
        return any(filename.startswith(path) for filename in self.tar.getnames())


class ShellEmulator:
    def __init__(self, config):
        self.username = config['username']
        self.vfs = VirtualFileSystem(config['tar_path'])
        self.invitation = f"{self.username}@virtualFileSystem:$ "
        self.start_script_path = config['start_script']

    def run(self):
        while(True):
            command = input(self.invitation)
            exit_code = self.execute_command(command)
            if exit_code:
                break

    def execute_command(self, command):
        if command.split(' ')[0] == "ls":
            if len(command.split(' ')) != 1:
                self.vfs.ls(command.split(' ')[1])
            else:
                self.vfs.ls()
        elif command.split(' ')[0] == 'cd':
            self.vfs.cd(command.split(' ')[1])
        elif command == 'clear':
            self._clear()
        elif command.split(' ')[0] == 'cp':
            first_file_name, second_file_name = command.split(' ')[1], command.split(' ')[2]
            self.vfs.cp(first_file_name, second_file_name)
        elif command == "exit":
            return True
        else:
            print(f"Command {command} does not exist")
        return False


    def run_startup_script(self):
        with open(self.start_script_path, 'r') as file:
            for line in file:
                line = line.strip()
                print(f'Executing: {line}')
                self.execute_command(line)

    def _clear(self):
        os.system('clear')

json_conf = load_configuration("conf.json")
shell = ShellEmulator(json_conf)
shell.run_startup_script()
