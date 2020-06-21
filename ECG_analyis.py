import numpy as np
import logging
import math
import pylab as plt
import scipy.signal as sp
import scipy.optimize
import sys
import json


def find_extremes(voltages):
    """Finds the max and min values in a list

    Finds the voltage 'extremes' of the ECG dataset

    :param voltages: list of ECG voltage readings

    :return: maximum and minim voltages in tuple form
    """
    logging.info("Finding Voltage Extremes...\n")
    ret = (min(voltages), max(voltages))
    return ret


def normalize_data(file_name):
    """Removes noise from data

    This function removes noise from the data by normalizing the data
    (dividing by the maximum magnitude), sinusoidal curve-fitting, and
    then subtracting the sinusoidal sequence from the data set

    :param file_name: string of the file path to a .csv dataset

    :return: 2D array of time sequence and normalized, noise-removed data
    """
    logging.info("Normalizing Data...\n")
    data = read_data(file_name)
    tt = data[:, 0]
    temp = data[:, 1]
    yy = temp / max(temp)
    res = fit_sin(tt, yy)
    # plt.plot(tt, yy, "k-", label="raw data", linewidth=1)
    # plt.plot(tt, res["fitfunc"](tt), "r-", label="fit curve", linewidth=2)
    # plt.show()
    normalized_data = np.subtract(yy, res["fitfunc"](tt))
    # plt.plot(tt, normalized_data, "k-", label="normalized data", linewidth=2)
    # plt.show()
    return np.column_stack((tt, normalized_data))


def fit_sin(tt, yy):
    """Determine waveform of noise

    Fit sin to the input time sequence, and return fitting parameters 'amp',
    'omega', 'phase', 'offset', 'freq', 'period' and 'fitfunc'
    This code was taken from stack exchange user 'unsym'

    :param tt: time sequence
    :param yy: magnitude sequence

    :returns: Dictionary containing sin waveform parameters
    """
    logging.info("Removing Noise...\n")
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1] - tt[0]))  # assume uniform spacing
    fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(fyy[1:]) + 1])  # excluding the zero
    # frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2. ** 0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2. * np.pi * guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c): return A * np.sin(w * t + p) + c

    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w / (2. * np.pi)

    def fitfunc(t): return A * np.sin(w * t + p) + c

    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f,
            "period": 1. / f, "fitfunc": fitfunc, "maxcov": np.max(pcov),
            "rawres": (guess, popt, pcov)}


def read_data(file_name):
    """ Reads in data from a .csv file

    Reads in lines, splits each line with a ',' character and removes
    the newline character. After creating two lists, one of the time sequences
    and one of the voltage sequences, this code merges them into a 2D
    array which it returns. This code also handles bad input which
    includes non-numeric characters and NaN values.

    :param file_name: string of the file path to a .csv dataset

    :return: 2D array of time sequence and votlage sequence
    """
    file = open(file_name, "r")
    voltages = list()
    times = list()
    counter = 0
    while True:
        line = file.readline()
        data = line.split(",")
        if data[0] == "":
            break
        try:
            time = float("%.9f" % float((data[0])))
            volt = float("%.9f" % (float(data[1].strip("\n"))))
            # print("Time: {}, Volt: {}".format(time, volt))
        except ValueError:
            logging.info("Error\n")
            continue
        if (math.isnan(time) or math.isnan(volt)):
            logging.info("Error\n")
            continue
        times.append(time)
        voltages.append(volt)
        f = find_extremes(voltages)
        if (f[0] < -300 or f[1] > 300):
            logging.info("Warning\n")
    ret = np.column_stack((times, voltages))
    return ret


def find_duration(data):
    """Finds the duration of the ECG data sequence

    Finds the duration by looking at the last time value
    as the first value is always at time = 0 seconds

    :param data: 2D array of time sequences and voltage sequences

    :return: Time duration of data sequence
    """
    logging.info("Detecting Duration of Data Stream...\n")
    return data[:, 0][-1]


def find_peaks(data):
    """Finds the voltage peaks of the data sequence

    Identifies heart-beat events by identifying local maxima
    in the voltage sequence from the ECG data set using
    a function from scipy called scipy.signal.find_peaks()

    :param data: list of voltages that have been normalized and
    processed to remove noise

    :return: list of indices where heart-beat events occur
    """
    logging.info("Detecting Heart Beats...\n")
    peaks = sp.find_peaks(data, distance=190)
    return peaks[0]


def num_beats(data):
    """ Counts number of heart beats found
    :param data: list of indices where heart-beat events were detected
    :return: Number of heart beats
    """
    logging.info("Counting Number of Beats...\n")
    return len(data)


def mean_bpm(var):
    """Calculates heart rate in BPM

    Uses functions find peaks, find duration, and num_beats
    to calculate number of heart beats over the duration
    of the dataset and finds heart rate in BPM

    :param var: string of the file path to a .csv dataset

    :return: Heart rate in BPm formatted to 3 decimal places
    """
    logging.info("Calculating Mean BPM...\n")
    beats = num_beats(find_peaks(normalize_data(var)[:, 1]))
    minutes = find_duration(read_data(var)) / 60
    answer = beats / minutes
    return float("%.3f" % answer)


def beat_times(peaks, name):
    """Finds the times at which heart beats

    Using list of indices where voltage peaks occur
    the corresponding time values are found and put
    into a list

    :param peaks: List of indices of voltage peaks
    :param name: string of the file path to a .csv dataset

    :return: List of times where heart-beats occured
    """
    logging.info("Calculating Beat Times...\n")
    ret = list()
    data = read_data(name)
    for num in peaks:
        ret.append(data[:, 0][num])
    return ret


def make_dict(duration, voltages, beats, mean_hr, beat_times):
    """Makes a dictionary following the format described on github

    :param duration: Time length of data sequence
    :param voltages: Voltage extremes in tuple form
    :param beats: Number of beats
    :param mean_hr: Calculated heart rate in BPM
    :param beat_times: List of times where heart beat events occured

    :return: Dictionary of data
    """
    metrics = {"Duration": duration,
               "Voltage Extremes": voltages,
               "Number of Beats": beats,
               "Mean Heart Rate": mean_hr,
               "Beat Times": beat_times}
    return metrics

if __name__ == "__main__":
    logging.basicConfig(filename="code_log.log", filemode='w',
                        level=logging.DEBUG)
    logging.info("Running Code...\n")
    # normalize_data("test_data/test_data1.csv")
    data = normalize_data(sys.argv[1])
    name = sys.argv[1].split(".")[0]
    metrics = make_dict(find_duration(data),
                        find_extremes(read_data(sys.argv[1])[:, 1]),
                        num_beats(find_peaks(data[:, 1])),
                        mean_bpm(sys.argv[1]),
                        beat_times(find_peaks(data[:, 1]), sys.argv[1]))
    filename = name + ".json"
    outfile = open(filename, 'w')
    json.dump(metrics, outfile)
    outfile.close()
    logging.info("End of code")
