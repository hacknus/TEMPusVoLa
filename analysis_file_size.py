from tiff_handler import load_series, get_frame_rate, plot_framedrops, plot_frame_hist
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def linear_func(x, m, b):
    return x * m


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

    resolution = []
    file_sizes = []
    for path in paths:
        path = dir_path + path
        timestamps, frames, x, y, file_size = load_series(path, False)
        intervals = np.diff(timestamps) / 1000 / 1000 / 1000
        intervals = np.round(intervals, 4)
        min_interval = intervals.min()
        frame_rate = get_frame_rate(timestamps)
        size = x[0] * y[0] / 1e6
        print(f"{x[0]}x{y[0]}, {size} MP")
        resolution.append(size)
        t = len(frames) / frame_rate
        t = (timestamps[-1] - timestamps[0]) / 1000 / 1000 / 1000
        file_sizes.append(file_size / 1e9 / t)
        print(f"framerate: {frame_rate:.2f} fps")
    resolution = np.array(resolution)
    file_sizes = np.array(file_sizes)
    popt, _ = curve_fit(linear_func, resolution[resolution < 11.5], file_sizes[resolution < 11.5])
    max_size_per_second = np.mean(file_sizes[resolution > 11.5])
    plt.scatter(resolution, file_sizes, color="black", label="TIF")
    r = np.linspace(min(resolution), max(resolution), 100)
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
