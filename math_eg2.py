"""2 methods for finding the mean of n natural numbers"""
# 1st
ls=[]
num=int(input("Enter the number:"))
def mean (no):
    if num<=0:
        print("Input error")
    for i in range(1,no+1):
        ls.append(i)
        i=i+1
    return sum(ls)/no
        
    
# 2ed
def mean_n(num):
    if num>=0:
        total=(num*(num+1))/2
        mean=total/num
        return mean
    else:
        print("Input error")

a=mean(num)
print("Mean upto", num,"is: ",a)       
b=mean_n(num)
print(b)