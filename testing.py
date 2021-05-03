class My_test:
    def __init__(self, x):
        self.x = x
        self.y = 5

list1 = []
list2 = []

a = My_test(5)
list1.append(a)
list2.append(a)
list2[0].x = 22
print(list1[0].x)
