'''A binary search function that returns the number of iterations taken to find the upper bound of a target value in a sorted array.'''
def binary_search_with_upper_bound(arr, target):

    left = 0
    right = len(arr) - 1
    iterations = 0
    upper_bound = None
    
    # Perform binary search to find the upper bound
    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        
        # Check if mid element is greater than or equal to target
        if arr[mid] >= target:
            upper_bound = arr[mid]
            right = mid - 1  
        else:
            left = mid + 1  
    
    return (iterations, upper_bound)


# Example usage
if __name__ == "__main__":
    test_array = [0.5, 1.2, 2.7, 3.8, 5.1, 6.9, 8.4]
    
    print("Тест 1:", binary_search_with_upper_bound(test_array, 3.0))
    print("Тест 2:", binary_search_with_upper_bound(test_array, 3.8))
    print("Тест 3:", binary_search_with_upper_bound(test_array, 10.0))
    print("Тест 4:", binary_search_with_upper_bound(test_array, 0.1))