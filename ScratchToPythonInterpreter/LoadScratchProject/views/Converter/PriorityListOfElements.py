class PriorityListOfElements(object):
    type_of_logical_field = ['operator_gt', 'operator_lt']
    type_of_variable_field = ['data_setvariableto', 'data_changevariableby']
    type_of_loop_field = ['control_repeat_until', 'control_if']
    type_of_motion_field = ['motion_turnright']
    type_of_event_field = ['event_whenflagclicked']

    def __init__(self, json_file):
        self.json_file = json_file
        self.list_of_elements = list() # lista ze wszystkimi elementami "bloczkami"
        self.generate_list_of_elements()
        # listy pomocnicze do generowania priority listy
        self.list_of_logical = list()
        self.list_of_variable = list()
        self.list_of_loop = list()
        self.list_of_motion = list()
        self.list_of_event = list()
        self.list_of_other = list()
        self.manage_element_to_correct_type()
        self.count_of_elements = self.calculate_count_of_all_elements()
        self.priority_list = self.generate_priority_list()

    def calculate_count_of_all_elements(self):
        return len(self.list_of_logical) + len(self.list_of_variable) + len(self.list_of_loop) + \
               len(self.list_of_motion) + len(self.list_of_event) + len(self.list_of_other)

    def generate_list_of_elements(self):
        for target in self.json_file["targets"]:
            for element in target['blocks']:
                self.list_of_elements.append({'id': element, 'prev_element': target['blocks'][element]['parent'],
                                              'next_element': target['blocks'][element]['next'],
                                              'val': target['blocks'][element]})

    def manage_element_to_correct_type(self):
        for e in self.list_of_elements:
            self.set_to_correct_type(e)

    def set_to_correct_type(self, e):
        if e['val']['opcode'] in self.type_of_logical_field:
            self.list_of_logical.append(e)
        elif e['val']['opcode'] in self.type_of_variable_field:
            self.list_of_variable.append(e)
        elif e['val']['opcode'] in self.type_of_loop_field:
            self.list_of_loop.append(e)
        elif e['val']['opcode'] in self.type_of_motion_field:
            self.list_of_motion.append(e)
        elif e['val']['opcode'] in self.type_of_event_field:
            self.list_of_event.append(e)
        else:
            self.list_of_other.append(e)

    def append_to_priority_list(self, value):
        for e in self.list_of_elements:
            if e['id'] == value:
                return e

    def find_first_element(self, ):
        priority_list = list()
        for e in self.list_of_elements:
            if e['prev_element'] is None:
                priority_list.append(e)
                self.list_of_elements.remove(e)
        return priority_list

    def generate_priority_list(self):
        priority_list = self.find_first_element()
        while len(priority_list) != self.count_of_elements:
            e = priority_list[len(priority_list) - 1]
            if e in self.list_of_loop:
                if e['val']['inputs']['CONDITION'] is not None:
                    new_e = self.append_to_priority_list(e['val']['inputs']['CONDITION'][1])
                    self.list_of_elements.remove(new_e)
                    priority_list.append(new_e)
                if e['val']['inputs']['SUBSTACK'] is not None:
                    new_e = self.append_to_priority_list(e['val']['inputs']['SUBSTACK'][1])
                    self.list_of_elements.remove(new_e)
                    priority_list.append(new_e)
            else:
                if e['next_element'] is not None:
                    element = self.append_to_priority_list(e['next_element'])
                    self.list_of_elements.remove(element)
                    priority_list.append(element)
                else:
                    if len(self.list_of_elements) > 0 and e['next_element'] is None:
                        for el in self.list_of_elements:
                            if el in self.list_of_loop:
                                priority_list.append(el)
                                if el['val']['inputs']['CONDITION'] is None:
                                    new_e = self.append_to_priority_list(el['val']['inputs']['CONDITION'][1])
                                    self.list_of_elements.remove(new_e)
                                    priority_list.append(new_e)
                                if el['val']['inputs']['SUBSTACK'] is None:
                                    new_e = self.append_to_priority_list(el['val']['inputs']['SUBSTACK'][1])
                                    self.list_of_elements.remove(new_e)
                                    priority_list.append(new_e)
        return priority_list

    def get_priority_list(self):
        return self.priority_list
