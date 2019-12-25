import sys

def read_instruction(index, registry):
    if index >= len(registry):
        print("index {} outside registry length {}".format(index, len(registry)))
        sys.exit(1)
    ins = registry[index]%100
    mode1 = registry[index] // 10**2 % 10
    mode2 = registry[index] // 10**3 % 10
    mode3 = registry[index] // 10**4 % 10
#    print("Original instruction: {}. Current index: {}. Instruction: {}, Modes: {}, {}, {}".format(registry[index], index, ins, mode1, mode2, mode3))
    if (ins == 99):
        print("OP code 99. Exits program")
        sys.exit(0)
    elif (ins == 1): # addition
        addend1              = registry[registry[index+1]] if mode1 == 0 else registry[index+1]
        addend2              = registry[registry[index+2]] if mode2 == 0 else registry[index+2]
        position_to_store_at = registry[index+3]
        registry[position_to_store_at] = addend1+addend2
        index += 4
    elif (ins == 2): # multiplication
        factor1              = registry[registry[index+1]] if mode1 == 0 else registry[index+1]
        factor2              = registry[registry[index+2]] if mode2 == 0 else registry[index+2]
        position_to_store_at = registry[index+3]
        registry[position_to_store_at] = factor1*factor2
        index += 4
    elif (ins == 3): # input
        param = registry[index]
        user_input = int(input("Choose input: "))
        position_to_store_at = registry[index+1]
        registry[position_to_store_at] = user_input
        index += 2
    elif (ins == 4): # output
        output_value = registry[registry[index+1]] if mode1 == 0 else registry[index+1]
        print("OUTPUT: {}".format(output_value))
        index += 2
    elif (ins == 5): # jump if true
        if (registry[registry[index+1]] if mode1 == 0 else registry[index+1]) != 0:
            index = registry[registry[index+2]] if mode2 == 0 else registry[index+2]
        else:
            index += 3
    elif (ins == 6): # jump if false
        if (registry[registry[index+1]] if mode1 == 0 else registry[index+1]) == 0:
            index = registry[registry[index+2]] if mode2 == 0 else registry[index+2]
        else:
            index += 3
    elif (ins == 7): # less than
        comp1 = registry[registry[index+1]] if mode1 == 0 else registry[index+1]
        comp2 = registry[registry[index+2]] if mode2 == 0 else registry[index+2]
        registry[registry[index+3]] = 1 if (comp1 < comp2) else 0
        index += 4
    elif (ins == 8): # equals
        comp1 = registry[registry[index+1]] if mode1 == 0 else registry[index+1]
        comp2 = registry[registry[index+2]] if mode2 == 0 else registry[index+2]
        registry[registry[index+3]] = 1 if (comp1 == comp2) else 0
        index += 4
    read_instruction(index, registry)

def main():
    registry = []
    with open("input.txt") as input:
        registry = [int(i) for i in input.readline().split(",")]
    read_instruction(0,registry)
    
if __name__ == '__main__':
    main()