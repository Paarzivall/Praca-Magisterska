from LoadScratchProject.views.Converter.BlocksOptions.BlockOptionsScratch import val_of_blocks


class AdditionalOptionsGenerator(object):
    def __init__(self, additional_options, element_name):
        self.additional_options = additional_options
        self.element_name = element_name
        self.categirize_to_correct_type()

    def categirize_to_correct_type(self):
        text_to_dict = self.additional_options if self.element_name not in val_of_blocks else val_of_blocks[self.element_name]['text']
        background_color = val_of_blocks[self.element_name]['color']
        if self.additional_options is not None:
            if 'variable_name' in self.additional_options and 'variable_value' in self.additional_options:
                text_to_dict = self.additional_options['variable_name'] + val_of_blocks[self.element_name]['text'] + \
                               self.additional_options['variable_value']
            elif 'name' in self.additional_options and 'value' in self.additional_options:
                text_to_dict = val_of_blocks[self.element_name]['text'] + self.additional_options['name'] + ' na ' + self.additional_options['value']
            elif 'degrees' in self.additional_options:
                text_to_dict = val_of_blocks[self.element_name]['text'] + self.additional_options['degrees']
            elif 'substack' in self.additional_options and 'condition' in self.additional_options:
                text_to_dict = val_of_blocks[self.element_name]['text']
        self.additional_options = {'text': text_to_dict, 'style': background_color, 'class': ''}

    def get_additional_options(self):
        return self.additional_options
