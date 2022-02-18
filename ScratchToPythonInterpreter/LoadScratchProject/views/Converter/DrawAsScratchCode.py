from LoadScratchProject.views.Converter.BlocksOptions.BlockOptionsScratch import val_of_blocks
import LoadScratchProject.views.Converter.BlocksOptions.TypeOfBlocks as TypeOfBlocks
from LoadScratchProject.views.Converter.ScratchBlockGenerator import IdGenerator, AdditionalOptionsGenerator
from LoadScratchProject.views.Converter.ScratchBlockGenerator.Block import Block
from LoadScratchProject.views.Converter.ScratchBlockGenerator.OutputBlock import OutputBlock

dict_of_left_elements = {'VARIABLE': [0, 1], 'CONDITION': [1], 'OPERAND1': [1, 1], 'DEGREES': [1, 1], 'OPERAND': [1], 'NUM1': [1, 1]}
dict_of_right_elements = {'OPERAND2': [1, 1], 'VALUE': [1, 1], 'NUM2': [1, 1]}
dict_of_child_elements = {'SUBSTACK': [1]}


class DrawAsScratchCode(object):
    def __init__(self, list_of_elements):
        self.list_of_elements = list_of_elements
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
                    return self.get_dict_field(dict_of_left_elements, e['val']['inputs'], l_e)
        if self.check_if_dict_exists(e['val'], 'fields'):
            for l_e in dict_of_left_elements:
                if self.check_if_dict_exists(e['val']['fields'], l_e):
                    return self.get_dict_field(dict_of_left_elements, e['val']['fields'], l_e)
        return None

    def get_right_value(self, e):
        if self.check_if_dict_exists(e['val'], 'inputs'):
            for l_e in dict_of_right_elements:
                if self.check_if_dict_exists(e['val']['inputs'], l_e):
                    return self.get_dict_field(dict_of_right_elements, e['val']['inputs'], l_e)
        if self.check_if_dict_exists(e['val'], 'fields'):
            for l_e in dict_of_right_elements:
                if self.check_if_dict_exists(e['val']['fields'], l_e):
                    return l_e, self.get_dict_field(dict_of_right_elements, e['val']['fields'], l_e)
        return None

    def get_child_value(self, e):
        if self.check_if_dict_exists(e['val'], 'inputs'):
            for l_e in dict_of_child_elements:
                if self.check_if_dict_exists(e['val']['inputs'], l_e):
                    return self.get_dict_field(dict_of_child_elements, e['val']['inputs'], l_e)
        if self.check_if_dict_exists(e['val'], 'fields'):
            for l_e in dict_of_child_elements:
                if self.check_if_dict_exists(e['val']['fields'], l_e):
                    return self.get_dict_field(dict_of_child_elements, e['val']['fields'], l_e)
        return None

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
            # if opcode == 'operator_and':
            # print(block_id, opcode, next_element, previous_element, child, left_value, right_value)
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
                if value.opcode == 'operator_not':
                    return str(val_of_blocks[value.opcode]['text']) + str(value.left_value) + str(
                        val_of_blocks[value.opcode]['text2'])
            return str(value.left_value) + str(val_of_blocks[value.opcode]['text'] + str(value.right_value))

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

    def generate_text_to_block(self, left_value, right_value, block_value, block_id):
        if block_id in self.list_of_child_elements:
            additional_text = '\t'
        else:
            additional_text = ''
        if right_value is None and left_value is not None:
            return additional_text + block_value['text'] + left_value + block_value['text2']
        elif right_value is not None and left_value is not None:
            return additional_text + block_value['text'] + left_value + block_value['text2'] + right_value
        elif right_value is None and left_value is None:
            return additional_text + block_value['text'] + block_value['text2']

    def generate_output_block_object(self):
        left_value, right_value = self.get_left_and_right_value()
        text_to_output = self.generate_text_to_block(left_value, right_value, val_of_blocks[self.actual_element.opcode], self.actual_element.block_id)
        block = OutputBlock(self.actual_element.block_id, self.actual_element.opcode, text_to_output)
        return block

    def generate_output_code(self):
        output_code = list()
        while len(self.list_of_ids) > 0:
            try:
                block = self.generate_output_block_object()
                output_code.append(block)
                # print(block)
                if self.actual_element.child is not None:
                    self.list_of_child_elements.append(self.actual_element.child)
                    self.actual_element = self.check_element_inside_other_element(self.actual_element.child)
                else:
                    self.actual_element = self.find_new_actual_element(self.actual_element.get_next_element())
                    if self.actual_element.previous_element in self.list_of_child_elements:
                        self.list_of_child_elements.append(self.actual_element.block_id)
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
