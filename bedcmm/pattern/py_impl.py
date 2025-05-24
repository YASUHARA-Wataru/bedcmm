# -*- coding: utf-8 -*-
"""
bedcmm pattern analysis method class(Python)

Author: YASUHARA Wataru
Copyright (c) 2025, Feel a Piece of the World
"""
import numpy as np

def pattern_1d(data,base):
    
    data = np.array(data)
    base = np.array(base)
    
    if len(data.shape) != 1:
        raise Exception('data must 1D array.')

    if len(base.shape) != 1:
        raise Exception('base must 1D array.')

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

def pattern_2d(data,base):
    
    data = np.array(data)
    base = np.array(base)
    
    if len(data.shape) != 2:
        raise Exception('data must 2D array.')

    if len(base.shape) != 2:
        raise Exception('base must 2D array.')


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

def pattern_3d(data,base):

    data = np.array(data)
    base = np.array(base)

    if len(data.shape) != 3:
        raise Exception('data must 3D array.')

    if len(base.shape) != 3:
        raise Exception('base must 3D array.')

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

def periodicity_1d(data):
    
    data = np.array(data)

    if len(data.shape) != 1:
        raise Exception('data must 1D array.')

    if np.min(data) < 0:
        raise Exception('data must be positive.')

    max_preiod = int(data.shape[0]/2)
    preiod = np.zeros(max_preiod+1)
    preiod[0] = np.mean(data)

    for a_preiod in range(1,max_preiod+1):
        temp_data = np.zeros(data.shape[0] - a_preiod)
        for index in range(data.shape[0] - a_preiod):
            temp_data[index] = min([data[index],data[index+a_preiod]])
                
        preiod[a_preiod]=np.mean((temp_data))
    
    return preiod


def periodicity_2d(data):
    
    data = np.array(data)

    if len(data.shape) != 2:
        raise Exception('data must 2D array.')

    if np.min(data) < 0:
        raise Exception('data must be positive.')

    max_preiod1 = int(data.shape[0]/2)
    max_preiod2 = int(data.shape[1]/2)
    preiod = np.zeros((max_preiod1+1,max_preiod2+1))

    for preiod1 in range(max_preiod1+1):
        for preiod2 in range(max_preiod2+1):
            if preiod1 == 0 and preiod2 == 0:
                preiod[0,0] = np.mean(data)
                continue
            temp_data = np.zeros((data.shape[0] - preiod1,data.shape[1] - preiod2))
            for index1 in range(data.shape[0] - preiod1):
                for index2 in range(data.shape[1] - preiod2):
                    temp_data[index1,index2]=min(data[index1,index2],data[index1+preiod1,index2+preiod2])

                preiod[preiod1,preiod2]=np.mean(temp_data)
        
    return preiod


def periodicity_3d(data):
    
    data = np.array(data)

    if len(data.shape) != 3:
        raise Exception('data must 3D array.')

    if np.min(data) < 0:
        raise Exception('data must be positive.')

    max_preiod1 = int(data.shape[0]/2)
    max_preiod2 = int(data.shape[1]/2)
    max_preiod3 = int(data.shape[2]/2)
    preiod = np.zeros((max_preiod1+1,max_preiod2+1,max_preiod3+1))

    for preiod1 in range(max_preiod1+1):
        for preiod2 in range(max_preiod2+1):
            for preiod3 in range(max_preiod3+1):
                if (preiod1 == 0) and (preiod2 == 0) and (preiod3 == 0):
                    preiod[0,0,0] = np.mean(data)
                    continue

                temp_data = np.zeros((data.shape[0] - preiod1,data.shape[1] - preiod2,data.shape[2] - preiod3))
                for index1 in range(data.shape[0] - preiod1):
                    for index2 in range(data.shape[1] - preiod2):
                        for index3 in range(data.shape[2] - preiod3):
                            temp_data[index1,index2,index3]=min(data[index1,index2,index3],data[index1+preiod1,index2+preiod2,index3+preiod3])

                preiod[preiod1,preiod2,preiod3]=np.mean(temp_data)
        
    return preiod


def continuity_1d(data):
    
    data = np.array(data)

    if len(data.shape) != 1:
        raise Exception('data must 1D array.')

    if np.min(data) < 0:
        raise Exception('data must be positive.')

    max_cont1 = data.shape[0]
    cont = np.zeros(max_cont1)
    for cont1 in range(1,max_cont1+1):
        temp_data = np.zeros(max_cont1 + 1 - cont1)
        for index1 in range(max_cont1 + 1 - cont1):
            temp_data[index1] = min(data[index1:index1+cont1].flatten())

        cont[cont1-1]=np.mean(temp_data)
        
    return cont


