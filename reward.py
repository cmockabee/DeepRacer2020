import math

def reward_function(params):
    ###############################################################################
    '''
    Super Fast Reward function (or not....)
    '''

    # ***** Function: Reward for proximity to optimal position *****
    def position_reward(distance_to_optimal, width_of_track, wheels_on_track):
        if distance_to_optimal <= .1 * width_of_track and wheels_on_track:
            return 80
        elif distance_to_optimal <= 0.25 * width_of_track and wheels_on_track:
            return 30
        elif distance_to_optimal <= 0.5 * width_of_track and wheels_on_track:
            return 6
        return 0

    # ***** Function: Reward for falling in the range of optimal speed *****
    def speed_reward(diff_between_speeds):
        if diff_between_speeds > 1.0:
            return 0
        elif diff_between_speeds > 0.90:
            return 5
        elif diff_between_speeds > 0.60:
            return 10
        elif diff_between_speeds > 0.30:
            return 20
        elif diff_between_speeds > 0.15:
            return 30
        elif diff_between_speeds > 0.10:
            return 40
        elif diff_between_speeds > 0.05:
            return 50
        return 60 # don't jump the speed reward like the position reward

    # ***** Parameters & Minor calculations *****
    waypoints = params['waypoints']  # list of (x,y)
    closest_waypoints = params['closest_waypoints'] # indices of the two closest waypoints
    x_ = params['x'] # agent's x location
    y_ = params['y'] # agent's y location
    wheels_on_track = params['all_wheels_on_track'] # boolean
    curr_speed = params['speed'] # speed in m/s

    # calculate some more params
    closest_prev_point = waypoints[closest_waypoints[0]]
    closest_next_point = waypoints[closest_waypoints[1]]

    distance_way_1 = distance(car_x=x_, car_y=y_, waypoint=closest_prev_point)
    distance_way_2 = distance(car_x=x_, car_y=y_, waypoint=closest_next_point)

    if distance_way_1 < distance_way_2:
        closest_waypoint = closest_prev_point
        closest_index = closest_waypoints[0]
    else:
        closest_waypoint = closest_next_point
        closest_index = closest_waypoint[1]

    # define some 'arbitrary' values
    reward = 1.0
    line_of_sight_speed = 7 # net line of site related to waypoints
    line_of_sight_position = 4

    # **** Param: Speed *****
    # calculate the optimal speed given the waypoints ahead
    best_speed = optimal_speed(waypoints=waypoints, line_of_sight=line_of_sight_speed,
                                index=closest_index)

    diff_in_speeds = abs(best_speed - curr_speed)

    # ***** Param: Optimal Point *****
    # Calculate optimal point on a curve
    ai = closest_index + line_of_sight_position
    if ai >= len(waypoints):
        ai = len(waypoints) - 1

    bi = closest_index - line_of_sight_position
    if bi < 0:
        bi = 0

    best_point = optimal_point(closest_waypoint=closest_waypoint,
                                next_point=waypoints[int(ai)], prev_point=waypoints[int(bi)],
                                buffer=1, width_of_track=params['track_width'])

    distance_to_optimal = distance(car_x=x_, car_y=y_, waypoint=best_point)

    # ***** Reward Calculations *****
    if not wheels_on_track:
        # lolz keep them wheelz on the track
        reward -= 150

    # Positional Reward
    reward += position_reward(distance_to_optimal=distance_to_optimal, width_of_track=params['track_width'], wheels_on_track=wheels_on_track)

    # Speed Reward
    reward += speed_reward(diff_between_speeds=diff_in_speeds)

    return reward


def mean(data):
    i = 0
    agg = 0
    for elem in data:
        i += 1
        agg += elem
    return (agg / i)


def distance(car_x, car_y, waypoint):
    ###############################################################################
    """distance calculates the distance between the car and given waypoint
    """
    x_ = math.pow((car_x - waypoint[0]), 2)
    y_= math.pow((car_y - waypoint[1]), 2)
    return math.sqrt(x_ + y_)


