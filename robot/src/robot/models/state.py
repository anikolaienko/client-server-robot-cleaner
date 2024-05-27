class RobotState:
    def __init__(self):
        self.name: str = None

        self.cleaning: bool = False
        self.paused: bool = False 
        self.reset: bool = False
        self._speed: int = 1

    @property
    def speed(self) -> bool:
        return self._speed
    
    @speed.setter
    def speed(self, value: int) -> None:
        if value < 1 or value > 5:
            raise ValueError("Speed should be one of the int values: 1, 2, 3, 4 or 5.")
        self._speed = value
    
    @property
    def delay(self) -> float:
        """
        Speed to delay in seconds:
            1 - 1 sec
            2 - 0.8 sec
            3 - 0.6 sec
            4 - 0.4 sec
            5 - 0.2 sec
        """
        return 0.2 * (6 - self._speed)
