from tiff_handler import load_series, get_frame_rate, plot_framedrops, plot_frame_hist
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

if __name__ == "__main__":
    paths = ["data/image_2022-02-15T15-36-26.04_0.tif", "data/image_2022-02-15T15-37-09.663_0.tif",
             "data/image_2022-02-15T15-37-36.853_0.tif"]
    dropped_frames = []
    resolution = []
    for path in paths:
        timestamps, frames, sizes = load_series(path, False)
        intervals = np.diff(timestamps) / 1000 / 1000 / 1000
        intervals = np.round(intervals, 4)
        min_interval = intervals.min()
        # plt.step(range(len(intervals)), intervals, color="black", where='pre')
        # plt.axhline(min_interval, color="red", ls="--")
        # plt.show()
        n = len(np.array(timestamps[1:])[intervals > min_interval])
        n = n / len(frames[1:]) * 100
        size = sizes[0] / 1e6
        resolution.append(size)
        dropped_frames.append(n)
        print(f"dropped frames: {n=:.1f} % for resolution {size=:.2f} MP")
    plt.scatter(resolution, dropped_frames, color="black")
    plt.xlabel("resolution [MP]")
    plt.ylabel("dropped frames [%]")
    plt.savefig("plots/dropped_frames_vs_resolution.pdf")
    plt.show()
