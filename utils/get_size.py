def get_size() -> int:
    try:
        size = int(input('Number of varibales?> '))
    except EOFError:
        print('Bye')
        quit(0)
    except ValueError:
        print('Invalid elements size')
        return get_size()
    return size