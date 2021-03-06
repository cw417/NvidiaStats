import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import re
import subprocess
from matplotlib.animation import FuncAnimation


def max_clock():
    # Get data for max GPU clock to later set GPU clock graph axis limit
    cmd = 'nvidia-smi -q | grep Video'
    check = str(subprocess.check_output(cmd, shell=True))
    reg = re.findall("\d+", check)
    return reg[1]

max_clock = int(max_clock())

def run():

  style.use('seaborn')

  fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)

  def animate(i):

    # Read data from CSV  
    data = pd.read_csv('nvidia_stats.csv')
    time = data['time_elapsed']
    GPU_temp = data['GPU_temp']
    GPU_clock = data['GPU_clock']
    GPU_use = data['GPU_use']
    fan_speed = data['fan_speed']

    # Define plot 1
    ax1.cla()
    ax1.set_ylim([0,100])
    ax1.plot(time, GPU_temp, label='GPU Temp', color='red')
    ax1.plot(time, GPU_use, label='GPU Use', color='green', linestyle='--')
    ax1.plot(time, fan_speed, label='Fan Speed', color='blue', linestyle='--')

    # Define plot 2
    ax2.cla()
    ax2.set_ylim([0,max_clock])
    ax2.plot(time, GPU_clock, label='GPU Clock')

    # Set plot 1 labels
    ax1.legend(loc='upper left')
    ax1.set_title('GPU Stats')
    ax1.text(time.iloc[-1], 100, f'GPU Temp: {GPU_temp.iloc[-1]}', horizontalalignment='right', verticalalignment='bottom')
    ax1.text(time.iloc[-1], 0, f'GPU Use: {GPU_use.iloc[-1]}', horizontalalignment='right', verticalalignment='top')

    # Set plot 2 labels
    ax2.legend(loc='upper left')
    ax2.set_xlabel('Time')
    ax2.text(time.iloc[-1], max_clock, f'GPU Clock: {GPU_clock.iloc[-1]}', horizontalalignment='right', verticalalignment='bottom')

    plt.tight_layout()

  ani = FuncAnimation(fig, animate, interval=2000)

  plt.show()

if __name__ == '__main__':
    run()