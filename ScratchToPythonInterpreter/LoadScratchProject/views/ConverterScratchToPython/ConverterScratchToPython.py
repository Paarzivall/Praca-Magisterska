from scratchclient import ScratchSession


class ConverterScratchToPython(object):
    def __init__(self, json_file):
        self.json_file = json_file
        self.list_of_variables = self.generate_list_of_variables()
        print(self.list_of_variables)

    def generate_list_of_variables(self):
        variables = []
        for target in self.json_file["targets"]:
            for element in target['variables']:
                variables.append({'name_of_variable': target['variables'][element][0],
                                 'value_of_variable': target['variables'][element][1]})
        return variables
