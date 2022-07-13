def task(array) -> int:
    for index, ch in enumerate(array):
        if ch == "0" or ch == 0:
            return index


print(task("111111111110000000000000000"))
