import os

sub_folders = 0
for root, dirs, files in os.walk(os.getcwd()):
    sub_folders += len(dirs)
    for item in files:
        path = os.path.join(root, item)
        print(path)

print('Sub-Folders:', sub_folders)
