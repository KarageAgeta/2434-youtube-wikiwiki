def chunks(l: list, size: int):
    for i in range(0, len(l), size):
        yield l[i:i + size]
