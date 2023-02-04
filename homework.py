class InfoMessage:
    """Informational message about the training."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность:{self.duration: .3f} ч.; '
                f'Дистанция:{self.distance: .3f} км; '
                f'Ср. скорость:{self.speed: .3f} км/ч; '
                f'Потрачено ккал:{self.calories: .3f}.')


class Training:
    """Basic training class."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Got the distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Got an average speed of movement."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Got the number of calories consumed."""
        raise NotImplementedError(f'Переопределите метод get_spend_calories '
                                  f'в {type(self).__name__}')

    def show_training_info(self) -> InfoMessage:
        """We return an informational message about the completed training."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Training: running."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        TIME_IN_MIN = self.duration * self.MIN_IN_H
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * TIME_IN_MIN)


class SportsWalking(Training):
    """Training: sports walking."""
    COEF_1: float = 0.035
    COEF_2: float = 0.029
    KM_IN_MS = 0.278
    SM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        HEIGHT_IN_M = self.height / self.SM_IN_M
        MS = self.get_mean_speed() * self.KM_IN_MS
        TIME_IN_MIN = self.duration * self.MIN_IN_H
        return (((self.COEF_1 * self.weight
                  + (MS**2 / HEIGHT_IN_M)
                  * self.COEF_2 * self.weight) * TIME_IN_MIN))


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP: float = 1.38
    COEF_3: float = 1.1
    COEF_4: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEF_3) * self.COEF_4
                * self.weight * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Read the data received from the sensors."""
    training_type: dict(str, Training) = {'SWM': Swimming,
                                          'RUN': Running,
                                          'WLK': SportsWalking}
    if workout_type not in training_type.keys():
        raise ValueError('Unknown type of training.')
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """The main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
