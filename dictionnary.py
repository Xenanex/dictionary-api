import requests

class Dictionnary():

    def __init__(self, max_error = 1):
        self.root_node = Node("")
        self.max_error = max_error
        pass

    def __add_word(self, word):
        current_node = self.root_node
        for letter in word:
            letter_node = current_node.get_child(letter)
            if letter_node is None:
                current_node.add_child(letter)
            current_node = current_node.get_child(letter)
        current_node.is_word = True

    def __get_node(self, start_with):
        current_node = self.root_node
        for letter in start_with:
            current_node = current_node.get_child(letter)
            if current_node is None:
                return None
        return current_node

    def __is_word(self, word):
        node = self.__get_node(word)
        if node is None:
            return False
        return node.is_word

    def load(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            raise RuntimeError("Trouble with the verification API")
        body = r.text
        for x in body.split("\n"):
            self.__add_word(x.lower())


    def is_present(self, word):
        return self.__is_word(word)

    def autocomplete(self, start_with):
        head_node = self.__get_node(start_with)
        if head_node is None:
            return set()

        return self.__autocomplete_rec(start_with, head_node)

    def __autocomplete_rec(self, curr_word, curr_node):
        result = set()
        if curr_node.is_word:
            result.add(curr_word)

        for letter,letter_node in curr_node.childs.items():
            result |= self.__autocomplete_rec(f"{curr_word}{letter}", letter_node)

        return result

    def __get_start_possibilities_with_error(self, start_with):
        return self.__get_start_possibilities_with_error_rec(start_with, "", self.root_node, 0)

    def __get_start_possibilities_with_error_rec(self, continue_with, curr_word, curr_node, curr_error):
        if curr_error > self.max_error:
            return set()


        if continue_with == "":
            return {curr_word}

        result = set()

        # Replace by "" => take the second letter
        replaced_letter = continue_with[0]

        next_continue_with = continue_with[1:]
        next_curr_error = curr_error + 1
        result |= self.__get_start_possibilities_with_error_rec(next_continue_with, curr_word, curr_node, next_curr_error)

        #Replace by all possibilities instead of first letter
        for letter,next_curr_node in curr_node.childs.items():
            if letter != continue_with[0]:
                next_curr_error = curr_error + 1
            else:
                next_curr_error = curr_error
            next_continue_with = continue_with[1:]
            next_curr_word = f"{curr_word}{letter}"
            result |= self.__get_start_possibilities_with_error_rec(next_continue_with, next_curr_word, next_curr_node, next_curr_error)

        return result


    def autocomplete_with_error(self, start_with):
        result = set()

        # List of start_possibility
        start_possibilities = self.__get_start_possibilities_with_error(start_with)
        for start_possibility in start_possibilities:
            result |= self.autocomplete(start_possibility)

        return result




class Node():

    def __init__(self, value, is_word=False):
        self.is_word = is_word
        self.value = value
        self.childs = {} # {"a": Node(True)}

    def add_child(self, child_value):
        self.childs[child_value] = Node(child_value)

    def get_child(self, value):
        return self.childs.get(value)


dictionnary = Dictionnary()
dictionnary.load(url="https://raw.githubusercontent.com/dwyl/english-words/master/words.txt")
print(dictionnary.autocomplete_with_error("ananas"))
