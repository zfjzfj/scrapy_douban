def foo(s):
    n = int(s)
    assert n != 0, 'n is zero!'
    return 10/n

foo('3')
foo('2')
foo('1')
foo('0')
