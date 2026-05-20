""""On binomial expantion all type in one ,, one other for cofficent finding"""
import math as mt
A=int(input("Enter the first term:"))
N=int(input("Enter the power term:"))
"""" BINOMIAL EXPANTION OF (a+x)^n"""



import math as mt

def binomial(x, a, n):
    ls = ""
    if n <= 0:
        print("Input error")
    else:
        for k in range(n + 1):
            term = f"{mt.comb(n, k)} a^{n - k} x^{k}"
            if k > 0:
                ls += " + "
            ls += term
        return ls.replace("a", str(a))

a = binomial(2, A, N)
print(a)
