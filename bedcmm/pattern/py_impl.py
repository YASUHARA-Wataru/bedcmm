# -*- coding: utf-8 -*-
"""
bedcmm pattern analysis method class(Python)

Author: YASUHARA Wataru
Copyright (c) 2025, Feel a Piece of the World
"""
import numpy as np
from ._config import implementation
if implementation == 'Cython':
    from .cy_impl import _pattern_1d_cy,_pattern_2d_cy,_pattern_3d_cy
    from .cy_impl import _periodicity_1d_core_cy,_periodicity_2d_core_cy,_periodicity_3d_core_cy
    from .cy_impl import _continuity_1d_core_cy,_continuity_2d_core_cy,_continuity_3d_core_cy


def period2index(period_min,period_max,fs):

    index_min = np.ceil(period_min/fs)
    index_max = np.floor(period_max/fs)

    if index_min <= index_max:
        raise Exception('period min lager than period max.')

    index = np.arange(index_min,index_max)

    return index

def pattern(data,base):
    data = np.ascontiguousarray(data, dtype=np.float64)
    base = np.ascontiguousarray(base, dtype=np.float64)
    data_dim = data.ndim

    if data_dim == 1:
        if base.ndim != 1:
            raise Exception('base must be same dimention with data array.')
        
        if implementation == 'Cython':
            result = _pattern_1d_cy(data,base)
        elif implementation == 'Python':
            result = _pattern_1d(data,base)
        else:
            raise Exception('error')

    elif data_dim == 2:
        if base.ndim != 2:
            raise Exception('base must be same dimention with data array.')
        
        if implementation == 'Cython':
            result = _pattern_2d_cy(data,base)
        elif implementation == 'Python':
            result = _pattern_2d(data,base)
        else:
            raise Exception('error')

    elif data_dim == 3:
        if base.ndim != 3:
            raise Exception('base must be same dimention with data array.')
        
        if implementation == 'Cython':
            result = _pattern_3d_cy(data,base)
        elif implementation == 'Python':
            result = _pattern_3d(data,base)
        else:
            raise Exception('error')
    else:
        raise Exception('data is too big dimention.')

    return result

def _pattern_1d(data,base):
    
    result = np.zeros(data.shape[0] + 1 - base.shape[0])
    for index in range(data.shape[0] + 1 - base.shape[0]):
        tmp_data = data[index:index+base.shape[0]]
        tmp_result = tmp_data[base != 0] / base[base!=0]
        if tmp_result[tmp_result >= 0].shape[0] == tmp_result.shape[0] :
            result[index] = min(tmp_result[tmp_result >= 0])
        elif tmp_result[tmp_result <= 0].shape[0] == tmp_result.shape[0]:
            result[index] = max(tmp_result[tmp_result <= 0])
        else:
            result[index] = 0
    
    return result

def _pattern_2d(data,base):
    
    result = np.zeros((data.shape[0] + 1 - base.shape[0],data.shape[1] + 1  - base.shape[1]))
    
    for i_index in range(data.shape[0] + 1  - base.shape[0]):
        for j_index in range(data.shape[1] + 1  - base.shape[1]):
            tmp_data = data[i_index:i_index+base.shape[0],j_index:j_index+base.shape[1]]
            tmp_result = tmp_data[base != 0] / base[base!=0]
            if tmp_result[tmp_result >= 0].shape[0] == tmp_result.shape[0] :
                result[i_index,j_index] = min(tmp_result[tmp_result >= 0])
            elif tmp_result[tmp_result <= 0].shape[0] == tmp_result.shape[0]:
                result[i_index,j_index] = max(tmp_result[tmp_result <= 0])
            else:
                result[i_index,j_index] = 0
    
    return result

def _pattern_3d(data,base):

    result = np.zeros((data.shape[0] + 1  - base.shape[0],data.shape[1] + 1  - base.shape[1],data.shape[2] + 1  - base.shape[2]))
    
    for i_index in range(data.shape[0] + 1  - base.shape[0]):
        for j_index in range(data.shape[1] + 1  - base.shape[1]):
            for k_index in range(data.shape[2] + 1  - base.shape[2]):
                tmp_data = data[i_index:i_index+base.shape[0],
                                j_index:j_index+base.shape[1],
                                k_index:k_index+base.shape[2]]
                tmp_result = tmp_data[base != 0] / base[base!=0]
                if tmp_result[tmp_result >= 0].shape[0] == tmp_result.shape[0] :
                    result[i_index,j_index,k_index] = min(tmp_result[tmp_result >= 0])
                elif tmp_result[tmp_result <= 0].shape[0] == tmp_result.shape[0]:
                    result[i_index,j_index,k_index] = max(tmp_result[tmp_result <= 0])
                else:
                    result[i_index,j_index,k_index] = 0
    
    return result

