from h_params import *
from utils import *

def mode(y):
    # class interval based node
    sz = h_params["mode"]["sz"]
    win = max(y) / sz
    curr = win / 2
    d = {}
    for i in range(sz):
        curr += win
        d[curr] = 0
    for val in y:
        key = min(d.keys(), key=lambda x: abs(x - val))
        d[key] += 1
    max_val = 0
    ans = 0
    for key in d.keys():
        if key == min(d.keys()):
            continue
        if d[key] > max_val:
            max_val = d[key]
            ans = key
    return ans

def peaks(y):
    # peak detection based on class intervals
    sz = h_params["peaks"]["sz"]
    max_win = h_params["peaks"]["max_win"]
    start,end=getStartEnd(y)
    if type(y)==tuple:
        y=y[0]
    win = max(y) / sz
    flag = 0
    a = 0
    b = 0
    crests = []
    for i in range(start, end):
        curr = y[i]
        win = max(y[max(i - max_win, 0):i]) / sz
        if curr > max(y[max(i - max_win, 0):i]) - win and flag == 0:
            flag = 1
            a = i
        if curr < max(y[max(i - max_win, 0):i]) - 2 * win and flag == 1:
            flag = 0
            b = i
            p = a
            l = 0
            for k in range(a, b + 1):
                if y[k] > l:
                    l = y[k]
                    p = k
            crests.append(p)
    return crests

def getStartEnd(y):
    # returns first non zero element index and last non zero index
    start = 0
    end = 0
    for i in range(len(y)):
        if y[i] != 0:
            end = i

    for i in range(len(y)):
        if y[len(y) - i - 1] != 0:
            start = len(y) - i
    return start, end
