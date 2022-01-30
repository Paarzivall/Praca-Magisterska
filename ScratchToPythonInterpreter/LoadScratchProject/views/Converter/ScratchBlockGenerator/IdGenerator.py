class IdGenerator(object):
    def __init__(self, id):
        self.id = self.generate_id(id)

    def generate_id(self, e_id):
        output_id = ''
        for e in e_id:
            output_id += str(ord(e))
        return output_id

    def get_id(self):
        return self.id