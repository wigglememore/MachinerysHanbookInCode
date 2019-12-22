# function to do 2d interpolation
# t for target


def two_d_row_interpolator(array, t, pre_t_i, post_t_i, t_col_i, goal_row_i):
    interpolate_start = float(array[pre_t_i][goal_row_i])
    interpolate_goal_sum = (t - float(array[pre_t_i][t_col_i]))
    interpolate_numerator = float(array[post_t_i][goal_row_i]) - float(array[pre_t_i][goal_row_i])
    interpolate_denominator = float(array[post_t_i][t_col_i]) - float(array[pre_t_i][t_col_i])
    interp_out = interpolate_start + (interpolate_goal_sum * (interpolate_numerator / interpolate_denominator))
    return interp_out


def two_d_col_interpolator(array, t, pre_t_i, post_t_i, t_row_i, goal_row_i):
    interpolate_col_start = array[goal_row_i][pre_t_i]
    interpolate_goal_sum = (t - float(array[t_row_i][pre_t_i]))
    interpolate_numerator = float(array[goal_row_i][post_t_i]) - float(array[goal_row_i][pre_t_i])
    interpolate_denominator = float(array[t_row_i][post_t_i]) - float(array[t_row_i][pre_t_i])
    interp_out = interpolate_col_start + (interpolate_goal_sum * (interpolate_numerator / interpolate_denominator))
    return interp_out
