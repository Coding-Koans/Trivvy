import os

class FS_ORM():
    def __init__(self, filename, blank_records):
        self.filename = f"{filename}.txt"
        self.cache = None
        self.blank_records = blank_records
        self.records = self.get_records()

    def save_records(self, records):
        self.overwrite_to_FS(records)

    def get_records(self):
        if self.cache or self.cache == self.blank_records:
            return self.cache

        if os.path.exists(self.filename):
            return self.read_from_existing_records()

        return self.create_new_blank_records()

    def read_from_existing_records(self):
        file = open(self.filename)
        records = eval(file.read())
        self.cache = records
        file.close()
        return records

    def create_new_blank_records(self):
        self.records = self.blank_records
        self.overwrite_to_FS(self.records)
        self.cache = self.records
        return self.records

    def overwrite_to_FS(self, records):
        file = open(self.filename, "wt")
        file.write(str(records))
        self.clear_score_cache()
        file.close()

    def clear_score_cache(self):
        self.cache = None
