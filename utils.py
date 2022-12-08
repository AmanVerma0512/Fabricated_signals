import math
import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import random
import statistics
from scipy.signal import find_peaks
from h_params import *
from SignalProcessing import *
import streamlit as st
from FeatureExtraction import *
import time
from h_params import *
from collections import ChainMap

dummy_prev=0.5


def removeKeys(obj, key):
    if key in obj:
        del obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = removeKeys(v, key)


def removeDictL2(obj, key=None, l=0):
    if key == None:
        key = list(obj.keys())[0]
    if key in obj and type(obj[key]) == dict and l == 0:
        del obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = removeDictL2(v, key, l + 1)

def is_set(x, n):
    return x & 2 ** n != 0

def Area(y):
    start, end = getStartEnd(y)
    return sum(y[start:end])

def dummyYStamina(y):
    y = self.y[:end] + self.y[start:end]
    for i in range(len(y)):
        if i <= end and i >= start:
            y[i] += 5
    return y

def area_till_reference_time(self, ref):
    start, _ = getStartEnd(self.y)
    return sum(self.y[start:ref])

def plot_y(y):
    plt.rcParams["figure.figsize"] = (15, 4)
    plt.plot(range(len(y)), y)
    plt.show()

def plot_detections(y,roots):
    plt.rcParams["figure.figsize"] = (15, 4)
    plt.plot(range(len(y)), y)
    vals = range(len(y))
    mark = [vals.index(i) for i in roots]
    plt.plot(roots, [y[i] for i in mark], ls="", marker="o", label="points")
    plt.show()

def plot_y_streamlit(y,roots,title):
    fig, ax = plt.subplots()
    ax.plot(y)
    ax.title(title)
    vals = range(len(y))
    mark = [vals.index(i) for i in roots]
    plt.plot(roots, [y[i] for i in mark], ls="", marker="o", label="points")
    st.pyplot(fig)

# mode values: save/streamlit
def plot(y,roots=None,title=None):
    mode=h_params["setting"]
    plot_dir=h_params["plot_dir"]
    fig, ax = plt.subplots()
    ax.plot(y)
    if title:
        ax.title(title)
    if roots:
        vals = range(len(y))
        mark = [vals.index(i) for i in roots]
        ax.plot(roots, [y[i] for i in mark], ls="", marker="o", label="points")
    if mode=="save":
        plt.savefig(plot_dir + title + ".png")
        plt.show()
    elif mode=='streamlit':
        st.pyplot(fig)
    else:
        plt.show()

