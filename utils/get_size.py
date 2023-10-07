def get_size() -> int:
    try:
        size = int(input('Number of varibales?> '))
    except EOFError:
        print('Bye')
        quit(0)
    except ValueError:
        print('Invalid variable number')
        return get_size()
    except KeyboardInterrupt:
        quit(0)
    return size