def periodicity(data, periods=None):

    data = np.ascontiguousarray(data, dtype=np.float64)
    data_dim = data.ndim

    if np.min(data) < 0:
        raise Exception('data must be positive.')
    
    # periodsのバリデーションを整理
    if periods is not None:
        # 1. 次元数の不一致をまずチェック
        if data_dim == 1:
            # 1Dの場合、periods自体がリストであるべき。かつ、その中身がリストであってはならない
            if not isinstance(periods, (list, np.ndarray)):
                raise Exception('periods must be a list or array for 1D data.')
            if len(periods) > 0 and isinstance(periods[0], (list, np.ndarray)):
                raise Exception('periods for 1D data should not be a nested list.')
        else:
            # 多次元の場合、外側のリストの長さが次元数と一致すべき
            if not isinstance(periods, (list, np.ndarray)) or len(periods) != data_dim:
                raise Exception(f'periods must be a list of length {data_dim}.')
            # 各要素がリスト（各次元のラグ候補）であることをチェック
            for p in periods:
                if not isinstance(p, (list, np.ndarray)):
                    raise Exception('Each element of periods must be a list of lags for multi-dimensional data.')


    if data_dim == 1:
        result = _periodicity_1d(data,periods)
    elif data_dim == 2:
        result = _periodicity_2d(data,periods)
    elif data_dim == 3:
        result = _periodicity_3d(data,periods)
    else:
        raise Exception('data is too big dimention.')

    return result

def _periodicity_1d(data,periods):
    
    if periods is None:
        periods = np.arange(0,int(data.shape[0]/2)+1)

    period = np.ascontiguousarray(periods,dtype=np.int64)

    if implementation == 'Cython':
        result = _periodicity_1d_core_cy(data,period)
    elif implementation == 'Python':
        result = _periodicity_1d_core(data,period)
    else:
        raise Exception('error')
    
    return result

def _periodicity_1d_core(data,period):

    result = np.zeros(len(period))
    for p_idx,a_preiod in enumerate(period):
        if a_preiod == 0:
            result[p_idx] = np.mean(data)
            continue
        temp_data = np.zeros(data.shape[0] - a_preiod)
        for index in range(data.shape[0] - a_preiod):
            temp_data[index] = min([data[index],data[index+a_preiod]])
                
        result[p_idx]=np.mean((temp_data))

    return result

def _periodicity_2d(data,periods):
    
    if periods is None:
        period1_list = np.arange(0,int(data.shape[0]/2)+1)
        period2_list = np.arange(0,int(data.shape[1]/2)+1)
    else:
        period1_list = periods[0]
        period2_list = periods[1]

    period1_list = np.ascontiguousarray(period1_list,dtype=np.int64)
    period2_list = np.ascontiguousarray(period1_list,dtype=np.int64)

    if implementation == 'Cython':
        result = _periodicity_2d_core_cy(data,period1_list,period2_list)
    elif implementation == 'Python':
        result = _periodicity_2d_core(data,period1_list,period2_list)
    else:
        raise Exception('error')
        
    return result

def _periodicity_2d_core(data,period1_list,period2_list):

    result = np.zeros((len(period1_list),len(period2_list)))
    for p1_idx,preiod1 in enumerate(period1_list):
        for p2_idx,preiod2 in enumerate(period2_list):
            if preiod1 == 0 and preiod2 == 0:
                result[p1_idx,p2_idx] = np.mean(data)
                continue
            temp_data = np.zeros((data.shape[0] - preiod1,data.shape[1] - preiod2))
            for index1 in range(data.shape[0] - preiod1):
                for index2 in range(data.shape[1] - preiod2):
                    temp_data[index1,index2]=min(data[index1,index2],data[index1+preiod1,index2+preiod2])

                result[p1_idx,p2_idx]=np.mean(temp_data)
    return result

def _periodicity_3d(data,periods):
    
    if periods is None:
        period1_list = np.arange(0,int(data.shape[0]/2)+1)
        period2_list = np.arange(0,int(data.shape[1]/2)+1)
        period3_list = np.arange(0,int(data.shape[2]/2)+1)
    else:
        period1_list = periods[0]
        period2_list = periods[1]
        period3_list = periods[2]

    period1_list = np.ascontiguousarray(period1_list,dtype=np.int64)
    period2_list = np.ascontiguousarray(period2_list,dtype=np.int64)
    period3_list = np.ascontiguousarray(period3_list,dtype=np.int64)

    if implementation == 'Cython':
        result = _periodicity_3d_core_cy(data,period1_list,period2_list,period3_list)
    elif implementation == 'Python':
        result = _periodicity_3d_core(data,period1_list,period2_list,period3_list)
    else:
        raise Exception('error')
        
    return result

