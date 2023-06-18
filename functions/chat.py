import _collections_abc
from typing import Dict, List
from enum import Enum


#propertype.name for name, .value for value
class PropertyType(str, Enum):
    string = 'string'
    integer= 'integer'
    float= 'float'          #API docs don't specify this - could generate an error
 
class property():
   def __init__(self, name: str, type: PropertyType, description: str, required: bool=False, enum: List=[], default: str=None):
        self.name = name
        self.type = type
        self.description = description
        self.required = required
        self.enum = enum
        self.default = default
  

class properties(Dict):
    def add(self, item: property):
        if isinstance(item, property):
            super().__setitem__(item.name, {'type': item.type.value, 'description': item.description, 'required': item.required})
        else:
            raise ValueError('Must be type "property."')

        # add enumerators if passed
        if item.enum != None and len(item.enum) > 0:
            super().__getitem__(item.name)['enum'] = item.enum

        # default of property
        if item.default != None:
            super().__getitem__(item.name)['default'] = item.default       


class function():
    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description
        self.properties = properties() #if properties is None else properties
        self.properties_wo_required = {}
    def to_json(self):
        # create "required" list for chatcompletion
        self.required =  [k for k, v in self.properties.items() if v['required'] == True]

        #remove 'required' attribute from properties as it is a list of it's own
        for k, v in self.properties.items():
            self.properties_wo_required[k] = {m: v[m] for m in v.keys() - {'required'}}

        funct = {'name' : self.name, 
                 'description' : self.description, 
                 'parameters' : { 'type': 'object', 
                                'properties' : self.properties_wo_required },
                 'required' :  self.required
                 }
        return funct


# Security is always a concern when relying on a 3rd party to tell your code what to execute.
# By moving to a dictionary object from a simple list, we can subsequently "look up" the function 
# that chatGPT returns to confirm we should be considering executing it.
class functions(_collections_abc.MutableMapping):
    def __init__(self):
        super().__init__()
        self._dict = dict()

    def __getitem__(self, key):
        return self._dict.__getitem__(key)

    def __setitem__(self, key, value):
        self._dict.__setitem__(key, value)
        self._changed = True

    def __delitem__(self, key):
        self._dict.__delitem__(key)
        self._changed = True

    def __iter__(self):
        return self._dict.__iter__()

    def __len__(self):
        return self._dict.__len__()

    # ChatGPT is expecting an List. 
    def to_json(self):
        l = []
        for item in self._dict:
            l.append(self._dict[item].to_json())
        return l

# You could use a list base if you would like:
#class functions(_collections_abc.MutableSequence):
#    def __init__(self):
#        self.data = []

#    def __len__(self):
#        return len(self.data)

#    def __repr__(self):
#        return repr(self.data)

#    def __delitem__(self, index):
#        self.data.__delitem__(index)

#    def __setitem__(self, index, value):
#        self.data.__setitem__(index, value)

#    def insert(self, index, value):
#        self.data.insert(index, value)

#    def __getitem__(self, index):
#        return self.data.__getitem__(index)

#    def append(self, value):
#        self.data.append(value)

#    def to_json(self):
#        l = []
#        for i in self.data:
#            l.append(i.to_json())
#        return l



