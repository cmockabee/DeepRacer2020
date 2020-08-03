def reward_function(params):
    ###############################################################################
    '''
    Super Fast Reward function (or not....)
    '''

    import math

    # Read input variables
    waypoints = params['waypoints']  # list of (x,y)
    closest_waypoints = params['closest_waypoints'] # indices of the two closest waypoints
    x_ = params['x'] # agent's x location
    y_ = params['y'] # agent's y location
    wheels_on_track = params['all_wheels_on_track'] # boolean
    curr_speed = params['speed'] # speed in m/s

    # define some 'arbitrary' values
    reward = 1.0
    line_of_sight = 3 # net line of site related to waypoints
    curve_sight = 4 #

    # calculate speed evaluation and turn evaluation
    def distance(car_x, car_y, waypoint):
        """distance calculates the distance between the car and given waypoint
        """
        x_ = math.pow((car_x - waypoint[0]), 2)
        y_= math.pow((car_y - waypoint[1]), 2)
        return math.sqrt(x_ + y_)

    # calculate some more params
    prev_point = waypoints[closest_waypoints[0]]
    next_point = waypoints[closest_waypoints[1]]
    
    distance_way_1 = distance(car_x=x_, car_y=y_, waypoints[closest_waypoints[0]])
    distance_way_2 = distance(car_x=x_, car_y=y_, waypoints[closest_waypoints[1]])

    closest_waypoint = waypoints[closest_waypoints[0]] if distance_way_1 < distance_way_2 else waypoints[closest_waypoints[1]]

    def drift(points):
        for point in points:


    # calculate the optimal speed given the waypoints ahead
    def optimal_speed(line_of_sight, waypoints, closest_index):
        """optimal_speed
        """
        # this is gonna be kinda arbitrary
        return 0

    return reward
    ## Initialize the reward with typical value
    #reward = 1.0
    #
    ## Calculate the direction of the center line based on the closest waypoints
    #next_point = waypoints[closest_waypoints[1]]
    #prev_point = waypoints[closest_waypoints[0]]
    #
    ## Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    #track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    ## Convert to degree
    #track_direction = math.degrees(track_direction)
    #
    ## Calculate the difference between the track direction and the heading direction of the car
    #direction_diff = abs(track_direction - heading)
    #if direction_diff > 180:
    #    direction_diff = 360 - direction_diff
    #
    ## Penalize the reward if the difference is too large
    #DIRECTION_THRESHOLD = 10.0
    #if direction_diff > DIRECTION_THRESHOLD:
    #    reward *= 0.5
    #
    #return reward
