def get_binary_combinations(n):
    combinations = []
    for i in range(1 << n):
        # Convert the current number to a binary string of length n
        combinations.append(format(i, '0' + str(n) + 'b'))
    return combinations

 
 