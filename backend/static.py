import linecache
import numpy as np
import re
import math
from scipy import interpolate
from interval import Interval

def del_repeat(data):
    t = []
    x = []
    y = []
    for i in data[0]:
        pos = data[0].index(i)
        if i in t:
            _idx = t.index(i)
            x[_idx] = (x[_idx] + data[1][pos]) / 2
            y[_idx] = (y[_idx] + data[2][pos]) / 2
        else:
            t.append(i)
            x.append(data[1][pos])
            y.append(data[2][pos])
    return [t, x, y]

def spline(data):
        t, x, y = del_repeat(data)
        x_ipo = interpolate.splrep(t, x, k=3)
        y_ipo = interpolate.splrep(t, y, k=3)
        _t = np.linspace(t[0], t[len(t) - 1], 500)
        x_ret = interpolate.splev(_t, x_ipo)
        y_ret = interpolate.splev(_t, y_ipo)
        _t = _t.tolist()
        _x = x_ret.tolist()
        _y = y_ret.tolist()
        _len = len(t)
        stroke = []
        rmv_t = []
        for i in range(1, _len):
            slength = t[i] - t[i - 1]
            if (slength >= 100):
                stroke.append(t[i - 1])
                stroke.append(t[i])
        for i, j in grouped(stroke, 2):
            zoom = Interval(i, j)
            for k in range(len(_t)):
                if (_t[k] in zoom):
                    rmv_t.append(_t[k])
        ret_x = []
        ret_y = []
        ret_t = []
        for x, y, t in zip(_x, _y, _t):
            if (t not in rmv_t):
                ret_t.append(t)
                ret_y.append(y)
                ret_x.append(x)
        ret_x = posNormalized(ret_x)
        ret_y = posNormalized(ret_y)
        return [[], ret_x, ret_y]

def grouped(iterable, n):
    return zip(*[iter(iterable)]*n)

def posNormalized(data):
    _min = np.min(data)
    ret = []
    for i in data:
        _new = i - _min
        ret.append(_new)
    return ret

def average(lst):
    tmp = 0
    for i in lst:
        tmp += float(i)
    return round(tmp / len(lst), 2)

def biaozhuncha(lst):
    tmp = []
    for i in range(len(lst)):
        tmp.append(float(lst[i]))
    return round(np.std(tmp, ddof=1), 2)

def fenge(lst1, lst2, avg, cnt, times):
    lst1x = []
    lst1y = []
    lst2x = []
    lst2y = []
    lst3x = []
    lst3y = []
    lst4x = []
    lst4y = []
    average1 = average(lst1)
    average2 = average(lst2)
    avg.append("(" + str(average1) + "," + str(average2) + ")")
    for i in range(len(lst1)):
        if float(lst1[i]) < average1 and float(lst2[i]) < average2:
            lst3x.append(lst1[i])
            lst3y.append(lst2[i])
        elif float(lst1[i]) < average1 and float(lst2[i]) > average2:
            lst1x.append(lst1[i])
            lst1y.append(lst2[i])
        elif float(lst1[i]) > average1 and float(lst2[i]) > average2:
            lst2x.append(lst1[i])
            lst2y.append(lst2[i])
        elif float(lst1[i]) > average1 and float(lst2[i]) < average2:
            lst4x.append(lst1[i])
            lst4y.append(lst2[i])
    if cnt != times:
        cnt += 1
        if len(lst1x) != 0:
            fenge(lst1x, lst1y, avg, cnt, times)
        if len(lst2x) != 0:
            fenge(lst2x, lst2y, avg, cnt, times)
        if len(lst3x) != 0:
            fenge(lst3x, lst3y, avg, cnt, times)
        if len(lst4x) != 0:
            fenge(lst4x, lst4y, avg, cnt, times)

def distance(dis, avg):
    for i in range(len(avg) - 1):
        for j in range(i + 1, len(avg)):
            x1 = float(re.findall(r"\d+\.?\d*", avg[i])[0])
            y1 = float(re.findall(r"\d+\.?\d*", avg[i])[1])
            x2 = float(re.findall(r"\d+\.?\d*", avg[j])[0])
            y2 = float(re.findall(r"\d+\.?\d*", avg[j])[1])
            distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            dis.append(str(distance))

def turn_to_float(lst):
    for i in range(len(lst)):
        lst[i] = float(lst[i])
    return lst

def deal(data_path, times):
    count = len(open(data_path, 'rU').readlines())
    info = []
    for i in range(count / 3):
        avg = []
        dis = []
        cnt = 0
        str_t = linecache.getline(data_path, 1 + 3 * i)
        str1 = linecache.getline(data_path, 2 + 3 * i)
        str2 = linecache.getline(data_path, 3 + 3 * i)
        t = str_t.split(',')
        x = str1.split(',')
        y = str2.split(',')
        t.pop()
        x.pop()
        y.pop()
        t = turn_to_float(t)
        x = turn_to_float(x)
        y = turn_to_float(y)
        data = [t, x, y]
        t, lst1, lst2 = spline(data)
        fenge(lst1, lst2, avg, cnt, times)
        distance(dis, avg)
        info.append(dis)
    return info

def train(train_path, times):
    a = 3
    info_max = []
    info_min = []
    info = deal(train_path, times)
    for i in range(len(info[0])):
        tmp = []
        for j in range(len(info)):
            tmp.append(info[j][i])
        info_min.append(round((average(tmp) - a * biaozhuncha(tmp)), 2))
        info_max.append(round((average(tmp) + a * biaozhuncha(tmp)), 2))
    return info_min, info_max

def test(test_path, info_min, info_max, times):
    R = []
    F = []
    result = []
    test = deal(test_path, times)
    for data in test:
        tmp_R = 0
        tmp_F = 0
        for i in range(len(data)):
            if float(data[i]) >= info_min[i] and float(data[i]) <= info_max[i]:
                tmp_R += 1
            else:
                tmp_F += 1
        R.append(tmp_R)
        F.append(tmp_F)
    for i in range(len(test)):
        tmp = float(R[i]) / (R[i] + F[i])
        result.append(tmp)
    print result

def main():
    train_path = '/Users/qiqi/Downloads/data(2).txt'
    test_path = '/Users/qiqi/Downloads/data(1).txt'
    times = 5
    info_min, info_max = train(train_path, times)
    test(test_path, info_min, info_max, times)

if __name__ == '__main__':
    main()