def continuity_2d(data):
    
    data = np.array(data)

    if len(data.shape) != 2:
        raise Exception('data must 2D array.')

    if np.min(data) < 0:
        raise Exception('data must be positive.')

    max_cont1 = data.shape[0]
    max_cont2 = data.shape[1]

    cont = np.zeros((max_cont1,max_cont2))    
    for cont1 in range(1,max_cont1+1):
        for cont2 in range(1,max_cont2+1):
            temp_data = np.zeros((max_cont1 + 1 - cont1,max_cont2 + 1 - cont2))
            for index1 in range(max_cont1 + 1 - cont1):
                for index2 in range(max_cont2 + 1 - cont2):
                        temp_data[index1,index2] = min(data[index1:index1+cont1,index2:index2+cont2].flatten())
            
            cont[cont1-1,cont2-1]=np.mean(temp_data)
        
    return cont

def continuity_3d(data):
    
    data = np.array(data)

    if len(data.shape) != 3:
        raise Exception('data must 3D array.')

    if np.min(data) < 0:
        raise Exception('data must be positive.')

    max_cont1 = data.shape[0]
    max_cont2 = data.shape[1]
    max_cont3 = data.shape[2]

    cont = np.zeros((max_cont1,max_cont2,max_cont3))    
    for cont1 in range(1,max_cont1+1):
        for cont2 in range(1,max_cont2+1):
            for cont3 in range(1,max_cont3+1):
                temp_data = np.zeros((max_cont1 + 1 - cont1,max_cont2 + 1 - cont2,max_cont3 + 1 - cont3))
                for index1 in range(max_cont1 + 1 - cont1):
                    for index2 in range(max_cont2 + 1 - cont2):
                        for index3 in range(max_cont3 + 1 - cont3):
                            temp_data[index1,index2,index3]=min(data[index1:index1+cont1,index2:index2+cont2,index3:index3+cont3].flatten())
                
                cont[cont1-1,cont2-1,cont3-1]=np.mean(temp_data)
        
    return cont


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
    result = pattern_1d(test1d_array,pattern_base_1d)
    print(result)
    result = pattern_2d(test2d_array,pattern_base_2d)
    print(result)
    result = pattern_3d(test3d_array,pattern_base_3d)
    print(result)
    result = pattern_1d(test1d_n_array,pattern_base_1d)
    print(result)
    result = pattern_2d(test2d_n_array,pattern_base_2d)
    print(result)
    result = pattern_3d(test3d_n_array,pattern_base_3d)
    print(result)
    print('periodicity')
    result = periodicity_1d(test1d_array)
    print(result)
    result = periodicity_2d(test2d_array)
    print(result)
    result = periodicity_3d(test3d_array)
    print(result)
    print('continuity')
    result = continuity_1d(test1d_array)
    print(result)
    result = continuity_2d(test2d_array)
    print(result)
    result = continuity_3d(test3d_array)
    print(result)

    try:
        result = pattern_1d(test2d_n_array,pattern_base_1d)
    except Exception as e:
        print(e)
    try:
        result = pattern_1d(test1d_n_array,pattern_base_2d)
    except Exception as e:
        print(e)
    try:
        result = pattern_2d(test1d_n_array,pattern_base_2d)
    except Exception as e:
        print(e)
    try:
        result = pattern_2d(test2d_n_array,pattern_base_1d)
    except Exception as e:
        print(e)
    try:
        result = pattern_3d(test1d_n_array,pattern_base_3d)
    except Exception as e:
        print(e)
    try:
        result = pattern_3d(test3d_n_array,pattern_base_1d)
    except Exception as e:
        print(e)


    try:
        result = periodicity_1d(test1d_n_array)
    except Exception as e:
        print(e)
    try:
        result = periodicity_1d(test2d_n_array)
    except Exception as e:
        print(e)
    try:
        result = periodicity_2d(test2d_n_array)
    except Exception as e:
        print(e)
    try:
        result = periodicity_2d(test1d_n_array)
    except Exception as e:
        print(e)
    try:
        result = periodicity_3d(test3d_n_array)
    except Exception as e:
        print(e)    
    try:
        result = periodicity_3d(test1d_n_array)
    except Exception as e:
        print(e)    

    try:
        result = continuity_1d(test1d_n_array)
    except Exception as e:
        print(e)
    try:
        result = continuity_1d(test2d_n_array)
    except Exception as e:
        print(e)

    try:
        result = continuity_2d(test2d_n_array)
    except Exception as e:
        print(e)
    try:
        result = continuity_2d(test1d_n_array)
    except Exception as e:
        print(e)

    try:
        result = continuity_3d(test3d_n_array)
    except Exception as e:
        print(e)
    try:
        result = continuity_3d(test1d_n_array)
    except Exception as e:
        print(e)
    
    pass

if __name__ == "__main__":
    main()
