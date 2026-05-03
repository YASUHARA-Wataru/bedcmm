# -*- coding: utf-8 -*-
# cython: boundscheck=False, wraparound=False, cdivision=True
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
# cython: language_level=3
"""
bedcmm pattern analysis method class(Cython)

Author: YASUHARA Wataru
Copyright (c) 2025, Feel a Piece of the World
"""
import numpy as np
cimport numpy as np
cimport cython

ctypedef np.float64_t DTYPE_d_t
ctypedef np.int32_t DTYPE_i_t

# Cレベルの関数を利用するために math をインポート
from libc.math cimport fmin
from libc.math cimport INFINITY
from libc.math cimport isnan

cpdef np.ndarray[DTYPE_d_t, ndim=1] _pattern_1d_cy(double[:] data,double[:] base):

    cdef np.ndarray[DTYPE_d_t, ndim=1] result
    cdef double temp_result
    cdef Py_ssize_t index
    cdef Py_ssize_t n_data, n_base
    cdef Py_ssize_t i
    cdef Py_ssize_t posi_cnt,nega_cnt,all_cnt
    cdef Py_ssize_t nega_posi_flag

    n_data = data.shape[0]
    n_base = base.shape[0]
    
    result = np.zeros(n_data + 1 - n_base, dtype=np.float64)

    for index in range(n_data + 1 - n_base):
        # negative check
        all_cnt = 0
        posi_cnt = 0
        nega_cnt = 0
        for i in range(n_base):
            if base[i] != 0:
                if (data[index+i] > 0 and base[i] > 0) or (data[index+i] < 0 and base[i] < 0):
                    all_cnt += 1
                    posi_cnt += 1
                elif (data[index+i] > 0 and base[i] < 0) or (data[index+i] < 0 and base[i] > 0):
                    all_cnt += 1
                    nega_cnt += 1

        if all_cnt == posi_cnt:
            nega_posi_flag = 1
        elif all_cnt == nega_cnt:
            nega_posi_flag = -1
        else:
            nega_posi_flag = 0

        # calc pattern
        if nega_posi_flag == 1:
            temp_result = INFINITY
            for i in range(n_base):
                if base[i] != 0:
                    if temp_result > <double> data[index+i]/base[i]:
                        temp_result = <double> data[index+i]/base[i]
            result[index] = temp_result

        elif nega_posi_flag == -1:
            temp_result = -INFINITY
            for i in range(n_base):
                if base[i] != 0:
                    if temp_result < <double> data[index+i]/base[i]:
                        temp_result = <double> data[index+i]/base[i]
            result[index] = temp_result
        else:
            result[index] = 0

    return result

cpdef np.ndarray[DTYPE_d_t, ndim=2] _pattern_2d_cy(double[:,:] data,double[:,:] base):

    cdef np.ndarray[DTYPE_d_t, ndim=2] result
    cdef double temp_result
    cdef Py_ssize_t index1,index2
    cdef Py_ssize_t n_data1, n_data2, n_base1, n_base2
    cdef Py_ssize_t i,j
    cdef Py_ssize_t posi_cnt,nega_cnt,all_cnt
    cdef Py_ssize_t nega_posi_flag

    n_data1 = data.shape[0]
    n_data2 = data.shape[1]
    n_base1 = base.shape[0]
    n_base2 = base.shape[1]
    
    result = np.zeros((n_data1 + 1 - n_base1, n_data2 + 1- n_base2), dtype=np.float64)

    for index1 in range(n_data1 + 1 - n_base1):
        for index2 in range(n_data2 + 1 - n_base2):
            # negative check
            all_cnt = 0
            posi_cnt = 0
            nega_cnt = 0
            for i in range(n_base1):
                for j in range(n_base2):
                    if base[i,j] != 0:
                        if (data[index1+i,index2+j] > 0 and base[i,j] > 0) or (data[index1+i,index2+j] < 0 and base[i,j] < 0):
                            all_cnt += 1
                            posi_cnt += 1
                        elif (data[index1+i,index2+j] > 0 and base[i,j] < 0) or (data[index1+i,index2+j] < 0 and base[i,j] > 0):
                            all_cnt += 1
                            nega_cnt += 1

            if all_cnt == posi_cnt:
                nega_posi_flag = 1
            elif all_cnt == nega_cnt:
                nega_posi_flag = -1
            else:
                nega_posi_flag = 0

            # calc pattern
            if nega_posi_flag == 1:
                temp_result = INFINITY
                for i in range(n_base1):
                    for j in range(n_base2):
                        if base[i,j] != 0:
                            if temp_result > <double> data[index1+i,index2+j]/base[i,j]:
                                temp_result = <double> data[index1+i,index2+j]/base[i,j]
                result[index1,index2] = temp_result

            elif nega_posi_flag == -1:
                temp_result = -INFINITY
                for i in range(n_base1):
                    for j in range(n_base2):
                        if base[i,j] != 0:
                            if temp_result < <double> data[index1+i,index2+j]/base[i,j]:
                                temp_result = <double> data[index1+i,index2+j]/base[i,j]
                result[index1,index2] = temp_result
            else:
                result[index1,index2] = 0

    return result

