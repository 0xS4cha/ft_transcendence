import csv
from types import Dataset


def parse_csv_dataset(path: str, separator: str) -> Dataset:
    with open(path, newline='', encoding='UTF-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=separator, quotechar='|')
        for row in spamreader:
            print(row)
    return Dataset()
