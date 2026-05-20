""""For finding median of n natural terms"""

num=int(input("Enter the number:"))
def median(num):
    if num<=0:
        print("Input error")
    elif num % 2 == 0 :
        print(f"Median of {num} natural numbers is", ((num/2)+((num+1)/2))/2)
    else:
        print(f"Median of {num} natural numbers is", ((num+1)/2))

a=median(num)