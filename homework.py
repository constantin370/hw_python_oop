class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type,
                 duration, distance,
                 speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        string_massage = (f'Тип тренировки: {self.training_type}; '
                          f'Длительность: { self.duration:.3f} ч.; '
                          f'Дистанция: {self.distance:.3f} км; '
                          f'Ср. скорость: {self.speed:.3f} км/ч; '
                          f'Потрачено ккал: {self.calories:.3f}.')
        return string_massage


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    LEN_HAND_SWING: float = 1.38
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    SECONDS_PER_HOUR: int = 3600

    def __init__(self, action: int, duration: float, weight: float) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_time_in_min = self.duration * self.MIN_IN_H

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
        string_massage: InfoMessage = InfoMessage(self.__class__.__name__,
                                                  self.duration,
                                                  self.get_distance(),
                                                  self.get_mean_speed(),
                                                  self.get_spent_calories())
        return string_massage


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        res = (self.CALORIES_MEAN_SPEED_MULTIPLIER
               * self.get_mean_speed()
               + self.CALORIES_MEAN_SPEED_SHIFT)
        result_spent_calories = (res * self.weight / self.M_IN_KM
                                 * self.duration * self.MIN_IN_H)
        return result_spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height) -> None:
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        kmh_in_msec = ((self.get_mean_speed()
                       * self.KMH_IN_MSEC)**2) * self.CM_IN_M
        result_spent_calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                                  + (kmh_in_msec / self.height)
                                  * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                                  * self.weight) * self.training_time_in_min)
        return result_spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result_distance_swimming = (self.action
                                    * self.LEN_STEP) / self.M_IN_KM
        return result_distance_swimming

    def get_mean_speed(self):
        result_mean_speed_swimming = ((self.length_pool * self.count_pool)
                                      / self.M_IN_KM) / self.duration
        return result_mean_speed_swimming

    def get_spent_calories(self):
        result_spent_calories_swing = (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
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
    info = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
