from LoadScratchProject.views.ConverterScratchToPython.BlocksFinders.VariablesFinder import VariablesFinder

global val_of_blocks
val_of_blocks = {
        'event_whenflagclicked': {
            'color': '#ffbf00',
            'text': 'Kiedy kliknięto',
        },
        'data_setvariableto': {
            'color': '#ff8c1a',
            'text': 'ustaw',
        },
        'control_repeat_until': {
            'color': '#ffab19',
            'text': 'powtarzaj aż',
        },
        'motion_turnright': {
            'color': '#4c97ff',
            'text': 'obróć w prawo o',
        },
        'operator_gt': {
            'color': '#59c059',
            'text': '[var] > [val]',
        },
        'operator_lt': {
            'color': '#59c059',
            'text': '[var] > [val]',
        },
        'data_changevariableby': {
            'color': '#ff8c1a',
            'text': 'zmień',
        },
        'data_showvariable': {
            'color': '#ff8c1a',
            'text': 'pokaż zmienną ',
        },
        'control_if': {
            'color': '#ffab19',
            'text': 'jeżeli',
        },
    }


class ConverterScratchToPython(object):
    type_of_logical_field = ['operator_gt', 'operator_lt']
    type_of_variable_field = ['data_setvariableto', 'data_changevariableby']
    type_of_loop_field = ['control_repeat_until', 'control_if']
    type_of_motion_field = ['motion_turnright']
    type_of_event_field = ['event_whenflagclicked']

    def __init__(self, priority_list):
        self.priority_list = priority_list
        self.scratch_code = list()
        self.draw_scratch_code()

    def draw_scratch_code(self):
        for e in self.priority_list:
            if e['val']['opcode'] in self.type_of_logical_field:
                self.scratch_code[len(self.scratch_code) - 1]['child'] = {'style': 'background-color:' + val_of_blocks[e['val']['opcode']]['color']}
                self.scratch_code[len(self.scratch_code) - 1]['text'] += self.generate_text_to_block(e, val_of_blocks[e['val']['opcode']]['text'])
            else:
                text_to_block = self.generate_text_to_block(e, val_of_blocks[e['val']['opcode']]['text'])
                optional_style = self.check_if_block_is_in_loop(e['id'])
                self.scratch_code.append({'id': e['id'], 'type_of_block': e['val']['opcode'], 'style': 'background-color:' + val_of_blocks[e['val']['opcode']]['color'] + ';height:100px', 'class': 'col-6 mt-1 rounded-3 ' + optional_style, 'text': text_to_block})

    def check_if_block_is_in_loop(self, e_id):
        for e in self.priority_list:
            if e['val']['opcode'] in self.type_of_loop_field:
                if e['val']['inputs']['SUBSTACK'][1] == e_id:
                    return 'ml-5'
                el = self.find_element(e_id)
                if el['prev_element'] == e['val']['inputs']['SUBSTACK'][1]:
                    return 'ml-5'
        return ''

    def find_element(self, value):
        for e in self.priority_list:
            if e['id'] == value:
                return e

    def generate_text_to_block(self, e, default_text):
        if e['val']['opcode'] in self.type_of_logical_field:
            return self.add_logical_text(e)
        elif e['val']['opcode'] in self.type_of_variable_field:
            return self.add_variable_text(e, default_text)
        elif e['val']['opcode'] in self.type_of_motion_field:
            return self.add_motion_text(e, default_text)
        return default_text

    def add_motion_text(self, e, default_text):
        return default_text + " " + e['val']['inputs']['DEGREES'][1][1] + " stopni"

    def add_variable_text(self, e, default_text):
        return default_text + " " + e['val']['fields']['VARIABLE'][0] + " na " + e['val']['inputs']['VALUE'][1][1]

    def add_logical_text(self,e):
        return " " + e['val']['inputs']['OPERAND1'][1][1] + " " + self.get_type_of_logical(e['val']['opcode']) + " " + e['val']['inputs']['OPERAND2'][1][1]

    def get_type_of_logical(self, type_of_block):
        if type_of_block == 'operator_gt':
            return '>'
        elif type_of_block == 'operator_lt':
            return '<'

    def get_scratch_code(self):
        return self.scratch_code