cpdef np.ndarray[DTYPE_d_t, ndim=3] _pattern_3d_cy(double[:,:,:] data,double[:,:,:] base):

    cdef np.ndarray[DTYPE_d_t, ndim=3] result
    cdef double temp_result
    cdef Py_ssize_t index1,index2,index3
    cdef Py_ssize_t n_data1, n_data2, n_data3, n_base1, n_base2, n_base3
    cdef Py_ssize_t i,j,k
    cdef Py_ssize_t posi_cnt,nega_cnt,all_cnt
    cdef Py_ssize_t nega_posi_flag

    n_data1 = data.shape[0]
    n_data2 = data.shape[1]
    n_data3 = data.shape[2]
    n_base1 = base.shape[0]
    n_base2 = base.shape[1]
    n_base3 = base.shape[2]
    
    result = np.zeros((n_data1 + 1 - n_base1, n_data2 + 1 - n_base2, n_data3 + 1 - n_base3), dtype=np.float64)

    for index1 in range(n_data1 + 1 - n_base1):
        for index2 in range(n_data2 + 1 - n_base2):
            for index3 in range(n_data3 + 1 - n_base3):
                # negative check
                all_cnt = 0
                posi_cnt = 0
                nega_cnt = 0
                for i in range(n_base1):
                    for j in range(n_base2):
                        for k in range(n_base3):
                            if base[i,j,k] != 0:
                                if (data[index1+i,index2+j,index3+k] > 0 and base[i,j,k] > 0) or (data[index1+i,index2+j,index3+k] < 0 and base[i,j,k] < 0):
                                    all_cnt += 1
                                    posi_cnt += 1
                                elif (data[index1+i,index2+j,index3+k] > 0 and base[i,j,k] < 0) or (data[index1+i,index2+j,index3+k] < 0 and base[i,j,k] > 0):
                                    all_cnt += 1
                                    nega_cnt += 1

                if all_cnt == posi_cnt:
                    nega_posi_flag = 1
                elif all_cnt == nega_cnt:
                    nega_posi_flag = -1
                else:
                    nega_posi_flag = 0

                # calc pattern
                if nega_posi_flag == 1:
                    temp_result = INFINITY
                    for i in range(n_base1):
                        for j in range(n_base2):
                            for k in range(n_base3):
                                if base[i,j,k] != 0:
                                    if temp_result > <double> data[index1+i,index2+j,index3+k]/base[i,j,k]:
                                        temp_result = <double> data[index1+i,index2+j,index3+k]/base[i,j,k]
                    result[index1,index2,index3] = temp_result

                elif nega_posi_flag == -1:
                    temp_result = -INFINITY
                    for i in range(n_base1):
                        for j in range(n_base2):
                            for k in range(n_base3):
                                if base[i,j,k] != 0:
                                    if temp_result < <double> data[index1+i,index2+j,index3+k]/base[i,j,k]:
                                        temp_result = <double> data[index1+i,index2+j,index3+k]/base[i,j,k]
                    result[index1,index2,index3] = temp_result
                else:
                    result[index1,index2,index3] = 0

    return result

