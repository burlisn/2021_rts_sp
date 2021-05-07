class Test:
    def __init__(self):
        self.y = 5

def changes(test):
    test.y += 1

s = Test()
p = Test()
d = Test()

changes(s)


print(s.y, p.y, d.y)
