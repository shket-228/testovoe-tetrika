def task(array):
    # Edge cases
    if not array or array[len(array) - 1] == "1":
        return -1  # Empty or have no 0
    if array[0] == "0":
        return 0  # Starts with 0

    # Binary search
    left, right = 0, len(array) - 1
    while True:
        mid = (left + right) // 2
        if array[mid] == "0":
            right = mid 
        elif array[mid + 1] == "1":
            left = mid
        else:
            return mid + 1


# Or just
# def task(array):
#    return array.find("0")


if __name__ == "__main__":
    print(task("111111111110000000000000000"))
