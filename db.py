
import pandas as pd
import numpy as np
from PIL import Image
import json
import os

class RolodexDirector:
    def __init__(self, pth, file_name='data.json'):
        self.local_pth = pth
        self.file_path = os.path.join(pth, file_name)
        self.data = []
        
        if not os.path.exists(pth):
            os.makedirs(pth)
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        else:
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)

    def append_data(self, id, photo_pth, name, relation, memory, log=None):
        new_entry = {
            'id': id,
            'picture': photo_pth,
            'name': name,
            'relation': relation,
            'memory': memory, 
            'log_ids': [log] if log else []
        }

        self.data.append(new_entry)
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)
        
        return new_entry

    def find_entries(self, property_name, value):
        matching_entries = [entry for entry in self.data if entry.get(property_name) == value]
        return matching_entries

# Example usage
PATH = 'faces/'
rolodex = RolodexDirector(pth=PATH)
