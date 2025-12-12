import numpy as np
import pandas as pd
from bedcmm import pattern as bedcmm
import matplotlib.pyplot as plt
import statsmodels.api as sm

# load data
df_tokyo = pd.read_csv('sample_data/data_東京_utf-8.csv',skiprows=4)
df_akankohan = pd.read_csv('sample_data/data_釧路市阿寒湖畔_utf-8.csv',skiprows=4)
# 欠損値補完
df_tokyo.iloc[:,1] = df_tokyo.iloc[:,1].interpolate(method='linear')
df_akankohan.iloc[:,1] = df_akankohan.iloc[:,1].interpolate(method='linear')
# 絶対温度化
K_cont = 273.15
np_temp_tokyo = np.array(df_tokyo.iloc[:,1]) + K_cont
np_temp_akankohan = np.array(df_akankohan.iloc[:,1]) + K_cont

# インパルスノイズを付加
np_temp_tokyo[180] = 5000

max_temp_day_tokyo = np.array([np.max(np_temp_tokyo[i*24:i*24+24]) for i in range(int(len(np_temp_tokyo)/24))])
min_temp_day_tokyo = np.array([np.min(np_temp_tokyo[i*24:i*24+24]) for i in range(int(len(np_temp_tokyo)/24))])
max_temp_day_akankohan = np.array([np.max(np_temp_akankohan[i*24:i*24+24]) for i in range(int(len(np_temp_akankohan)/24))])
min_temp_day_akankohan = np.array([np.min(np_temp_akankohan[i*24:i*24+24]) for i in range(int(len(np_temp_akankohan)/24))])
diff_temp_tokyo = max_temp_day_tokyo - min_temp_day_tokyo
diff_temp_akankohan = max_temp_day_akankohan - min_temp_day_akankohan
print(f"tokyo min max diff maen:{np.mean(diff_temp_tokyo)}")
print(f"akankohan min max diff mean:{np.mean(diff_temp_akankohan)}")
print(f"akankohan/tokyo diff ratio:{np.mean(diff_temp_akankohan)/np.mean(diff_temp_tokyo)}")

max_lag = 97
#max_lag = int(len(np_temp_tokyo)/2)
min_lag = 12
periodicity_tokyo = bedcmm.periodicity_1d(np_temp_tokyo)
periodicity_akankohan = bedcmm.periodicity_1d(np_temp_akankohan)
acf_tokyo = sm.tsa.stattools.acf(np_temp_tokyo, nlags=max_lag)
acf_akankohan = sm.tsa.stattools.acf(np_temp_akankohan, nlags=max_lag)
print(f"tokyo periodicity std :{np.std(periodicity_tokyo[min_lag:max_lag])}")
print(f"akankohan periodicity std :{np.std(periodicity_akankohan[min_lag:max_lag])}")
print(f"akankohan/tokyo periodicyty ratio :{np.std(periodicity_akankohan[min_lag:max_lag])/np.std(periodicity_tokyo[min_lag:max_lag])}")
print(f"tokyo acf std :{np.std(acf_tokyo[min_lag:max_lag])}")
print(f"akankohan acf std :{np.std(acf_akankohan[min_lag:max_lag])}")
print(f"akankohan/tokyo acf ratio :{np.std(acf_tokyo[min_lag:max_lag])/np.std(acf_akankohan[min_lag:max_lag])}")


tokyo_temp_fft = np.abs(np.fft.fft(np_temp_tokyo))[:int(len(np_temp_tokyo)/2)]/len(np_temp_tokyo)*2
akankohan_temp_fft = np.abs(np.fft.fft(np_temp_akankohan))[:int(len(np_temp_akankohan)/2)]/len(np_temp_akankohan)*2
temp_freq = np.fft.fftfreq(len(np_temp_tokyo))[:int(len(np_temp_akankohan)/2)]
day_freq_ind = np.where(temp_freq >= 1/24)[0][0]
print(f"day freq amp of tokyo:{tokyo_temp_fft[day_freq_ind]}")
print(f"day freq amp of akankohan:{akankohan_temp_fft[day_freq_ind]}")
print(f"akankohan/tokyo ratio of day freq amp:{akankohan_temp_fft[day_freq_ind]/tokyo_temp_fft[day_freq_ind]}")


fig,ax = plt.subplots(2,1,sharex=True)
fig.suptitle('2024 Temperature')
ax[0].set_title('Tokyo')
ax[0].plot(np_temp_tokyo)
ax[0].grid()
ax[0].set_ylim([250,320])
#ax[0].set_ylim([260,5500])
ax[0].set_ylabel('Temperature [K]')
ax[1].set_title('Akankohan')
ax[1].plot(np_temp_akankohan)
ax[1].grid()
ax[1].set_ylim([250,320])
ax[1].set_ylabel('Temperature [K]')
plt.tight_layout()


fig,ax = plt.subplots(4,1,sharex=True)
fig.suptitle('Temperature Periodicity')
ax[0].set_title('Tokyo')
ax[0].plot(periodicity_tokyo)
ax[0].grid()
ax[0].set_ylim([288,291])
ax[0].set_xlim([0,max_lag])
ax[0].set_xticks([12,24,36,48,60,72,84])
ax[0].set_ylabel('Periodicity\n of bedcmm')
ax[1].set_title('Akankohan')
ax[1].plot(periodicity_akankohan)
ax[1].grid()
ax[1].set_ylim([276,279])
ax[1].set_xlim([0,max_lag])
ax[1].set_xticks([12,24,36,48,60,72,84])
ax[1].set_ylabel('Periodicity\n of bedcmm')
ax[2].set_title('Tokyo')
ax[2].plot(acf_tokyo)
ax[2].grid()
ax[2].set_xticks([12,24,36,48,60,72,84])
ax[2].set_ylabel('Periodicity\n of acf')
ax[3].set_title('Akankohan')
ax[3].plot(acf_akankohan)
ax[3].grid()
ax[3].set_xticks([12,24,36,48,60,72,84])
ax[3].set_xlabel('Periodicity Time[hour]')
ax[3].set_ylabel('Periodicity\n of acf')
plt.tight_layout()

fig,ax = plt.subplots(2,1,sharex=True)
fig.suptitle('FT of Temperature')
ax[0].set_title('Tokyo')
ax[0].plot(temp_freq,tokyo_temp_fft)
ax[0].plot(temp_freq[day_freq_ind],tokyo_temp_fft[day_freq_ind],'o')
ax[0].grid()
#ax[0].set_ylim([0,4])
ax[0].set_ylim([0,10])
ax[0].set_ylabel('power[K]')
ax[1].set_title('Akankohan')
ax[1].plot(temp_freq,akankohan_temp_fft)
ax[1].plot(temp_freq[day_freq_ind],akankohan_temp_fft[day_freq_ind],'o')
ax[1].grid()
#ax[1].set_ylim([0,4])
ax[1].set_ylim([0,10])
ax[1].set_ylabel('power[K]')
ax[1].set_xlabel('freq [/hour]')
plt.tight_layout()
plt.show()
