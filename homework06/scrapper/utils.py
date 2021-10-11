import csv
from definitions import DATA_DIR


def load_data(filename: str = "SMSSpamCollection"):
    with open(DATA_DIR / filename, 'r', encoding='utf-8') as f:
        data = list(csv.reader(f, delimiter="\t"))
    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
    return X, y
