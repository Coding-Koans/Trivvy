class Questions_Asked():
    
    def __init__(self):
        self._log = []
        self._clear_received = False

    def log(self, question):
        self._log.append(question)

    def clear_all(self):
        self._log = []
        self._clear_received = True

    def all_logged(self):
        return self._log
