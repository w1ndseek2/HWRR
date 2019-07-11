from dtw import dtw
import numpy as np
import math
from matplotlib import pyplot
from scipy import interpolate
from interval import Interval

# class handleList():
#     @staticmethod
#     def simple_select(lst):
#         split = []
#         for i in range(1, len(lst) - 1):
#             if lst[i - 1] < lst[i] and lst[i + 1] < lst[i]:
#                 split.append((1, i))
#             if lst[i - 1] > lst[i] and lst[i + 1] > lst[i]:
#                 split.append((2, i))
#         return split

#     @staticmethod
#     def simple_dtw(r, t):
#         split1, split2 = handleList.simple_select(r), handleList.simple_select(
#             t)
#         f = lambda lst: [i[1] for i in lst]
#         g = lambda idx, l: [l[i] for i in idx]
#         # pyplot.subplot(2, 1, 1)
#         # handleList.draw(r, f(split1))
#         # pyplot.subplot(2, 1, 2)
#         # handleList.draw(t, f(split2))
#         x = g(f(split1), r)
#         y = g(f(split2), t)
#         # print(x, y)
#         d = dtw(
#             np.array(x).reshape(-1, 1),
#             np.array(y).reshape(-1, 1), lambda x, y: np.abs(x - y))
#         return d[0] / len(d[-1])

#     @staticmethod
#     def split_dtw(r, t):
#         split1, split2 = QiQi.fenge(r, t)
#         # f = lambda lst: [i[1] for i in lst]
#         g = lambda idx, l: [l[i] for i in idx]
#         # pyplot.subplot(2, 1, 1)
#         # handleList.draw(r, split1)
#         # pyplot.subplot(2, 1, 2)
#         # handleList.draw(t, split2)
#         x = g(split1, r)
#         y = g(split2, t)
#         # print(x, y)
#         d = dtw(
#             np.array(x).reshape(-1, 1),
#             np.array(y).reshape(-1, 1), lambda x, y: np.abs(x - y))

#         return d[0] / len(d[-1])

#     @staticmethod
#     def section_dtw(r, t):
#         split1, split2 = QiQi.fenge(r, t)
#         # print(split1, split2, len(r), len(t))
#         idx1 = 0
#         idx2 = 0
#         d = 0
#         for i in range(len(split1)):
#             x = r[idx1:split1[i]]
#             y = t[idx2:split2[i]]
#             ans = dtw(
#                 np.array(x).reshape(-1, 1),
#                 np.array(y).reshape(-1, 1), lambda x, y: np.abs(x - y))
#             d += ans[0] / len(ans[-1])
#             idx1 = split1[i]
#             idx2 = split2[i]
#         return d / (len(split1) + 1)

#     @staticmethod
#     def draw(lst, split):
#         f = lambda lst: [i for i in range(len(lst))]
#         g = lambda idx, l: [l[i] for i in idx]
#         pyplot.plot(f(lst), lst)
#         pyplot.plot(f(lst), lst, 'r.')
#         pyplot.plot(split, g(split, lst), 'g*')

#     @staticmethod
#     def search(lst):
#         for i in range(5, len(lst)):
#             try:
#                 if lst[i] >= lst[i - 5] and lst[i] >= lst[
#                         i - 4] and lst[i] >= lst[i - 3] and lst[i] >= lst[
#                             i - 2] and lst[i] >= lst[i - 1] and lst[i] >= lst[
#                                 i + 1] and lst[i] >= lst[i + 2] and lst[
#                                     i] >= lst[i + 3] and lst[i] >= lst[
#                                         i + 4] and lst[i] >= lst[i + 5]:
#                     flag = 1
#                     return i, flag
#                 elif lst[i] <= lst[i - 5] and lst[i] <= lst[
#                         i - 4] and lst[i] <= lst[i - 3] and lst[i] <= lst[
#                             i - 2] and lst[i] <= lst[i - 1] and lst[i] <= lst[
#                                 i + 1] and lst[i] <= lst[i + 2] and lst[
#                                     i] <= lst[i + 3] and lst[i] <= lst[
#                                         i + 4] and lst[i] <= lst[i + 5]:
#                     flag = 0
#                     return i, flag
#             except:
#                 return False

