class Block(object):
    def __init__(self, block_id=None, opcode=None, next_element=None, previous_element=None, child=None, left_value=None, right_value=None):
        self.block_id = block_id
        self.opcode = opcode
        self.next_element = next_element
        self.previous_element = previous_element
        self.child = child
        self.left_value = left_value
        self.right_value = right_value

    def get_block_id(self):
        return self.block_id

    def get_opcode(self):
        return self.opcode

    def get_next_element(self):
        return self.next_element

    def get_previous_element(self):
        return self.previous_element

    def get_child(self):
        return self.child

    def get_left_value(self):
        return self.left_value

    def get_right_value(self):
        return self.right_value

    def __str__(self):
        return self.block_id + " " + self.opcode + " " + self.left_value