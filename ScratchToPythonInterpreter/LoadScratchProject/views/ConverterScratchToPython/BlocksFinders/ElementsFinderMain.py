from abc import ABC, abstractmethod


class ElementsFinderMain(ABC):
    @abstractmethod
    def __init__(self, json_file, element):
        self.json_file = json_file
        self.element = element
        self.list_of_elements = []

    @abstractmethod
    def find_element(self):
        pass

    @abstractmethod
    def get_list_of_elements(self):
        return self.list_of_elements

    @abstractmethod
    def get_name_of_element(self):
        return self.element
