#!/usr/bin/python
class FilterModule(object):
    def filters(self):
        return {
            'sort_dict_bykey': self.sort_dict_bykey
        }
    def sort_dict_bykey(self,dict_input):
        dict_input.sort(key=lambda d: sorted(d.keys())[0])
        return dict_input