def _periodicity_3d_core(data,period1_list,period2_list,period3_list):

    result = np.zeros((len(period1_list),len(period2_list),len(period3_list)))

    for p1_idx,preiod1 in enumerate(period1_list):
        for p2_idx,preiod2 in enumerate(period2_list):
            for p3_idx,preiod3 in enumerate(period3_list):
                if (preiod1 == 0) and (preiod2 == 0) and (preiod3 == 0):
                    result[p1_idx,p2_idx,p3_idx] = np.mean(data)
                    continue

                temp_data = np.zeros((data.shape[0] - preiod1,data.shape[1] - preiod2,data.shape[2] - preiod3))
                for index1 in range(data.shape[0] - preiod1):
                    for index2 in range(data.shape[1] - preiod2):
                        for index3 in range(data.shape[2] - preiod3):
                            temp_data[index1,index2,index3]=min(data[index1,index2,index3],data[index1+preiod1,index2+preiod2,index3+preiod3])

                result[p1_idx,p2_idx,p3_idx]=np.mean(temp_data)
    return result

def continuity(data, conts=None):

    data = np.ascontiguousarray(data, dtype=np.float64)
    data_dim = data.ndim

    if np.min(data) < 0:
        raise Exception('data must be positive.')
    
    # periodsのバリデーションを整理
    if conts is not None:
        # 1. 次元数の不一致をまずチェック
        if data_dim == 1:
            # 1Dの場合、periods自体がリストであるべき。かつ、その中身がリストであってはならない
            if not isinstance(conts, (list, np.ndarray)):
                raise Exception('periods must be a list or array for 1D data.')
            if len(conts) > 0 and isinstance(conts[0], (list, np.ndarray)):
                raise Exception('periods for 1D data should not be a nested list.')
        else:
            # 多次元の場合、外側のリストの長さが次元数と一致すべき
            if not isinstance(conts, (list, np.ndarray)) or len(conts) != data_dim:
                raise Exception(f'periods must be a list of length {data_dim}.')
            # 各要素がリスト（各次元のラグ候補）であることをチェック
            for p in conts:
                if not isinstance(p, (list, np.ndarray)):
                    raise Exception('Each element of periods must be a list of lags for multi-dimensional data.')

    if data_dim == 1:
        result = _continuity_1d(data,conts)
    elif data_dim == 2:
        result = _continuity_2d(data,conts)
    elif data_dim == 3:
        result = _continuity_3d(data,conts)
    else:
        raise Exception('data is too big dimention.')

    return result

def _continuity_1d(data,conts):
    
    if conts is None:
        conts = np.arange(0,data.shape[0])

    period_list = np.ascontiguousarray(conts,dtype=np.int64)

    if implementation == 'Cython':
        result = _continuity_1d_core_cy(data,period_list)
    elif implementation == 'Python':
        result = _continuity_1d_core(data,period_list)
    else:
        raise Exception('error')

    return result

def _continuity_1d_core(data,conts_list):

    result = np.zeros(len(conts_list))

    max_len = data.shape[0]
    for c1_idx,cont1 in enumerate(conts_list):

        if cont1 == 0:
            result[c1_idx] = np.mean(data)
            continue

        temp_data = np.zeros(max_len - cont1)
        for index1 in range(max_len - cont1):
            temp_data[index1] = min(data[index1:index1+cont1+1].flatten())

        result[c1_idx]=np.mean(temp_data)

    return result

def _continuity_2d(data,conts):
    
    if conts is None:
        conts1_list = np.arange(0,data.shape[0])
        conts2_list = np.arange(0,data.shape[1])
    else:
        conts1_list = conts[0]
        conts2_list = conts[1]

    conts1_list = np.ascontiguousarray(conts1_list,dtype=np.int64)
    conts2_list = np.ascontiguousarray(conts2_list,dtype=np.int64)
    
    if implementation == 'Cython':
        result = _continuity_2d_core_cy(data,conts1_list,conts2_list)
    elif implementation == 'Python':
        result = _continuity_2d_core(data,conts1_list,conts2_list)
    else:
        raise Exception('error')

    return result

