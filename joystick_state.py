NUM_OF_BUTTONS = 12
NUM_OF_AXES = 6

class JoystickState:
    def __init__(self):
        self.axes = [0.0 for i in range(0, NUM_OF_AXES)]
        self.buttons = [False for i in range(0, NUM_OF_BUTTONS)]