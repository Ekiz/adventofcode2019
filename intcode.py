import sys
import itertools
import time
import threading
from collections import defaultdict

def read_instruction(index: int, registry: list, input: list = list(), output: list = list()):
    if index >= len(registry):
        print("index {} outside registry length {}".format(index, len(registry)))
        sys.exit(1)
    ins   = registry[index] % 100
    mode1 = registry[index] // 100   % 10
    mode2 = registry[index] // 1000  % 10
    mode3 = registry[index] // 10000 % 10
    # print("Original instruction: {}. Current index: {}. Instruction: {}, Modes: {}, {}, {}".format(registry[index], index, ins, mode1, mode2, mode3))
    if (ins == 99):
        # print("OP code 99. Exits program")
        return
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
        waitcount = 0
        while not input:
            if waitcount > 1000:
                print("Thread is probably never gonna finish... exiting")
                return
            waitcount += 1
            time.sleep(0.000001)
        input_value = input.pop(0)
        position_to_store_at = registry[index+1]
        registry[position_to_store_at] = input_value
        index += 2
    elif (ins == 4): # output
        output_value = registry[registry[index+1]] if mode1 == 0 else registry[index+1]
        output.append(output_value)
        # print("OUTPUT: {}".format(output_value))
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
    read_instruction(index, registry, input, output)

def find_noun_and_verb_for_output(registry: list, expected_output: int):
    for noun in range(100):
        for verb in range(100):
            reg_copy = registry.copy()
            reg_copy[1], reg_copy[2] = noun, verb
            read_instruction(index = 0, registry=reg_copy)
            if reg_copy[0] ==  expected_output:
                return 100*noun+verb

def amplification_circuit(registry: list, min_phase_settings: int, max_phase_settings: int):
    max_thruster_signal = 0
    for permutation in itertools.permutations(range(min_phase_settings, max_phase_settings+1)):
        inputs = [[i] for i in permutation]
        inputs.append(inputs[0])
        inputs[0].append(0)
        finaloutput = inputs[0]
        threads = list()
        for i in range(len(permutation)):
            threads.append(threading.Thread(target=read_instruction, args=(0, registry.copy(), inputs[i], inputs[i+1])))
        for thread in threads:
            thread.start()
        threads[-1].join() # Wait for last thread to finish
        max_thruster_signal = max(max_thruster_signal, finaloutput[0])
    return max_thruster_signal

def main():
    registry = []
    
    with open("input_day2.txt") as input:
        registry = [int(i) for i in input.readline().split(",")]
    reg_copy = registry.copy()
    reg_copy[1], reg_copy[2] = 12, 2
    read_instruction(0, reg_copy)
    print("Day 2, part 1. Position 0's value is: {}".format(reg_copy[0]))
    print("Day 2, part 2. Noun and verb combined is: {}".format(find_noun_and_verb_for_output(registry.copy(), 19690720)))
    
    with open("input_day5.txt") as input:
        registry = [int(i) for i in input.readline().split(",")]
    input = [1]
    output = list()
    read_instruction(0, registry.copy(), input, output)
    print("Day 5, part 1: The diagnostic code is: {}".format(output[-1]))
    input = [5]
    output = list()
    read_instruction(0, registry.copy(), input, output)
    print("Day 5, part 2: The diagnostic code is: {}".format(output[-1]))

    with open("input_day7.txt") as input:
        registry = [int(i) for i in input.readline().split(",")]
    print("Day 7, part 1: Max thruster signal is: {}".format(amplification_circuit(registry.copy(), 0, 4)))
    print("Day 7, part 2: Max thruster signal is: {}".format(amplification_circuit(registry.copy(), 5, 9)))
    
if __name__ == '__main__':
    main()