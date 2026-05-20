
import random
print("Enter \n 'r' for rock \n 'p' for paper \n 's' for sisors") 
while True:
    inp=input ("Enter: ")
    list=["r","s","p"]
    sel= random.choice(list)
    if inp==sel:
            print(f"Tie computer has selected {sel} too.")
    elif sel=="P" and inp=="s":
            print(f"You win , computer has selected {sel}.")
    elif sel=="P" and inp=="r":
            print(f"You loss , computer has selected {sel}.")

    elif sel=="r" and inp=="s":
            print(f"You loss , computer has selected {sel}.")

    elif sel=="r" and inp=="p":
            print(f"You win , computer has selected {sel}.")

    elif sel=="r" and inp=="s":
            print(f"You loss , computer has selected {sel}.")

    elif sel=="s" and inp=="p":
            print(f"You loss , computer has selected {sel}.")

    elif sel=="s" and inp=="r":
            print(f"You win , computer has selected {sel}.")

    else:
            print(f"You has selected an invalid term -  {inp} .")

    