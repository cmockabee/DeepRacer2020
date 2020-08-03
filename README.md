# DeepRacer2020

## Introduction
*Developers, start your engines*

Developers of all skill levels can get hands on with machine learning through a cloud based 3D racing simulator, fully autonomous 1/18th scale race car driven by reinforcement learning, and global racing league.

[Introduction to DeepRacer](https://aws.amazon.com/deepracer/)
[AWS DeepRacer console](https://console.aws.amazon.com/deepracer/home?region=us-east-1#welcome)

## Requirements
To get started with DeepRacer:
- Create an AWS account ([AWS](https://console.aws.amazon.com/console/))
- Create an DeepRacer user account ([AWS DeepRacer console](https://console.aws.amazon.com/deepracer/home?region=us-east-1#welcome))

## Strategy
DeepRacer uses reinforcement learning to train the car, meaning the car's success is contingent on how well it is rewarded or penalized for its behavior during training runs.

A strategy for an optimized model then requires an understanding of impactful parameters and how to cleverly weigh them. 

Parameters

```python
{
    "all_wheels_on_track": Boolean,        # flag to indicate if the agent is on the track
    "x": float,                            # agent's x-coordinate in meters
    "y": float,                            # agent's y-coordinate in meters
    "closest_objects": [int, int],         # zero-based indices of the two closest objects to the agent's current position of (x, y).
    "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
    "distance_from_center": float,         # distance in meters from the track center
    "is_crashed": Boolean,                 # Boolean flag to indicate whether the agent has crashed.
    "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not.
    "is_offtrack": Boolean,                # Boolean flag to indicate whether the agent has gone off track.
    "is_reversed": Boolean,                # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
    "heading": float,                      # agent's yaw in degrees
    "objects_distance": [float, ],         # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
    "objects_heading": [float, ],          # list of the objects' headings in degrees between -180 and 180.
    "objects_left_of_center": [Boolean, ], # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
    "objects_location": [(float, float),], # list of object locations [(x,y), ...].
    "objects_speed": [float, ],            # list of the objects' speeds in meters per second.
    "progress": float,                     # percentage of track completed
    "speed": float,                        # agent's speed in meters per second (m/s)
    "steering_angle": float,               # agent's steering angle in degrees
    "steps": int,                          # number steps completed
    "track_length": float,                 # track length in meters.
    "track_width": float,                  # width of the track
    "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center

}
```

## Reward functions

### Optimal Path
This function will reward the car some value depending on its proximity to the calculated optimal path.
The goal is to calculate the minimum curve between 2 points without compromising the car's ability to stay on the road.
[Check out page 7 of this link for the labeled figure of which the calculations stem.](http://navybmr.com/study%20material/14336a/14336A_ch3.pdf)

To calculate the optimal path:

```
    Find the car's position (x, y)
    Find the closest waypoint
    ---Find PC and PT (these coordinates will be +/- some length from the closest waypoint) 
    ---Find midpoint of line PC-PT
    Define tangents of points PC and PT
    ---Define intersection of tangents (point PI) This is the apex of the curve.
    ---Find leg lengths of right trianges PC/midpoint/PI and PT/midpoint/PI
    ---Calculate angles PI/PC/midpoint and PI/PT/midpoint (points PC and PT being the center of the angles)
    -------Find angles O/PC/midpoint and O/PT/midpoint by using complementary angles (90 - previous calculations)
    ---------Find R for both sides of the curve (curve radii)
    ---------Find length of line O/PI
    ------------Find M [M = R(1 - cos(delta/2))]
    -------------Minimize M as much as possible (subtract track width/2? testing to be done)
    -------------Define new midpoint on curve *(optimal position)* [the closest waypoint - minimization to edge)
```

Once the optimal position is found, the car's actual position is compared to the optimal, and a reward is derived.
       

## Resources

 - [http://navybmr.com/study%20material/14336a/14336A_ch3.pdf](http://navybmr.com/study%20material/14336a/14336A_ch3.pdf)