class FormScore:
    def __init__(self, y):
        self.y = y
        self.start, self.end = getStartEnd(self.y)

    def tempo(self):
        # return array, avg, standard deviation
        xp = peaks(self.y)
        xp = [int(i) for i in xp]

        curr_tempo = []
        for i in range(1, len(xp)):
            curr_tempo.append(xp[i] - xp[i - 1])

        return curr_tempo, sum(curr_tempo) / len(curr_tempo) if len(curr_tempo) else 0, np.var(curr_tempo)

    def sudden_release(self):
        # detecting using high negative slope and low value
        max_to_fall_ratio = h_params["sudden_release"]["max_to_fall_ratio"]
        fall_time = h_params["sudden_release"]["fall_time"]
        start,end=self.start,self.end
        y=self.y
        if type(y)==tuple:
            y=y[0]
        m = max(y)
        delta = m * max_to_fall_ratio
        t0 = fall_time
        sud = []
        for i in range(len(y)):
            j = 0
            while j <= t0 and y[i - j] >= y[i]:
                j += 1
            if j != 0 and y[i - j + 1] - y[i] > delta:
                sud.append(i)
        return sud

    def jitter(self):
        # detecting using moving average intersections
        window_size = h_params["jitter"]["window_size"]
        delta = h_params["jitter"]["delta"]
        t0 = h_params["jitter"]["t0"]
        x_dist_rel = h_params["jitter"]["x_dist_rel"]
        y = self.y
        m = mode(y)
        moving_averages = []
        jitter = []

        for i in range(len(y)):
            window_average = np.sum(y[max(0, i - window_size):i]) / window_size
            moving_averages.append(window_average)
            k = 0
            cross = []
            for j in range(t0):
                if y[i - j] > window_average and y[i - j - 1] < window_average or y[i - j] < window_average and y[
                    i - j - 1] > window_average and abs(y[i] - m) < x_dist_rel * max(y):
                    k += 1
                    cross.append(i - j)
            if k >= delta and abs(y[i] - m) < x_dist_rel * max(y):
                jitter.append(int(sum(cross) / len(cross)))
        start, end = getStartEnd(y)
        xp = peaks(y)
        xp = [int(i) for i in xp]

        dj = {}
        for p in xp:
            dj[p] = []

        xp.insert(0, 0)
        xp.append(len(y) - 1)

        # merging within a rep
        for j in jitter:
            for i in range(len(xp) - 1):
                l = xp[i]
                r = xp[i + 1]
                if i < (len(xp) - 1) and j >= l and j <= r:
                    dj[l].append(j)

        fj = []
        for key in dj.keys():
            if len(dj[key]) > 0:
                fj.append(int(sum(dj[key]) / len(dj[key])))

        for j in jitter:
            if y[j] < max(y) / 12:
                jitter.remove(j)
        return jitter

    def smooth_blips(self):
        sm = h_params["smooth_blips"]["sm"]
        y = smoothen(self.y, sm)
        prominent_peaks, _ = find_peaks(y, prominence=10, width=2)

        y_max = statistics.mean([y[i] for i in prominent_peaks])
        small_peaks, _ = find_peaks(y, height=[0.6 * y_max, 0.8 * y_max], width=2)

        return len(prominent_peaks) / (len(small_peaks) + len(prominent_peaks))

    def area_stamina(self):
        # stamina score using area
        ref = int(max(self.y) * 1.4)
        start, end = getStartEnd(self.y)
        total_power = sum(self.y[start:end])
        ref_ls = []
        for i in range(len(self.y)):
            if i <= end and i >= start:
                ref_ls.append(ref)
            else:
                ref_ls.append(0)
        ideal_power = ref * (end - start)
        score = total_power / ideal_power
        return score

    def dummy_area_stamina2(self):
        ref = int(max(self.y) * 1.4)
        start, end = getStartEnd(self.y)



        total_power = sum(y[start:end])
        ideal_power = ref * (end - start)
        score = total_power / ideal_power
        return score

    def rings_stamina_v0(self, power_ref=0.8, time_ref=200):
        #  v0 of stamaina calculation using punishing factors
        start, end = getStartEnd(self.y)
        xp = peaks(y)
        xp = [self.y[int(i)] for i in xp]
        peakVals=[y[i] for i in xp]
        ref_y = statistics.mean(peakVals[:min(3, len(peakVals))])
        ref_y *= power_ref
        ref = (end - start) * ref_y
        ref2 = time_ref * ref_y
        A=Area(self.y)
        area = A
        pow = min(1, (ref2 - area) / ref)
        t = end - start
        t = min(1, (t) / time_ref)

        score = max(0, min(1 - (pow * t), 1)) * 100
        return score

    def rings_stamina_v1(self, power_ref=0.8, time_ref=250):
        # calculates ring stamina using reference power and time punishing factors
        start, end = getStartEnd(self.y)
        xp = peaks(y)
        xp = [self.y[int(i)] for i in xp]
        ref_y = statistics.mean(xp[:min(3, len(xp))])
        m = mode(y)
        ref_y -= m
        ref_y *= power_ref
        ref = (end - start) * ref_y
        ref2 = time_ref * ref_y
        A=Area(self.y)
        area = A - m * (end - start)
        pow = min(1, (ref2 - area) / ref)
        t = end - start
        t = min(1, (t) / time_ref)
        score = max(0, min(1 - (pow * t), 1)) * 100
        return score

    def power(self, bwt=60, gender="men's", exercise_mode="Equipped Powerlifting"):
        if h_params["bwt"]:
            bwt = h_params["bwt"]
        if h_params["gender"]:
            gender = h_params["gender"]
        if h_params["mode"]:
            exercise_mode = h_params["exercise_mode"]

        params = {
            "men's":
                {"Equipped Powerlifting":
                     {"A": 1236.25115,
                      "B": 1449.21864,
                      "C": 0.01644},
                 "Classic Powerlifting":
                     {"A": 1199.72839,
                      "B": 1025.18162,
                      "C": 0.00921},
                 "Equipped Bench Press":
                     {"A": 381.22073,
                      "B": 733.79378,
                      "C": 0.02398},
                 "Classic Bench Press":
                     {"A": 320.98041,
                      "B": 281.40258,
                      "C": 0.01008}},
            "women's":
                {"Equipped Powerlifting":
                     {"A": 758.63878,
                      "B": 949.31382,
                      "C": 0.02435},
                 "Classic Powerlifting":
                     {"A": 610.32796,
                      "B": 1045.59282,
                      "C": 0.03048},
                 "Equipped Bench Press":
                     {"A": 221.82209,
                      "B": 357.00377,
                      "C": 0.02937},
                 "Classic Bench Press":
                     {"A": 142.40398,
                      "B": 442.52671,
                      "C": 0.04724}},

        }
        xp = peaks(y)
        d = {}
        for i in xp:
            d[i] = self.y[i]
        d = {k: v for k, v in sorted(d.items(), key=lambda item: -item[1])}
        c = min(3, len(xp))
        o = 0
        power = 0
        for key in list(d.keys()):
            power += d[key]
            o += 1
            if (o > c):
                break
        power /= c
        coeff = 100 / (params[gender][exercise_mode]["A"] - params[gender][exercise_mode]["B"] * (
                    2.718281828459 ** (-1 * params[gender][exercise_mode]["C"] * bwt)))
        return power, power * coeff


