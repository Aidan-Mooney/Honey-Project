from src.extract.get_latest_folder import get_latest_folder


def get_last_date():
    dir = get_latest_folder()
    if not dir:
        return None
    with open(f"data/extract/{dir}/purchases.csv", "r", encoding="utf-8") as f:
        top_line = f.readline()
    return top_line.split(",")[2]
