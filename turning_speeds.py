import csv
import numpy as np
from two_d_interpolator import two_d_col_interpolator, two_d_row_interpolator


def surface_speed_hss_turning(data_array, row_store, user_tool, user_feed, user_doc):
    for column_index in range(0, data_array.shape[1]):
        if user_tool in data_array[0][column_index]:
            column_store = column_index
            break
    speed = float(data_array[row_store][column_store])

    # __________ open relevant adjustments file __________
    file_dir = 'C:/Users/matth/Desktop/Python/MachiningHelper/Data/'
    file_name = 'Cutting_Speed_Adjustment_Factors_for_Turning_with_HSS_Tools.csv'
    file_to_open = file_dir + file_name
    with open(file_to_open) as adjust_f:
        data_iter = csv.reader(adjust_f)
        data = [data for data in data_iter]
    data_adjust = np.asarray(data, dtype=None)

    # __________ calculating feed factor for HSS turning __________
    if round(user_feed, 3) == 0.012:
        ff = 1.0
        print('Given feed equals the default feed')
    elif user_feed > float(data_adjust[data_adjust.shape[0] - 1][0]):
        print(data_adjust.shape[0])
        ff = float(data_adjust[data_adjust.shape[0] - 1][2])
        print('Given feed above feed range in table, using max feed factor')
    else:
        print('Feed factor needs to be interpolated')
        for adjust_row_index in range(1, data_adjust.shape[0] - 1):
            if float(data_adjust[adjust_row_index][0]) < user_feed:
                below_index = adjust_row_index
                above_index = below_index + 1
        ff = two_d_row_interpolator(data_adjust, user_feed, below_index, above_index, 0, 2)

    # ____________________ calculating depth of cut factor for HSS turning____________________
    if user_doc == 0.125:
        fd = 1.0
        print('Given depth of cut equals the given depth of cut')
    elif user_doc > float(data_adjust[data_adjust.shape[0] - 1][3]):
        print(data_adjust.shape[0])
        fd = float(data_adjust[data_adjust.shape[0] - 1][5])
        print('Given depth of cut above depth of cut range in table, using max depth of cut factor')
    else:
        print('Depth of cut needs to be interpolated')
        for adjust_row_index in range(1, data_adjust.shape[0] - 1):
            if float(data_adjust[adjust_row_index][3]) < user_feed:
                below_index = adjust_row_index
                above_index = below_index + 1
        fd = two_d_row_interpolator(data_adjust, user_feed, below_index, above_index, 3, 5)

    # ____________________ calculate adjusted speed ____________________
    speed_adjusted = round(speed * ff * fd, 2)
    s = f'Surface speed of {speed_adjusted}, feed of {user_feed} and DOC of {user_doc}'
    return s


def feed_speed_not_hss_turning(data_array, row_store, user_tool, user_feed, user_doc):
    column_store = []
    for column_index in range(0, data_array.shape[1]):
        if user_tool in data_array[0][column_index]:
            column_store.append(column_index)
    fs_opt = data_array[row_store][column_store[0]].split('_')
    fs_avg = data_array[row_store][column_store[1]].split('_')

    # _________ open relevant adjustments file __________
    file_dir = 'C:/Users/matth/Desktop/Python/MachiningHelper/Data/'
    file_name = 'Turning_Speed_Adjustment_Factors_for_Feed_Depth_of_Cut_and_Lead_Angle.csv'
    file_to_open = file_dir + file_name
    with open(file_to_open) as adjust_f:
        data_iter = csv.reader(adjust_f)
        data = [data for data in data_iter]
    data_adjust = np.asarray(data, dtype=None)

    # ____________________ calculating feed factor for non HSS turning ____________________
    # expand this for the depth of cut and lead angle sections of the adjustment table

    # default feeds are calculated as avg and opt, doc = 0.1 inches, lead angle = 15 degrees
    # if feed is equal to either opt or av feed, you use that feed
    if float(fs_opt[0]) == user_feed:
        print('Given feed equals the default optimum feed')
        ff = 1.0
        # DOCLA_row_index = 2
    elif float(fs_avg[0]) == user_feed:
        print('Given feed equals the default average feed')
        ff = 1.0
        # DOCLA_row_index = 2
    else:
        print('Feed factor needs to be interpolated')
        # find columns using ratio of average and optimum surface speeds
        ratio_va_vo = float(fs_avg[1]) / float(fs_opt[1])
        for adjust_feed_col_index in range(1, 8):
            if float(data_adjust[1][adjust_feed_col_index]) < ratio_va_vo:
                col_before_index = adjust_feed_col_index
            col_after_index = col_before_index + 1
        # find row, check max and min (will give single row) and if not, interpolate to find two rows
        ratio_cf_of = user_feed / (float(fs_opt[0]) / 1000)
        if ratio_cf_of > float(data_adjust[2][0]):
            row_index = 2
            # interpolate between columns using the values from row 2
            ff = two_d_col_interpolator(data_adjust, ratio_va_vo, col_before_index, col_after_index, 1, row_index)
        elif ratio_cf_of < float(data_adjust[11][0]):
            row_index = 11
            # interpolate between columns using the values from row 2
            ff = two_d_col_interpolator(data_adjust, ratio_va_vo, col_before_index, col_after_index, 1, row_index)
        else:
            # find the two row indices based on ratio of user to optimum feed
            for adjust_feed_row_index in range(2, data_adjust.shape[0]):
                if float(data_adjust[adjust_feed_row_index][0]) > ratio_cf_of:
                    row_below_index = adjust_feed_row_index
                row_above_index = row_below_index - 1
            # interpolate between rows for first column
            col_before_value = two_d_row_interpolator(data_adjust, ratio_cf_of, row_below_index, row_above_index, 0, col_before_index)
            # interpolate between rows for second column
            col_after_value = two_d_row_interpolator(data_adjust, ratio_cf_of, row_below_index, row_above_index, 0, col_after_index)
            # interpolate between columns using the two row interpolation values
            interpolate_col_start = col_before_value
            interpolate_goal_sum = (ratio_va_vo - float(data_adjust[1][col_before_index]))
            interpolate_numerator = col_after_value - col_before_value
            interpolate_denominator = float(data_adjust[1][col_after_index]) - float(data_adjust[1][col_before_index])
            ff = interpolate_col_start + (interpolate_goal_sum * (interpolate_numerator / interpolate_denominator))

    speed = round(float(fs_opt[1]) * ff, 2)

    s = f'Surface speed of {speed}, feed of {user_feed} and DOC of {user_doc}'
    return s