#     @staticmethod
#     def adjust(x1, x2, fengedian1, fengedian2, lst1, lst2, tmp1, tmp2, flag1,
#                flag2):
#         point1, flag1 = handleList.search(tmp1)
#         point2, flag2 = handleList.search(tmp2)
#         x1 += point1 + 1
#         x2 += point2 + 1
#         if len(fengedian1) == 0:
#             tmp1 = lst1[0:x1 + 1]
#             tmp2 = lst2[0:x2 + 1]
#         else:
#             tmp1 = lst1[fengedian1[-1] + 1:x1 + 1]
#             tmp2 = lst2[fengedian2[-1] + 1:x2 + 1]
#         distance = abs(tmp1[-1] - tmp2[-1])
#         if len(tmp1) > len(tmp2) and flag2 == 1:
#             x = x1
#             while x > x1 + 2 - len(tmp1):
#                 x -= 1
#                 if lst1[x] >= lst1[x - 1] and lst1[x] >= lst1[x + 1] and abs(
#                         lst1[x] - lst2[x2]) < distance:
#                     x1 = x
#                     break
#         elif len(tmp1) < len(tmp2) and flag1 == 1:
#             x = x2
#             while x > x2 + 2 - len(tmp2):
#                 x -= 1
#                 if lst2[x] >= lst2[x - 1] and lst2[x] >= lst2[x + 1] and abs(
#                         lst1[x1] - lst2[x]) < distance:
#                     x2 = x
#                     break
#         elif len(tmp1) > len(tmp2) and flag2 == 0:
#             x = x1
#             while x > x1 + 2 - len(tmp1):
#                 x -= 1
#                 if lst1[x] <= lst1[x - 1] and lst1[x] <= lst1[x + 1] and abs(
#                         lst1[x] - lst2[x2]) < distance:
#                     x1 = x
#                     break
#         elif len(tmp1) < len(tmp2) and flag1 == 0:
#             x = x2
#             while x > x2 + 2 - len(tmp2):
#                 x -= 1
#                 if lst2[x] <= lst2[x - 1] and lst2[x] <= lst2[x + 1] and abs(
#                         lst1[x1] - lst2[x]) < distance:
#                     x2 = x
#                     break
#         fengedian1.append(x1)
#         fengedian2.append(x2)
#         return x1, x2

#     @staticmethod
#     def reselect(lst1, lst2):
#         fengedian1 = []
#         fengedian2 = []
#         x1 = -1
#         x2 = -1
#         flag1 = 0
#         flag2 = 0
#         while (handleList.search(lst1[x1 + 1:])
#                and handleList.search(lst2[x2 + 1:])):
#             tmp1 = lst1[x1 + 1:]
#             tmp2 = lst2[x2 + 1:]
#             x1, x2 = handleList.adjust(x1, x2, fengedian1, fengedian2, lst1,
#                                        lst2, tmp1, tmp2, flag1, flag2)
#         return fengedian1, fengedian2

#     @staticmethod
#     def show_select_dtw(r, t):
#         split1, split2 = QiQi.fenge(r, t)
#         pyplot.subplot(2, 1, 1)
#         handleList.draw(r, split1)
#         pyplot.subplot(2, 1, 2)
#         handleList.draw(t, split2)

#     @staticmethod
#     def show_reslect1_dtw(r, t):
#         split1, split2 = handleList.reselect(r, t)
#         pyplot.subplot(2, 1, 1)
#         handleList.draw(r, split1)
#         pyplot.subplot(2, 1, 2)
#         handleList.draw(t, split2)

#     @staticmethod
#     def show_reslect2_dtw(r, t):
#         split1, split2 = QiQi2.fenge(r, t)
#         pyplot.subplot(2, 1, 1)
#         handleList.draw(r, split1)
#         pyplot.subplot(2, 1, 2)
#         handleList.draw(t, split2)


class PreProcess():
    @staticmethod
    def preprocess(lst):
        ret = []
        t = np.mean(lst)
        for i in lst:
            ret.append(i - t)
        return np.array(ret).reshape(-1, 1)

    @staticmethod
    def grouped(iterable, n):
        return zip(*[iter(iterable)] * n)

    @staticmethod
    def posNormalized(data):
        _min = np.mean(data)
        ret = []
        for i in data:
            _new = i - _min
            ret.append(_new)
        return ret

    @staticmethod
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

    @staticmethod
    def spline(data):
        t, x, y = del_repeat(data)
        x_ipo = interpolate.splrep(t, x, k=3)
        y_ipo = interpolate.splrep(t, y, k=3)
        _t = np.linspace(t[0], t[len(t) - 1], 500)
        # _t = np.arange(t[0], t[len(t) - 1], 10)
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


