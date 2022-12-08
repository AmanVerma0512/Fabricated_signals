#!/usr/bin/env python
# coding: utf-8

# In[1]:


import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from abc import ABC, abstractmethod
from collections import ChainMap


# In[10]:


def get_score(y,h_params,header):
    class Score(ABC):
        @abc.abstractmethod
        def coachingTip():
            pass

        @abc.abstractmethod
        def userProfileScore(history, current_score):  # given previous score, how to update
            pass

        @abc.abstractmethod
        def subScores():
            pass

        @abc.abstractmethod
        def score():  # aggregation, reassign from Policy.aggregation variants
            pass

        @abc.abstractmethod
        def compute():  # core computation of score
            pass

    dummy_prev=0.5
    class Tempo(Score):
        scoreType = "tempo"

        def __init__(self, y, configs):
            self.y = y
            self.config = configs
            self.prevScore = dummy_prev  # getPrevScore()
            self.compute()
            self.coachingTip()

        def compute(self):
            xp = peaks(self.y)
            xp = [int(i) for i in xp]
            curr_tempo = []
            for i in range(1, len(xp)):
                curr_tempo.append(xp[i] - xp[i - 1])
            self.currScore = np.var(curr_tempo)
            avg = sum(curr_tempo) / len(curr_tempo) if len(curr_tempo) else 0
            self.currScore /= avg
            self.currScore *= 100
            self.currScore = 100 - self.currScore
            self.currScore = clip100(self.currScore)

            meta = {}
            meta["peaks"] = xp
            meta["curr_tempo"] = curr_tempo
            meta["avg"] = avg
            meta["currScore"] = self.currScore
            self.meta=meta
            return curr_tempo, avg, self.currScore

        # config variatitons: peaks

        def coachingTip(self):
            self.coachingTipRes = coachingTipTemplate(Tempo.scoreType, self.currScore)
            return self.coachingTipRes

        def userProfileScore(self):
            return userProfileTemplate(self.currScore, self.prevScore)

        def score(self):
            return self.currScore

        def subScores(self):
            res = {}
            res[Tempo.scoreType] = {}
            self.compute()
            res[Tempo.scoreType]["score"] = self.currScore
            res[Tempo.scoreType]["coachingTip"] = self.coachingTipRes
            res[Tempo.scoreType]["meta"] = self.meta
            return res


    class TempoFactory():
        def configuredObject(y, configs):
            usingScipyPeaks = configs["scipyPeaks"]
            if usingScipyPeaks:
                global peaks
                currPeaks = peaks
                peaks = scipyPeaks
            tempo = Tempo(y, configs)
            if usingScipyPeaks:
                peaks = currPeaks

            return tempo

    class Jitter(Score):
        scoreType = "jitter"

        def __init__(self, y, configs):
            self.y = y
            self.config = configs
            self.prevScore = dummy_prev
            self.compute()
            self.coachingTip()

        def compute(self):
            window_size = self.config["window_size"]
            delta = self.config["delta"]
            t0 = self.config["t0"]
            x_dist_rel = self.config["x_dist_rel"]
            jitterPolicyThreshold = self.config["jitterPolicyThreshold"]
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
            self.currScore = 1 - Policy.rep_and_threshold(self.y, jitter, jitterPolicyThreshold)
            self.currScore *= 100
            self.currScore = clip100(self.currScore)

            meta = {}
            meta["per rep jitter dictionary"] = dj
            self.meta=meta


            return self.currScore

        def smooth_blips(self):
            config = self.config["smoothBlips"]
            smoothenFactor = config["smoothenFactor"]
            prominentPeaksProminence = config["prominentPeaksProminence"]
            prominentPeaksWidth = config["prominentPeaksWidth"]
            smallPeaksHeightLowerFactor = config["smallPeaksHeightLowerFactor"]
            smallPeaksHeightHigherFactor = config["smallPeaksHeightHigherFactor"]
            smallPeaksWidth = config["smallPeaksHeightHigherFactor"]

            temp = self.y
            temp.sort()
            y_max = statistics.mean(temp[max(-3, -len(temp) + 1):])
            y = smoothen(self.y, smoothenFactor)
            prominent_peaks, _ = find_peaks(y, prominence=prominentPeaksProminence * y_max, width=prominentPeaksWidth)
            small_peaks, _ = find_peaks(y,
                                        height=[smallPeaksHeightLowerFactor * y_max, smallPeaksHeightHigherFactor * y_max],
                                        width=smallPeaksWidth)
            self.currScore = 100 * len(prominent_peaks) / (len(small_peaks) + len(prominent_peaks))
            self.currScore = clip100(self.currScore)
            return self.currScore

        def coachingTip(self):
            self.coachingTipRes = coachingTipTemplate(Jitter.scoreType, self.currScore)
            return self.coachingTipRes

        def userProfileScore(self):
            return userProfileTemplate(self.currScore, self.prevScore)

        def score(self):
            self.compute()
            return self.currScore

        def subScores(self):
            res = {}
            res[Jitter.scoreType] = {}
            self.compute()
            res[Jitter.scoreType]["score"] = self.currScore
            res[Jitter.scoreType]["coachingTip"] = self.coachingTipRes
            res[Jitter.scoreType]["meta"] = self.meta
            return res

    class JitterFactory():
        def configuredObject(y,configs):
            usingScipyPeaks=configs["scipyPeaks"]
            if usingScipyPeaks:
                global peaks
                currPeaks=peaks
                peaks = scipyPeaks
            jitter=Jitter(y,configs)
            if usingScipyPeaks:
                peaks=currPeaks
            if "smoothBlips" in configs:
                jitter.compute = jitter.smooth_blips
            return jitter

    class Power(Score):
        scoreType = "power"

        def __init__(self, y, configs):
            self.y = y
            self.config = configs
            self.prevScore = dummy_prev
            self.compute()
            self.coachingTip()

        def compute(self):
            bwt = self.config["bwt"]
            gender = self.config["gender"]
            exercise_mode = self.config["exercise_mode"]

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
                if i<len(self.y):
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
            self.normalizedScore = power * coeff
            self.unNormalizedScore = power
            if (self.getPowerReferenceFromHistory() * self.config["growth factor"])==0:
                self.currScore=0
                return

            self.powerReferenceFromHistory=self.getPowerReferenceFromHistory()
            meta = {}
            meta["power"] = power
            meta["powerReferenceFromHistory"] = self.powerReferenceFromHistory
            self.meta = meta

            self.currScore = 100*power / (self.powerReferenceFromHistory * self.config["growth factor"])

        def getPowerReferenceFromHistory(self):
            # assessment workout data->
            # ->zone 3 power data, ->maximum stregnth
            return 22.666666666666668
            # return self.unNormalizedScore

        def coachingTip(self):
            self.coachingTipRes = coachingTipTemplate(Power.scoreType, self.currScore)
            return self.coachingTipRes

        def userProfileScore(self):
            return userProfileTemplate(self.currScore, self.prevScore)

        def score(self):
            return self.currScore

        def unNormalizedScore(self):
            return self.unNormalizedScore

        def subScores(self):
            res = {}
            res[Power.scoreType] = {}
            self.compute()
            res[Power.scoreType]["score"] = self.currScore
            res[Power.scoreType]["coachingTip"] = self.coachingTipRes
            try:
                res[Power.scoreType]["meta"] = self.meta
            except:
                print("no meta")
            return res


    class PowerFactory():
        def configuredObject(y,configs):
            if "scipyPeaks" in configs:
                global peaks
                currPeaks=peaks
                peaks = scipyPeaks
                power=Power(y,configs)
                peaks=currPeaks
                return power
            else:
                return Power(y,configs)

    from numpy import diff
    class Explosiveness(Score):
        scoreType = "explosiveness"

        def __init__(self, y, configs):
            self.y = y
            self.config = configs
            self.prevScore = dummy_prev
            self.compute()
            self.coachingTip()

        def compute(self):
            # calculate 2 paramters:
            #     1.y[peak] - y[base]
            #     2. total time of descent on smoothened curve in a rep
            xp = peaks(self.y)

            temp = [x for x in self.y]
            temp.sort()
            hi = sum(temp[-3:]) / 3
            dx = 1
            dy = diff(smoothen(y=y, window_size=5)) / dx
            ddy = diff(dy) / dx
            roots = []
            for i in range(len(ddy)):
                if dy[i] == 0 and ddy[i] <= sum(ddy) / (4 * len(ddy)) and y[i] > 0.1 * max(y):
                    roots.append(i)
            temp = [y[i] for i in roots]
            base = mode(self.y)
            cumm = 0
            for i in range(len(self.y) - 1):
                if self.y[i + 1] > self.y[i]:
                    cumm += 1
            if len(xp)==0:
                self.currScore=0
                return
            avg_asc = cumm / len(xp)
            self.currScore = (hi - base) / avg_asc
            self.currScore *= 100
            meta = {}
            meta["base/mode"] = base
            meta["average ascent"] = avg_asc
            meta["peak value used"] = hi
            self.meta=meta

        def coachingTip(self):
            self.coachingTipRes = coachingTipTemplate(Explosiveness.scoreType, self.currScore)
            return self.coachingTipRes

        def userProfileScore(self):
            return userProfileTemplate(self.currScore, self.prevScore)

        def score(self):
            return self.currScore

        def subScores(self):
            res = {}
            res[Explosiveness.scoreType] = {}
            self.compute()
            res[Explosiveness.scoreType]["score"] = self.currScore
            res[Explosiveness.scoreType]["coachingTip"] = self.coachingTipRes
            res[Explosiveness.scoreType]["meta"] = self.meta
            return res


    class ExplosivenessFactory():
        def configuredObject(y, configs):
            if configs["scipyPeaks"]:
                global peaks
                currPeaks = peaks
                peaks = scipyPeaks
            explosiveness = Explosiveness(y, configs)
            if configs["scipyPeaks"]:
                peaks = currPeaks

            return explosiveness

    class AggPowerScore(Score):
        scoreType = "agg power"

        def __init__(self, y, configs):
            self.y = y
            self.config = configs
            self.prevScore = dummy_prev
            self.subScoresObjects = [
                PowerFactory.configuredObject(y, configs[Power.scoreType]),
                ExplosivenessFactory.configuredObject(y, configs[Explosiveness.scoreType])
            ]
            self.compute()
            self.coachingTip()

        def compute(self):
            self.currScore = 0
            totalWeights = 0
            for subScore in self.subScoresObjects:
                w = self.config['w_' + subScore.scoreType]
                self.currScore += float(w) * subScore.score()
                totalWeights += w
            self.currScore /= totalWeights
            return self.currScore

        def coachingTip(self):
            self.coachingTipRes = ""
            for subScore in self.subScoresObjects:
                self.coachingTipRes += subScore.coachingTip() + ", "
            self.coachingTipRes = self.coachingTipRes[:-2]
            return self.coachingTipRes

        def userProfileScore(self):
            return userProfileTemplate(self.currScore, self.prevScore)

        def score(self):
            return self.currScore

        def subScores(self):
            #         binary string to choose
            resList = [subScore.subScores() for subScore in self.subScoresObjects]
            subScoreDict = dict(ChainMap(*resList))
            res = {}
            res["subScores"] = subScoreDict
            res["score"] = self.currScore
            res["coachingTip"] = self.coachingTipRes
            res = {
                AggPowerScore.scoreType: res
            }
            return res


    class AggPowerScoreFactory():
        def configuredObject(y, configs):
            powerScore = AggPowerScore(y, configs)
            return powerScore

    class SuddenRelease(Score):
        scoreType = "sudden release"

        def __init__(self, y, configs):
            self.y = y
            self.config = configs
            self.prevScore = dummy_prev
            self.start, self.end = getStartEnd(y)
            self.compute()
            self.coachingTip()

        def compute(self):
            # detecting using high negative slope and low value
            max_to_fall_ratio = self.config["max_to_fall_ratio"]
            fall_time = self.config["fall_time"]
            start, end = self.start, self.end
            y = self.y
            if type(y) == tuple:
                y = y[0]
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
            self.currScore = Policy.rep_and_threshold(self.y, sud, 0) * 100
            self.currScore = clip100(self.currScore)
            meta = {}
            meta["max_to_fall_ratio"] = max_to_fall_ratio
            meta["fall_time"] = fall_time
            meta["points"] = sud
            self.meta=meta
            return self.currScore

        def coachingTip(self):
            self.coachingTipRes = coachingTipTemplate(self.scoreType, self.currScore)
            return self.coachingTipRes

        def userProfileScore(self):
            return userProfileTemplate(self.currScore, self.prevScore)

        def score(self):
            self.compute()
            return self.currScore

        def subScores(self):
            res = {}
            res[SuddenRelease.scoreType] = {}
            self.compute()
            res[SuddenRelease.scoreType]["score"] = self.currScore
            res[SuddenRelease.scoreType]["coachingTip"] = self.coachingTipRes
            res[SuddenRelease.scoreType]["meta"] = self.meta
            return res

    class SuddenReleaseFactory():
            def configuredObject(y,configs):
                suddenRelease=SuddenRelease(y,configs)
                return suddenRelease

    class AggFormScore(Score):
        scoreType = "formscore"

        def __init__(self, y, configs):
            self.y = y
            self.config = configs
            self.prevScore = dummy_prev
            self.subScoresObjects = [
                JitterFactory.configuredObject(y, configs[Jitter.scoreType]),
                TempoFactory.configuredObject(y, configs[Tempo.scoreType]),
                SuddenReleaseFactory.configuredObject(y, configs[SuddenRelease.scoreType])
            ]
            self.compute()
            self.coachingTip()

        def compute(self):
            self.currScore = 0
            totalWeight = 0
            for subScore in self.subScoresObjects:
                w = self.config['w_' + subScore.scoreType]
                self.currScore += float(w) * subScore.score()
                totalWeight += w
            self.currScore /= totalWeight
            return self.currScore

        def coachingTip(self):
            self.coachingTipRes = ""
            for subScore in self.subScoresObjects:
                self.coachingTipRes += subScore.coachingTip() + ", "
            self.coachingTipRes = self.coachingTipRes[:-2]
            return self.coachingTipRes

        def userProfileScore(self):
            return userProfileTemplate(self.currScore, self.prevScore)

        def score(self):
            return self.currScore

        def subScores(self):
            resList = [subScore.subScores() for subScore in self.subScoresObjects]
            subScoreDict = dict(ChainMap(*resList))
            res = {}
            res["subScores"] = subScoreDict
            res["score"] = self.currScore
            res["coachingTip"] = self.coachingTipRes
            res = {
                AggFormScore.scoreType: res
            }
            return res

    class FormScoreFactory():
        def configuredObject(y,configs):
            if "scipyPeaks" in configs:
                global peaks
                currPeaks=peaks
                peaks = scipyPeaks
                formScore=AggFormScore(y,configs)
                peaks=currPeaks
                return formScore
            else:
                return AggFormScore(y,configs)
            
    class AreaStamina(Score):
        scoreType = "area stamina"

        def __init__(self, y, configs):
            self.y = y
            self.config = configs
            self.prevScore = dummy_prev  # getPrevScore()
            self.compute()
            self.coachingTip()

        def compute(self):
            referenceFactor = self.config["referenceFactor"]
            ref = int(max(self.y) * referenceFactor)
            start, end = getStartEnd(self.y)
            total_power = sum(self.y[start:end])
            ideal_power = ref * (end - start)
            if ideal_power==0:
                self.currScore=0
                return self.currScore
            self.currScore = total_power / ideal_power
            self.currScore *= 100
            self.currScore = clip100(self.currScore)

            meta = {}
            meta["total power/area"] = total_power
            meta["length"] = end-start
            meta["ideal power/reference x length"] = ideal_power
            self.meta=meta

            return self.currScore

        def coachingTip(self):
            self.coachingTipRes = coachingTipTemplate(AreaStamina.scoreType, self.currScore)
            return self.coachingTipRes

        def userProfileScore(self):
            return userProfileTemplate(self.currScore, self.prevScore)

        def score(self):
            return self.currScore

        def subScores(self):
            res = {}
            res[AreaStamina.scoreType] = {}
            res[AreaStamina.scoreType]["score"] = self.currScore
            res[AreaStamina.scoreType]["coachingTip"] = self.coachingTipRes
            res[AreaStamina.scoreType]["meta"] = self.meta
            return res


    class AreaStaminaFactory():
        def configuredObject(y, configs):
            if configs["peaks"]["scipyPeaks"]:
                global peaks
                currPeaks = peaks
                peaks = scipyPeaks
            areaStamina = AreaStamina(y, configs)
            if configs["peaks"]["scipyPeaks"]:
                peaks = currPeaks
            return areaStamina
        
    class RingStamina(Score):
        scoreType = "ring stamina"

        def __init__(self, y, configs):
            self.y = y
            self.config = configs
            self.prevScore = dummy_prev  # getPrevScore()
            self.compute()
            self.coachingTip()

        def compute(self):
            power_ref = h_params["ring_stamina"]["power_ref"]
            time_ref = h_params["ring_stamina"]["time_ref"]
            start, end = getStartEnd(self.y)
            xp = peaks(y)
            peakVals = [self.y[int(i)] for i in xp]
            ref_y = statistics.mean(peakVals[:min(3, len(peakVals))])
            ref_y *= power_ref
            ref = (end - start) * ref_y
            if ref == 0:
                self.currScoroe = 0
                return self.currScore
            ref2 = time_ref * ref_y
            A = Area(self.y)
            area = A
            pow = min(1, (ref2 - area) / ref)
            t = end - start
            t = min(1, (t) / time_ref)
            self.currScore = max(0, min(1 - (pow * t), 1)) * 100
            self.currScore = clip100(self.currScore)

            meta = {}
            meta["xp"] = xp
            meta["ref_y"] = ref_y
            meta["ref_denominator"] = ref
            meta["ref_y_(subtracted from)"] = self.currScore
            meta["power punishing factor"]=pow
            meta["time punishing factor"]=t
            self.meta=meta

            return self.currScore

        def peakBased(self):
            power_ref = self.config["peakBased"]["power_ref"]
            time_ref = self.config["peakBased"]["time_ref"]
            start, end = getStartEnd(self.y)
            xp = peaks(y)
            xp = [self.y[int(i)] for i in xp]
            ref_y = statistics.mean(xp[:min(3, len(xp))])
            m = mode(y)
            ref_y -= m
            ref_y *= power_ref
            ref = (end - start) * ref_y
            ref2 = time_ref * ref_y
            A = Area(self.y)
            area = A - m * (end - start)
            pow = min(1, (ref2 - area) / ref)
            t = end - start
            t = min(1, (t) / time_ref)
            self.currScore = max(0, min(1 - (pow * t), 1)) * 100
            self.currScore = clip100(self.currScore)
            return self.currScore

        def coachingTip(self):
            self.coachingTipRes = coachingTipTemplate(RingStamina.scoreType, self.currScore)
            return self.coachingTipRes

        def userProfileScore(self):
            return userProfileTemplate(self.currScore, self.prevScore)

        def score(self):
            self.compute()
            return self.currScore

        def subScores(self):
            res = {}
            res[RingStamina.scoreType] = {}
            res[RingStamina.scoreType]["score"] = self.currScore
            res[RingStamina.scoreType]["coachingTip"] = self.coachingTipRes
            res[RingStamina.scoreType]["meta"] = self.meta
            return res


    class RingStaminaFactory():
        def configuredObject(y, configs):
            ringStamina = RingStamina(y, configs)
            if configs["peakBased"]:
                ringStamina.compute = ringStamina.peakBased
            return ringStamina
        
    class TotalTime(Score):
        scoreType = "total time"

        def __init__(self, y, configs):
            self.y = y
            self.config = configs
            self.prevScore = dummy_prev  # getPrevScore()
            self.compute()
            self.coachingTip()

        def compute(self):
            start, end = getStartEnd(self.y)
            self.currScore = 0
            for i in range(start, end + 1):
                if self.y[i] > 0.1 * max(self.y):
                    self.currScore += 1

            meta={}
            meta["start,end"]=(start,end)
            meta["low_filter"]=0.1 * max(self.y)
            self.meta=meta
            return self.currScore

        def coachingTip(self):
            self.coachingTipRes = coachingTipTemplate(TotalTime.scoreType, self.currScore)
            return self.coachingTipRes

        def userProfileScore(self):
            return userProfileTemplate(self.currScore, self.prevScore)

        def score(self):
            self.compute()
            return self.currScore

        def subScores(self):
            res = {}
            res[TotalTime.scoreType] = {}
            res[TotalTime.scoreType]["score"] = self.currScore
            res[TotalTime.scoreType]["coachingTip"] = self.coachingTipRes
            res[TotalTime.scoreType]["meta"] = self.meta
            return res


    class TotalTimeFactory():
        def configuredObject(y, configs):
            totalTime = TotalTime(y, configs)
            return totalTime

    TotalTimeFactory.configuredObject(y, h_params1["stamina"]["total time"]).subScores()

    class Stamina(Score):
        scoreType = "stamina"

        def __init__(self, y, configs):
            self.y = y
            self.config = configs
            self.prevScore = dummy_prev
            self.subScoresObjects = [
                AreaStaminaFactory.configuredObject(y, configs[AreaStamina.scoreType]),
                #         RingStaminaFactory.configuredObject(y,configs[RingStamina.scoreType])
                # TotalTimeFactory.configuredObject(y, configs[TotalTime.scoreType]),
            ]
            self.compute()
            self.coachingTip()

        def compute(self):
            self.currScore = 0
            totalWeights = 0
            for subScore in self.subScoresObjects:
                w = self.config['w_' + subScore.scoreType]
                self.currScore += float(w) * subScore.score()
                totalWeights += w
            self.currScore /= totalWeights
            return self.currScore

        def coachingTip(self):
            self.coachingTipRes = ""
            for subScore in self.subScoresObjects:
                self.coachingTipRes += subScore.coachingTip() + ", "
            self.coachingTipRes = self.coachingTipRes[:-2]
            return self.coachingTipRes

        def userProfileScore(self):
            return userProfileTemplate(self.currScore, self.prevScore)

        def score(self):
            return self.currScore

        def subScores(self):
            resList = [subScore.subScores() for subScore in self.subScoresObjects]
            subScoreDict = dict(ChainMap(*resList))
            res = {}
            res["subScores"] = subScoreDict
            res["score"] = self.currScore
            res["coachingTip"] = self.coachingTipRes
            res = {
                Stamina.scoreType: res
            }
            return res


    class StaminaFactory():
        def configuredObject(y,configs):
            if configs["peaks"]["scipyPeaks"]:
                global peaks
                currPeaks=peaks
                peaks = scipyPeaks
            stamina=Stamina(y,configs)
            if configs["peaks"]["scipyPeaks"]:
                peaks=currPeaks
            return stamina


    # In[30]:


    class StaminaFactory():
        def configuredObject(y,configs):
            if configs["peaks"]["scipyPeaks"]:
                global peaks
                currPeaks=peaks
                peaks = scipyPeaks
            stamina=Stamina(y,configs)
            if configs["peaks"]["scipyPeaks"]:
                peaks=currPeaks
            return stamina


    def removeKeys(obj, key):
        if key in obj: 
            del obj[key]
        for k, v in obj.items():
            if isinstance(v,dict):
                item = removeKeys(v, key)

    def removeDictL2(obj, key=None,l=0):
        if key==None:
            key=list(obj.keys())[0]
        if key in obj and type(obj[key])==dict and l==0:
            del obj[key]
        for k, v in obj.items():
            if isinstance(v,dict):
                item = removeDictL2(v, key,l+1)

    def getScores(y, configs, header):
        # META()
        subScoresObjects = [
            FormScoreFactory.configuredObject(y,configs["formScore"]), \
            StaminaFactory.configuredObject(y,configs["stamina"]), \
            AggPowerScoreFactory.configuredObject(y,configs["power"]) ,\
            TotalTimeFactory.configuredObject(y,{})
        ]

        resList = [subScore.subScores() for subScore in subScoresObjects]
        res = dict(ChainMap(*resList))
        res = {
            "scores": res
            # "metadata":META.get()
        }
        if header["score"] == False:
            removeKeys(res, "score")
        if header["coachingTip"] == False:
            removeKeys(res, "coachingTip")
        if header["subScores"] == False:
            removeKeys(res, "subScores")
        if header["meta"] == False:
            removeKeys(res, "meta")
        return res
    return getScores(y,h_params,header)


# In[11]:


from h_params import *


# In[12]:


header={
    "subScores":True,
    "coachingTip":True,
    "score":True,
    "meta":True
}


# In[13]:


get_score(y,h_params,header)


# In[ ]:




