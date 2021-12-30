from LoadScratchProject.views.ConverterScratchToPython.BlocksFinders.ElementsFinderMain import ElementsFinderMain


class VariablesFinder(ElementsFinderMain):
    def __init__(self, json_file, name_of_element):
        super().__init__(json_file, name_of_element)
        self.list_of_elements = self.find_element()

    def find_element(self):
        variables = []
        for target in self.json_file["targets"]:
            for element in target['blocks']:
                variable = target['blocks'][element]
                if variable['opcode'] == self.element:
                    variables.append({'id_of_variable': element,
                                      'name_of_variable': variable['fields']['VARIABLE'][0],
                                      'value_of_variable': variable['inputs']['VALUE'][1][1]})
        return variables

    def get_list_of_elements(self):
        super().get_list_of_elements()

    def get_name_of_element(self):
        super().get_name_of_element()

    def get_list_of_elements(self):
        return self.list_of_elements