def _continuity_2d_core(data,conts1_list,conts2_list):

    result = np.zeros((len(conts1_list),len(conts2_list)))
    
    max_len1 = data.shape[0]
    max_len2 = data.shape[1]

    for c1_idx,cont1 in enumerate(conts1_list):
        for c2_idx,cont2 in enumerate(conts2_list):

            if cont1 == 0 and cont2 == 0:
                result[c1_idx,c2_idx] = np.mean(data)

            temp_data = np.zeros((max_len1 - cont1,max_len2 - cont2))
            for index1 in range(max_len1 - cont1):
                for index2 in range(max_len2 - cont2):
                        temp_data[index1,index2] = min(data[index1:index1+cont1+1,index2:index2+cont2+1].flatten())
            
            result[c1_idx,c2_idx]=np.mean(temp_data)

    return result

def _continuity_3d(data,conts):
    
    if conts is None:
        conts1_list = np.arange(0,data.shape[0])
        conts2_list = np.arange(0,data.shape[1])
        conts3_list = np.arange(0,data.shape[2])
    else:
        conts1_list = conts[0]
        conts2_list = conts[1]
        conts3_list = conts[2]

    conts1_list = np.ascontiguousarray(conts1_list,dtype=np.int64)
    conts2_list = np.ascontiguousarray(conts2_list,dtype=np.int64)
    conts3_list = np.ascontiguousarray(conts3_list,dtype=np.int64)

    if implementation == 'Cython':
        result = _continuity_3d_core_cy(data,conts1_list,conts2_list,conts3_list)
    elif implementation == 'Python':
        result = _continuity_3d_core(data,conts1_list,conts2_list,conts3_list)
    else:
        raise Exception('error')

    return result

def _continuity_3d_core(data,conts1_list,conts2_list,conts3_list):

    result = np.zeros((len(conts1_list),len(conts2_list),len(conts3_list)))

    max_len1 = data.shape[0]
    max_len2 = data.shape[1]
    max_len3 = data.shape[2]

    for c1_idx,cont1 in enumerate(conts1_list):
        for c2_idx,cont2 in enumerate(conts2_list):
            for c3_idx,cont3 in enumerate(conts3_list):
                temp_data = np.zeros((max_len1 - cont1,max_len2 - cont2,max_len3 - cont3))
                for index1 in range(max_len1 - cont1):
                    for index2 in range(max_len2 - cont2):
                        for index3 in range(max_len3 - cont3):
                            temp_data[index1,index2,index3]=min(data[index1:index1+cont1+1,index2:index2+cont2+1,index3:index3+cont3+1].flatten())
                
                result[c1_idx,c2_idx,c3_idx]=np.mean(temp_data)
        
    return result


