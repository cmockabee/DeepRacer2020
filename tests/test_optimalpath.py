
import math
from DeepRacer2020 import optimal_point

waypoints = [(-3, 1.1), (0, 0.1), (1, 0), (2, 0.1), (5, 1.1)]
waypoints2 = [(4, 2.4), (1, 1.5), (0, 0), (1, -.6), (4, -1.2)]


width_of_track = 1
edge_buffer = 1


def test_optimalpath():

	closest_waypoint = waypoints[2]

	pc = waypoints[0]
	pt = waypoints[4]
	midpoint = ((pc[0] + pt[0]) / 2, (pc[1] + pt[1]) / 2)
	d = math.sqrt((midpoint[0] - closest_waypoint[0])**2 + (midpoint[1] - closest_waypoint[1])**2)


	if d < width_of_track / 2:
		optimal_point = midpoint
	elif closest_waypoint[0] == midpoint[0]:
		new_d = d - width_of_track / 2
		optimal_point = (closest_waypoint[0], closest_waypoint[1] + new_d)
	else:
		m = (closest_waypoint[1]-midpoint[1]) / (closest_waypoint[0]-midpoint[0])
		new_d = width_of_track / 2 - edge_buffer
		print(f"New d: {new_d}")
		c = 1 / math.sqrt(1 + m**2)
		s = m / math.sqrt(1 + m**2)
		optimal_point = (closest_waypoint[0] + new_d * c, closest_waypoint[1] + new_d * s)



	print(f"Distance from midpoint to closest_waypoint: {d}")
	print(f"Optimal Point: {optimal_point}")
	return optimal_point
