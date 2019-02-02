
class pid:
    def __init__(self):
        self.kP = 0.0
        self.kI = 0.0
        self.kD = 0.0
        self.target = 0.0
        self.error = 0.0
        self.integral = 0.0
        self.derivative = 0.0
        self.last_error = 0.0
