# DictReader used to import the contents of a CSV file ignoring case sensitivity
# Source: https://micropyramid.com/blog/how-to-implement-case-insensitive-csv-dictreader-in-python/

import csv


class InsensitiveDictReader(csv.DictReader):
    @property
    def fieldnames(self):
        return [field.strip().lower() for field in csv.DictReader.fieldnames.fget(self)]

    def next(self):
        return InsensitiveDict(csv.DictReader.next(self))


class InsensitiveDict(dict):
    def __getitem__(self, key):
        return dict.__getitem__(self, key.strip().lower())
