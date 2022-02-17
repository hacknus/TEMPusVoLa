from tiff_handler import load_series, get_frame_rate, plot_framedrops, plot_frame_hist
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    dir_path = "data/"
    paths = ['image_2022-02-17T14-23-05.649_0.tif', 'image_2022-02-17T14-25-27.857_0.tif',
             'image_2022-02-17T14-27-20.301_0.tif', 'image_2022-02-17T14-26-14.757_0.tif',
             'image_2022-02-17T14-24-19.375_0.tif', 'image_2022-02-17T14-28-21.007_0.tif',
             'image_2022-02-17T14-27-43.767_0.tif', 'image_2022-02-17T14-24-54.559_0.tif',
             'image_2022-02-17T14-22-01.668_0.tif', 'image_2022-02-17T14-26-46.5_0.tif',
             'image_2022-02-17T14-23-46.949_0.tif']
    t = []
    fps_d = []
    sizes = []
    for path in paths:
        path = dir_path + path
        timestamps, frames, x, y = load_series(path, False)
        intervals = np.diff(timestamps) / 1000 / 1000 / 1000
        intervals = np.round(intervals, 4)
        min_interval = intervals.min()
        ti = []
        frame_dropped_per_second = []
        for i in range(int(1 / min_interval), len(timestamps)):
            n = np.array(timestamps[i - int(1 / min_interval):i])[intervals[i - int(1 / min_interval):i] > min_interval]
            ti.append((timestamps[i] - timestamps[0]) / 1e9)
            frame_dropped_per_second.append(len(n))
        frame_rate = get_frame_rate(timestamps)
        n = np.array(timestamps[1:])[intervals > min_interval]
        size = x[0] * y[0] / 1e6
        print(f"framerate: {frame_rate=:.2f}")
        sizes.append(size)
        fps_d.append(frame_dropped_per_second)
        t.append(ti)
    zipped = list(zip(sizes, fps_d, t))
    zipped.sort()
    for size, fps, ti in zipped:
        plt.plot(ti, fps, label=f"{size:.2f} MP")
    plt.xlabel("time [s]")
    plt.ylabel("frame dropped per second [1/s]")
    plt.legend()
    plt.savefig("plots/dropped_frames_vs_time.pdf")
    plt.show()