cpdef np.ndarray[DTYPE_d_t, ndim=1] _periodicity_1d_core_cy(double[:] data, Py_ssize_t[:] periods):
    """
    1次元データの周期性解析コアロジック (Cython版)
    """
    cdef Py_ssize_t n_data = data.shape[0]
    cdef Py_ssize_t n_periods = periods.shape[0]
    cdef np.ndarray[DTYPE_d_t, ndim=1] result = np.zeros(n_periods, dtype=np.float64)
    
    cdef Py_ssize_t p_idx, i, lag
    cdef double temp_sum
    cdef Py_ssize_t count
    cdef double mean_val = 0

    for p_idx in range(n_periods):
        lag = periods[p_idx]
        
        temp_sum = 0
        count = n_data - lag
        
        # 内側のループを純粋なCで回す
        # スライシングを使わず、インデックス i と i+lag を直接比較
        for i in range(count):
            # libc.math.fmin を使うことで Python の min() 呼び出しを回避
            temp_sum += fmin(data[i], data[i + lag])
                
        if count > 0:
            result[p_idx] = <double> temp_sum / count
        else:
            result[p_idx] = 0
            
    return result


cpdef np.ndarray[DTYPE_d_t, ndim=2] _periodicity_2d_core_cy(double[:,:] data, Py_ssize_t[:] periods1, Py_ssize_t[:] periods2):
    """
    2次元データの周期性解析コアロジック (Cython版)
    """
    cdef Py_ssize_t n_data1 = data.shape[0]
    cdef Py_ssize_t n_data2 = data.shape[1]
    cdef Py_ssize_t n_periods1 = periods1.shape[0]
    cdef Py_ssize_t n_periods2 = periods2.shape[0]
    cdef np.ndarray[DTYPE_d_t, ndim=2] result = np.zeros((n_periods1,n_periods2), dtype=np.float64)
    
    cdef Py_ssize_t p_idx1, p_idx2, i, j, lag1, lag2 
    cdef double temp_sum
    cdef Py_ssize_t count1, count2
    cdef double mean_val = 0

    for p_idx1 in range(n_periods1):
        for p_idx2 in range(n_periods2):
            lag1 = periods1[p_idx1]
            lag2 = periods2[p_idx2]
                
            temp_sum = 0
            count1 = n_data1 - lag1
            count2 = n_data2 - lag2
            
            # 内側のループを純粋なCで回す
            # スライシングを使わず、インデックス i と i+lag を直接比較
            for i in range(count1):
                for j in range(count2):
                    # libc.math.fmin を使うことで Python の min() 呼び出しを回避
                    temp_sum += fmin(data[i,j], data[i + lag1,j + lag2])
                    
            if (count1 > 0) & (count2 > 0):
                result[p_idx1,p_idx2] = <double> temp_sum / (count1 * count2)
            else:
                result[p_idx1,p_idx2] = 0
            
    return result


cpdef np.ndarray[DTYPE_d_t, ndim=3] _periodicity_3d_core_cy(double[:,:,:] data, Py_ssize_t[:] periods1, Py_ssize_t[:] periods2, Py_ssize_t[:] periods3):
    """
    3次元データの周期性解析コアロジック (Cython版)
    """
    cdef Py_ssize_t n_data1 = data.shape[0]
    cdef Py_ssize_t n_data2 = data.shape[1]
    cdef Py_ssize_t n_data3 = data.shape[2]
    cdef Py_ssize_t n_periods1 = periods1.shape[0]
    cdef Py_ssize_t n_periods2 = periods2.shape[0]
    cdef Py_ssize_t n_periods3 = periods3.shape[0]
    cdef np.ndarray[DTYPE_d_t, ndim=3] result = np.zeros((n_periods1,n_periods2,n_periods3), dtype=np.float64)
    
    cdef Py_ssize_t p_idx1, p_idx2, p_idx3, i, j, k, lag1, lag2, lag3
    cdef double temp_sum
    cdef Py_ssize_t count1, count2, count3
    cdef double mean_val = 0

    for p_idx1 in range(n_periods1):
        for p_idx2 in range(n_periods2):
            for p_idx3 in range(n_periods3):
                lag1 = periods1[p_idx1]
                lag2 = periods2[p_idx2]
                lag3 = periods3[p_idx3]
                    
                temp_sum = 0
                count1 = n_data1 - lag1
                count2 = n_data2 - lag2
                count3 = n_data3 - lag3
                
                # 内側のループを純粋なCで回す
                # スライシングを使わず、インデックス i と i+lag を直接比較
                for i in range(count1):
                    for j in range(count2):
                        for k in range(count3):
                            # libc.math.fmin を使うことで Python の min() 呼び出しを回避
                            temp_sum += fmin(data[i,j,k], data[i + lag1,j + lag2,k + lag3])
                        
                if (count1 > 0) & (count2 > 0) & (count3 > 0):
                    result[p_idx1,p_idx2,p_idx3] = <double> temp_sum / (count1 * count2 * count3)
                else:
                    result[p_idx1,p_idx2,p_idx3] = 0
            
    return result

