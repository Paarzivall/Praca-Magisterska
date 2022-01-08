from zipfile import ZipFile
import json


class Files(object):
    def __init__(self, file):
        self.zip_file = file
        self.json_file = self.extract_json_file_from_zip()

    def extract_json_file_from_zip(self):
        with ZipFile(self.zip_file, 'r') as zip:
            first = zip.infolist()[0]
            with zip.open(first, "r") as json_file:
                json_content = json.load(json_file)
        return json_content

    def get_json_file(self):
        return self.json_file
