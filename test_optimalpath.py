
import math


waypoints = [(-4, 0.4), (-1, 0.1), (0, 0), (1, 0.1), (4, 0.4)]
width_of_track = 1

def test_optimalpath():

	closest_waypoint = waypoints[2]

	pc = waypoints[0]
	pt = waypoints[4]
	midpoint = ((pc[0]-pt[0])/2, (pc[1]-pt[1])/2)
	d = sqrt((midpoint[0]-closest_waypoint[0])^2+(midpoint[1]-closest_waypoint[1])^2)


	if d < width_of_track / 2:
		optimal_point = midpoint
	else:
		m = (closest_waypoint[1]-midpoint[1]) / (closest_waypoint[0]-midpoint[0])
		new_d = d - width_of_track / 2
		c = 1/sqrt(1+m^2)
		s = m/sqrt(1+m^2)
		optimal_point = (closest_waypoint[0] + new_d * c, closest_waypoint[1] + new_d * s)


	return optimal_point