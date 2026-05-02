# Open Implementation of Patented Algorithm (Japan Patent)
This repository provides an open implementation of the "Base Extraction Division Minimum Method," which is registered as a patent in Japan.

- This implementation is intended for research, verification, and evaluation purposes.
- Commercial use or redistribution requires obtaining a license (see below).

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

## Demo
By running `pattern_demo.ipynb` and `communication_demo.ipynb`, you can obtain simple sample results:

Easy explanation is in `doc`.

## How to run faster
```python setup.py build_ext --inplace```
run with cython(pattern modules)

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

## Contact
fapow.contact[at]gmail.com