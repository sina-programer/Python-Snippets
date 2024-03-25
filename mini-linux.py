from abc import abstractmethod, ABC
import operator

class Item(ABC):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    def rename(self, new_name):
        self.name = new_name

    @abstractmethod
    def is_file(self): return

    @abstractmethod
    def is_folder(self): return

    @property
    def path(self):
        names = [self.name]
        parent = self.parent
        while parent is not None:
            names.append(parent.name)
            parent = parent.parent
        return '/'.join(names[::-1])


class File(Item):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.context = None

    def write(self, context):
        self.context = context

    def is_file(self): return True
    def is_folder(self): return False


class Folder(Item):
    def __init__(self, name, parent=None):
        super().__init__(name, parent=parent)
        self.sub_folders = []
        self.sub_files = []

    def is_file(self): return False
    def is_folder(self): return True

    def get_folder_by_name(self, name):
        for folder in self.sub_folders:
            if folder.name == name:
                return folder

    def get_file_by_name(self, name):
        for file in self.sub_files:
            if file.name == name:
                return file

    def get_item_by_name(self, name):
        if name in self.sub_folder_names:
            return self.get_folder_by_name(name)
        elif name in self.sub_file_names:
            return self.get_file_by_name(name)

    @property
    def sub_folder_names(self): return list(map(operator.attrgetter('name'), self.sub_folders))

    @property
    def sub_file_names(self): return list(map(operator.attrgetter('name'), self.sub_files))


class Manager:
    def __init__(self):
        self.root = Folder('root')
        self.current_dir = self.root

    def command_mkdir(self, folder_name):
        if folder_name in self.current_dir.sub_folder_names:
            print('Error: Folder Already Exists')
        else:
            folder = Folder(folder_name, parent=self.current_dir)
            self.current_dir.sub_folders.append(folder)

    def command_cd(self, folder_name):
        if folder_name == '..' and self.current_dir.parent is not None:
            self.current_dir = self.current_dir.parent
        elif folder_name in self.current_dir.sub_folder_names:
            self.current_dir = self.current_dir.get_folder_by_name(folder_name)
        else:
            print('Error: Folder Does Not Exists')

    def command_touch(self, parent_folder, file_name):
        if parent_folder in self.current_dir.sub_folder_names:
            folder = self.current_dir.get_folder_by_name(parent_folder)
            file = File(file_name, folder)
            folder.sub_files.append(file)

    def command_ls(self):
        for folder in self.current_dir.sub_folders:
            print('++', folder.name)
        for file in self.current_dir.sub_files:
            print(file.name)

    def command_pwd(self, name):
        item = self.current_dir.get_item_by_name(name)
        if item is None:
            print('File Does Not Exists')
        else:
            print(item.path)

    def command_vi(self, file_name, end='!q'):
        stdin = []
        while True:
            line = input()
            if line.endswith(end):
                break
            stdin.append(line)

    def command_rn(self, old_name, new_name):
        item = self.current_dir.get_item_by_name(old_name)
        item.rename(new_name)

    def command_rmdir(self, folder_name):
        folder = self.current_dir.get_folder_by_name(folder_name)
        self.current_dir.sub_folders.remove(folder)

    def command_rm(self, file_name):
        file = self.current_dir.get_file_by_name(file_name)
        self.current_dir.sub_files.remove(file)

    def command_mv(self, origin, destination):
        destination = self.current_dir.get_folder_by_name(destination)
        item = self.current_dir.get_item_by_name(origin)
        item.parent = destination
        if item.is_file():
            self.current_dir.sub_files.remove(item)
            destination.sub_files.append(item)
        else:
            self.current_dir.sub_folders.remove(item)
            destination.sub_folders.append(item)

    @property
    def commands(self):
        prefix = 'command_'
        commands = list(filter(lambda x: prefix in x, dir(self)))
        return list(map(lambda x: x.removeprefix(prefix), commands))

    def get_command(self, command):
        return getattr(self, f"command_{command}")

    def validate_path(self, path, delimiter='/'):
        names = path.split(delimiter)
        root = self.current_dir
        for name in names:
            subroot = root.get_item_by_name(name)
            if subroot:
                root = subroot
            else:
                return False
        return True

    def loop(self):
        while True:
            prompt = input(self.current_dir.path + '> ')
            command, *args = prompt.split()
            if command not in self.commands:
                print('Exception: Invalid Command')
            method = self.get_command(command)
            method(*args)


if __name__ == "__main__":
    manager = Manager()
    manager.loop()
