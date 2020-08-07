import math
from DeepRacer2020 import optimal_speed, distance, r_squared, line_of_best_fit, mean

def test_mean():
    set_1 = [5,5,5,5,5,5]
    mean_1 = mean(set_1)

    assert mean_1 == 5

    set_2 = [3, 5, 7, 9, 11]
    mean_2 = mean(set_2)

    assert mean_2 == 7

def test_distance():
    x_1 = 3
    y_1 = 2
    point_1 = [9, 7]
    distance_1 = distance(x_1, y_1, point_1)

    assert round(distance_1, 5) == 7.81025

    x_2 = 21
    y_2 = 112
    point_2 = [1, 7]
    distance_2 = distance(x_2, y_2, point_2)

    assert round(distance_2, 5) == 106.88779

    x_3 = 76
    y_3 = 13
    point_3 = [145, 127]
    distance_3 = distance(x_3, y_3, point_3)

    assert round(distance_3, 5) == 133.25539


def test_line_of_best_fit():
    x_1 = [0, 2, 5, 22]
    y_1 = [1, 3, 8, 9]
    slope_1, intercept_1 = line_of_best_fit(xs=x_1, ys=y_1)

    assert round(slope_1, 6) == 0.303055
    assert round(intercept_1, 6) == 3.052849

    x_2 = [0, 2, 5, 22, 24, 52, 32, 13, 0]
    y_2 = [1, 3, 8, 9, 15, 23, 13, 1, 0]
    slope_2, intercept_2 = line_of_best_fit(xs=x_2, ys=y_2)

    assert round(slope_2, 6) == 0.407214
    assert round(intercept_2, 6) == 1.324216


def test_r_squared():
    points_1 = [[0,0], [1, 1], [2, 2], [3,3]]
    r_1 = r_squared(points=points_1)

    assert r_1 == 1.0

    points_2 = [[0, 1], [2,3], [5, 8], [22, 9], [24, 15], [52, 23], [32, 13], [13, 1], [0, 0]]
    r_2 = r_squared(points=points_2)

    assert round(r_2, 5) == 0.84667


def test_optimal_speed():
    sight_1 = 3
    points_1 = [[0,0], [1, 1], [2, 2], [3,3]]
    speed_1 = optimal_speed(waypoints=points_1, line_of_sight=sight_1, index=0)

    assert speed_1 == 2.0

    sight_2 = 9
    points_2 = [[0, 1], [2,3], [5, 8], [22, 9], [24, 15], [52, 23], [32, 13], [13, 1], [0, 0]]
    speed_2 = optimal_speed(waypoints=points_2, line_of_sight=sight_2, index=0)

    assert speed_2 ==  1.2
