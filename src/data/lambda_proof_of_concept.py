printers_1 = list()
for i in range(2):
    printers_1.append(lambda: print(i))

printers_1[0]()

printers_2 = list()
for i in range(2):
    printers_2.append((lambda x: lambda: print(x))(i))

printers_2[0]()
