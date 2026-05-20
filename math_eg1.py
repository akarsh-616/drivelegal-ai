#Collatz Conjecture
#num=5476377146882523136
#num=1770887431076116955137
num = int(input("Enter any number:"))
count=0
sequence=[num]
while num != 1:
    if num % 2 == 0:
       num = num * (1/2)
    else:
        num = 3 * num + 1
    sequence.append(num)
    count += 1

print("It took",count,"steps to reach 1.")
print("Sequence",sequence)