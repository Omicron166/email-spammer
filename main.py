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

    if command == 'template':

        if args[0] == 'list':
            # Print the available template names

            print('Templates:')
            for template in storage.templates.keys():
                print('\t' + template)

        elif args[0] == 'show':
            if not storage.templates.get(args[1]):
                print(f'[!] Template {args[1]} not found')
                continue
            print(storage.templates[args[1]])

        elif args[0] == 'import':
            # Import a template from a file
            if isfile(args[1]):

                with open(args[1]) as f:
                    template = ''.join(f.readlines())

                # IDEA: check if args[2] exists and use it as filename
                name = input('Template name: ')

                # Check if already exists a template
                if storage.templates.get(name) != None:
                    print(f'[!] Template {name} already exists')
                    # Ask for an overwrite
                    choice = input('Do you want to overwrite it? y/n: ').lower()
                    if choice == 'n' or choice == 'no':
                        print('[i] Canceled')
                        continue
                
                # Print the template options
                print('Template options:')
                for option in Template(template).settings:
                    print('\t' + option)

                # Write the template in the storage
                storage.templates[name] = template
                storage.write()
                print(f'Template {name} imported succesfully')
            else:
                print(f'[!] Error, {args[1]} is not a file')

        elif args[0] == 'export':
            # Export a template
            
            # Check if the template exists
            if not storage.templates.get(args[1]):
                print(f'[!] Template {args[1]} not found')
                continue
            
            # IDEA: check if args[2] exists and use it as filename
            filename = input('filename: ')
            print('[i] Writing template')

            with open(filename, 'w') as f:
                f.write(storage.templates[args[1]])
            # ToDo: Handle file write exceptions
            print('[i] Template exported successfully')
        
        elif args[0] == 'remove':
            # Delete a template

            # Check if the template exists
            if not storage.templates.get(args[1]):
                print(f'[!] Template {args[1]} not found')
                continue

            # Delete the template and write the storage
            storage.templates.pop(args[1])
            storage.write()
        
