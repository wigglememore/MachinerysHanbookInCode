material_to_tool_dict = {
    'Plain Carbon and Alloy Steels': ['HSS', 'UCH', 'UCT', 'CCH', 'CCT'],
    'Tool Steels': ['HSS', 'UCH', 'UCT', 'CCH', 'CCT'],
    'Stainless Steels': ['HSS', 'UCH', 'UCT', 'CCH', 'CCT'],
    'Ferrous Cast Metals': ['HSS', 'UCH', 'UCT', 'CCH', 'CCT'],
    'Copper Alloys': ['HSS', 'UCT'],
    'Titanium and Titanium Alloys': ['HSS', 'UCT'],
    'Light Metals': ['HSS', 'UCT'],
    'Superalloys': ['HSS', 'UCT', 'CH', 'CT']
}


# material type, material designation, operation, brinell hardness, tool, feed, DOC
def get_input(tool_dict):
    # base directory for the tables of feed and speed data
    directory_base = 'C:/Users/matth/Desktop/Python/MachiningHelper/Data/Cutting_Feeds_and_Speeds_for_'

    # ____________________ ask for material type so the program knows which file to open ____________________
    material_types = [
        'Plain Carbon and Alloy Steels', 'Tool Steels', 'Stainless Steels',
        'Ferrous Cast Metals', 'Copper Alloys', 'Titanium and Titanium Alloys',
        'Light Metals', 'Superalloys'
    ]
    print_material_types = ''
    for i in range(0, len(material_types)):
        print_material_types = print_material_types + material_types[i] + ' [' + str(i) + '], '
    print('Material types: ' + print_material_types)
    user_material_type_value = int(input('Input a material type: '))
    if user_material_type_value not in range(0, len(material_types)):
        print('Invalid input')
        exit()
    user_material_type = material_types[user_material_type_value]

    # ____________________ ask for specific material designation ____________________
    user_material = input('Input a material designation: ')
    # have some checks here to see if the material exists

    # ____________________ ask for operation ____________________
    operation_types = ['Turning', 'Milling', 'Drilling']
    print_operations = ''
    for i in range(0, len(operation_types)):
        print_operations = print_operations + operation_types[i] + ' [' + str(i) + '], '
    print('Operations: ' + print_operations)
    user_operation_value = int(input('Input an operation: '))
    if user_operation_value not in range(0, len(operation_types)):
        print('Invalid input')
        exit()
    user_operation = operation_types[user_operation_value]

    # ____________________ ask for specific brinell hardness ____________________
    user_brinell_hardness = int(input('Input a material Brinell Hardness (type "n/a" if unknown): '))
    # allow brinell, rockwell or use the average value for that material

    # ____________________ ask for tool type ____________________
    tool_types = tool_dict[user_material_type]
    print_tool_types = ''
    for i in range(0, len(tool_types)):
        print_tool_types = print_tool_types + tool_types[i] + ' [' + str(i) + '], '
    print('Tool types: ' + print_tool_types)
    user_tool_value = int(input('Input a tool type: '))
    if user_tool_value not in range(0, len(tool_types)):
        print('Invalid input')
        exit()
    user_tool = tool_types[user_tool_value]

    # ____________________ ask for feed ____________________
    user_feed_unit = int(input('Enter your feed unit (per rev): thou [0] or mm [1]: '))
    user_feed_input = int(input('Enter your feed: '))
    if user_feed_unit == 0:
        user_feed = user_feed_input / 1000
    else:
        user_feed = (user_feed_input * 39.37007874015748) / 1000

    # ____________________ ask for depth of cut ____________________
    user_doc_unit = int(input('Enter your depth of cut unit (per rev): thou [0] or mm [1]: '))
    user_doc_input = int(input('Enter your depth of cut: '))
    if user_doc_unit == 0:
        user_doc = user_doc_input / 1000
    else:
        user_doc = (user_doc_input * 39.37007874015748) / 1000

    # ____________________ create file name and directory ____________________
    directory_operation = user_operation.replace(' ', '_')
    directory_material = user_material_type.replace(' ', '_')
    file_to_open = directory_base + directory_operation + '_' + directory_material + '.csv'

    # ____________________ return the necessary data ____________________
    return user_operation, file_to_open, user_material, user_brinell_hardness, user_tool, user_feed, user_doc
