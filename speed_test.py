import time
import numpy as np
from bedcmm.pattern import periodicity
import time
import pandas as pd

def generate_random(N, seed=0):
    rng = np.random.default_rng(seed)
    return rng.random(N)  # [0, 1)


def generate_periodic(N, freq=5, noise_std=0.1, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(N)

    # 正弦波を [0,1] にシフト
    signal = 0.5 * (np.sin(2 * np.pi * freq * t / N) + 1.0)

    noise = rng.normal(0, noise_std, N)
    data = signal + noise

    # 負値をクリップ
    return np.clip(data, 0, None)


def generate_spike_noise(signal, spike_prob=0.01, spike_scale=1.0, seed=0):
    rng = np.random.default_rng(seed)
    spikes = rng.random(len(signal)) < spike_prob

    # 正のスパイクのみ
    spike_values = rng.random(len(signal)) * spike_scale

    corrupted = signal.copy()
    corrupted[spikes] += spike_values[spikes]

    return corrupted


def generate_dataset(N, mode="random", seed=0):
    if mode == "random":
        return generate_random(N, seed)

    elif mode == "periodic":
        return generate_periodic(N, seed=seed)

    elif mode == "spike":
        base = generate_periodic(N, seed=seed)
        return generate_spike_noise(base, seed=seed)

    else:
        raise ValueError("Unknown mode")

if __name__ == "__main__":
    N_list = [1000, 5000, 10000]
    result_N = []
    result_mode = []
    result_time_msec = []
    
    for mode in ["random", "periodic", "spike"]:
        print(f"\n=== Mode: {mode} ===")
        for N in N_list:
            data = generate_dataset(N, mode=mode, seed=42)
            print(f"N={N}, mean={np.mean(data):.4f}, std={np.std(data):.4f}")
            start = time.perf_counter()
            result = periodicity(data)
            end = time.perf_counter()
            print(f"time: {(end - start)*1000:.2f} ms")
            result_mode.append(mode)
            result_N.append(N)
            result_time_msec.append((end - start)*1000)
    
    result_df = pd.DataFrame({'mode':result_mode,'N':result_N,'time_msec':result_time_msec})
    print(result_df)