def main():
    test1d_array = [1,0,2,3.5,4,0]
    test2d_array = [[1,0,2,3.5,4,0],
                    [1,0,2,3.5,4,0],
                    [1,0,3,5,4,0],
                    [1,0,2,5,4,0],
                    [1,0,2,3.5,4,0],]
    test3d_array = [[[1,0,2,3.5,4,0],
                    [1,0,2,3.5,4,0],
                    [1,0,3,5,4,0],
                    [1,0,2,5,4,0],
                    [1,0,2,3.5,4,0],],
                    [[1,0,2,3.5,4,0],
                    [1,0,2,3.5,4,0],
                    [1,0,3,5,4,0],
                    [1,0,2,5,4,0],
                    [1,0,2,3.5,4,0],],
                    [[1,0,2,3.5,4,0],
                    [1,0,2,3.5,4,0],
                    [1,0,3,5,4,0],
                    [1,0,2,5,4,0],
                    [1,0,2,3.5,4,0],]]
    test1d_n_array = [-1,0,-2,3.5,4,0]
    test2d_n_array = [[-1,0,2,3.5,4,0],
                    [1,0,2,3.5,4,0],
                    [1,0,3,5,4,0],
                    [1,0,2,5,4,0],
                    [1,0,2,3.5,4,0],]
    test3d_n_array = [[[-1,0,2,3.5,4,0],
                    [1,0,2,3.5,4,0],
                    [1,0,3,5,4,0],
                    [1,0,2,5,4,0],
                    [1,0,2,3.5,4,0],],
                    [[1,0,2,3.5,4,0],
                    [1,0,2,3.5,4,0],
                    [1,0,3,5,4,0],
                    [1,0,2,5,4,0],
                    [1,0,2,3.5,4,0],],
                    [[1,0,2,3.5,4,0],
                    [1,0,2,3.5,4,0],
                    [1,0,3,5,4,0],
                    [1,0,2,5,4,0],
                    [1,0,2,3.5,4,0],]]


    pattern_base_1d = [1,0,2]
    pattern_base_2d = [[1,0,2],[1,0,2]]
    pattern_base_3d = [[[1,0,2],
                        [1,0,2]],
                       [[1,0,2,],
                        [1,0,2]]]
    
    test1d_array = np.array(test1d_array,dtype=np.float64)
    test2d_array = np.array(test2d_array,dtype=np.float64)
    test3d_array = np.array(test3d_array,dtype=np.float64)
    test1d_n_array = np.array(test1d_n_array,dtype=np.float64)
    test2d_n_array = np.array(test2d_n_array,dtype=np.float64)
    test3d_n_array = np.array(test3d_n_array,dtype=np.float64)
    pattern_base_1d = np.array(pattern_base_1d,dtype=np.float64)
    pattern_base_2d = np.array(pattern_base_2d,dtype=np.float64)
    pattern_base_3d = np.array(pattern_base_3d,dtype=np.float64)

    print('pattern')
    result = pattern(test1d_array,pattern_base_1d)
    print(result)
    result = pattern(test2d_array,pattern_base_2d)
    print(result)
    result = pattern(test3d_array,pattern_base_3d)
    print(result)
    result = pattern(test1d_n_array,pattern_base_1d)
    print(result)
    result = pattern(test2d_n_array,pattern_base_2d)
    print(result)
    result = pattern(test3d_n_array,pattern_base_3d)
    print(result)
    print('periodicity')
    result = periodicity(test1d_array)
    print(result)
    result = periodicity(test2d_array)
    print(result)
    result = periodicity(test3d_array)
    print(result)

    result = periodicity(test1d_array,periods=[1,2])
    print(result)
    result = periodicity(test2d_array,periods=[[1,2],[1]])
    print(result)
    result = periodicity(test3d_array,periods=[[1,2],[1],[1,2]])    
    print(result)

    print('continuity')
    result = continuity(test1d_array)
    print(result)
    result = continuity(test2d_array)
    print(result)
    result = continuity(test3d_array)
    print(result)


    result = continuity(test1d_array,conts=[1,2])
    print(result)
    result = continuity(test2d_array,conts=[[1,2],[1]])
    print(result)
    result = continuity(test3d_array,conts=[[1,2],[1],[1,2]])
    print(result)


    try:
        result = pattern(test2d_n_array,pattern_base_1d)
    except Exception as e:
        print(e)
    try:
        result = pattern(test1d_n_array,pattern_base_2d)
    except Exception as e:
        print(e)
    try:
        result = pattern(test1d_n_array,pattern_base_2d)
    except Exception as e:
        print(e)
    try:
        result = pattern(test2d_n_array,pattern_base_1d)
    except Exception as e:
        print(e)
    try:
        result = pattern(test1d_n_array,pattern_base_3d)
    except Exception as e:
        print(e)
    try:
        result = pattern(test3d_n_array,pattern_base_1d)
    except Exception as e:
        print(e)

    print('negative error check')
    try:
        result = periodicity(test1d_n_array)
    except Exception as e:
        print(e)
    try:
        result = periodicity(test2d_n_array)
    except Exception as e:
        print(e)
    try:
        result = periodicity(test2d_n_array)
    except Exception as e:
        print(e)
    try:
        result = periodicity(test1d_n_array)
    except Exception as e:
        print(e)
    try:
        result = periodicity(test3d_n_array)
    except Exception as e:
        print(e)    
    try:
        result = periodicity(test1d_n_array)
    except Exception as e:
        print(e)    

    try:
        result = continuity(test1d_n_array)
    except Exception as e:
        print(e)
    try:
        result = continuity(test2d_n_array)
    except Exception as e:
        print(e)

    try:
        result = continuity(test2d_n_array)
    except Exception as e:
        print(e)
    try:
        result = continuity(test1d_n_array)
    except Exception as e:
        print(e)

    try:
        result = continuity(test3d_n_array)
    except Exception as e:
        print(e)
    try:
        result = continuity(test1d_n_array)
    except Exception as e:
        print(e)
    

    print('periods error check')
    try:
        result = periodicity(test1d_array,periods=[[1,2],[1,2]])
    except Exception as e:
        print(e)
    try:
        result = periodicity(test3d_array,periods=[1,2])
    except Exception as e:
        print(e)    
    try:
        result = periodicity(test2d_array,periods=[[1,2],[1,2],[1,2]])
    except Exception as e:
        print(e)    

    try:
        result = continuity(test1d_array,conts=[[1,2],[1,2]])
    except Exception as e:
        print(e)
    try:
        result = continuity(test3d_array,conts=[1,2])
    except Exception as e:
        print(e)    
    try:
        result = continuity(test2d_array,conts=[[1,2],[1,2],[1,2]])
    except Exception as e:
        print(e)    


    pass

if __name__ == "__main__":
    main()
