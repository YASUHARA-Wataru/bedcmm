# -*- coding: utf-8 -*-
# cython: boundscheck=False, wraparound=False, cdivision=True
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
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

    # データの平均をあらかじめ計算（lag=0用）
    for i in range(n_data):
        mean_val += data[i]
    mean_val /= <double> n_data

    for p_idx in range(n_conts):
        lag = conts[p_idx]
        
        if lag == 0:
            result[p_idx] = mean_val
            continue
            
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

            if (lag1 == 0) & (lag2 == 0):
                result[p_idx1,p_idx2] = mean_val
                continue
                
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

                if (lag1 == 0) & (lag2 == 0) & (lag3 == 0):
                    result[p_idx1,p_idx2] = mean_val
                    continue
                    
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
