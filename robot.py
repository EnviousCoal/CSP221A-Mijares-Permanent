import abc
import logging
import functools

def log_action(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        logging.info(f"{self.name}: starting {func.__name__}")
        result = func(self, *args, **kwargs)
        logging.info(f"{self.name}: finished {func.__name__}")
        return result
    return wrapper

logging.basicConfig(level=logging.INFO)
def run_task_safely(robot, **kwargs):
    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as e:
        logging.error(str(e))
    else:
        print(result)
    finally:
        print(f"{robot.name} battery is now {robot.battery}%.")
    
class InsufficientBatteryError(Exception):
    def __init__(self, name, required, available):
        self.name = name
        self.required = required
        self.available = available
        message = f"{name} needs {required}% battery for this task but only has {available}%."
        super().__init__(message)

class Robot(abc.ABC):
    manufacturer = "Nova Robotics"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self._battery = 0
        self.battery = battery
        Robot.population += 1

    def use_battery(self, amount):
        if amount > self.battery:
            raise InsufficientBatteryError(self.name, amount, self.battery)
        self.battery -= amount

    @classmethod
    def from_config(cls, config):
        return cls(**config)
    
    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        self._battery = value

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', battery={self.battery})"

    @abc.abstractmethod
    def perform_task(self):
        pass

class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=50):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity
    
    @log_action
    def perform_task(self):
        self.use_battery(8)
        return f"{self.name} vacuumed the living room."
       

class DroneRobot(Robot):
    def __init__(self, name, battery=100, max_altitude=120):
        super().__init__(name, battery)
        self.max_altitude = max_altitude

    def perform_task(self):
        self.use_battery(15)
        return f"{self.name} completed a delivery flight."

def fleet_report(robots):
    for robot in robots:
        print(str(robot))
