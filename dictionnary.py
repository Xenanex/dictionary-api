import requests

class Dictionnary():

    def __init__(self):
        self.words = []
        pass

    def load(self, url):
        r = requests.get(url)
        # Response possible:
        #   - Not exist: {"found":false,"word":"gikdfofgda","error":"word not found"}
        #   - Exist: {"found":true,"word":"test","length":4}
        if r.status_code != 200:
            raise RuntimeError("Trouble with the verification API")
        body = r.text
        self.words.extend(map(lambda x: x.lower(),body.split("\n")))

    def is_present(self, word):
        print(f"WORD:{self.words[1]}")
        return word in self.words