class Policy:
    # flags one rep based on threshold, and returns fraction of reps which do not cross the threshold
    def rep_and_threshold(y, detected, threshold):
        start,end=getStartEnd(y)
        xp = peaks(y)
        xp = [int(i) for i in xp]

        dj = {}
        for p in xp:
            dj[p] = []

        xp.insert(0, 0)
        xp.append(len(y) - 1)

        for p in xp:
            if p >= start or p >= end:
                xp.remove(p)

        # merging within a rep
        for j in detected:
            for i in range(1, len(xp) - 1):
                l = xp[i]
                r = xp[i + 1]
                if i < (len(xp) - 1) and j >= l and j <= r:
                    dj[l].append(j)

        fj = 0
        for key in dj.keys():
            if len(dj[key]) > threshold:
                fj += 1
        return fj / len(list(dj.keys()))


# prints all the calculated metrics
class Scoring:
    def __init__(self, fs: FormScore, pol="rep_and_threshold"):
        self.fs = fs
        self.pol = Policy
        a, b, c = fs.tempo()
        if pol == "rep_and_threshold":
            # print(self.fs.sudden_release())
            sr_metric = Policy.rep_and_threshold(self.fs.y, fs.sudden_release(),
                                                 0)  # min(10, (self.sudden_release()) / (2 * len(a)))
            jitter_metric = Policy.rep_and_threshold(self.fs.y, self.fs.jitter(), 4)

        blip_jitter_metric = fs.smooth_blips()

        it_metric = math.sqrt(c) / b
        if print_flag:
            print("\nMETRICS\nSudden Release metric: ", 10 * (sr_metric), ",\nJitter Metric: ", 10 * (jitter_metric),
                  ",\nInconsistent Tempo Metric: ", 10 * (it_metric),
                  ",\nBlips Jitter Metric: ", 10 * (blip_jitter_metric)
                  )

        blip_jitter_metric = 1 - fs.smooth_blips()

        d = {}
        d["power"] = fs.power()
        d["form"] = {}
        d["form"]["sudden_metric"] = 10 * clip1(sr_metric)
        d["form"]["jitter_metric"] = 10 * clip1(jitter_metric)
        d["form"]["it_metric"] = 10 * clip1(it_metric)

        d["ring stamina"] = clip10(fs.rings_stamina_v2())
        # d["ipf"] = fs.ipf_gl_coeff(bwt=fs.h_params["body_weight"],gender=fs.h_params["gender"],mode=fs.h_params["mode"])

        d["form"]["blip_jitter_metric"] = 10 * clip1(blip_jitter_metric)

        d["global_score"] = fs.h_params["global_score"]
        d["rep_score"] = 33.333 * (
                    fs.h_params["l0"] * sr_metric + 0 * jitter_metric + fs.h_params["l2"] * it_metric + fs.h_params[
                "l3"] * blip_jitter_metric)
        d["global_score"] = (1 - fs.h_params["discount"]) * d["rep_score"] + d["global_score"] * (
        fs.h_params["discount"])
        d["ring stamina"] = fs.rings_stamina_v2()

        coaching_tip = ""
        if it_metric > 0.5:
            coaching_tip += "Make sure each set is of 4 seconds!"
        else:
            coaching_tip += "Good rhythm! Keep it up!"

        if jitter_metric > 0.5:
            coaching_tip += " Do not shake. Hold the equipment firmly."
        else:
            coaching_tip += " Good grip! Keep it up!"

        if sr_metric > 0.3:
            coaching_tip += " Do not release the equipment in a single session"
        else:
            coaching_tip += " Good job holding the equipment! Keep it up!"

        d["coaching_tip"] = coaching_tip

        self.d = d
        t = time.time()
        d["timeID"] = str(t)


    def scores(self):
        return self.d

def clip1(x):
    return max(0, min(1, x))

def clip10(x):
    return max(0, min(10, x))

def clip100(x):
    return max(0, min(100, x))

def coachingTipTemplate(scoreType,scoreVal):
    if scoreVal>5:
        return "good "+scoreType
    else:
        return "bad "+scoreType

def userProfileTemplate(currScore,prevScore):
    return currScore+prevScore*0.8

def scipyPeaks(y):
    prominent_peaks, _ = find_peaks(y, prominence=10, width=2)
    return prominent_peaks
