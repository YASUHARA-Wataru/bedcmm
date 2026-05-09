import pytest
import numpy as np
from bedcmm.pattern.py_impl import pattern, periodicity

def test_pattern_1d_calculation():
    # パターンマッチングの数値計算テスト
    data = np.array([1.0, 0.0, 2.0, 4.0, 0.0, 8.0], dtype=np.float64)
    base = np.array([1.0, 0.0, 2.0], dtype=np.float64)
    
    # インデックス0: [1,0,2]/[1,0,2] -> min(1/1, 2/2) = 1.0
    # インデックス3: [4,0,8]/[1,0,2] -> min(4/1, 8/2) = 4.0
    result = pattern(data, base)
    
    assert result[0] == 1.0
    assert result[3] == 4.0

def test_periodicity_warning_on_negative(recwarn):
    # 負の値が含まれる場合に警告が出るかテスト
    data = np.array([-1.0, 2.0, 3.0])
    periodicity(data)
    
    assert len(recwarn) > 0
    assert "data contains negative" in str(recwarn[-1].message)

def test_pattern_dimension_mismatch():
    # データとベースの次元が合わない場合に例外を投げるか
    data = np.array([1, 2, 3])
    base = np.array([[1, 2], [3, 4]]) # 2D base vs 1D data
    
    with pytest.raises(Exception) as excinfo:
        pattern(data, base)
    assert "base must be same dimention" in str(excinfo.value)