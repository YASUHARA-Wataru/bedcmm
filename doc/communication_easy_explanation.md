## Fundamental Theory of bedcmm

The basic theory of **bedcmm** (Base Extraction Division Correlation Minimum Method) involves setting a base, dividing values other than zero by the base value, and using the minimum result as the correlation value.

![core_pic](pic/bedcmm_core.png)

---

## Theory of Communication Multiplexing with bedcmm

**Communication multiplexing using bedcmm** refers to applying bedcmm during signal demodulation for binary signals.

### Modulation

During modulation (spreading), the signal is extended to the length of the base. When the bit is 1, the base is inserted; when it is 0, zeros of the same length as the base are inserted.

![mod_pic](pic/bedcmm_modulation.png)

### Demodulation

For demodulation, as shown in the figure, correlation values are obtained using bedcmm. By applying an appropriate delay filter afterward and extracting data at intervals matching the original bit length, the original data can be recovered.

- **Demodulation (Overview)**  
![demod_pic](pic/bedcmm_demodulation.png)

Since bedcmm obtains the correlation by focusing only on the parts where the base has 1s, the minimum value among those positions is used. That is, if there are no zeros in the 1-bit positions, it is judged as 1; if any zeros are found, it is judged as 0. This allows for the processing shown in the figure.

- **Demodulation (Core Processing)**  
![demod_core_pic](pic/bedcmm_comm_demod.png)

---

## Comparison Table of Sequences by Theoretical Values (Example)

| Sequence / Method | Synchronization Condition | Sequence Length | Cross-Correlation | Quantization | Multiplexing Number |
|--|--|--|--|--|--|
| M sequence, GOLD sequence | Code phase synchronization required | Long (theoretically 15 or more, practically 31 or more) | Choose as low as possible | 6–8 bits | Many |
| ZCZ sequence | Coarse synchronization (quasi-synchronization) within the zone required | Long (theoretically zone = 1 with efficiency 1/2, practically from 16) | Zero within the zone | 4–8 bits | Few |
| BEDCMM | Symbol boundary synchronization of transmitted signals required | Short (confirmed range: 2 users at length 6 – 19 users at length 31) | 0 | 1 bit | Few (within the confirmed range) |

---

## Maximum Theoretical Multiplexing with bedcmm

|Signal Length|Theoretical Multiplexing|
|--|--|
|6|2|
|7|2|
|8|3|
|9|3|
|10|4|
|11|4|
|12|5|
|13|6|
|14|6|
|15|(7)|
|16|(8)|
|17|(9)|
|18|(9)|
|19|(10)|
|20|(11)|
|21|(12)|
|22|(12)|
|23|(13)|
|24|(14)|
|25|(15)|
|26|(15)|
|27|(16)|
|28|(17)|
|29|(17)|
|30|(18)|
|31|(19)|
|32|(20)|

※() is the minimum number because only a portion of the data has been confirmed