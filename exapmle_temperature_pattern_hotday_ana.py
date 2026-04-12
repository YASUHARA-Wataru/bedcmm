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

max_temp_thre = 25 + K_cont
min_temp_thre = 20 + K_cont


max_temp_day_tokyo = np.array([np.max(np_temp_tokyo[i*24:i*24+24]) for i in range(int(len(np_temp_tokyo)/24))])
min_temp_day_tokyo = np.array([np.min(np_temp_tokyo[i*24:i*24+24]) for i in range(int(len(np_temp_tokyo)/24))])
max_temp_day_akankohan = np.array([np.max(np_temp_akankohan[i*24:i*24+24]) for i in range(int(len(np_temp_akankohan)/24))])
min_temp_day_akankohan = np.array([np.min(np_temp_akankohan[i*24:i*24+24]) for i in range(int(len(np_temp_akankohan)/24))])
hot_night_day_tokyo = (max_temp_day_tokyo>max_temp_thre) & (min_temp_day_tokyo>min_temp_thre)
hot_night_day_tokyo_cont3 = [np.sum(hot_night_day_tokyo[i:i+3])==3  for i in range(366-3)]
hot_night_day_akankohan = (max_temp_day_akankohan>max_temp_thre) & (min_temp_day_akankohan>min_temp_thre)
hot_night_day_akankohan_cont3 = [np.sum(hot_night_day_akankohan[i:i+3])==3  for i in range(366-3)]

print(f"tokyo min max temp cont hot 3 days:{np.sum(hot_night_day_tokyo_cont3)}/{len(hot_night_day_tokyo_cont3)}")
print(f"akankohan min max temp cont hot 3 days:{np.sum(hot_night_day_akankohan_cont3)}/{len(hot_night_day_akankohan_cont3)}")


base = np.array([max_temp_thre,max_temp_thre,0,0,0,0,0,0,0,0,0,0,
                 min_temp_thre,min_temp_thre,0,0,0,0,0,0,0,0,0,0,
                 max_temp_thre,max_temp_thre,0,0,0,0,0,0,0,0,0,0,
                 min_temp_thre,min_temp_thre,0,0,0,0,0,0,0,0,0,0,
                 max_temp_thre,max_temp_thre,0,0,0,0,0,0,0,0,0,0,
                 min_temp_thre,min_temp_thre],dtype=np.float64)

pattern_tokyo = bedcmm.pattern(np_temp_tokyo,base)
pattern_akankohan = bedcmm.pattern(np_temp_akankohan,base)

hot_continus_hour_tokyo = pattern_tokyo>1
hot_continus_hour_akankohan = pattern_akankohan>1

hot_continus_day_tokyo = [ np.sum(hot_continus_hour_tokyo[i*24:i*24+24])>0 for i in range(int(len(np_temp_tokyo)/24))]
hot_continus_day_akankohan = [ np.sum(hot_continus_hour_akankohan[i*24:i*24+24])>0 for i in range(int(len(np_temp_akankohan)/24))]
print(f"tokyo 12hour pattern cont hot 3 days:{np.sum(hot_continus_day_tokyo)}/{len(hot_continus_day_tokyo)-3}")
print(f"akankohan 12hour pattern cont hot 3 days:{np.sum(hot_continus_day_akankohan)}/{len(hot_continus_day_akankohan)-3}")


