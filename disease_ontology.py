import json

class DiseaseOntology():
    def __init__(self):
        self.id = None
        self.name = ""
        self.definition = ""
        self.synonym = []
        self.parents = []
        self.ancestors = []
        self.children = []
        self.deprecated = 0 # False

    def __repr__(self):
        '''
        temp_dict = {}
        temp_dict['id'] = self.id
        temp_dict['name'] = self.name
        temp_dict['definition'] = self.definition
        temp_dict['synonym'] = self.synonym
        temp_dict['parents'] = self.parents
        temp_dict['ancestors'] = self.ancestors
        temp_dict['children'] = self.children
        temp_dict['deprecated'] = (self.deprecated == 1)
        return repr(temp_dict)
        '''
        # convert to json
        return repr(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]