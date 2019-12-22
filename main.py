from get_user_input import get_input, material_to_tool_dict
from feeds_and_speeds_high_level import feeds_and_speeds

# to do:
# make a gosh darn flow chart to sort out all the logic
# ask for brinell or rockwell hardness (with input) or average
# complete all data tables
# use extra tables of adjustment factors to calculate final surface speeds, give a feed and DOC input
# # done for turning with hss
# # done for turning with not hss (only for feed, expand to doc and lead angle)
# put feed and doc factors into their own files (adjustments_hss_turning.py) etc
# output a final RPM, feed and DOC
# sk for material diameter in get_input()
# after material has been asked about, only certain tool options should be available
# # done
# error messages if the material doesn't exist or an input is given that doesn't exist etc

u_operation, file_to_open, u_material, u_brinell_hardness, u_tool, u_feed, u_doc = get_input(material_to_tool_dict)
fs = feeds_and_speeds(u_operation, u_material, u_brinell_hardness, u_tool, file_to_open, u_feed, u_doc)

print(fs)
