class json:

    def __init__(self, file):
        self.file = file

    def get_list(self):
        import json

        js = None

        with open(self.file) as file:
            js = json.load(file)
            file.close()

        return js
