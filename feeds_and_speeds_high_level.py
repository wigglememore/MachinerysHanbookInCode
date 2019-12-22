import csv
import numpy as np
from turning_speeds import surface_speed_hss_turning, feed_speed_not_hss_turning
from find_row import row_index


def feeds_and_speeds(user_operation, user_material, user_brinell_hardness, user_tool, file, user_feed, user_doc):
    # data from here for HSS is based on a feed on 0.012 inch/rev and a depth of cut of 0.125 inch
    # data from here for others is based on a feed on 0.01 inch/rev, lead angle of 15 degrees, and nose radius of 3/64

    # __________ open the relevant file of feeds and speeds for operation and material type __________
    with open(file) as dest_f:
        data_iter = csv.reader(dest_f)
        data = [data for data in data_iter]
    data_array = np.asarray(data, dtype=None)

    # __________ pick row of data __________
    # picking the row is general to turning, milling and drilling/reaming operations
    row_store = row_index(data_array, user_material, user_brinell_hardness)
    # if user operation == turning
    # __________ find column, select relevant feeds and/or speeds and calculate adjustments __________
    if user_tool == 'HSS':
        hss_speed = surface_speed_hss_turning(data_array, row_store, user_tool, user_feed, user_doc)
        return hss_speed
    else:
        non_hss_feeds_and_speeds = feed_speed_not_hss_turning(data_array, row_store, user_tool, user_feed, user_doc)
        return non_hss_feeds_and_speeds
