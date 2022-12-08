import numpy as np
from FeatureExtraction import mode
import random
from utils import *

# Add break
def stop(y):
    fs=FormScore(y)
    sud=fs.sudden_release()
    _,rep_t,_=fs.tempo()
    a=sud[int(len(sud)/2)]
    y2=y[:a]+[0 for i in range(int(rep_t))] + y[a:]
    return y2


# Decay signal
def decay(y,decay=0.5):
    m=mode(y) - max(y)*0.3
    for i in range(len(y)):
        if y[i]>m:
            y[i] *= (2.718 ** (-i * 0.0001 * decay))
    return y

# Noisy signal
def noisy(y):
    import random
    return [y[i] + random.random() * 0.2 * max(y) if y[i] > max(y) * (1 / 12) else y[i] for i in range(len(y))]

# Sudden release
def release(y):
    d = {}
    key = 0
    d[key] = y
    return [0 if d[key][i] > max(y) * (1 / 12) and random.random() > 0.95 else d[key][i] for i in
            range(len(d[key]))]

# Inconsistent tempo
def distort(y):
    d = {}
    key = 0
    d[key] = y
    xp = np.array(range(0, len(y), int(len(y) / 20)))
    xp = [int(i) for i in xp]
    yn = []
    for i in range(len(xp) - 1):
        if random.random() > 0.5:
            A = d[key][xp[i]:xp[i + 1]]
            w = sum([[x, sum([x, A[n + 1]]) / 2] for n, x in enumerate(A) if n < len(A) - 1], [])
            yn += w
        else:
            yn += d[key][xp[i]:xp[i + 1]]
    return yn

def smoothen(y, window_size=5):
    avg = []
    for i in range(len(y)):
        avg.append(np.sum(y[max(0, i - window_size):i]) / window_size)
    return avg
