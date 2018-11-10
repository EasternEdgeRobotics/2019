"""Module to control the thruster using the maestro library."""

# Motor Controller limits measured in maestro units
# Values should be adjusted so that the center, stops the thrusters;
# These values typically align with the maestro settings
MIN_SPEED = 4000
CENTER_SPEED = 6000
MAX_SPEED = 8000


class Thruster:
    """Thruster class."""

    # When using motor controllers, the maestro's speed setting can be used to tune the
    # responsiveness of the robot.  Low values dampen acceleration, making for a more
    # stable robot. High values increase responsiveness, but can lead to a tippy robot.
    # Try values around 50 to 100.
    RESPONSE = 70

    def __init__(self, maestro, ch):
        """Pass the maestro controller object and the maestro channel numbers being used for the thruster's motor controller."""
        self.maestro = maestro
        self.ch = ch
        # Init thruster accel and speed parameters
        self.maestro.setAccel(ch, 0)
        self.maestro.setSpeed(ch, RESPONSE)
        # thruster min/max and center Values
        self.min_s = MIN_SPEED
        self.max_s = MAX_SPEED
        self.center_s = CENTER_SPEED

    def ThrusterScale(self, thruster):
        """Scale thruster speed(-1.0 to 1.0) to maestro servo min/center/max limits."""
        if (thruster >= 0):
            t = int(self.center_s + (self.max_s - self.center_s) * thruster)
        else:
            t = int(self.center_s + (self.center_s - self.min_s) * thruster)
        return(t)

    def Fly(self, speed):
        """
        Drive thrusters given speed parameters.

        Valid inputs range between -1.0 and 1.0.
        """
        thruster = self.ThrusterScale(speed)
        self.maestro.setTarget(self.ch, thruster)

    def Stop(self):
        """Stop the thrusters."""
        self.maestro.setTarget(self.ch, self.center_s)

    def Close(self):
        """Stop the thrusters."""
        self.Stop()
