from LoadScratchProject.views.ConverterScratchToPython.BlocksFinders.VariablesFinder import VariablesFinder

global val_of_blocks
val_of_blocks = {
        'event_whenflagclicked': {
            'color': 'pink',
            'text': 'Kiedy kliknięto',
        },
        'data_setvariableto': {
            'color': 'orange',
            'text': 'ustaw [var] na [val]',
        },
        'control_repeat_until': {
            'color': 'yellow',
            'text': 'powtarzaj aż',
        },
        'motion_turnright': {
            'color': 'blue',
            'text': 'obróć w prawo o ',
        },
        'operator_gt': {
            'color': 'green',
            'text': '[var] > [val]',
        },
        'operator_lt': {
            'color': 'green',
            'text': '[var] > [val]',
        },
        'data_changevariableby': {
            'color': 'orange',
            'text': 'zmień [var] o [val]',
        },
        'data_showvariable': {
            'color': 'orange',
            'text': 'pokaż zmienną ',
        },
        'control_if': {
            'color': 'orange',
            'text': 'jeżeli coś to coś ',
        },
    }


class ConverterScratchToPython(object):

    def __init__(self, json_file):
        self.json_file = json_file
        self.list_of_variables = VariablesFinder(self.json_file, 'data_setvariableto').get_list_of_elements()
        #print(self.list_of_variables)
        self.list_of_elements = list()
        self.priority_list = list()
        self.generate_list_of_elements()
        self.generate_priority_list()
        self.list_of_logical = list()
        self.generate_list_of_logical()
        self.scratch_code = list()
        self.draw_scratch_code()

    def draw_scratch_code(self):
        for p_e in self.priority_list:
            for e in self.list_of_elements:
                if p_e == e['id']:
                    self.scratch_code.append({'id': e['id'], 'type_of_block': e['val']['opcode'], 'style': 'background-color:' + val_of_blocks[e['val']['opcode']]['color'] + ';height:100px', 'class': 'col-6 mt-1', 'text': val_of_blocks[e['val']['opcode']]['text']})
        self.add_logical()
        self.add_variables()
        self.add_turning()
        self.add_change_variable_field()

    def add_change_variable_field(self):
        for e in self.scratch_code:
            if e['type_of_block'] == 'data_changevariableby':
                for element in self.list_of_elements:
                    if e['id'] == element['id']:
                        e['text'] = 'zmień ' + element['val']['fields']['VARIABLE'][0] + ' o ' + element['val']['inputs']['VALUE'][1][1]

    def add_turning(self):
        for e in self.scratch_code:
            if e['type_of_block'] == 'motion_turnright':
                for element in self.list_of_elements:
                    if e['id'] == element['id']:
                        e['text'] += element['val']['inputs']['DEGREES'][1][1] + ' stopni'

    def add_variables(self):
        for e in self.scratch_code:
            for var in self.list_of_variables:
                if e['id'] == var['id_of_variable']:
                    e['text'] = 'ustaw ' + var['name_of_variable'] + " na " + var['value_of_variable']

    def add_logical(self):
        tmp = ['control_repeat_until', 'control_if']
        for e in self.scratch_code:
            if e['type_of_block'] in tmp: #TODO sprawdzić resztę pętli jak coś dodać listę i zmienić '==' na 'in'
                for logical in self.list_of_logical:
                    if logical['parent'] == e['id']:
                        e['text'] += " " + logical['var'] + " " + self.get_type_of_logical(logical['type_of_block']) \
                                     + " " + logical['val_to']

    def get_type_of_logical(self, type_of_block):
        if type_of_block == 'operator_gt':
            return '>'
        elif type_of_block == 'operator_lt':
            return '<'
        elif type_of_block == 'control_if':
            return 'if'

    def generate_list_of_logical(self):
        list_of_operators = ['operator_gt', 'operator_lt']
        for e in self.list_of_elements:
            if e['id'] not in self.priority_list and e['val']['opcode'] in list_of_operators:
                self.list_of_logical.append({'id': e['id'], 'type_of_block': e['val']['opcode'],
                                             'parent': e['val']['parent'], 'var': e['val']['inputs']['OPERAND1'][1][1],
                                             'val_to': e['val']['inputs']['OPERAND2'][1][1]}) #TODO dodać jakieś wartości potrzebne
            elif e['id'] not in self.priority_list:
                print(e['id'], e['val']['opcode'])
                self.list_of_logical.append({'id': e['id'], 'type_of_block': e['val']['opcode'],
                                             'parent': e['val']['parent'], 'var': 'asd',
                                             'val_to': 'fgh'})

    def get_scratch_code(self):
        return self.scratch_code

    def generate_list_of_elements(self):
        for target in self.json_file["targets"]:
            for element in target['blocks']:
                self.list_of_elements.append({'id': element, 'prev_element': target['blocks'][element]['parent'], 'next_element': target['blocks'][element]['next'], 'val': target['blocks'][element]})
        # print(self.list_of_elements)

    def generate_priority_list(self):
        elements = self.list_of_elements
        # print(elements)
        self.priority_list.append(self.find_first_element(elements))
        while len(elements) - 1 > len(self.priority_list):
            id = self.find_element(elements, self.priority_list[len(self.priority_list) - 1])
            self.priority_list.append(id)
        # print(self.priority_list)

    def find_element(self, list_of_element, parent_element):
        for element in list_of_element:
            if element['val']['parent'] == parent_element:
                return element['id']

    def find_first_element(self, list_of_elements):
        for element in list_of_elements:
            if element['val']['parent'] is None:
                return element['id']
