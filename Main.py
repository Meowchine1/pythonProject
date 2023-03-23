# формирует интервал времени о τ, по истечении которого завершится обслуживание требования
import math
import random

import Condition
from Constant import *
from Device import Device
from Requirement import Requirement


def random_exp(coef):
    R = random.random()
    return (-1 / coef) * math.log(R)


# определяет момент выполнения сегмента процесса
def next_moment(n, coef):
    return n + random_exp(coef)


def requirements_segment(t):
    global N_requirement, device
    requirement = Requirement()
    if device.get_Q_size() < queue_max_size:
        requirement.set_t_postyp(t)
        device.put_into_Q(requirement)
        N_requirement += 1
        # формирует интерфал времени (длительность интервала времени между очередными поступлениями требований)
        # по истечении которого повторится работа этого сегмента
        # определяется очередной момент выполнения сегмента
        device.set_s_postyp(next_moment(t, lambd))
        device.set_s_start(next_moment(t, nu)) # nu
    # сегмент завершшает работу


def start_service_segment(t):
    global device
    if device.is_Q_Empty():
        device.set_s_start(infinity)
        # завершение работы сегмента
    elif device.get_condition() != Condition.Condition.BUSY:
        requirement = device.take_Q_elem()  # удалили из очереди задачу
        # состояние занят
        device.set_condition(Condition.Condition.BUSY)
        requirement.set_t_start(t)
        device.set_s_end(next_moment(t, nu))
        device.set_s_start(infinity)
        device.set_actual_requirement(requirement)
    else:
        device.set_s_start(next_moment(t, nu))

def end_service_segment(t):
    global N_requirement, device
    # export from queue
    requirement = device.get_actual_requirement()
    requirement.set_t_end(t)
    device.put_into_Q_served(requirement)
    N_requirement -= 1
    device.set_condition(Condition.Condition.FREE)
    device.set_s_start(next_moment(t, nu))
    device.set_s_end(infinity)
    return requirement.get_t_end() - requirement.get_t_start() + requirement.get_t_start() - requirement.get_t_postyp()


# счетчик модельного времени
n_n = 0
device = Device()
N_requirement = 0

interval_0_start = infinity
interval_0_end = infinity
interval_1_start = infinity
interval_1_end = infinity
interval_2_start = infinity
interval_2_end = infinity
interval_3_start = infinity
interval_3_end = infinity
interval_4_start = infinity
interval_4_end = infinity
interval_5_start = infinity
interval_5_end = infinity

interval_0 = []
interval_1 = []
interval_2 = []
interval_3 = []
interval_4 = []
interval_5 = []
i = 0


def saveInterval(interval_list, interval_start, interval_end):
    interval_list.append(interval_end - interval_start)
    interval_start = infinity
    interval_end = infinity
    return interval_list, interval_start, interval_end

def redirect_timer(interval_0_start, interval_0_end, interval_0_list,
                   interval_1_start, interval_1_end, interval_1_list,
                   interval_2_start, i):
    if interval_0_start != infinity:
        interval_0_end = i
        interval_0_list, interval_0_start, interval_0_end = saveInterval(interval_0_list, interval_0_start, interval_0_end)

    elif interval_1_start != infinity:
        interval_1_end = i
        interval_1_list, interval_1_start, interval_1_end = saveInterval(interval_1_list, interval_1_start, interval_1_end)

    if interval_2_start == infinity:
        interval_2_start = i
    # иначе продолжаем счет интервала
    return interval_0_start, interval_0_end, interval_0_list, interval_1_start, \
           interval_1_end, interval_1_list, interval_2_start

def time_fixation(i):
    global interval_0_start, interval_0_end, interval_0, interval_1_start, interval_1_end, interval_1, \
        interval_2_start, interval_2_end, interval_2, interval_3_start, interval_3_end, interval_3, \
        interval_4_start, interval_4_end, interval_4, interval_5_start, interval_5_end, interval_5, N_requirement
    if N_requirement == 0:
        if interval_0_start == infinity:
            interval_0_start = i
            if len(interval_0) > 0:
                interval_1_end = i
                saveInterval(interval_1, interval_1_start, interval_1_end)
        # иначе продолжаем счет для нулевого интервала

    elif N_requirement == 1:
        interval_0_start, interval_0_end, interval_0, interval_2_start, interval_2_end, interval_2, \
        interval_1_start = redirect_timer(interval_0_start, interval_0_end, interval_0, interval_2_start,
                                          interval_2_end, interval_2, interval_1_start, i)

    elif N_requirement == 2:
        interval_1_start, interval_1_end, interval_1, interval_3_start, interval_3_end, interval_3, \
        interval_2_start = redirect_timer(interval_1_start, interval_1_end, interval_1,  interval_3_start,
                                          interval_3_end, interval_3, interval_2_start, i)

    elif N_requirement == 3:
        interval_2_start, interval_2_end, interval_2, interval_4_start, interval_4_end, interval_4, \
        interval_3 = redirect_timer(interval_2_start, interval_2_end, interval_2, interval_4_start,
                                    interval_4_end, interval_4, interval_3, i)

    elif N_requirement == 4:
        interval_3_start, interval_3_end, interval_3, interval_5_start, interval_5_end, interval_5, \
        interval_4 = redirect_timer(interval_3_start, interval_3_end, interval_3, interval_5_start,
                                    interval_5_end, interval_5, interval_4, i)

    elif N_requirement == 5:
        if interval_5_start == infinity:
            interval_5_start = i
            interval_4_end = i
            interval_4, interval_4_start, interval_4_end = saveInterval(interval_4, interval_4_start, interval_4_end)
    # return interval_0_start, interval_0_end, interval_0, interval_1_start, interval_1_end, interval_1, \
    #               interval_2_start, interval_2_end, interval_2, interval_3_start, interval_3_end, interval_3, \
    #               interval_4_start, interval_4_end, interval_4, interval_5_start, interval_5_end, interval_5, N_requirement


while device.get_Q_served_size() < N:
    i = min(device.get_s_postyp(), device.get_s_start(), device.get_s_end())
    time_fixation(i)

    if device.get_s_postyp() == i:
        requirements_segment(i)

    if device.get_s_start() == i:
        start_service_segment(i)

    if device.get_s_end() == i:
        n_n += end_service_segment(i)

K = device.get_Q_served_size()
print(interval_1)