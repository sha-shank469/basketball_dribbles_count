# football_dribbles_count

# To Run the Script:
    
    python3 main.py

# Logic behind dribbles count:
The function calculates the change in the y-coordinate of the basketball (delta_y) by subtracting the current y-coordinate from the previous y-coordinate.

It then checks if there was a significant upward change in the y-coordinate (self.prev_delta_y > self.dribble_threshold) in the previous frame and a significant downward change (delta_y < -self.dribble_threshold) in the current frame. This pattern indicates a dribble. 

If the conditions are met, it increments the dribble count (self.dribble_count).

# Example
Frame 1: Basketball center at coordinates (100, 200).
Frame 2: Basketball center moves to coordinates (100, 180).
In this example:

prev_y_center: 200
y_center: 180
delta_y: 180 - 200 = -20

Given that self.prev_delta_y is None initially, the dribble count will not be updated in this case.

However, in subsequent frames, if the ball moves upwards significantly and then downwards by more than the dribble threshold (indicating a dribble), the dribble count will be incremented accordingly.

# TO DO:
Here i am mentioning what else we can do if a person is moving in field
1. Double Dribbles
2. Ball trajectory detection
3. travel detection of a player.(I tried but in the video provided the person is stable).