import dictionary

# main loop

dictionary.initialize()

while True:
    s = input('dict: ')
    if s == 'quit()':
        dictionary.quit_browser()
        break

    parts = s.split(' ')
    if len(parts) != 2:
        print('invalid syntax\n')
        continue

    command = parts[0]
    word = parts[1]

    if ';' in word:
        print('no results found for ' + word + '\n')
        continue

    if command == 'def':
        out = dictionary.definition(word, 2, 2)
        for o in out: print(o)
    elif command == 'syn':
        out = dictionary.synonym(word, 3)
        for o in out: print(o)
    else:
        print('unknown command')

    print('')