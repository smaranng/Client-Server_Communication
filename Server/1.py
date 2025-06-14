def push_zeros_to_end(n, arr):
    non_zero_elements = [num for num in arr if num != 0]
    zero_count = arr.count(0)
    result = non_zero_elements + [0] * zero_count
    return result

n = int(input("Enter the value of N: "))
print("Enter the elements of the array:")
arr = list(map(int, input().split()))  # Take space-separated input and convert to integers

# Validate if the input array has the correct number of elements
if len(arr) != n:
    print(f"Error: Expected {n} elements, but got {len(arr)}.")
else:
    result = push_zeros_to_end(n, arr)
    print("Output:", *result)
