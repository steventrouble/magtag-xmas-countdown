from adafruit_datetime import datetime, time, timedelta


def get_next(now, day_sched):
    if not day_sched:
        return None
    now_time = now.time()
    for i in day_sched:
        if now_time < i:
            return datetime.combine(now, i)
    else:
        return datetime.combine(now + timedelta(days=1), day_sched[0])


def gen_schedule():
    sched = {}
    for r in ["31N", "33S"]:
        sched[r] = {}
        for i in ["MF", "Sa", "Su"]:
            sched[r][i] = []

    sched["31N"]["MF"] = gen_31n_mf()
    sched["31N"]["Sa"] = gen_31n_weekend()
    sched["31N"]["Su"] = gen_31n_weekend()
    sched["33S"]["MF"] = gen_33s_mf()
    sched["33S"]["Sa"] = gen_33s_sa()
    sched["33S"]["Su"] = gen_33s_su()
    return sched


def gen_31n_mf():
    s = []
    for i in [6, 7, 9, 10, 11, 12, 13, 14, 18, 19, 20, 21]:
        s.append(time(i, 22))
        s.append(time(i, 52))
    s += [
        time(5, 52),
        time(8, 15),
        time(8, 30),
        time(8, 52),
        time(15, 21),
        time(16, 6),
        time(16, 21),
        time(16, 36),
        time(17, 6),
        time(17, 21),
        time(17, 36),
        time(17, 51),
    ]
    s.sort()
    return s


def gen_31n_weekend():
    s = []
    for i in range(7, 22):
        s.append(time(i, 22))
        s.append(time(i, 52))
    s.append(time(6, 53))
    s.sort()
    return s


def gen_33s_mf():
    s = []
    for i in [9, 10, 11, 12, 13, 14, 15, 16]:
        s.append(time(i, 13))
        s.append(time(i, 44))
    s += [
        time(5, 17),
        time(5, 47),
        time(6, 31),
        time(7, 10),
        time(7, 10),
        time(7, 44),
        time(7, 59),
        time(8, 15),
        time(8, 40),
        time(17, 12),
        time(17, 43),
        time(18, 7),
        time(18, 41),
        time(19, 13),
        time(19, 39),
        time(20, 9),
        time(20, 39),
    ]
    s.sort()
    return s


def gen_33s_sa():
    s = [
        time(6, 33),
        time(7, 33),
        time(8, 33),
        time(9, 2),
        time(9, 32),
        time(10, 2),
        time(10, 28),
        time(10, 58),
        time(11, 28),
        time(11, 58),
        time(12, 28),
        time(12, 58),
        time(13, 28),
        time(13, 58),
        time(14, 32),
        time(15, 2),
        time(15, 32),
        time(16, 2),
        time(16, 32),
        time(17, 1),
        time(17, 31),
        time(18, 1),
        time(18, 28),
        time(19, 26),
        time(20, 28),
    ]
    return s


def gen_33s_su():
    s = []
    for i in range(6, 21):
        s.append(time(i, 26))
    return s
