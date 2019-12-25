def get_number_as_list(number):
    if number < 10:
        return [number]
    element = number%10
    return get_number_as_list(int(number/10)) + [element]

def at_least_one_double(numbers):
    ret = []
    for number in numbers:
        number_list = get_number_as_list(number)
        number_unique = set(number_list)
        if len(number_list)!=len(number_unique):
           ret.append(number)
    return ret

def at_least_one_exactly_double(numbers):
    ret = []
    for number in numbers:
        nl = get_number_as_list(number)
        elements = set(nl)
        counts = [nl.count(element) for element in elements]
        if (2 in counts):
            ret.append(number)
    return ret
            
def all_non_desc(numbers):
    remove_set = set()
    for number in numbers:
        current_no = 0
        number_list = get_number_as_list(number)
        for digit in number_list:
            if (digit < current_no):
                remove_set.add(number)
                break
            else:
                current_no = digit
    return set(numbers)-remove_set

def main():
    print(len(at_least_one_exactly_double(all_non_desc(range(124075, 580769)))))

if __name__ == '__main__':
    main()