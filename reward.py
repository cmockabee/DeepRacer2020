def reward_function(params):
    ###############################################################################
    '''
    Super Fast Reward function (or not....)
    '''

    import math

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

    # define some 'arbitrary' values
    reward = 1.0
    line_of_sight = 3 # net line of site related to waypoints



    # ***** Helper Functions *****
    def distance(car_x, car_y, waypoint):
        """distance calculates the distance between the car and given waypoint
        """
        x_ = math.pow((car_x - waypoint[0]), 2)
        y_= math.pow((car_y - waypoint[1]), 2)
        return math.sqrt(x_ + y_)

    def drift(points):
        x_drift = 0
        y_drift = 0

        for i in range(len(points)):
            if i == (len(points) - 1):
                break
            next_elem = points[(i + 1)]

            diff_x = point[i][0] - next_elem[0]
            diff_y = point[i][1] - next_elem[1]

            if diff_x == 0 or diff_y == 0:

    # **** Param: Speed *****
    distance_way_1 = distance(car_x=x_, car_y=y_, waypoint=closest_prev_point)
    distance_way_2 = distance(car_x=x_, car_y=y_, waypoint=closest_next_point)

    closest_waypoint = closest_prev_point if distance_way_1 < distance_way_2 else closest_next_point

    # calculate the optimal speed given the waypoints ahead
    def optimal_speed(line_of_sight, waypoints, closest_index):
        """optimal_speed
        """
        # this is gonna be kinda arbitrary
        return 0


    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])

    # Convert to degree
    track_direction = math.degrees(track_direction)


    #

    # Calculate optimal point on a curve
    optimal_point = optimal_point(closest_waypoints[0], next_point, prev_point, 1, params['track_width'])

    return reward


def optimal_point(closest_waypoint, next_point, prev_point, edge_buffer, width_of_track):
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
        new_d = d - width_of_track / 2 - edge_buffer
        optimal_point = (closest_waypoint[0], closest_waypoint[1] + new_d)

    # Typical case - find new points closer to edge to cut curve
    else:
        m = (closest_waypoint[1] - midpoint[1]) / (closest_waypoint[0] - midpoint[0])
        new_d = width_of_track / 2 - edge_buffer
        c = 1 / math.sqrt(1 + m**2)
        s = m / math.sqrt(1 + m**2)
        optimal_point = (closest_waypoint[0] + new_d * c, closest_waypoint[1] + new_d * s)

    return optimal_point
