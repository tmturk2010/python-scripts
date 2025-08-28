n1 = int(input("Lütfen ilk numarayı girin: "))
n2 = int(input("Lütfen ikinci numarayı girin: "))
op = str(input("Lütfen yapacağınız işlemi yazınız (+, -, *, /): "))
if op == ("+"):
     print(n1 + n2)
elif op == ("-"):
    print(n1 - n2)
elif op == ("*"):
    print(n1 * n2)
elif op == ("/"):
    print(n1 / n2)
else:
    print("Hatalı tuşlama yaptınız")