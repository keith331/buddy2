import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# from matplotlib.backend_bases import key_press_handler

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import ScalarFormatter
from collections import defaultdict
from tabulate import tabulate



'''
Only supports jupyter notebook
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
'''


# Generate a window
root = tk.Tk()
root.title('SoundCheck result analyzer')
root.geometry("1400x900+50+50")


# ==== Tableau20 colors3
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
         (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
         (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
         (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
         (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255, g / 255, b / 255)

# Read raw data
# fr0 = pd.read_excel('test_use 2020-4-29 MIC.xlsx',sheet_name='mic_FRF_L--mic_FRF_ENV')
# fr1 = pd.read_excel('test_use 2020-4-29 MIC.xlsx',sheet_name='mic_FRF_R--mic_FRF_ENV')
fr0 = pd.read_excel('test_use 2020-7-3 MIC.xlsx',sheet_name='mic_FRF_L')
fr1 = pd.read_excel('test_use 2020-7-3 MIC.xlsx',sheet_name='mic_FRF_R')
fr_data = [fr0,fr1]



sens0 = pd.read_excel('test_use 2020-7-3 MIC.xlsx',sheet_name='SensitivityL')
sens1 = pd.read_excel('test_use 2020-7-3 MIC.xlsx',sheet_name='SensitivityR')
# sens2 = pd.read_excel('DUT SENS.xlsx',sheet_name='Mic 2 Sens')
# sens3 = pd.read_excel('DUT SENS.xlsx',sheet_name='Mic 3 Sens')
sens_data = [sens0,sens1]


# thd0 = pd.read_excel('joplin result.xlsx',sheet_name='THD')
# thd1 = pd.read_excel('DUT THD.xlsx',sheet_name='Mic 0 THD')
# thd2 = pd.read_excel('DUT THD.xlsx',sheet_name='Mic 0 THD')
# thd3 = pd.read_excel('DUT THD.xlsx',sheet_name='Mic 0 THD')
# thd_data = [thd0,thd1,thd2,thd3]
# thd_data = [thd0]

# Data perameter setting
mic_number = int(input('Which number of Mics (0,1,2,3): '))
s = [0,1,2,3]
if mic_number not in s:
    print('Mic_number is wrong')
    exit()


# ===== for debug
# print(freshdata.keys())

sens_df = sens_data[mic_number]
# thd_df = thd_data[mic_number]
fr_df = fr_data[mic_number]
fr_x = list(fr_df.columns[1:])
fr_x_counts = fr_df.shape[1]
# thd_x = list(thd_df.columns[1:])
# thd_x_counts = thd_df.shape[1]



total_data = fr_df.shape[0]
parts = int(input('Part numbers: '))

if parts > total_data:
    print('Data out of range!')
    exit()
beginning = 0
trials = int(input('Trial time: '))


'''
raw_mode = bool(input('Check out particular curves (y => Yes, "Enter" => No) ?'))

if raw_mode:
    designated_part = int(input('Which number of samples ?'))

    if designated_part > total_data:
        print('Data out of range!')
        exit()

    else:
        designated_part = designated_part * trials
        beginning = designated_part - trials

'''


# Chart perameter settings
fig = plt.figure(figsize=(5,5))
plt.subplots_adjust(left=0.07,right=0.92,wspace=0.35)
left_color = '#016392'
variance_color = '#c72e29'
linewidth = 2


# ==== Define freshdata as dictionary with list type
freshdata = defaultdict(list)


# ==== define necessary format for plot chart
def style(self):
    plt.grid(which='minor',linestyle='-',color='#b6b6b6', axis='x')
    plt.grid(which='major',linestyle='-',color='#565656', axis='x', linewidth=1.5)
    plt.xticks(fontsize=13)
    plt.xlim(100,22000)
    plt.xscale('log',basex = 10)
    plt.yticks(fontsize=12)

# ==== change the x-axis of log plot appreance
    for axix in [self.xaxis, self.yaxis]:
        axix.set_major_formatter(ScalarFormatter())


def raw_mode_chart():

    raw_ax1 = plt.subplot(2,1,1,facecolor='#f2f2f2')
    style(raw_ax1)
    plt.ylabel('Variance (dBV)', fontsize=12)

    for k in range(beginning,designated_part):

        freshdata['raw_fr%d' %k] = list(fr_df.iloc[k,1:])
        id = fr_df.iloc[k,0]
        freshdata['raw_sn%d'%k].append(id)
        raw_ax1.plot(fr_x, freshdata['raw_fr%d' %k], linewidth=linewidth, label=freshdata['raw_sn%d'%k])


    print(freshdata.keys())
    print(beginning)
    print(designated_part)
    raw_ax1.legend(loc='upper left', fontsize='large')


    raw_ax2 = plt.subplot(2,1,2,facecolor='#f2f2f2')
    style(raw_ax2)
    plt.ylabel('THD (%)', fontsize=12)

    for k in range(beginning,designated_part):

        freshdata['raw_thd%d' %k] = list(thd_df.iloc[k,1:])
        raw_ax2.plot(thd_x, freshdata['raw_thd%d' %k], linewidth=linewidth,label=freshdata['raw_sn%d'%k])

    raw_ax2.legend(loc='upper left', fontsize='large')


def fr_chart():

    for k in range(beginning,parts):

        id = fr_df.iloc[k * trials,0]
        freshdata['sn'].append(id)

        for i in range(1,fr_x_counts):

            if k == 0:
                col = trials
            elif k == 1:
                col = trials * 2
            elif k == 2:
                col = trials * 3
            elif k == 3:
                col = trials * 4
            elif k == 4:
                col = trials * 5
            elif k == 5:
                col = trials * 6
            elif k == 6:
                col = trials * 7
            elif k == 7:
                col = trials * 8
            elif k == 8:
                col = trials * 9
            elif k == 9:
                col = trials * 10

            avg = round(fr_df.iloc[k*trials:col,i].mean(),2)
            max = round(fr_df.iloc[k*trials:col,i].max(),2)
            min = round(fr_df.iloc[k*trials:col,i].min(),2)
            R = round(max - min,2)

            freshdata['fr_avg%d' %k].append(avg)
            freshdata['fr_max%d' %k].append(max)
            freshdata['fr_min%d' %k].append(min)
            freshdata['fr_R%d' %k].append(R)


    ax1 = plt.subplot(211)
    plt.title('FR_Average of %d'%trials + ' measurements',fontsize=14)
    style(ax1)
    plt.ylabel('Level (dBV)', fontsize=12)
    ax1a = plt.subplot(212)
    ax1a.spines["top"].set_visible(False)
    ax1a.spines["right"].set_visible(False)
    plt.title('FR_Range of %d'%trials + ' measurements',fontsize=14)
    style(ax1a)
    plt.ylabel('Level (dBV)', fontsize=16)
    # plt.title('Averag of %s' % trials + ' times test',fontsize=15,fontname='Arial')

    for i in range(beginning,parts):
        ax1.plot(fr_x, freshdata['fr_avg%d'%i], linewidth=linewidth, label=freshdata['sn'][i])
        ax1a.plot(fr_x, freshdata['fr_R%d'%i], linewidth=linewidth, label=freshdata['sn'][i])

    # ===Vanriance curve   default disable
    # plt.fill_between(fr_x, freshdata['fr_max0'], freshdata['fr_min0'], label='Range of %s' %freshdata['sn'][0], color=variance_color)

    ax1.legend(loc='upper left', fontsize='small')
    # ax1a.legend(loc='upper left', fontsize='x-small')



def thd_chart():

    for k in range(beginning,parts):

        for i in range(1,thd_x_counts):

            if k == 0:
                col = trials
            elif k == 1:
                col = trials * 2
            elif k == 2:
                col = trials * 3
            elif k == 3:
                col = trials * 4
            elif k == 4:
                col = trials * 5
            elif k == 5:
                col = trials * 6
            elif k == 6:
                col = trials * 7
            elif k == 7:
                col = trials * 8
            elif k == 8:
                col = trials * 9
            elif k == 9:
                col = trials * 10

            avg = round(thd_df.iloc[k*trials:col,i].mean(),2)
            max = round(thd_df.iloc[k*trials:col,i].max(),2)
            min = round(thd_df.iloc[k*trials:col,i].min(),2)
            R = round(max - min,2)

            freshdata['thd_avg%d' %k].append(avg)
            freshdata['thd_max%d' %k].append(max)
            freshdata['thd_min%d' %k].append(min)
            freshdata['thd_R%d' %k].append(R)


    # ============ debug...
    # print(freshdata['thd_max2'])
    # print(freshdata['thd_min2'])
    # print(len(freshdata['thd_R2']))
    # print(freshdata.keys())


    ax2 = plt.subplot(3,4,(5,6),facecolor='#f2f2f2')
    plt.title('THD_Average of  %d'%trials + ' measurements',fontsize=14)
    style(ax2)
    plt.ylabel('THD (%)', fontsize=12)
    ax2a = plt.subplot(3,4,(7,8),facecolor='#f2f2f2')
    plt.title('THD_Range of %d'%trials + ' measurements',fontsize=14)
    style(ax2a)
    plt.ylabel('THD %', fontsize=12)

    # plt.title('FR Range',fontsize=15,fontname='arial')
    # ax1.set_ylabel('dBV',color=left_color)
    # ax1.tick_params(axis='y', labelcolor=left_color)

    for i in range(beginning,parts):
        ax2.plot(thd_x, freshdata['thd_avg%d'%i], linewidth=linewidth, label=freshdata['sn'][i])
        ax2a.plot(thd_x, freshdata['thd_R%d'%i], linewidth=linewidth, label=freshdata['sn'][i])

    # ===Vanriance curve===   default disable
    # plt.fill_between(thd_x,freshdata['thd_max0'],freshdata['thd_min0'], label=freshdata['sn'][0], color=variance_color)

    # ax2.legend(loc='upper left', fontsize='x-small')
    # ax2a.legend(loc='upper left', fontsize='small')


def sens_chart():

    for k in range(beginning,parts):

        for i in range(0,trials):

            if k == 0:
                col = i
            elif k == 1:
                col = i + (trials * k)
            elif k == 2:
                col = i + (trials * k)
            elif k == 3:
                col = i + (trials * k)
            elif k == 4:
                col = i + (trials * k)
            elif k == 5:
                col = i + (trials * k)
            elif k == 6:
                col = i + (trials * k)
            elif k == 7:
                col = i + (trials * k)
            elif k == 8:
                col = i + (trials * k)
            elif k == 9:
                col = i + (trials * k)

            sens = round(sens_df.iloc[col,1],2)
            freshdata['sens%d' %k].append(sens)

    # ax3 = plt.subplot(2,3,4,facecolor='#f2f2f2')
    # ax3.boxplot(freshdata['sens_df'])
    ax4 = plt.subplot(2,2,(3,4))
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    # plt.title('Sensitivity Part-to-Part', fontsize=14)
    ax4.yaxis.grid(color='#868686')

    for i in range(beginning,parts):

        freshdata['name_store'].append(freshdata['sn'][i][-6:])
        freshdata['sens_store'].append(freshdata['sens%d' %i])

    ax4.set_xticklabels(freshdata['name_store'])

    print(freshdata['name_store'])
    print(tabulate(freshdata['sens_store']))
    # plt.ylim(-38,-37)



# === Box style
    bp = ax4.boxplot(freshdata['sens_store'],patch_artist=True)


    for box in bp['boxes']:
        box.set(color='#6794a7', linewidth=1)
        box.set(facecolor = '#c3d6df')

    for whisker in bp['whiskers']:
        whisker.set(color='#6794a7',linewidth=1)

    for cap in bp['caps']:
        cap.set(color='#6794a7',linewidth=1)

    for median in bp['medians']:
        median.set(color='#6794a7',linewidth=1.5)

    for flier in bp['fliers']:
        flier.set(marker='o', color='#e7298a', alpha=0.5)


# if raw_mode:
#     print('Raw data mode')
#     raw_mode_chart()
# else:
fr_chart()
    # thd_chart()
# sens_chart()
# fig.tight_layout(h_pad=0.1)

# ======================== Tkinter session ====================================


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand=1)


toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()

labelfont = ('arial black', 18 , 'bold')
Passed = tk.Label(root,text='Passed:\n %s' %trials,bg='#a8a6a7',width=8,height=3)
Passed.config(font=labelfont)
Passed.pack(side=tk.LEFT)

Failed = tk.Label(root,text='Failed:\n 0', bg='#a8a6a7',width=8,height=3)
Failed.config(font=labelfont)
Failed.pack(side=tk.LEFT,padx=1)

rate = tk.Label(root,text='Yield:\n 100%', bg='#a8a6a7',width=8,height=3)
rate.config(font=labelfont)
rate.pack(side=tk.LEFT)

button = tk.Button(master=root, text="Quit", command=_quit, width=8,height=3, relief='raised')
button.config(font=labelfont)
button.pack(side=tk.RIGHT)



root.mainloop()

# Only support jupyter notebook
# interact(ax1,data_number=(1,total,1))
