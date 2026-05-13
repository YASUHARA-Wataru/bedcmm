# bedcmm

![CI](https://github.com/YASUHARA-Wataru/bedcmm/actions/workflows/ci_test.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/bedcmm.svg)](https://badge.fury.io/py/bedcmm)
![Python Versions](https://img.shields.io/pypi/pyversions/bedcmm)

# Open Implementation of Patented Algorithm (Japan Patent)
This repository provides an open implementation of the "Base Extraction Division Minimum Method," which is registered as a patent in Japan.

- This implementation is intended for research, verification, and evaluation purposes.
- Commercial use or redistribution requires obtaining a license (see below).

bedcmm is a library for robust periodicity, pattern extraction, and communication multiplexing based on a patented method.

## Features
A robust algorithm for pattern extraction and periodicity analysis,
designed to remain stable under outliers and impulsive noise.

- Quantitative pattern extraction
- Quantitative periodicity calculation
  - Applied to pitch detection robust to impulsive (spike) noise  
    https://github.com/YASUHARA-Wataru/bedcmmPitch
  - Periodicity analysis robust to outliers  
    (`example_temperature_period_ana.py`)
  - Support for missing values (NaN)
    - Periodicity can be computed directly without interpolation or preprocessing
    - Outputs the valid data ratio (`valid_ratio`) as a measure of reliability
    - Shows behavior similar to autocorrelation on complete data, while remaining applicable to datasets with missing values
- Quantitative continuity calculation
- Multiplexing communication using shorter sequences than M-sequences and only 1-bit quantization.However, synchronization is required(only send), randomness is not guaranteed, and signal-to-noise ratio (SNR) is not improved.
- Cross-periodicity analysis (not part of the core patented claims)
  - A method for comparing periodic structures between signals, analogous to the relationship between autocorrelation and cross-correlation
  
  Note: When the same signal is provided as both inputs, the result corresponds to auto-periodicity.

## Install
```bash
pip install bedcmm
```
## Example
- pattern
```python
import numpy as np
import bedcmm

np.random.seed(0)

# 周期 + ノイズ
base = np.tile([1, 0, 0, 0], 25)
noise = np.random.randint(0, 2, len(base)) * 0.1

x = base + noise

score = bedcmm.pattern.periodicity(x)

print("periodicity score:", score)
```
- communication
```python
import numpy as np
import bedcmm

base1 = [False, False, False, False, False, True, True, True]
base2 = [False, False, False, True, False, False, True, True]
base3 = [False, True, False, False, False, False, True, True]
tx1 = np.tile(base1, 5)
tx2 = np.tile(base2, 5)
tx3 = np.tile(base3, 5)

tx = np.array([tx1,tx2,tx3])

send_signal = bedcmm.communication.multiplexing(tx)
print(send_signal)

demod_signal1 = bedcmm.communication.demodulate(send_signal,base1)
demod_signal2 = bedcmm.communication.demodulate(send_signal,base2)
demod_signal3 = bedcmm.communication.demodulate(send_signal,base3)

print("demod_signal1:", demod_signal1)
print("demod_signal2:", demod_signal2)
print("demod_signal3", demod_signal3)
```

## Demo
By running `pattern_demo.ipynb` and `communication_demo.ipynb`, you can obtain simple sample results:

A brief explanation is available in the `doc` directory.

## How to run faster
```python setup.py build_ext --inplace```
Run with Cython (pattern modules)

## Calculation speed
The benchmark script is ```speed_test.py```.

### Cython
```
       mode      N  time_msec
0    random   1000     2.6160
1    random   5000    61.1024
2    random  10000   245.1453
3  periodic   1000     1.2297
4  periodic   5000    28.6166
5  periodic  10000   110.1707
6     spike   1000     1.3126
7     spike   5000    27.9070
8     spike  10000   113.7231
```
### Python only
```
       mode      N   time_msec
0    random   1000    188.5421
1    random   5000   4593.9274
2    random  10000  19079.0753
3  periodic   1000    196.6179
4  periodic   5000   4723.4922
5  periodic  10000  18833.8787
6     spike   1000    206.1020
7     spike   5000   4802.0938
8     spike  10000  19601.9191
```

## Patent Information
This algorithm is based on the following Japanese patent:

- Patent Number: JP Patent No. 7537807
- Title: Pattern Extraction and Communication Multiplexing Method
- Registration Date: August 13, 2024
- Summary: Methods for pattern extraction, periodicity calculation, continuity calculation, and communication multiplexing.

## Scope of Patent and Non-Patented Implementations

This repository contains both implementations covered by the patent and independent auxiliary or extended implementations.

- Patent-covered components:
  - Core algorithm for pattern extraction and periodicity analysis based on the Base Extraction Division Minimum Method

- Extended implementations:
  - Handling of missing values (NaN)

- Non-patented implementations:
  - Cross-periodicity analysis (e.g., `cross_periodicity` and related functions)

The applicability of the patent may depend on the specific use case and implementation details.

## Contact
fapow.contact[at]gmail.com