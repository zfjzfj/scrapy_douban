
# simple math expression parser

def lexer(s):
    '''token generator, yields a list of tokens'''
    yield s

if __name__ == '__main__':
    for token in lexer("1 + (2 - 3) * 456"):
        print token
