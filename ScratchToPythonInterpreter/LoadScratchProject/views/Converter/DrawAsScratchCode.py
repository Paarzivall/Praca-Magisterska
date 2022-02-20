from LoadScratchProject.views.Converter.BlocksOptions.BlockOptionsScratch import val_of_blocks
from LoadScratchProject.views.Converter.BlocksOptions.mathop_options import mathop_options
import LoadScratchProject.views.Converter.BlocksOptions.TypeOfBlocks as TypeOfBlocks
from LoadScratchProject.views.Converter.ScratchBlockGenerator import IdGenerator, AdditionalOptionsGenerator
from LoadScratchProject.views.Converter.ScratchBlockGenerator.Block import Block
from LoadScratchProject.views.Converter.ScratchBlockGenerator.OutputBlock import OutputBlock

dict_of_left_elements = {'VARIABLE': [0, 1], 'CONDITION': [1], 'OPERAND1': [1, 1], 'DEGREES': [1, 1], 'OPERAND': [1],
                         'NUM1': [1, 1], 'TIMES': [1, 1], 'KEY_OPTION': [0], 'OPERATOR': [0], 'FROM': [1, 1],
                         'STRING1': [1, 1], 'LETTER': [1, 1], 'STEPS': [1, 1], 'MESSAGE': [1, 1], 'DURATION': [1, 1], 'STOP_OPTION': [1]}
dict_of_right_elements = {'OPERAND2': [1, 1], 'VALUE': [1, 1], 'NUM2': [1, 1], 'NUM': [1, 1], 'STRING': [1, 1], 'TO': [1, 1], 'STRING2': [1, 1], 'SECS': [1, 1]}
dict_of_child_elements = {'SUBSTACK': [1], 'SUBSTACK2': [1]}