cpdef np.ndarray[DTYPE_d_t, ndim=1] _continuity_1d_core_cy(double[:] data, Py_ssize_t[:] conts):
    """
    1次元データの連続性解析コアロジック (Cython版)
    """
    cdef Py_ssize_t n_data = data.shape[0]
    cdef Py_ssize_t n_conts = conts.shape[0]
    cdef np.ndarray[DTYPE_d_t, ndim=1] result = np.zeros(n_conts, dtype=np.float64)
    
    cdef Py_ssize_t p_idx, i, j, lag
    cdef double temp_sum,temp_min
    cdef Py_ssize_t count
    cdef double mean_val = 0

    for p_idx in range(n_conts):
        lag = conts[p_idx]
        
        temp_sum = 0
        count = n_data - lag
        
        # 内側のループを純粋なCで回す
        # スライシングを使わず、インデックス i と i+lag を直接比較
        for i in range(count):
            temp_min = data[i]
            for j in range(lag+1):
                if data[i + j] < temp_min:
                    temp_min = data[i+j]

            temp_sum += temp_min
                
        if count > 0:
            result[p_idx] = <double> temp_sum / count
        else:
            result[p_idx] = 0
            
    return result

cpdef np.ndarray[DTYPE_d_t, ndim=2] _continuity_2d_core_cy(double[:,:] data, Py_ssize_t[:] conts1, Py_ssize_t[:] conts2):
    """
    2次元データの連続性解析コアロジック (Cython版)
    """
    cdef Py_ssize_t n_data1 = data.shape[0]
    cdef Py_ssize_t n_data2 = data.shape[1]
    cdef Py_ssize_t n_conts1 = conts1.shape[0]
    cdef Py_ssize_t n_conts2 = conts2.shape[0]
    cdef np.ndarray[DTYPE_d_t, ndim=2] result = np.zeros((n_conts1,n_conts2), dtype=np.float64)
    
    cdef Py_ssize_t p_idx1, p_idx2, i, j, k, l, lag1, lag2, num_cnt 
    cdef double temp_sum, temp_min
    cdef Py_ssize_t count1, count2
    cdef double mean_val = 0

    # データの平均をあらかじめ計算（lag=0用）
    for i in range(n_data1):
        for j in range(n_data2):
            mean_val += data[i,j]
    mean_val /= <double> n_data1*n_data2

    for p_idx1 in range(n_conts1):
        for p_idx2 in range(n_conts2):
            lag1 = conts1[p_idx1]
            lag2 = conts2[p_idx2]
                
            temp_sum = 0
            count1 = n_data1 - lag1
            count2 = n_data2 - lag2
            num_cnt = 0
            # 内側のループを純粋なCで回す
            # スライシングを使わず、インデックス i と i+lag を直接比較
            for i in range(count1):
                for j in range(count2):
                    temp_min = data[i,j]
                    for k in range(lag1+1):
                        for l in range(lag2+1):
                            if data[i+k,j+l] < temp_min:
                                temp_min = data[i+k,j+l]

                    num_cnt += 1
                    temp_sum += temp_min
                    
            if (count1 > 0) & (count2 > 0):
                result[p_idx1,p_idx2] = <double> temp_sum / num_cnt
            else:
                result[p_idx1,p_idx2] = 0
            
    return result


