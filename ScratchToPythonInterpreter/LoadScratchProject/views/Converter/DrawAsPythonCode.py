from LoadScratchProject.views.Converter.BlocksOptions.BlockOptionsPython import val_of_blocks
import LoadScratchProject.views.Converter.BlocksOptions.TypeOfBlocks as TypeOfBlocks


class DrawAsPythonCode(object):
    def __init__(self, priority_list):
        self.priority_list = priority_list
        self.python_code = list()
        self.draw_python_code()
        # print(self.python_code)

    def draw_python_code(self):

        added_text = list()
        for e in self.priority_list:
            if e['val']['opcode'] in TypeOfBlocks.type_of_logical_field:
                self.python_code[len(self.python_code) - 1]['code'] += self.generate_text_to_block(e, val_of_blocks[e['val']['opcode']]['code'])
            else:
                code_to_block = self.generate_text_to_block(e, val_of_blocks[e['val']['opcode']]['code'])
                optional_class = self.check_if_block_is_in_loop(e['id'])
                self.python_code.append({'id': self.generate_id(e['id']), 'type_of_block': e['val']['opcode'], 'class': 'block_of_python_code ' + optional_class, 'code': code_to_block})
            if val_of_blocks[e['val']['opcode']]['additional_code'] is not None and val_of_blocks[e['val']['opcode']]['additional_code'] not in added_text:
                added_text.append(val_of_blocks[e['val']['opcode']]['additional_code'])
                tmp = list(val_of_blocks[e['val']['opcode']]['additional_code'])
                for num, text in enumerate(tmp[::-1]):
                    if num == 1:
                        optional_class = 'ml-1'
                    else:
                        optional_class = 'ml-4'
                    text_to_add = {'id': self.generate_id(e['id']) + "", 'type_of_block': None,
                                   'code': text, 'class': 'block_of_python_code ' + optional_class}
                    self.python_code.insert(0, text_to_add)
            self.remove_necessary_class()

    def generate_id(self, e_id):
        output_id = ''
        for e in e_id:
            output_id += str(ord(e))
        return output_id

    def remove_necessary_class(self):
        for e in self.python_code:
            if e['type_of_block'] in TypeOfBlocks.type_of_event_field:
                e['class'] = 'ml-1 block_of_python_code'

    def add_optional_class(self, e_id):
        e = self.find_element(e_id)
        if e['val']['opcode'] in TypeOfBlocks.type_of_loop_field:
            return self.check_if_block_is_in_loop(e_id)
        elif e['val']['opcode'] in TypeOfBlocks.type_of_event_field:
            return ''

    def check_if_block_is_in_loop(self, e_id):
        for e in self.priority_list:
            if e['val']['opcode'] in TypeOfBlocks.type_of_loop_field:
                if e['val']['inputs']['SUBSTACK'][1] == e_id:
                    return 'ml-5'
                el = self.find_element(e_id)
                if el['prev_element'] == e['val']['inputs']['SUBSTACK'][1]:
                    return 'ml-5'
        return 'ml-4'

    def find_element(self, value):
        for e in self.priority_list:
            if e['id'] == value:
                return e

    def generate_text_to_block(self, e, default_text):
        if e['val']['opcode'] in TypeOfBlocks.type_of_logical_field:
            return self.add_logical_text(e)
        elif e['val']['opcode'] in TypeOfBlocks.type_of_variable_field:
            return self.add_variable_text(e, default_text)
        elif e['val']['opcode'] in TypeOfBlocks.type_of_motion_field:
            return self.add_motion_text(e, default_text)
        return default_text

    def add_motion_text(self, e, default_text):
        return default_text + e['val']['inputs']['DEGREES'][1][1] + ")"

    def add_variable_text(self, e, default_text):
        return e['val']['fields']['VARIABLE'][0] + " = " + e['val']['inputs']['VALUE'][1][1]

    def add_logical_text(self, e):
        return " " + e['val']['inputs']['OPERAND1'][1][1] + " " + self.get_type_of_logical(e['val']['opcode']) + " " + e['val']['inputs']['OPERAND2'][1][1]

    def get_type_of_logical(self, type_of_block):
        if type_of_block == 'operator_gt':
            return '>'
        elif type_of_block == 'operator_lt':
            return '<'
        elif type_of_block == 'operator_equals':
            return '=='
        return 'Nieznany'

    def get_python_code(self):
        return self.python_code