from tiff_handler import load_series, get_frame_rate, plot_framedrops, plot_frame_hist
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    paths = ["data/old/image_2022-02-17T12-13-05.09_0.tif", "data/old/image_2022-02-15T15-36-26.04_0.tif",
             "data/old/image_2022-02-15T15-37-09.663_0.tif", "data/old/image_2022-02-15T15-37-36.853_0.tif"]
    dir_path = "data/"
    paths = ['image_2022-02-17T14-23-05.649_0.tif', 'image_2022-02-17T14-25-27.857_0.tif',
             'image_2022-02-17T14-27-20.301_0.tif', 'image_2022-02-17T14-26-14.757_0.tif',
             'image_2022-02-17T14-24-19.375_0.tif', 'image_2022-02-17T14-28-21.007_0.tif',
             'image_2022-02-17T14-27-43.767_0.tif', 'image_2022-02-17T14-24-54.559_0.tif',
             'image_2022-02-17T14-22-01.668_0.tif', 'image_2022-02-17T14-26-46.5_0.tif',
             'image_2022-02-17T14-23-46.949_0.tif', 'image_2022-02-17T16-29-49.706_0.tif']
    dropped_frames = []
    resolution = []
    for path in paths:
        path = dir_path + path
        timestamps, frames, x, y = load_series(path, False)
        intervals = np.diff(timestamps) / 1000 / 1000 / 1000
        intervals = np.round(intervals, 4)
        min_interval = intervals.min()
        frame_rate = get_frame_rate(timestamps)
        n = len(np.array(timestamps[1:])[intervals > min_interval])
        n = n / len(frames[1:]) * 100
        size = x[0] * y[0] / 1e6
        print(x[0], y[0])
        resolution.append(size)
        dropped_frames.append(n)
        print(f"dropped frames: {n=:.1f} % for resolution {size=:.2f} MP")
        print(f"framerate: {frame_rate=:.2f}")
    avi_res = np.sort(resolution)[::-1]
    avi_dropped_frames = [40, 39, 39, 38, 38, 38, 37, 35, 33, 29, 26, 0]
    plt.scatter(resolution, dropped_frames, color="black", label="TIF")
    plt.scatter(avi_res, avi_dropped_frames, color="red", marker="x", label="AVI")
    print(avi_res)
    plt.axvline(avi_res[0], ls="--", color="orange")
    plt.axvline(avi_res[0] / 4, ls="--", color="orange")
    plt.axvline(avi_res[0] / 16, ls="--", color="orange")
    plt.legend()
    plt.xlabel("resolution [MP]")
    plt.ylabel("dropped frames [%]")
    plt.savefig("plots/dropped_frames_vs_resolution.pdf")
    plt.show()