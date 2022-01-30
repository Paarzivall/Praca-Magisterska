from LoadScratchProject.views.Converter.BlocksOptions.BlockOptionsScratch import val_of_blocks
import LoadScratchProject.views.Converter.BlocksOptions.TypeOfBlocks as TypeOfBlocks
from LoadScratchProject.views.Converter.ScratchBlockGenerator import IdGenerator, AdditionalOptionsGenerator


class DrawAsScratchCode(object):
    def __init__(self, priority_list):
        # print(priority_list)
        self.priority_list = priority_list
        self.scratch_code = list()
        self.draw_scratch_code()
        self.actual_tab = 0
        # print(self.scratch_code)

    def draw_scratch_code(self):
        for e in self.priority_list:
            id = self.get_id_of_block(e)
            element_name = self.get_element_name(e)
            type_of_block = self.get_type_of_block(e)
            next_element = self.get_next_element(e)
            prev_element = self.get_prev_element(e)
            additional_options = self.get_additional_options(e)
            tmp_scratch_code = self.generate_element(id, element_name, type_of_block, next_element, prev_element, additional_options)
            # print(tmp_scratch_code)
            self.scratch_code.append(tmp_scratch_code)

    def generate_element(self, id, element_name, type_of_block, next_element, prev_element, additional_options):
        # print(id, element_name, type_of_block, next_element, prev_element, additional_options)
        for element in val_of_blocks:
            if element == element_name:
                id = IdGenerator.IdGenerator(id).get_id()
                child = None
                substacks = None
                if type_of_block != 'logical_block': # z wyłączeniem bloków logicznych
                    if additional_options is not None:
                        if 'substack' not in additional_options and 'condition' not in additional_options: # z wyłączeniem pętli
                            additional_options = self.generate_additional_options(additional_options, element_name)
                        else:
                            substack = self.find_element_by_id(additional_options['substack'])
                            condition = self.find_element_by_id(additional_options['condition'][0])
                            # print(condition)
                            self.priority_list.remove(condition)
                            additional_options = self.generate_additional_options(additional_options, element_name)
                            child = self.generate_additional_options_for_loop(condition)
                            substacks = self.generate_substacks(substack)
                    else:
                        additional_options = self.generate_additional_options(additional_options, element_name)
                    additional_options['id'] = id
                    additional_options['child'] = child
                    additional_options['substacks'] = substacks
                    return additional_options

    def is_generated(self, id):
        for element in self.scratch_code:
            if element['id'] == id:
                return True
        return False

    def get_element_from_scratch_code(self, id):
        for element in self.scratch_code:
            if element['id'] == id:
                self.scratch_code.remove(element)
                return element

    def generate_substacks(self, substack):
        list_of_substacks = list()
        while True:
            if substack is not None:
                id = IdGenerator.IdGenerator(substack['id']).get_id()
                if self.is_generated(id):
                    list_of_substacks.append(self.get_element_from_scratch_code(id))
                else:
                    element = self.find_element_by_id(substack['id'])
                    additional_options = self.generate_additional_options(self.get_additional_options(element), self.get_element_name(element))
                    list_of_substacks.append(additional_options)
                self.remove_from_priority_list(substack)
                substack = self.find_element_by_id(substack['next_element'])
            else:
                break
        return list_of_substacks

    def remove_from_priority_list(self, element):
        self.priority_list.remove(element)

    def find_element_by_id(self, e_id):
        for e in self.priority_list:
            if e['id'] == e_id:
                return e

    def generate_additional_options_for_loop(self, condition):
        if condition['type_of_block'] == 'and_or_block':
            block_left = self.find_element_by_id(condition['additional_options']['block_left'])
            block_right = self.find_element_by_id(condition['additional_options']['block_right'])
            # self.remove_from_priority_list(block_left)
            # self.remove_from_priority_list(block_right)
            block_left = AdditionalOptionsGenerator.AdditionalOptionsGenerator(block_left['additional_options'], block_left['element_name']).get_additional_options()
            block_right = AdditionalOptionsGenerator.AdditionalOptionsGenerator(block_right['additional_options'], block_right['element_name']).get_additional_options()
            condition = AdditionalOptionsGenerator.AdditionalOptionsGenerator(condition['additional_options'], condition['element_name']).get_additional_options()
            additional_options_for_condition = {'text': block_left['text'] + condition['text'] + block_right['text'], 'style': condition['style'], 'class': ''}
        elif condition['type_of_block'] == 'not_block':
            block_right_tmp = self.find_element_by_id(condition['additional_options']['block_right'])
            block_right = AdditionalOptionsGenerator.AdditionalOptionsGenerator(block_right_tmp['additional_options'], block_right_tmp['element_name']).get_additional_options()
            text = block_right['text']
            if 'block_name' in block_right_tmp['additional_options'].keys():
                block_left = self.find_element_by_id(block_right_tmp['additional_options']['block_name'])
                self.remove_from_priority_list(block_left)
                block_left = AdditionalOptionsGenerator.AdditionalOptionsGenerator(block_left['additional_options'], block_left['element_name']).get_additional_options()
                text = block_left['text'] + text + block_right_tmp['additional_options']['value']
            condition = AdditionalOptionsGenerator.AdditionalOptionsGenerator(condition['additional_options'], condition['element_name']).get_additional_options()
            additional_options_for_condition = {'text': condition['text'] + text, 'style': condition['style'], 'class': ''}
        else:
            additional_options_for_condition = AdditionalOptionsGenerator.AdditionalOptionsGenerator(
                condition['additional_options'], condition['element_name']).get_additional_options()
        return additional_options_for_condition

    def generate_additional_options(self, additional_options, element_name):
        additional_options = AdditionalOptionsGenerator.AdditionalOptionsGenerator(additional_options, element_name).get_additional_options()
        return additional_options

    def get_additional_options(self, e):
        return e['additional_options']

    def get_prev_element(self, e):
        return e['prev_element']

    def get_next_element(self, e):
        return e['next_element']

    def get_type_of_block(self, e):
        return e['type_of_block']

    def get_element_name(self, e):
        return e['element_name']

    def get_id_of_block(self, e):
        return e['id']

    def get_scratch_code(self):
        return self.scratch_code
