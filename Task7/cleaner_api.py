from robot_protocol import RobotState, WATER

# класс Чистильщик API
class CleanerApi:

    # конструктор 
    def __init__(self, robot_protocol):
        self.__robot_protocol = robot_protocol
        self.cleaner_state = RobotState(0.0, 0.0, 0, WATER)

    def get_x(self):
        return self.cleaner_state.x

    def get_y(self):
        return self.cleaner_state.y

    def get_angle(self):
        return self.cleaner_state.angle

    def get_state(self):
        return self.cleaner_state.state

    def activate_cleaner(self,code):
        for command in code:
            cmd = command.split(' ')
            if cmd[0]=='move':
                self.cleaner_state = self.__robot_protocol.move(int(cmd[1]), self.cleaner_state) 
            elif cmd[0]=='turn':
                self.cleaner_state = self.__robot_protocol.turn(int(cmd[1]), self.cleaner_state)
            elif cmd[0]=='set':
                self.cleaner_state = self.__robot_protocol.set_state(cmd[1], self.cleaner_state) 
            elif cmd[0]=='start':
                self.cleaner_state = self.__robot_protocol.start(self.cleaner_state)
            elif cmd[0]=='stop':
                self.cleaner_state = self.__robot_protocol.stop(self.cleaner_state)
