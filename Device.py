import queue

from Condition import Condition
from Constant import infinity


class Device:
    def __init__(self):
        self.condition = Condition.FREE  # в начальный момент состояние свободен
        self.t_0 = 0  # начальный момент модельного времент
        self.s_postyp = 0  # момент активации сегмента поступления
        self.s_start = infinity  # момент активации сегмента начала
        self.s_end = infinity  # момент активации сегмента завершения
        self.n_q = 0  # число требований в очереди
        self.Q = queue.LifoQueue()
        self.Q_served = queue.LifoQueue()

    def is_Q_Empty(self):
        return self.Q.empty()

    def get_Q_size(self):
        return self.Q.qsize()

    def get_Q_served_size(self):
        return self.Q_served.qsize()

    def get_Q(self):
        return self.Q

    def get_Q_served(self):
        return self.Q_served

    def put_into_Q(self, requirement):
        self.Q.put(requirement)

    def take_Q_elem(self):
        return self.Q.get()

    def take_Q_served_elem(self):
        return self.Q_served.get()

    def put_into_Q_served(self, requirement):
        self.Q_served.put(requirement)

    def get_condition(self):
        return self.condition

    def set_condition(self, condition):
        self.condition = condition

    def get_t_0(self):
        return self.t_0

    def set_t_0(self, t_0):
        self.t_0 = t_0

    def get_s_postyp(self):
        return self.s_postyp

    def set_s_postyp(self, s_postyp):
        self.s_postyp = s_postyp

    def get_s_start(self):
        return self.s_start

    def set_s_start(self, s_start):
        self.s_start = s_start

    def get_s_end(self):
        return self.s_end

    def set_s_end(self, s_end):
        self.s_end = s_end

    def get_n_q(self):
        return self.n_q

    def set_n_q(self, n_q):
        self.n_q = n_q