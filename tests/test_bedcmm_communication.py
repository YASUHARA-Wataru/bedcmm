import pytest
import numpy as np
from bedcmm.communication import modulate, multiplexing, demodulate

def test_modulate_basic():
    # 基本的な変調のテスト
    data = np.array([1, 0], dtype=bool)
    key = np.array([1, 1, 0], dtype=bool)
    # 期待値: [1, 1, 0, 0, 0, 0] (データ1ならkeyそのまま、0なら全0)
    expected = np.array([1, 1, 0, 0, 0, 0], dtype=bool)
    
    result = modulate(data, key)
    np.testing.assert_array_equal(result, expected)

def test_multiplexing_logic():
    # 多重化のテスト (OR演算のようになっているか)
    mod1 = np.array([1, 0, 1, 0], dtype=bool)
    mod2 = np.array([0, 0, 1, 1], dtype=bool)
    expected = np.array([1, 0, 1, 1], dtype=bool)
    
    result = multiplexing(np.array([mod1, mod2]))
    np.testing.assert_array_equal(result, expected)

def test_communication_round_trip():
    # 送信 -> 変調 -> 復調 の流れを確認
    send_data = np.array([1, 0, 1], dtype=bool)
    key = np.array([1, 0, 1], dtype=bool)
    
    # 変調
    modulated = modulate(send_data, key)
    # 復調
    demodulated_signal = demodulate(modulated, key)
    
    # 復調直後はスライド計算の結果なので、キーの長さごとにサンプリングして元の値を確認
    # (実装のmain文にあるロジックを参考に抽出)
    result_bits = demodulated_signal[::len(key)]
    np.testing.assert_array_equal(result_bits, send_data)