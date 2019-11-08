from sys import argv
from os import walk, system

# default root should be main directory
# where all .md files are stored
defaultRoot = ''

folders = {
    'example': 'C:/example-directory/',
}

if len(argv) == 1 and argv[0] != '-c':
    searchTerm = input('Enter search term: ')
    rootPath = defaultRoot
    run = True
elif len(argv) == 2 and argv[1] != '-c':
    if argv[1] == '-o':
        searchTerm = input('Enter search term: ')
        rootPath = defaultRoot
        run = True
    elif argv[1] == 'help':
        print('Usage: search.py[options](keyword folder/custom path)\nOptions:\n-o: allows user to open specific file\n-c: allows user to add custom path to search within')
        run = False
    else:
        searchTerm = argv[1]
        rootPath = defaultRoot
        run = True
elif len(argv) == 3 and argv[1] != '-c':
    if argv[1] == '-o':
        searchTerm = argv[2]
        rootPath = defaultRoot
    else:
        searchTerm = argv[1]
        rootPath = folders.get(argv[2])
    run = True
elif len(argv) == 4:
    if argv[1] == '-o':
        searchTerm = argv[2]
        rootPath = folders.get(argv[3])
        run = True
    elif argv[1] == '-c':
        searchTerm = argv[2]
        rootPath = argv[3]
        run = True
    else:
        run = False
        print('Error: incorrect input format')
elif argv[1] == '-o' and argv[2] == '-c':
    searchTerm = argv[3]
    rootPath = argv[4]
    run = True
else:
    print('Error: incorrect input format')
    run = False

if run == True:
    references = {}
    for path, dirs, files in walk(rootPath):
        for file in files:
            counter = 0
            if file.endswith('.md'):
                activeFile = open('{0}/{1}'.format(path, file), 'r', errors='ignore')
                searchLines = activeFile.readlines()
                activeFile.close()

                for line in searchLines:
                    if searchTerm.lower() in line.lower():
                        counter += 1
                        subPath = path.replace(rootPath, '') + '\\' + file
                        references[subPath] = counter

    for reference in references:
        print('{0} references to {1} found in: {2}'.format(references.get(reference), searchTerm, reference))

    if len(argv) != 1 and argv[1] == '-o':
        openFile = input('What file would you like to open? ')
        referenceKeys = references.keys()

        if openFile == 'nvm':
            pass
        else:
            for key in referenceKeys:
                if openFile in key:
                    fullPath = rootPath + key
                    print(fullPath)
                    system('atom {0}'.format(fullPath))
                    break
            else:
                print('Error: file not found')