cpdef np.ndarray[DTYPE_d_t, ndim=3] _continuity_3d_core_cy(double[:,:,:] data, Py_ssize_t[:] conts1, Py_ssize_t[:] conts2, Py_ssize_t[:] conts3):
    """
    3次元データの連続性解析コアロジック (Cython版)
    """
    cdef Py_ssize_t n_data1 = data.shape[0]
    cdef Py_ssize_t n_data2 = data.shape[1]
    cdef Py_ssize_t n_data3 = data.shape[2]
    cdef Py_ssize_t n_conts1 = conts1.shape[0]
    cdef Py_ssize_t n_conts2 = conts2.shape[0]
    cdef Py_ssize_t n_conts3 = conts3.shape[0]
    cdef np.ndarray[DTYPE_d_t, ndim=3] result = np.zeros((n_conts1,n_conts2,n_conts3), dtype=np.float64)
    
    cdef Py_ssize_t p_idx1, p_idx2, p_idx3, i, j, k, l, m, n, lag1, lag2, lag3, num_cnt
    cdef double temp_sum, temp_min
    cdef Py_ssize_t count1, count2, count3
    cdef double mean_val = 0

    # データの平均をあらかじめ計算（lag=0用）
    for i in range(n_data1):
        for j in range(n_data2):
            for k in range(n_data3):
                mean_val += data[i,j,k]
    mean_val /= <double> n_data1*n_data2*n_data3

    for p_idx1 in range(n_conts1):
        for p_idx2 in range(n_conts2):
            for p_idx3 in range(n_conts3):
                lag1 = conts1[p_idx1]
                lag2 = conts2[p_idx2]
                lag3 = conts3[p_idx3]
                    
                temp_sum = 0
                count1 = n_data1 - lag1
                count2 = n_data2 - lag2
                count3 = n_data3 - lag3
                num_cnt = 0
                # 内側のループを純粋なCで回す
                # スライシングを使わず、インデックス i と i+lag を直接比較
                for i in range(count1):
                    for j in range(count2):
                        for k in range(count3):
                            temp_min = data[i,j,k]
                            for l in range(lag1+1):
                                for m in range(lag2+1):
                                    for n in range(lag3+1):
                                        if data[i+l,j+m,k+n] < temp_min:
                                            temp_min = data[i+l,j+m,k+n]
                            num_cnt += 1
                            temp_sum += temp_min
                        
                if (count1 > 0) & (count2 > 0) & (count3 > 0):
                    result[p_idx1,p_idx2,p_idx3] = <double> temp_sum / num_cnt
                else:
                    result[p_idx1,p_idx2,p_idx3] = 0
            
    return result


def _nanperiodicity_1d_core_cy(
    np.ndarray[np.float64_t, ndim=1] data,
    np.ndarray[np.int64_t, ndim=1] period
):
    cdef Py_ssize_t p_len = period.shape[0]
    cdef Py_ssize_t max_len = data.shape[0]

    cdef np.ndarray[np.float64_t, ndim=1] result = np.zeros(p_len, dtype=np.float64)
    cdef np.ndarray[np.float64_t, ndim=1] valid_ratio = np.zeros(p_len, dtype=np.float64)

    cdef Py_ssize_t p_idx, i
    cdef Py_ssize_t a_period
    cdef Py_ssize_t total_count, valid_count
    cdef double valid_sum
    cdef double x, y

    for p_idx in range(p_len):
        a_period = period[p_idx]

        valid_sum = 0.0
        valid_count = 0
        total_count = max_len - a_period

        for i in range(max_len - a_period):

            x = data[i]
            y = data[i + a_period]

            if not (isnan(x) or isnan(y)):
                if x < y:
                    valid_sum += x
                else:
                    valid_sum += y
                valid_count += 1

        if valid_count > 0:
            result[p_idx] = valid_sum / valid_count
        else:
            result[p_idx] = np.nan

        if total_count > 0:
            valid_ratio[p_idx] = <double>valid_count / <double>total_count
        else:
            valid_ratio[p_idx] = 0.0

    return result, valid_ratio

