# Финальный проект спринта: модуль фитнес-трекера
from dataclasses import asdict, dataclass


@dataclass(init=True, repr=False,
           eq=False, order=False,
           unsafe_hash=False, frozen=False,
           kw_only=False,
           slots=False)
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Выводим информацию о тренировке."""
        message_print = self.MESSAGE.format(**asdict(self))
        return message_print


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    SECONDS_PER_HOUR: int = 3600

    def __init__(self, action: int, duration: float, weight: float) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result_distance: float = (self.action * self.LEN_STEP) / self.M_IN_KM
        return result_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result_mean_speed: float = self.get_distance() / self.duration
        return result_mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        self.get_mean_speed()
        self.weight
        self.M_IN_KM
        self.duration
        self.MIN_IN_H

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        show_message: InfoMessage = InfoMessage(type(self).__name__,
                                                self.duration,
                                                self.get_distance(),
                                                self.get_mean_speed(),
                                                self.get_spent_calories())
        return show_message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        result_spent_calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                        * self.get_mean_speed()
                                        + self.CALORIES_MEAN_SPEED_SHIFT)
                                        * self.weight / self.M_IN_KM
                                        * self.duration * self.MIN_IN_H)
        return result_spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        kmh_in_msec: float = ((self.get_mean_speed()
                               * self.KMH_IN_MSEC)**2) * self.CM_IN_M
        result_spent_calories: float = (
            (self.CALORIES_WEIGHT_MULTIPLIER
             * self.weight + (kmh_in_msec / self.height)
             * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
             * self.weight) * (self.duration
                               * self.MIN_IN_H))
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

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""
        result_mean_speed_swimming: float = (
            (self.length_pool * self.count_pool)
            / self.M_IN_KM) / self.duration
        return result_mean_speed_swimming

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        result_spent_calories_swing: float = (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight * self.duration)
        return result_spent_calories_swing


def read_package(workout_type: str, data: list[int]) -> Training:
    training_type: dict[str, type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    if workout_type in training_type:
        return training_type[workout_type](*data)


def check_data(data: list) -> list:
    """Функция проверки и перевода данных c str во float."""
    # На случай если в packages придет число в виде
    # строки или же вообще не понятно что.
    try:
        numbers_in_the_list: list[float] = ([float(element_checking)
                                             for element_checking in data])
        return numbers_in_the_list
    except ValueError:
        print(f'ERROR {ValueError}')
        exit()


def main(training: Training) -> str:
    """Главная функция."""
    try:
        info = training.show_training_info()
        print(info.get_message())
        return info.get_message()
    except AttributeError:
        print(f'ERROR {AttributeError}')


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        check: list = check_data(data)
        training: dict[str, list[float]] = read_package(workout_type, check)
        main(training)
