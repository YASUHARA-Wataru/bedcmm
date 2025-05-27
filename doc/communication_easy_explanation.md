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

(*Created based on ChatGPT; possible inaccuracies may be present.*)

| Item                         | **bedcmm**           | Gold Sequence (n=5)        | Walsh Code (length 16)       | ZC Sequence (e.g., length 13) |
|------------------------------|----------------------|-----------------------------|-------------------------------|-------------------------------|
| **Quantization Bit Depth**   | **1 bit** (assumed)  | 6–8 bits (typical)          | 4–8 bits (assumes orthogonality) | 4–8 bits (complex phase dependent) |
| **Sequence Length**          | **12** (tested up to 12) | 31                        | 16 (2⁴)                        | 13 (prime)                     |
| **Max Theoretical Multiplexing** | **5** (calculated) | 33 (theoretical)            | 16 (fully orthogonal)          | 1 (mainly for autocorrelation) |
| **Autocorrelation Property** | Good (suited for 1-bit design) | Excellent (binary)       | Perfect orthogonality         | Excellent (small except at zero) |
| **Cross-correlation Property** | 0                 | -1, 0, 1 (three values)     | 0 (fully orthogonal)           | Small at distance              |
| **Demodulation Cost**        | **Low (logic only)** | Medium (correlation)        | Medium (orthogonal operations) | High (FFT/complex inner product) |
| **Compatibility with 1-bit** | **High**             | Low (depends on ADC)        | Low (amplitude orthogonality) | Low (complex orthogonality)   |
| **Main Application Fields**  | IoT, low-power communication (emerging) | CDMA, GPS            | WLAN, control communication    | 5G, radar, acoustic processing |

---

## Maximum Theoretical Multiplexing with bedcmm

| Signal Length     | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|-------------------|---|---|---|---|----|----|----|----|----|
| Theoretical Multiplexing | 2 | 2 | 3 | 3 | 4  | 4  | 5  |(5) |(6) |

※() is the minimum number because only a portion of the data has been confirmed