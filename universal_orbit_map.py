import sys
from collections import defaultdict

def count_orbits(orbits, key, orbits_count):
    if orbits.get(key) == None:
        return orbits_count
    else:
        count = 0
        for orbit in orbits.get(key):
            count += count_orbits(orbits, orbit, 1+orbits_count)
        return count+orbits_count

def get_all_ancestors(orbits, object):
    if object not in orbits.keys():
        return [object]
    else:
        return [object]+get_all_ancestors(orbits, orbits.get(object))

def find_common_object(list_1, list_2):
    for element in list_1:
        if element in list_2:
            return element
    print("SOMETHING WENT WRONG, NO COMMON OBJECT FOUND!")

def find_path(orbits, first, second):
    first_ancestors = get_all_ancestors(orbits, first)
    second_ancestors = get_all_ancestors(orbits, second)
    common_ancestor = find_common_object(first_ancestors, second_ancestors)
    first_ancestors = first_ancestors[2:first_ancestors.index(common_ancestor)+1]
    second_ancestors = second_ancestors[1:second_ancestors.index(common_ancestor)]
    second_ancestors.reverse()
    return first_ancestors+second_ancestors
    
def main():
    orbits = defaultdict(set)
    reversed_orbits = dict()
    with open('input.txt', 'r') as input:
        for line in input:
            orbit = line.rstrip('\n').split(")")
            orbits[orbit[0]].add(orbit[1])
            reversed_orbits.update({orbit[1]: orbit[0]})
    print("Orbit count is: {}".format(count_orbits(orbits, "COM", 0)))
    first = "YOU"
    second = "SAN"
#    print(reversed_orbits)
    print("Number of steps from {} to {} is: {}".format(first, second, len(find_path(reversed_orbits, first, second))))

if __name__ == '__main__':
    main()