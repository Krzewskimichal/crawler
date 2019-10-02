import csv
import sys

print("Search element by:\n"
      "1: name\n"
      "2: price\n"
      "3: brand\n"
      "4: model\n"
      "input number from 1 to 4")

#  input category to search
search = input(": ")

file = csv.reader(open("products.csv", "r"), delimiter=",")

#  print elements from products.csv file by "phrase" input
if search == "1":
    phrase = input("name: ")
    for row in file:
        if phrase in row:
            print(row)

elif search == "2":
    phrase = input("price: ")
    for row in file:
        if phrase in row:
            print(row)

elif search == "3":
    phrase = input("brand: ")
    for row in file:
        if phrase in row:
            print(row)

elif search == "4":
    phrase = input("model: ")
    for row in file:
        if phrase in row:
            print(row)
