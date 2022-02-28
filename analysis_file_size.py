import os

from tiff_handler import load_series, get_frame_rate, plot_framedrops, plot_frame_hist
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def linear_func(x, m, b):
    return x * m


if __name__ == "__main__":
    path_internal = '/Volumes/Thor SSD/TestDataInternal'
    path_external = '/Volumes/Thor SSD/TestDataExternal'
    paths_internal = []
    paths_external = []
    for path in os.listdir(path_internal):
        if path[-5:] == "0.tif":
            paths_internal.append(path_internal + "/" + path)
    for path in os.listdir(path_external):
        if path[-5:] == "0.tif":
            paths_external.append(path_external + "/" + path)
    file_sizes_external = []
    resolution_external = []
    file_sizes_internal = []
    resolution_internal = []
    for path in paths_external:
        timestamps, frames, x, y, file_size = load_series(path, False)
        intervals = np.diff(timestamps) / 1000 / 1000 / 1000
        intervals = np.round(intervals, 4)
        min_interval = intervals.min()
        frame_rate = get_frame_rate(timestamps)
        size = x[0] * y[0] / 1e6
        print(f"{x[0]}x{y[0]}, {size} MP")
        resolution_external.append(size)
        t = len(frames) / frame_rate
        t = (timestamps[-1] - timestamps[0]) / 1000 / 1000 / 1000
        file_sizes_external.append(file_size / 1e9 / t)
        print(f"framerate: {frame_rate:.2f} fps")
    resolution_external = np.array(resolution_external)
    file_sizes_external = np.array(file_sizes_external)
    for path in paths_internal:
        timestamps, frames, x, y, file_size = load_series(path, False)
        intervals = np.diff(timestamps) / 1000 / 1000 / 1000
        intervals = np.round(intervals, 4)
        min_interval = intervals.min()
        frame_rate = get_frame_rate(timestamps)
        size = x[0] * y[0] / 1e6
        print(f"{x[0]}x{y[0]}, {size} MP")
        resolution_internal.append(size)
        t = len(frames) / frame_rate
        t = (timestamps[-1] - timestamps[0]) / 1000 / 1000 / 1000
        file_sizes_internal.append(file_size / 1e9 / t)
        print(f"framerate: {frame_rate:.2f} fps")
    resolution_external = np.array(resolution_external)
    file_sizes_external = np.array(file_sizes_external)
    res_threshold = 10
    popt, _ = curve_fit(linear_func, resolution_external[resolution_external < res_threshold],
                        file_sizes_external[resolution_external < res_threshold])
    max_size_per_second = np.mean(file_sizes_external[resolution_external > res_threshold])
    plt.scatter(resolution_external, file_sizes_external, color="black", label="TIF")
    plt.scatter(resolution_internal, file_sizes_internal, color="red", label="TIF")
    r = np.linspace(min(resolution_external), max(resolution_external), 100)
    plt.plot(r, linear_func(r, *popt), color="red", ls="--")
    plt.axhline(max_size_per_second, color="orange", ls="--")
    print(f"file size = {popt[0]:.2f} GB per second per resolution")
    print(f"file size at 11 MP = {popt[0] * 11:.2f} GB per second")
    print(f"file size for 30s at 11 MP = {popt[0] * 11 * 30:.2f} GB")
    print(f"MAX file size for 30s = {max_size_per_second * 30:.2f} GB")
    print(f"MAX estimation for 1 flight = {max_size_per_second * 60 * 30:.2f} GB")
    plt.xlabel("resolution [MP]")
    plt.ylabel("file size per second [GB/s]")
    plt.savefig("plots/file_sizes.pdf")
    plt.show()
