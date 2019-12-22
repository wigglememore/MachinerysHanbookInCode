def row_index(data_array, UM, UBH):
    for row_index in range(0, data_array.shape[0]):
        if UM in data_array[row_index][0]:
            row_store = row_index
            lower = data_array[row_index][1]
            upper = data_array[row_index][2]
            if UBH > int(lower) and UBH < int(upper):
                break
    return row_store
