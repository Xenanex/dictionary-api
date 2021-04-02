import requests

class Dictionnary():
    MAX_ERROR = 0

    def __init__(self):
        self.root_node = Node("")
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
            return []

        return self.__autocomplete_rec(start_with, head_node)

    def __autocomplete_rec(self, curr_word, curr_node):
        result = []
        if curr_node.is_word:
            result.append(curr_word)

        for letter,letter_node in curr_node.childs.items():
            result.extend(self.__autocomplete_rec(f"{curr_word}{letter}", letter_node))

        return result

    def __get_start_possibilities_with_error(self, start_with):
        return self.__get_start_possibilities_with_error_rec(start_with, "", self.root_node, 0)

    def __get_start_possibilities_with_error_rec(self, continue_with, curr_word, curr_node, curr_error):
        if curr_error > MAX_ERROR or curr_node is None:
            return []

        if continue_with == "":
            return [curr_word]

        result = []

        # Replace by "" => take the second letter
        replaced_letter = continue_with[0]
        replaced_node = curr_node.childs.get(replaced_letter, Node(""))

        second_letter = continue_with[1:2]
        next_continue_with = continue_with[2:]
        next_curr_word = f"{curr_word}"
        next_curr_node = replaced_node.childs.get(continue_with[1:2])
        next_curr_error = curr_error + 1
        result.extend(__get_node_possibilities_with_error_rec(next_continue_with, next_curr_word, next_curr_node, next_curr_error))

        #Replace by all possibilities instead of first letter
        for letter,next_curr_node in curr_node.childs.items():
            if letter != continue_with[0]:
                curr_error += 1
            next_continue_with = continue_with[1:]
            next_curr_word = f"{curr_word}{letter}"
            result.extend(__get_node_possibilities_with_error_rec(next_continue_with, next_curr_word, next_curr_node, next_curr_error))

        return result


    def autocomplete_with_error(self, start_with):
        result = []

        # List of start_possibility
        start_possibilities = self.__get_start_possibilities_with_error(start_with, MAX_ERROR)
        for start_possibility in start_possibilities:
            result.extend(autocomplete(self, start_possibility))

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
