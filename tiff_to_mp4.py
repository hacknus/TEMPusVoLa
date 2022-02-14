from tiff_handler import open_tiff
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# open tiff
# get framedrops
# duplicate frames for framedrops
# save mp4

interval = 50
fig = plt.figure()

ani = animation.ArtistAnimation(fig, ims, interval=interval, blit=True, repeat_delay=1000)
# save animation

# needs ffmpeg to be installed
mywriter = animation.FFMpegWriter(fps=24)
print("saving mp4...")
ani.save(f'test.mp4', savefig_kwargs={'facecolor': 'black'}, writer=mywriter, dpi=600)
