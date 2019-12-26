import sys
import os

def calculate_fuel(weight: int) -> int:
    if (weight < 9):
        return 0
    else:
        fuel = int(weight/3)-2
        return fuel + calculate_fuel(fuel)

def main():
    print("Starting main")
    filepath = r"C:\Users\ekis_\Desktop\adventofcode\day1\input.txt"
    sum = 0
    with open(filepath, 'r') as input:
        for line in input:
          sum += calculate_fuel(int(line))
          print ("partialsum: {}".format(sum))
    print("sum: {}".format(sum))

if __name__ == '__main__':
    main()