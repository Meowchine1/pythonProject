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
    global N_requirement, device, fail_req
    requirement = Requirement() # создает новое требовани
    if device.get_Q_size() < queue_max_size:  # проверка наличия места в очереди
        requirement.set_t_postyp(t) # наделяет это требование значениями атрибутов
        device.put_into_Q(requirement) # ставит требование в очередь
        N_requirement += 1
        #device.set_s_start(next_moment(t, nu)) # nu
    # иначе отказ в обслуживании
    device.set_s_postyp(next_moment(t, lambd)) # определяет очередной момент выполнения сегмента процесса
    fail_req += 1


def set_start_segment(t):
    if not device.is_Q_Empty():
        device.set_s_start(next_moment(t, nu))  # nu
    else:
        device.set_s_start(infinity)

def start_service_segment(t):
    global device
    if device.is_Q_Empty():  # Если очередь Q пуста
        device.set_s_start(infinity) # сегмент завершает свою работу
    elif device.get_condition() != Condition.Condition.BUSY:  # если устройство не занято
        requirement = device.take_Q_elem()  # удалили из очереди задачу
        device.set_condition(Condition.Condition.BUSY) # переводит прибор в состояние «занят»
        requirement.set_t_start(t) # наделяет выбранное требование значениями атрибутов

        device.set_s_end(next_moment(t, nu)) # момент выполнения сегмента процесса, связанного с уходом требования
        device.set_s_start(infinity)  # момент активизации сегмента начала устанавливается в бесконечность
        device.set_actual_requirement(requirement) # требование над которым будет работать сегмент процесса
    else:
        device.set_s_start(infinity) # если устройство занято, то завершаем процесс. Ждем момента от сегмента завершения

def end_service_segment(t):
    global N_requirement, device

    requirement = device.get_actual_requirement()
    requirement.set_t_end(t) # изменяет значения атрибутов требования
    device.put_into_Q_served(requirement) # ставит требование, завершившее обслуживание, в очередь
    N_requirement -= 1
    device.set_condition(Condition.Condition.FREE) # переводит прибор в состояние «свободен»
    device.set_s_start(t) #активизируется сегмента процесса начала обслуживания
    device.set_s_end(infinity) # сегмент ухода завершает работу
    return requirement.get_t_end() - requirement.get_t_start() + requirement.get_t_start() - requirement.get_t_postyp()


# счетчик модельного времени
n_n = 0
device = Device()
N_requirement = 0
fail_req = 0

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
        interval_3_start = redirect_timer(interval_2_start, interval_2_end, interval_2, interval_4_start,
                                    interval_4_end, interval_4, interval_3_start, i)

    elif N_requirement == 4:
        interval_3_start, interval_3_end, interval_3, interval_5_start, interval_5_end, interval_5, \
        interval_4_start = redirect_timer(interval_3_start, interval_3_end, interval_3, interval_5_start,
                                    interval_5_end, interval_5, interval_4_start, i)

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

    if (device.get_s_start() < i) | (device.get_s_start() == infinity):  # лишние установки времени
        set_start_segment(i)

######################################################################################################

K = device.get_Q_served_size()
T = i
mat_exp = 1/T
q = device.get_Q_served()
sum_ = 0
while not q.empty():
  end = q.get().get_t_end()
  queue_moment = q.get().get_t_start()
  sum_ += (end - queue_moment)

print("оценка математического ожидания длительности пребывания требований в системе обслуживания =", sum_ / K)


interval1_sum = sum(interval_1) / T
interval2_sum = sum(interval_2) / T
interval3_sum = sum(interval_3) / T
interval4_sum = sum(interval_4) / T
interval5_sum = sum(interval_5) / T

n_ = interval1_sum + 2 * interval2_sum + 3 * interval3_sum + 4 * interval4_sum + 5 * interval5_sum

print("оценка математического ожидания числа требований в системе обслуживания =", n_)



print("вероятность отказа в обслуживании требования =", (fail_req / K)  )