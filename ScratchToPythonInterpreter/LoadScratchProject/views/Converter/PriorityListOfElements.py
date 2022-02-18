import LoadScratchProject.views.Converter.BlocksOptions.TypeOfBlocks as block


class PriorityListOfElements(object):
    def __init__(self, json_file):
        self.json_file = json_file
        self.list_of_elements = list()  # lista ze wszystkimi elementami "bloczkami"
        self.generate_list_of_elements()
        # self.priority_list = self.generate_priority_list()
        # self.print_priority_list()

    def get_list_of_elements(self):
        return self.list_of_elements

    def print_priority_list(self):
        for e in self.priority_list:
            print(e)

    def generate_list_of_elements(self):
        for target in self.json_file["targets"]:
            for element in target['blocks']:
                self.list_of_elements.append({'id': element, 'prev_element': target['blocks'][element]['parent'],
                                              'next_element': target['blocks'][element]['next'],
                                              'val': target['blocks'][element]})

    def generate_priority_list(self):
        priority_list = list()
        for e in self.list_of_elements:
            if e['prev_element'] in priority_list:
                priority_list.insert(priority_list.index(e['prev_element']) + 1, e['id'])
            elif e['prev_element'] is None:
                priority_list.insert(0, e['id'])
            else:
                priority_list.insert(len(priority_list), e['id'])
        return self.add_options_to_block(priority_list)

    def find_next_element(self, e_id):
        for e in self.list_of_elements:
            if e['id'] == e_id:
                return e['next_element']

    def find_prev_element(self, e_id):
        for e in self.list_of_elements:
            if e['id'] == e_id:
                return e['prev_element']

    def add_options_to_block(self, priority_list):
        output_code = list()
        for e in priority_list:
            element_name = self.find_element_in_list_of_elements(e)
            type_of_block, additional_options = self.find_conditions(e)
            next_element = self.find_next_element(e)
            prev_element = self.find_prev_element(e)
            output_code.append(
                {'id': e, 'element_name': element_name, 'type_of_block': type_of_block, 'next_element': next_element,
                 'prev_element': prev_element,'additional_options': additional_options})
        return output_code

    def get_loop_options(self, element):
        return 'loop_block', {'substack': element['SUBSTACK'][1], 'condition': [element['CONDITION'][1]]}

    def get_math_operation_options(self, element):
        return 'math_operation', {'variable_name': element['NUM1'][1][1], 'variable_value': element['NUM2'][1][1]}

    def get_logical_options(self, element):
        if len(element) == 1:
            return 'not_block', {'block_right': element['OPERAND'][1]}
        else:
            if isinstance(element['OPERAND1'][1], list) and isinstance(element['OPERAND2'][1], list):
                return 'logical_block', {'variable_name': element['OPERAND1'][1][1], 'variable_value': element['OPERAND2'][1][1]}
            elif isinstance(element['OPERAND1'][1], str):
                return 'logical_block', {'block_name': element['OPERAND1'][1], 'value': element['OPERAND2'][1][1]}
            return 'and_or_block', {'block_left': element['OPERAND1'][1], 'block_right': element['OPERAND2'][1]}

    def get_variable_field(self, element):
        return 'variable_block', {'name': element['fields']['VARIABLE'][0],
                                  'value': element['inputs']['VALUE'][1][1]}

    def get_motion_field(self, element):
        return 'motion_block', {'degrees': element['DEGREES'][1][1]}

    def find_conditions(self, e_id):
        for e in self.list_of_elements:
            if e['id'] == e_id:
                if len(e['val']['inputs']) > 0:
                    if e['val']['opcode'] in block.type_of_logical_field:
                        return self.get_logical_options(e['val']['inputs'])
                    elif e['val']['opcode'] in block.type_of_math_operation_field:
                        return self.get_math_operation_options(e['val']['inputs'])
                    elif e['val']['opcode'] in block.type_of_variable_field:
                        return self.get_variable_field(e['val'])
                    elif e['val']['opcode'] in block.type_of_loop_field:
                        return self.get_loop_options(e['val']['inputs'])
                    elif e['val']['opcode'] in block.type_of_motion_field:
                        return self.get_motion_field(e['val']['inputs'])
                    else:
                        return 'other_block', None
                else:
                    if e['val']['opcode'] in block.type_of_event_field:
                        return 'event_block', None
        return 'other_block', None

    def find_element_in_list_of_elements(self, e_id):
        for e in self.list_of_elements:
            if e['id'] == e_id:
                return e['val']['opcode']
        return None

    def get_priority_list(self):
        return self.priority_list