def _nanperiodicity_2d_core_cy(
    np.ndarray[np.float64_t, ndim=2] data,
    np.ndarray[np.int64_t, ndim=1] period1_list,
    np.ndarray[np.int64_t, ndim=1] period2_list
):
    cdef Py_ssize_t p1_len = period1_list.shape[0]
    cdef Py_ssize_t p2_len = period2_list.shape[0]

    cdef Py_ssize_t max_len1 = data.shape[0]
    cdef Py_ssize_t max_len2 = data.shape[1]

    cdef np.ndarray[np.float64_t, ndim=2] result = np.zeros((p1_len, p2_len), dtype=np.float64)
    cdef np.ndarray[np.float64_t, ndim=2] valid_ratio = np.zeros((p1_len, p2_len), dtype=np.float64)

    cdef Py_ssize_t p1_idx, p2_idx, i, j
    cdef Py_ssize_t period1, period2
    cdef Py_ssize_t total_count, valid_count
    cdef double valid_sum
    cdef double x, y

    for p1_idx in range(p1_len):
        period1 = period1_list[p1_idx]

        for p2_idx in range(p2_len):
            period2 = period2_list[p2_idx]

            valid_sum = 0.0
            valid_count = 0
            total_count = (max_len1 - period1) * (max_len2 - period2)

            for i in range(max_len1 - period1):
                for j in range(max_len2 - period2):

                    x = data[i, j]
                    y = data[i + period1, j + period2]

                    if not (isnan(x) or isnan(y)):
                        if x < y:
                            valid_sum += x
                        else:
                            valid_sum += y
                        valid_count += 1

            if valid_count > 0:
                result[p1_idx, p2_idx] = valid_sum / valid_count
            else:
                result[p1_idx, p2_idx] = np.nan

            if total_count > 0:
                valid_ratio[p1_idx, p2_idx] = <double>valid_count / <double>total_count
            else:
                valid_ratio[p1_idx, p2_idx] = 0.0

    return result, valid_ratio

def _nanperiodicity_3d_core_cy(
    np.ndarray[np.float64_t, ndim=3] data,
    np.ndarray[np.int64_t, ndim=1] period1_list,
    np.ndarray[np.int64_t, ndim=1] period2_list,
    np.ndarray[np.int64_t, ndim=1] period3_list
):
    cdef Py_ssize_t p1_len = period1_list.shape[0]
    cdef Py_ssize_t p2_len = period2_list.shape[0]
    cdef Py_ssize_t p3_len = period3_list.shape[0]

    cdef Py_ssize_t max_len1 = data.shape[0]
    cdef Py_ssize_t max_len2 = data.shape[1]
    cdef Py_ssize_t max_len3 = data.shape[2]

    cdef np.ndarray[np.float64_t, ndim=3] result = np.zeros((p1_len, p2_len, p3_len), dtype=np.float64)
    cdef np.ndarray[np.float64_t, ndim=3] valid_ratio = np.zeros_like(result)

    cdef Py_ssize_t p1_idx, p2_idx, p3_idx, i, j, k
    cdef Py_ssize_t period1, period2, period3
    cdef Py_ssize_t total_count, valid_count
    cdef double valid_sum
    cdef double x, y

    for p1_idx in range(p1_len):
        period1 = period1_list[p1_idx]

        for p2_idx in range(p2_len):
            period2 = period2_list[p2_idx]

            for p3_idx in range(p3_len):
                period3 = period3_list[p3_idx]

                valid_sum = 0.0
                valid_count = 0

                total_count = (
                    (max_len1 - period1)
                    * (max_len2 - period2)
                    * (max_len3 - period3)
                )

                for i in range(max_len1 - period1):
                    for j in range(max_len2 - period2):
                        for k in range(max_len3 - period3):

                            x = data[i, j, k]
                            y = data[i + period1, j + period2, k + period3]

                            if not (isnan(x) or isnan(y)):
                                if x < y:
                                    valid_sum += x
                                else:
                                    valid_sum += y
                                valid_count += 1

                if valid_count > 0:
                    result[p1_idx, p2_idx, p3_idx] = valid_sum / valid_count
                else:
                    result[p1_idx, p2_idx, p3_idx] = np.nan

                if total_count > 0:
                    valid_ratio[p1_idx, p2_idx, p3_idx] = <double>valid_count / <double>total_count
                else:
                    valid_ratio[p1_idx, p2_idx, p3_idx] = 0.0

    return result, valid_ratio

