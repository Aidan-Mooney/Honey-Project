import os


def get_latest_folder():
    base_path = "data/extract"
    path_list = os.listdir(base_path)
    if not path_list:
        return None
    else:
        return sorted(path_list, reverse=True)[0]
