import sys
import itertools
import time
import threading
from collections import defaultdict

def read_instruction(index: int, registry: list, input: list, output: list):
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
                return
            waitcount += 1
            time.sleep(0.00001)
        user_input = input.pop(0)
        position_to_store_at = registry[index+1]
        registry[position_to_store_at] = user_input
        index += 2
    elif (ins == 4): # output
        output_value = registry[registry[index+1]] if mode1 == 0 else registry[index+1]
        output.append(output_value)
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
    read_instruction(index, registry, input, output)

#def amplification_circuit(registry):
#    max_thruster_signal = 0
#    for permutation in itertools.permutations([0,1,2,3,4]):
#        ampliphier_settings = list(permutation)
#        output = Output()
#        second_input = 0
#        for ampliphier in ampliphier_settings:
#            output.reset()
#            read_instruction(0, registry.copy(), Input([ampliphier]+[second_input]), output)
#            second_input = output.output_values[0]          
#        if sum(output.output_values) >= max_thruster_signal:
#            max_thruster_signal = 
#            print("Largest thruster signal is: {} with permutation: {}".format(max_thruster_signal, permutation))
#    return max_thruster_signal

def amplification_circuit_with_loops(registry: list, min_phase_settings: int, max_phase_settings: int):
    max_thruster_signal = 0
    for permutation in itertools.permutations(range(min_phase_settings,max_phase_settings+1)):
        print("Testing permutation: {}".format(permutation))
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
        print("Max thruster signal so far: {}".format(max_thruster_signal))
    return max_thruster_signal

def main():
    registry = []
    with open("input.txt") as input:
        registry = [int(i) for i in input.readline().split(",")]
    
    print("Max thruster signal is: {}".format(amplification_circuit_with_loops(registry.copy(), 5, 9)))
    #outputs = Output()
    #inputs = Input([5])
    #read_instruction(0,registry.copy(),inputs, outputs)
    
if __name__ == '__main__':
    main()