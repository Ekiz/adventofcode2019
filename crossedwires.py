import sys

def main():
    filepath = r"C:\Users\ekis_\Desktop\adventofcode\day3\input.txt"
    with open(filepath, 'r') as input:
        first_wire = input.readline().split(',')
        second_wire = input.readline().split(",")
        first_set = get_coordinate_set(first_wire)
        second_set = get_coordinate_set(second_wire)
        
        overlaps = first_set.intersection(second_set)
        abs_overlaps = [(abs(x),abs(y)) for (x,y) in overlaps]
        min_number_of_steps = sys.maxsize
        sum_steps = 0;
        print(overlaps)
        for overlap in overlaps:
            sum_steps = get_smallest_number_of_steps_to_coordinate(overlap, first_wire)+get_smallest_number_of_steps_to_coordinate(overlap, second_wire)
            if sum_steps < min_number_of_steps:
                min_number_of_steps = sum_steps
        

        print("Closest distance: {}".format(sorted(list(map(sum, abs_overlaps)))[0]))
        print("Smallest number of steps {}".format(min_number_of_steps))
            
def get_coordinate_set(coordinate_instructions):
    ret = set()
    x = y = 0
    for wire in coordinate_instructions:
        letter = wire[0]
        number = int(str(wire[1:]))
        if (wire[0]=='R'):
            ret.update(zip(range(x+1,x+number+1), [y for ys in range(number)]))
            x = x+number;
        elif (wire[0]=='L'):
            ret.update(zip(range(x-number+1,x+1), [y for ys in range(number)]))
            x = x-number;
        elif (wire[0]=='U'):
            ret.update(zip([x for xs in range(number)], range(y+1,y+number+1)))
            y = y+number;
        elif (wire[0]=='D'):
            ret.update(zip([x for xs in range(number)], range(y-number+1,y+1)))
            y = y-number;
    return ret
    
def get_smallest_number_of_steps_to_coordinate(coordinates, coordinate_instructions):
    ret = 0
    x = y = 0
    sum_steps = 0
    for wire in coordinate_instructions:
        letter = wire[0]
        number = int(str(wire[1:]))
        new = set()
        if (wire[0]=='R'):
            new = set(zip(range(x+1,x+number+1), [y for ys in range(number)]))
            delta = x
            coordinate = 0
            x = x+number;
        elif (wire[0]=='L'):
            new = set(zip(range(x-number+1,x+1), [y for ys in range(number)]))
            delta = x
            coordinate = 0
            x = x-number;
        elif (wire[0]=='U'):
            new = set(zip([x for xs in range(number)], range(y+1,y+number+1)))
            delta = y
            coordinate = 1
            y = y+number;
        elif (wire[0]=='D'):
            new = set(zip([x for xs in range(number)], range(y-number+1,y+1)))
            delta = y
            coordinate = 1
            y = y-number;
        
        if coordinates in new:
            print("Sumsteps before {} Coordinates {} delta {} x {} y {}".format(sum_steps, coordinates[coordinate], delta, x, y))
            sum_steps += abs(coordinates[coordinate]-delta)
            print("Found it in {} steps!".format(sum_steps))
            return sum_steps
        
        sum_steps += number
    print("NOT FOUND ERROR")
    sys.exit(0)

if __name__ == "__main__":
    main()