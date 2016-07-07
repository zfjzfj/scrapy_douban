def grep(pattern):
    print("Searching for", pattern)
    while True:
        line = (yield)
        if pattern in line:
            print(line)


search = grep('love')
next(search)
#output: Searching for coroutine
search.send("I love you")
search.send("Don't you love me?")
search.send("I love coroutine instead!")
#output: I love coroutine instead!
search.close()
