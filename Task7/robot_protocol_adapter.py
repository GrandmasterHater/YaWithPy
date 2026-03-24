# Чтобы не менять pure_robot прокидываю функции через адаптер.
import pure_robot
import robot_protocol

class RobotAdapter:
    def transfer_to_cleaner(self, message): 
        return pure_robot.transfer_to_cleaner(message)

    # перемещение
    def move(self, dist, state): 
        return pure_robot.move(pure_robot.transfer_to_cleaner, dist, state)

    # поворот
    def turn(self, turn_angle, state): 
        return pure_robot.turn(pure_robot.transfer_to_cleaner, turn_angle, state)

    # установка режима работы
    def set_state(self, new_internal_state, state): 
        return pure_robot.set_state(pure_robot.transfer_to_cleaner, new_internal_state, state)

    # начало чистки
    def start(self, state): 
        return pure_robot.start(pure_robot.transfer_to_cleaner, state)

    # конец чистки
    def stop(self, state): 
        return pure_robot.stop(pure_robot.transfer_to_cleaner, state)

    # интерпретация набора команд
    def make(self, code, state): 
        return pure_robot.make(pure_robot.transfer_to_cleaner, code, state)