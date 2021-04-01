import requests

class Dictionnary():

    def __init__(self):
        self.words = []
        pass

    def load(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            raise RuntimeError("Trouble with the verification API")
        body = r.text
        self.words.extend([x.lower() for x in body.split("\n")])

    def is_present(self, word):
        return word in self.words
