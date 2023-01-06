from os import path, makedirs
import json

class ConfigStorage(object):
    def __init__(self, datafolder: str) -> None:
        self.datafolder = datafolder
        self.connections = {}
        self.victims = {
            "unique": {},
            "groups": {}
        }
        self.templates = {}

        if not path.isdir(datafolder):
            makedirs(datafolder)
            self.write()
        else:
            self.read()
    
    def write(self):
            with open(path.join(self.datafolder, 'connections.json'), 'w') as f:
                json.dump(self.connections, f)
            
            with open(path.join(self.datafolder, 'victims.json'), 'w') as f:
                json.dump(self.victims, f)
            
            with open(path.join(self.datafolder, 'templates.json'), 'w') as f:
                json.dump(self.templates, f)

    def read(self):
            with open(path.join(self.datafolder, 'connections.json'), 'r') as f:
                self.connections = json.load(f)
            
            with open(path.join(self.datafolder, 'victims.json'), 'r') as f:
                self.victims = json.load(f)
            
            with open(path.join(self.datafolder, 'templates.json'), 'r') as f:
                self.templates = json.load(f)
