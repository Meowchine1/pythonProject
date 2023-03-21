# формирует интервал времени о τ, по истечении которого завершится обслуживание требования
import math
import random

from Condition import Condition
from Constant import lambd, queue_max_size, infinity, N
from Device import Device
from Requirement import Requirement


def random_exp():
    R = random.random()
    return (-1 / lambd) * math.log(R)

# определяет момент выполнения сегмента процесса
def next_moment(n):
    return n + random_exp()

def requirements_segment(t, device):
    requirement = Requirement()
    requirement.set_t_postyp(t)
    if device.get_Q_size() < queue_max_size:
        device.put_into_Q(requirement)
        # формирует интерфал времени (длительность интервала времени между очередными поступлениями требований)
        # по истечении которого повторится работа этого сегмента
        repeat_interval = random_exp()
        # определяется очередной момент выполнения сегмента
        device.set_s_postyp(next_moment(t))
        device.set_s_start(next_moment(t))
    # сегмент завершшает работу

def start_service_segment(t, device):
    if device.is_Q_Empty():
        device.set_s_start(infinity)
        # завершение работы сегмента
    else:
        requirement = device.take_Q_elem()
        # состояние занят
        device.set_condition(Condition.BUSY)
        requirement.set_t_start(t)
        device.set_s_end(next_moment(t))
        device.set_s_start(infinity)
        return requirement

def end_service_segment(t, device, requirement):
    requirement.set_t_end(t)
    device.put_into_Q_served(requirement)
    device.set_condition(Condition.FREE)
    device.set_s_start(next_moment(t))
    return requirement.get_t_end() - requirement.get_t_start() + requirement.get_t_start() - requirement.get_t_postyp()

# счетчик модельного времени
n_n = 0
device = Device()
requirement = Requirement()
k1 = 0
k2 = 0
k3 = 0
i = 0
while i < N:

    if device.get_s_postyp() <= i:
        requirements_segment(i, device)
        #print(1)

    if device.get_s_start() <= i:
        requirement = start_service_segment(i, device)
        #print(2)

    if device.get_s_end() <= i:
        n_n += end_service_segment(i, device, requirement)
        #print(3)
    i = next_moment(i)

u_n = device.get_Q_served_size()
print("мат ожидание числа требований в системе обслуживания", u_n, "\nмат ожидание длительности пребывания требования в системе обслуживания", n_n/u_n)
