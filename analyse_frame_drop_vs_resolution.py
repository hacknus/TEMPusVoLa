import os

from tiff_handler import load_series, get_frame_rate, plot_framedrops, plot_frame_hist
import numpy as np
import matplotlib.pyplot as plt

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
    dropped_frames_external = []
    resolution_external = []
    dropped_frames_internal = []
    resolution_internal = []
    for path in paths_internal:
        print(path)
        timestamps, frames, x, y, _ = load_series(path, False)
        intervals = np.diff(timestamps) / 1000 / 1000 / 1000
        intervals = np.round(intervals, 4)
        min_interval = intervals.min()
        frame_rate = get_frame_rate(timestamps)
        n = len(np.array(timestamps[1:])[intervals > min_interval])
        n = n / len(frames[1:]) * 100
        size = x[0] * y[0] / 1e6
        print(x[0], y[0])
        resolution_internal.append(size)
        dropped_frames_internal.append(n)
        print(f"dropped frames: {n=:.1f} % for resolution {size=:.2f} MP")
        print(f"framerate: {frame_rate=:.2f}")
    for path in paths_external:
        timestamps, frames, x, y, _ = load_series(path, False)
        intervals = np.diff(timestamps) / 1000 / 1000 / 1000
        intervals = np.round(intervals, 4)
        min_interval = intervals.min()
        frame_rate = get_frame_rate(timestamps)
        n = len(np.array(timestamps[1:])[intervals > min_interval])
        n = n / len(frames[1:]) * 100
        size = x[0] * y[0] / 1e6
        print(x[0], y[0])
        resolution_external.append(size)
        dropped_frames_external.append(n)
        print(f"dropped frames: {n=:.1f} % for resolution {size=:.2f} MP")
        print(f"framerate: {frame_rate=:.2f}")
    avi_dropped_frames = [40, 39, 39, 38, 38, 38, 37, 35, 33, 29, 26, 0]
    avi_res = [12.288, 12.026336, 11.728, 11.444992, 11.154, 10.878048, 10.5944, 9.504, 8.4728, 7.5008, 6.8544, 3.072]
    plt.scatter(resolution_external, dropped_frames_external, color="black", label="TIF EXT")
    plt.scatter(resolution_internal, dropped_frames_internal, color="red", label="TIF INT")
    plt.scatter(avi_res, avi_dropped_frames, color="red", marker="x", label="AVI")
    plt.axvline(avi_res[0], ls="--", color="orange")
    plt.axvline(avi_res[0] / 4, ls="--", color="orange")
    plt.axvline(avi_res[0] / 16, ls="--", color="orange")
    plt.legend()
    plt.xlabel("resolution [MP]")
    plt.ylabel("dropped frames [%]")
    plt.savefig("plots/dropped_frames_vs_resolution.pdf")
    plt.show()