class ImprovedSplit():
    @staticmethod
    def is_jida(lst, i):
        if lst[i] >= lst[i - 5] and lst[i] >= lst[i - 4] and lst[i] >= lst[
                i - 3] and lst[i] >= lst[i - 2] and lst[i] >= lst[
                    i - 1] and lst[i] >= lst[i + 1] and lst[i] >= lst[
                        i + 2] and lst[i] >= lst[i + 3] and lst[i] >= lst[
                            i + 4] and lst[i] >= lst[i + 5]:
            return 1

    @staticmethod
    def is_jixiao(lst, i):
        if lst[i] <= lst[i - 5] and lst[i] <= lst[i - 4] and lst[i] <= lst[
                i - 3] and lst[i] <= lst[i - 2] and lst[i] <= lst[
                    i - 1] and lst[i] <= lst[i + 1] and lst[i] <= lst[
                        i + 2] and lst[i] <= lst[i + 3] and lst[i] <= lst[
                            i + 4] and lst[i] <= lst[i + 5]:
            return 1

    @staticmethod
    def search(lst):
        for i in range(5, len(lst)):
            try:
                if is_jida(lst, i):
                    flag = 1
                    return i, flag
                elif is_jixiao(lst, i):
                    flag = 0
                    return i, flag
            except:
                return False

    @staticmethod
    def fengedian(x, tmp):
        point, flag = search(tmp)
        x += point + 1
        return x, flag

    @staticmethod
    def adjust(x1, x2, fengedian1, fengedian2, lst1, lst2, tmp1, tmp2, flag1,
               flag2):
        # point1, flag1 = search(tmp1)
        # point2, flag2 = search(tmp2)
        # x1 += point1+1
        # x2 += point2+1
        if len(fengedian1) == 0:
            tmp1 = lst1[0:x1 + 1]
            tmp2 = lst2[0:x2 + 1]
        else:
            tmp1 = lst1[fengedian1[-1] + 1:x1 + 1]
            tmp2 = lst2[fengedian2[-1] + 1:x2 + 1]
        distance = abs(tmp1[-1] - tmp2[-1])
        if len(tmp1) >= len(tmp2) and flag2 == 1:
            x = x1
            is_lst1_long = 1
            while x > x1 + 2 - len(tmp1):
                # print 'lst1 long, adjust x1: ', x1, x
                x -= 1
                if lst1[x] >= lst1[x - 1] and lst1[x] >= lst1[x + 1] and abs(
                        lst1[x] - lst2[x2]) < distance:
                    x1 = x
                    break
        elif len(tmp1) < len(tmp2) and flag1 == 1:
            x = x2
            is_lst1_long = 0
            while x > x2 + 2 - len(tmp2):
                # print 'lst2 long, adjust x2: ', x2, x
                x -= 1
                if lst2[x] >= lst2[x - 1] and lst2[x] >= lst2[x + 1] and abs(
                        lst1[x1] - lst2[x]) < distance:
                    x2 = x
                    break
        elif len(tmp1) >= len(tmp2) and flag2 == 0:
            x = x1
            is_lst1_long = 1
            while x > x1 + 2 - len(tmp1):
                # print 'lst1 long, adjust x1: ', x1, x
                x -= 1
                if lst1[x] <= lst1[x - 1] and lst1[x] <= lst1[x + 1] and abs(
                        lst1[x] - lst2[x2]) < distance:
                    x1 = x
                    break
        elif len(tmp1) < len(tmp2) and flag1 == 0:
            x = x2
            is_lst1_long = 0
            while x > x2 + 2 - len(tmp2):
                # print 'lst2 long, adjust x2: ', x2, x
                x -= 1
                if lst2[x] <= lst2[x - 1] and lst2[x] <= lst2[x + 1] and abs(
                        lst1[x1] - lst2[x]) < distance:
                    x2 = x
                    break
        # fengedian1.append(x1)
        # fengedian2.append(x2)
        return x1, x2, is_lst1_long

    @staticmethod
    def split(lst1, lst2):
        fengedian1 = []
        fengedian2 = []
        x1 = -1
        x2 = -1
        flag1 = 0
        flag2 = 0
        avg_dis = abs(np.mean(lst1) - np.mean(lst2))
        while (search(lst1[x1 + 1:]) and search(lst2[x2 + 1:])):
            tmp1 = lst1[x1 + 1:]
            tmp2 = lst2[x2 + 1:]
            x1, flag1 = fengedian(x1, tmp1)
            split1 = x1
            x2, flag2 = fengedian(x2, tmp2)
            split2 = x2
            is_break = 0
            if (abs(x1 - x2) > avg_dis):
                x1, x2, is_lst1_long = adjust(x1, x2, fengedian1, fengedian2,
                                              lst1, lst2, tmp1, tmp2, flag1,
                                              flag2)
                while (is_lst1_long == 1 and x1 == split1):
                    # print 'lst1 long: ', x1, x2
                    tmp2 = lst2[x2 + 1:]
                    if not search(tmp2):
                        is_break = 1
                        break
                    x2, flag2 = fengedian(x2, tmp2)
                    split2 = x2
                    # print x1, x2
                    x1, x2, is_lst1_long = adjust(x1, x2, fengedian1,
                                                  fengedian2, lst1, lst2, tmp1,
                                                  tmp2, flag1, flag2)
                    # print x1, x2
                while (is_lst1_long == 0 and x2 == split2):
                    # print 'lst2 long: ', x1, x2
                    tmp1 = lst1[x1 + 1:]
                    if not search(tmp1):
                        is_break = 1
                        break
                    x1, flag1 = fengedian(x1, tmp1)
                    split1 = x1
                    # print x1, x2
                    x1, x2, is_lst1_long = adjust(x1, x2, fengedian1,
                                                  fengedian2, lst1, lst2, tmp1,
                                                  tmp2, flag1, flag2)
                    # print x1, x2
            else:
                x1, x2, is_lst1_long = adjust(x1, x2, fengedian1, fengedian2,
                                              lst1, lst2, tmp1, tmp2, flag1,
                                              flag2)
            if not is_break:
                fengedian1.append(x1)
                fengedian2.append(x2)
        return fengedian1, fengedian2


