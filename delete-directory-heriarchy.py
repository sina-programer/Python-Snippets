import os

def delete(path):
    global DELETED_FILES, REMAINED_FILES, FREED_SPACE

    try:
        if os.path.isfile(path):
            file_size = os.path.getsize(path)
            os.remove(path)
            DELETED_FILES += 1
            FREED_SPACE += file_size

        else:
            for item in os.listdir(path):
                delete(item)
            os.rmdir(path)

    except Exception:
        REMAINED_FILES += 1


PATH = ""
DELETED_FILES = 0
REMAINED_FILES = 0
FREED_SPACE = 0
