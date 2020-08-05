def reward_function(params):
    ###############################################################################
    '''
    Reward function example
    '''

    import math

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Initialize the reward with typical value
    reward = 1.0

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

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