class DynamicProcess():
    @staticmethod
    def dtw(list_x, list_y):
        split_x, split_y = ImprovedSplit.split(list_x, list_y)
        arr = lambda x, y: np.abs(x - y)
        pos_x = 0
        pos_y = 0
        d = 0
        for i in range(len(split_x)):
            list_part_x = list_x[pos_x:split_x[i]]
            list_part_y = list_y[pos_y:split_y[i]]
            x = np.array(PreProcess.posNormalized(list_part_x)).reshape(-1, 1)
            y = np.array(PreProcess.posNormalized(list_part_y)).reshape(-1, 1)
            if len(list_part_x) > len(list_part_y):
                ans = dtw(x, y, arr)
                d += ans[0] / len(ans[-1])
            else:
                ans = dtw(y, x, arr)
                d += ans[0] / len(ans[-1])
            pos_x = split_x[i]
            pos_y = split_y[i]
        return d / (len(split_x) + 1)

    @staticmethod
    def compare(real_list, test_list):
        return precompare(real_list, PreProcess.spline(test_list))

    @staticmethod
    def precompare(real_list, test_list):
        d_x = []
        d_y = []
        for i in real_list:
            d_x.append(dtw(i[1], test_list[1]))
            d_y.append(dtw(i[2], test_list[2]))
        return math.sqrt(np.mean(d_x)**2 + np.mean(d_y)**2)

    @staticmethod
    def pre_real_list(real_list):
        ret_list = []
        for _i in real_list:
            i = PreProcess.spline(_i)
            ret_list.append(i)
        return ret_list

    @staticmethod
    def pre_length(prl):
        d_x = []
        d_y = []
        for i in range(prl):
            for j in range(prl):
                if i != j:
                    d_x.append(dtw(prl[i][1], prl[j][1]))
                    d_y.append(dtw(prl[i][2], prl[j][2]))
        return math.sqrt(np.mean(d_x)**2 + np.mean(d_y)**2)


# def match(real_list, compare_list, fz=0.6):
#     x = np.mean([
#         DynamicProcess.compare(real_list, real_list[0]),
#         DynamicProcess.compare(real_list, real_list[1]),
#         DynamicProcess.compare(real_list, real_list[2])
#     ])
#     y = DynamicProcess.compare(real_list, compare_list)

#     return y * fz < x


def match(preprocessd_real_list, pre_length, compare_list, limit=0.6):
    x = DynamicProcess.compare(preprocessd_real_list, compare_list)
    return x * limit < pre_length
