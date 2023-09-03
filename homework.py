class InfoMessage:
    """Информационное сообщение о тренировке."""
    pass


class Training:
    """Базовый класс тренировки."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    CALORIE_LOSS_RATIO_WHEN_SWIMMING_ONE: float = 1.1
    CALORIE_LOSS_RATIO_WHEN_SWIMMING_TWO: int = 2
    RATIO_WALKING_ONE: float = 0.035
    RATIO_WALKING_TWO: float = 0.029
    LEN_STEP: float = 0.65
    LEN_HAND_SWING: float = 1.38
    M_IN_KM: int = 1000
    TIME_IN_MINUTES: int = 60
    SECONDS_PER_HOUR: int = 3600

    def __init__(self, action: int, duration: float, weight: float) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_time_in_min = self.duration * self.TIME_IN_MINUTES

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result_distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return result_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result_mean_speed = self.get_distance() / self.duration
        return result_mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        result_spent_calories_1 = (
            self.CALORIES_MEAN_SPEED_MULTIPLIER
            * self.get_mean_speed()
            + self.CALORIES_MEAN_SPEED_SHIFT)
        result_spent_calories_2 = (
            result_spent_calories_1
            * self.weight / self.M_IN_KM
            * self.training_time_in_min)
        return result_spent_calories_2

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        string_massage = (
            f'Тип тренировки: {self.__class__.__name__};'
            f'Продолжительность: { self.duration:.3f} ч.;'
            f'Дистанция: {self.get_distance():.3f} км;'
            f'Средняя скорость: {self.get_mean_speed():.3f} км/ч;'
            f'Потрачено ккал: {self.get_spent_calories():.3f}.')
        return string_massage


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        super().get_spent_calories()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int, duration: float, weight: float,
                 height) -> None:
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        meters_per_second = ((self.get_mean_speed() * self.M_IN_KM)
                             / self.SECONDS_PER_HOUR)**2
        result_spent_calories = ((self.RATIO_WALKING_ONE * self.weight
                                  + (meters_per_second / self.height)
                                  * self.RATIO_WALKING_TWO
                                  * self.weight) * self.training_time_in_min)
        return result_spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result_distance_swimming = (self.action
                                    * self.LEN_HAND_SWING) / self.M_IN_KM
        return result_distance_swimming

    def get_mean_speed(self):
        result_mean_speed_swimming = ((self.length_pool * self.count_pool)
                                      / self.M_IN_KM) / self.duration
        return result_mean_speed_swimming

    def get_spent_calories(self):
        result_spent_calories_swing = (
            (self.get_mean_speed() + self.CALORIE_LOSS_RATIO_WHEN_SWIMMING_ONE)
            * self.CALORIE_LOSS_RATIO_WHEN_SWIMMING_TWO
            * self.weight * self.duration)
        return result_spent_calories_swing


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        if workout_type == 'SWM':
            return Swimming(*data)
        if workout_type == 'RUN':
            return Running(*data)
        if workout_type == 'WLK':
            return SportsWalking(*data)
    except AttributeError:
        print('Ошибка AttributeError')


def main(training: Training) -> str:
    """Главная функция."""
    try:
        info = training.show_training_info()
        print(info)
        return info
    except AttributeError:
        print(f'\nERROR: {AttributeError}')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