class DrawAsScratchCode(object):
    def __init__(self, list_of_elements):
        self.list_of_elements = list_of_elements
        # print(list_of_elements)
        self.list_of_ids = self.generate_list_of_ids()
        self.list_of_child_elements = list()
        self.actual_element, self.list_of_blocks = self.generate_list_of_blocks()
        self.output_code = self.generate_output_code()
        self.scratch_code = self.generate_scratch_code()

    def generate_list_of_ids(self):
        list_of_ids = list()
        for e in self.list_of_elements:
            list_of_ids.append(e['id'])
        return list_of_ids

    def check_if_dict_exists(self, e, dict_to_check):
        if dict_to_check in e.keys():
            if len(e[dict_to_check]) > 0:
                return True
        return False

    def get_dict_field(self, dict_to_search, element_dict, l_e):
        try:
            if isinstance(element_dict[l_e][dict_to_search[l_e][0]], list):
                return element_dict[l_e][dict_to_search[l_e][0]][dict_to_search[l_e][1]]
            return element_dict[l_e][dict_to_search[l_e][0]]
        except IndexError:
            return element_dict[l_e][dict_to_search[l_e][0]]

    def get_left_value(self, e):
        if self.check_if_dict_exists(e['val'], 'inputs'):
            for l_e in dict_of_left_elements:
                if self.check_if_dict_exists(e['val']['inputs'], l_e):
                    return str(self.get_dict_field(dict_of_left_elements, e['val']['inputs'], l_e))
        if self.check_if_dict_exists(e['val'], 'fields'):
            for l_e in dict_of_left_elements:
                if self.check_if_dict_exists(e['val']['fields'], l_e):
                    return str(self.get_dict_field(dict_of_left_elements, e['val']['fields'], l_e))
        return None

    def get_right_value(self, e):
        if self.check_if_dict_exists(e['val'], 'inputs'):
            for l_e in dict_of_right_elements:
                if self.check_if_dict_exists(e['val']['inputs'], l_e):
                    return str(self.get_dict_field(dict_of_right_elements, e['val']['inputs'], l_e))
        if self.check_if_dict_exists(e['val'], 'fields'):
            for l_e in dict_of_right_elements:
                if self.check_if_dict_exists(e['val']['fields'], l_e):
                    return l_e, str(self.get_dict_field(dict_of_right_elements, e['val']['fields'], l_e))
        return None

    def get_child_value(self, e):
        list_of_child = list()
        for x in dict_of_child_elements:
            if self.check_if_dict_exists(e['val'], 'inputs'):
                for l_e in dict_of_child_elements:
                    if self.check_if_dict_exists(e['val']['inputs'], l_e):
                        child = self.get_dict_field(dict_of_child_elements, e['val']['inputs'], l_e)
                        if child not in list_of_child:
                            list_of_child.append(child)
            if self.check_if_dict_exists(e['val'], 'fields'):
                for l_e in dict_of_child_elements:
                    if self.check_if_dict_exists(e['val']['fields'], l_e):
                        child = self.get_dict_field(dict_of_child_elements, e['val']['fields'], l_e)
                        if child not in list_of_child:
                            list_of_child.append(child)
        if len(list_of_child) == 0:
            return None
        elif len(list_of_child) == 1:
            return list_of_child[0]
        else:
            return list_of_child

    def generate_list_of_blocks(self):
        list_of_blocks = list()
        actual_element = None
        for e in self.list_of_elements:
            block_id = e['id']
            opcode = e['val']['opcode']
            next_element = e['next_element']
            previous_element = e['prev_element']
            child = self.get_child_value(e)
            left_value = self.get_left_value(e)
            right_value = self.get_right_value(e)
            # if opcode == 'control_if_else':
            #    print(block_id, opcode, next_element, previous_element, child, left_value, right_value)
            block = Block(block_id, opcode, next_element, previous_element, child, left_value, right_value)
            if previous_element is None:
                actual_element = block
            list_of_blocks.append(block)
        return actual_element, list_of_blocks

    def find_new_actual_element(self, next_element_id):
        for element in self.list_of_blocks:
            if element.get_block_id() == next_element_id:
                return element

    def check_element_inside_other_element(self, value):
        if value in self.list_of_ids:
            self.list_of_ids.remove(value)
            return self.check_element_inside_other_element(self.find_new_actual_element(value))
        return value

    def get_value_of_block(self, value):
        if isinstance(value, str):
            return value
        else:
            if isinstance(self.check_element_inside_other_element(value), Block):
                try:
                    value.left_value = self.get_value_of_block(self.check_element_inside_other_element(value.left_value))
                    value.right_value = self.get_value_of_block(self.check_element_inside_other_element(value.right_value))
                except:
                    pass
                if value.opcode in ['operator_not', 'operator_mod', 'operator_random', 'operator_join', 'operator_contains', 'operator_letter_of']:
                    if value.opcode in ['operator_mod']:
                        return str(val_of_blocks[value.opcode]['text']) + '(' + str(value.left_value) + str(val_of_blocks[value.opcode]['text2']) + str(value.right_value) + ')'
                    elif value.opcode in ['operator_random', 'operator_join', 'operator_letter_of']:
                        return str(val_of_blocks[value.opcode]['text']) + str(value.left_value) + str(val_of_blocks[value.opcode]['text2']) + str(value.right_value)
                    elif value.opcode in ['operator_contains']:
                        return str(val_of_blocks[value.opcode]['text']) + str(value.left_value) + str(val_of_blocks[value.opcode]['text2']) + str(value.right_value) + str(val_of_blocks[value.opcode]['text3'])
                    return str(val_of_blocks[value.opcode]['text']) + '(' + str(value.left_value) + str(val_of_blocks[value.opcode]['text2']) + ')'
                elif value.opcode in ['operator_round', 'operator_length']:
                    return '(' + str(val_of_blocks[value.opcode]['text']) + str(value.right_value) + ')'
                elif value.opcode in ['operator_mathop']:
                    return mathop_options[value.left_value] + '(' + str(value.right_value) + ')'
            return str(value.left_value) + str(val_of_blocks[value.opcode]['text']) + str(value.right_value)

    def get_left_and_right_value(self):
        left_value = None
        right_value = None
        if self.actual_element.left_value is not None:
            left_value = self.check_element_inside_other_element(self.actual_element.left_value)
            left_value = self.get_value_of_block(left_value)
        if self.actual_element.right_value is not None:
            right_value = self.check_element_inside_other_element(self.actual_element.right_value)
            right_value = self.get_value_of_block(right_value)
        return left_value, right_value

    def generate_text_to_block(self, left_value, right_value, block_value, block_id, opcode):
        if block_id in self.list_of_child_elements:
            additional_text = '\t'
        else:
            additional_text = ''
        if opcode in ['looks_sayforsecs', 'looks_thinkforsecs']:
            return additional_text + block_value['text'] + left_value + block_value['text2'] + right_value + block_value['text3']
        if right_value is None and left_value is not None:
            return additional_text + block_value['text'] + left_value + block_value['text2']
        elif right_value is not None and left_value is not None:
            return additional_text + block_value['text'] + left_value + block_value['text2'] + right_value
        elif right_value is None and left_value is None:
            return additional_text + block_value['text'] + block_value['text2']

    def generate_output_block_object(self):
        left_value, right_value = self.get_left_and_right_value()
        # print(self.actual_element.opcode, left_value, right_value)
        text_to_output = self.generate_text_to_block(left_value, right_value, val_of_blocks[self.actual_element.opcode], self.actual_element.block_id, self.actual_element.opcode)
        block = OutputBlock(self.actual_element.block_id, self.actual_element.opcode, text_to_output)
        return block

    def del_element(self):
        try:
            self.list_of_ids.remove(self.actual_element.block_id)
        except ValueError:
            pass

    def add_child_elements(self, output_code):
        self.list_of_child_elements.append(self.actual_element.child)
        self.actual_element = self.check_element_inside_other_element(self.actual_element.child)
        block = self.generate_output_block_object()
        output_code.append(block)
        while self.actual_element.next_element is not None:
            self.find_other_child_blocks()
            block = self.generate_output_block_object()
            output_code.append(block)
        return output_code

    def add_multiply_child_elements(self, output_code, act_elem):
        for child in self.actual_element.child:
            self.list_of_child_elements.append(child)
            self.actual_element = self.check_element_inside_other_element(child)
            block = self.generate_output_block_object()
            output_code.append(block)
            while self.actual_element.next_element is not None:
                self.find_other_child_blocks()
                block = self.generate_output_block_object()
                output_code.append(block)
            output_code.append(OutputBlock(act_elem.block_id, act_elem.opcode, val_of_blocks[act_elem.opcode]['text3']))
        return output_code

    def find_other_child_blocks(self):
        self.actual_element = self.find_new_actual_element(self.actual_element.get_next_element())
        self.list_of_child_elements.append(self.actual_element.block_id)
        self.actual_element = self.check_element_inside_other_element(self.actual_element.block_id)

    def generate_output_code(self):
        output_code = list()
        while len(self.list_of_ids) > 0:
            try:
                self.del_element()
                block = self.generate_output_block_object()
                output_code.append(block)
                act_elem = self.actual_element
                if self.actual_element.child is not None:
                    if isinstance(self.actual_element.child, str):
                        output_code = self.add_child_elements(output_code)
                    else:
                        output_code = self.add_multiply_child_elements(output_code, act_elem)
                else:
                    self.actual_element = self.find_new_actual_element(self.actual_element.get_next_element())
                    if self.actual_element.previous_element in self.list_of_child_elements:
                        self.list_of_child_elements.append(self.actual_element.block_id)
                self.actual_element = self.find_new_actual_element(act_elem.get_next_element())
            except AttributeError:
                break
        return output_code

    def generate_scratch_code(self):
        scratch_code = list()
        for block in self.output_code:
            opcode = block.opcode
            id = IdGenerator.IdGenerator(block.block_id).get_id()
            scratch_code.append({'id': id, 'opcode': opcode, 'text': block.text_value, 'background': val_of_blocks[opcode]['color'], 'class': self.add_class(block.block_id)})
        return scratch_code

    def add_class(self, block_id):
        if block_id in self.list_of_child_elements:
            return 'ml-5'
        return ''

    def get_scratch_code(self):
        return self.scratch_code
