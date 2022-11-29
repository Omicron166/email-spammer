from core.config import ConfigStorage
from os.path import isfile
from core.templates import Template

# Initializate the data storage
storage = ConfigStorage('./.data')

while True:
    cmd = input('email-spammer> ')
    args = cmd.split()
    command = args.pop(0)
    if command == '': continue
