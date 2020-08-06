from DeepRacer2020 import reward_function


def test_reward_function():
    waypoints = [[0, 1], [2,3], [5, 8], [22, 9], [24, 15], [52, 23], [32, 13], [13, 1], [0, 0]]

    params = {
        'waypoints': waypoints,
        'closest_waypoints': [0, 1],
        'x': 0,
        'y': 0,
        'all_wheels_on_track': True,
        'speed': 50,
        'track_width': 20,
    }

    return reward_function(params=params)
