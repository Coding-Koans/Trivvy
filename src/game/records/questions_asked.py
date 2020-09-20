from src.game.records.file_system_orm import FS_ORM

class Questions_Asked():
    
    def __init__(self, filename = "questions_asked"):
        new_log = []
        self.fs = FS_ORM(filename, new_log)
        self.log = self.fs.get_records()

    def log(self, question):
        self.log = self.fs.get_records()
        self.log.append(question)
        self.fs.save_records(self.log)

    def clear_all(self):
        self.log = []
        self.fs.save_records(self.log)

    def all_logged(self):
        self.log = self.fs.get_records()
        return self.log
