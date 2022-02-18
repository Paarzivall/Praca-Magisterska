class OutputBlock(object):
    def __init__(self, block_id, opcode, text_value):
        self.block_id = block_id
        self.opcode = opcode
        self.text_value = text_value

    def get_text_value(self):
        return self.text_value

    def __str__(self):
        return self.text_value
        # return self.block_id + " " + self.opcode + " " + self.text_value