def _cross_periodicity_1d_core_cy(
    double[::1] x,
    double[::1] y,
    np.int64_t[::1] periods
):
    cdef Py_ssize_t i, p_idx, n = x.shape[0]
    cdef Py_ssize_t y_n = y.shape[0]
    cdef Py_ssize_t period
    cdef double temp_sum
    cdef long count

    cdef np.ndarray[np.float64_t, ndim=1] result = np.zeros(periods.shape[0], dtype=np.float64)

    for p_idx in range(periods.shape[0]):
        period = periods[p_idx]
        temp_sum = 0.0
        count = 0

        for i in range(n):
            if i + period < y_n:
                if x[i] < y[i + period]:
                    temp_sum += x[i]
                else:
                    temp_sum += y[i + period]
                count += 1

        if count > 0:
            result[p_idx] = temp_sum / count
        else:
            result[p_idx] = 0.0

    return result

def _cross_periodicity_2d_core_cy(
    double[:, ::1] x,
    double[:, ::1] y,
    np.int64_t[::1] px_list,
    np.int64_t[::1] py_list
):
    cdef Py_ssize_t H = x.shape[0]
    cdef Py_ssize_t W = x.shape[1]
    cdef Py_ssize_t yH = y.shape[0]
    cdef Py_ssize_t yW = y.shape[1]

    cdef Py_ssize_t ix, iy, i, j
    cdef Py_ssize_t px, py
    cdef Py_ssize_t ni, nj

    cdef double temp_sum
    cdef long count

    cdef np.ndarray[np.float64_t, ndim=2] result = np.zeros(
        (px_list.shape[0], py_list.shape[0]),
        dtype=np.float64
    )

    for ix in range(px_list.shape[0]):
        px = px_list[ix]

        for iy in range(py_list.shape[0]):
            py = py_list[iy]

            temp_sum = 0.0
            count = 0

            for i in range(H):
                ni = i + px
                if ni < 0 or ni >= yH:
                    continue

                for j in range(W):
                    nj = j + py
                    if nj < 0 or nj >= yW:
                        continue

                    if x[i, j] < y[ni, nj]:
                        temp_sum += x[i, j]
                    else:
                        temp_sum += y[ni, nj]

                    count += 1

            if count > 0:
                result[ix, iy] = temp_sum / count
            else:
                result[ix, iy] = 0.0

    return result
    
def _cross_periodicity_3d_core_cy(
    double[:, :, ::1] x,
    double[:, :, ::1] y,
    np.int64_t[::1] px_list,
    np.int64_t[::1] py_list,
    np.int64_t[::1] pz_list
):
    cdef Py_ssize_t D = x.shape[0]
    cdef Py_ssize_t H = x.shape[1]
    cdef Py_ssize_t W = x.shape[2]

    cdef Py_ssize_t yD = y.shape[0]
    cdef Py_ssize_t yH = y.shape[1]
    cdef Py_ssize_t yW = y.shape[2]

    cdef Py_ssize_t ix, iy, iz, i, j, k
    cdef Py_ssize_t px, py, pz
    cdef Py_ssize_t ni, nj, nk

    cdef double temp_sum
    cdef long count

    cdef np.ndarray[np.float64_t, ndim=3] result = np.zeros(
        (px_list.shape[0], py_list.shape[0], pz_list.shape[0]),
        dtype=np.float64
    )

    for ix in range(px_list.shape[0]):
        px = px_list[ix]

        for iy in range(py_list.shape[0]):
            py = py_list[iy]

            for iz in range(pz_list.shape[0]):
                pz = pz_list[iz]

                temp_sum = 0.0
                count = 0

                for i in range(D):
                    ni = i + px
                    if ni < 0 or ni >= yD:
                        continue

                    for j in range(H):
                        nj = j + py
                        if nj < 0 or nj >= yH:
                            continue

                        for k in range(W):
                            nk = k + pz
                            if nk < 0 or nk >= yW:
                                continue

                            if x[i, j, k] < y[ni, nj, nk]:
                                temp_sum += x[i, j, k]
                            else:
                                temp_sum += y[ni, nj, nk]

                            count += 1

                if count > 0:
                    result[ix, iy, iz] = temp_sum / count
                else:
                    result[ix, iy, iz] = 0.0

    return result