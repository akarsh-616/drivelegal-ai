""""For finding C(n,r) for n and r for Z+ve"""
import math as mt
num=int(input("Enter n:"))
t=int(input("Enter r:"))
def combination(n,r):
    if n<0 or r<0 or r>n:
        print("Input error")

    else:
        print(f"The value of C({n}:{r}) is equal: ", ((mt.factorial(n))/(mt.factorial(r)*mt.factorial(n-r))))

a=combination(num,t)