def line_of_best_fit(xs, ys):
    x_y_mult = []
    for (x, y) in zip(xs, ys):
        x_y_mult.append(x*y)

    x_mult = []
    for x in xs:
        x_mult.append(x*x)

    x_mean = mean(xs)
    y_mean = mean(ys)
    mult_mean = mean(x_y_mult)
    x_mult_mean = mean(x_mult)

    possible_denom =  ((x_mean*x_mean) - x_mult_mean)
    denominator = 9999999 if possible_denom == 0 else possible_denom

    slope = (((x_mean*y_mean) - mult_mean) / denominator)

    intercept = mean(ys) - slope*mean(xs)

    return slope, intercept


def r_squared(points):
    ###############################################################################
    xs = []
    ys = []

    for point in points:
        xs.append(point[0])
        ys.append(point[1])

    slope, intercept = line_of_best_fit(xs=xs, ys=ys)

    best_fit_line = []
    for x in xs:
        best_fit_line.append(((slope*x) + intercept))

    def squared_error(ys_orig, ys_line):
        sum = 0
        for (yo, ym) in zip(ys_orig, ys_line):
            sum += math.pow((yo - ym), 2)

        return sum

    y_orig_mean = mean(ys)
    y_mean_line = []
    for y in ys:
        y_mean_line.append(y_orig_mean)

    squared_error_regr = squared_error(ys, best_fit_line)
    squared_error_y_mean = squared_error(ys, y_mean_line)

    squared_error_y_mean = 0.000001 if squared_error_y_mean == 0 else squared_error_y_mean

    return 1 - (squared_error_regr/squared_error_y_mean)


def optimal_point(closest_waypoint, next_point, prev_point, buffer, width_of_track):
    ###############################################################################
    '''
    Calculating the optimal point to cut curves
    '''

    # Find midpoint and distance from close waypoint to midpoint
    pc = next_point
    pt = prev_point
    midpoint = ((pc[0] + pt[0]) / 2, (pc[1] + pt[1]) / 2)
    d = math.sqrt((midpoint[0] - closest_waypoint[0])**2 + (midpoint[1] - closest_waypoint[1])**2)

    # Slight curve - optimal point is the midpoint of the line
    if d < width_of_track / 2:
        optimal_point = midpoint

    # Vertical curve - rare case that would otherwise cause undefined slope
    elif closest_waypoint[0] == midpoint[0]:
        new_d = d - width_of_track / 2 - buffer
        optimal_point = (closest_waypoint[0], closest_waypoint[1] + new_d)

    # Typical case - find new points closer to edge to cut curve
    else:
        m = (closest_waypoint[1] - midpoint[1]) / (closest_waypoint[0] - midpoint[0])
        new_d = width_of_track / 2 - buffer
        c = 1 / math.sqrt(1 + m**2)
        s = m / math.sqrt(1 + m**2)
        optimal_point = (closest_waypoint[0] + new_d * c, closest_waypoint[1] + new_d * s)

    return optimal_point


def optimal_speed(waypoints, line_of_sight, index):
    ###############################################################################
    """
    optimal_speed
    """
    # Set speed suggestions
    LOW_SPEED = 1.0
    FIRST_GEAR = 1.2
    SECOND_GEAR = 1.4
    THIRD_GEAR = 1.6
    FOURTH_GEAR = 1.8
    FIFTH_GEAR = 2.0
    ECO_BOOST = 2.2
    MAX_SPEED = 2.4

    next_index = index + line_of_sight
    next_index = (len(waypoints) - 1) if next_index >= len(waypoints) else next_index
    points_ahead = waypoints[int(index):int(next_index)]

    r_value = r_squared(points=points_ahead)

    if r_value < 0.40:
        return LOW_SPEED
    elif r_value < 0.60:
        return FIRST_GEAR
    elif r_value < 0.70:
        return SECOND_GEAR
    elif r_value < 0.80:
        return THIRD_GEAR
    elif r_value < 0.85:
        return FOURTH_GEAR
    elif r_value < 0.90:
        return FIFTH_GEAR
    elif r_value < 0.95:
        return ECO_BOOST

    return MAX_SPEED
