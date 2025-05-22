# -*- coding: utf-8 -*-
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

cpdef np.ndarray[DTYPE_d_t, ndim=1] pattern_1d(np.ndarray[DTYPE_d_t, ndim=1] data,np.ndarray[DTYPE_d_t, ndim=1] base):

    cdef np.ndarray[DTYPE_d_t, ndim=1] tmp_data,tmp_result 
    cdef np.ndarray[DTYPE_d_t, ndim=1] result
    cdef int index

    if len((<object> data).shape) != 1:
        raise Exception('data must 1D array.')

    if len((<object> base).shape) != 1:
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


cpdef np.ndarray[DTYPE_d_t, ndim=2] pattern_2d(np.ndarray[DTYPE_d_t, ndim=2] data,np.ndarray[DTYPE_d_t, ndim=2] base):

    cdef np.ndarray[DTYPE_d_t, ndim=2] tmp_data
    cdef np.ndarray[DTYPE_d_t, ndim=1] tmp_result 
    cdef np.ndarray[DTYPE_d_t, ndim=2] result
    cdef int i_index,j_index

    if len((<object> data).shape) != 2:
        raise Exception('data must 2D array.')

    if len((<object> base).shape) != 2:
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

cpdef np.ndarray[DTYPE_d_t, ndim=3] pattern_3d(np.ndarray[DTYPE_d_t, ndim=3] data,np.ndarray[DTYPE_d_t, ndim=3] base):

    cdef np.ndarray[DTYPE_d_t, ndim=3] tmp_data 
    cdef np.ndarray[DTYPE_d_t, ndim=1] tmp_result 
    cdef np.ndarray[DTYPE_d_t, ndim=3] result
    cdef int i_index,j_index,k_index

    if len((<object> data).shape) != 3:
        raise Exception('data must 3D array.')

    if len((<object> base).shape) != 3:
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


cpdef np.ndarray[DTYPE_d_t, ndim=1] periodicity_1d(np.ndarray[DTYPE_d_t, ndim=1] data):

    cdef int max_preiod
    cdef np.ndarray[DTYPE_d_t, ndim=1] preiod,temp_data
    cdef int a_preiod,index
    
    if np.min(data) < 0:
        raise Exception('data must be positive.')

    max_preiod = int(data.shape[0]/2)
    preiod = np.zeros(max_preiod+1)
    preiod[0] = np.mean(data)

    for a_preiod in range(1,max_preiod+1):
        temp_data = np.zeros(len(data) - a_preiod)
        for index in range(data.shape[0] - a_preiod):
            temp_data[index] = min([data[index],data[index+a_preiod]])
                
        preiod[a_preiod]=np.mean(temp_data)
    
    return preiod


cpdef np.ndarray[DTYPE_d_t, ndim=2] periodicity_2d(np.ndarray[DTYPE_d_t, ndim=2] data):

    cdef int max_preiod1,max_preiod2
    cdef np.ndarray[DTYPE_d_t, ndim=2] preiod ,temp_data
    cdef int preiod1,preiod2
    
    if len((<object> data).shape) != 2:
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
                    temp_data[index1,index2] =min([data[index1,index2],data[index1+preiod1,index2+preiod2]])

                preiod[preiod1,preiod2]=np.mean(temp_data)
        
    return preiod

cpdef np.ndarray[DTYPE_d_t, ndim=3] periodicity_3d(np.ndarray[DTYPE_d_t, ndim=3] data):

    cdef int max_preiod1,max_preiod2,max_preiod3
    cdef np.ndarray[DTYPE_d_t, ndim=3] preiod,temp_data
    cdef int preiod1,preiod2,preiod3
    
    if len((<object> data).shape) != 3:
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
                            temp_data[index1,index2,index3]=min([data[index1,index2,index3],data[index1+preiod1,index2+preiod2,index3+preiod3]])

                preiod[preiod1,preiod2,preiod3]=np.mean(temp_data)
        
    return preiod


cpdef np.ndarray[DTYPE_d_t, ndim=1] continuity_1d(np.ndarray[DTYPE_d_t, ndim=1] data):

    cdef int max_cont1
    cdef np.ndarray[DTYPE_d_t, ndim=1] cont,temp_data
    cdef int cont1

    if len((<object> data).shape) != 1:
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

cpdef np.ndarray[DTYPE_d_t, ndim=2] continuity_2d(np.ndarray[DTYPE_d_t, ndim=2] data):

    cdef int max_cont1,max_cont2
    cdef np.ndarray[DTYPE_d_t, ndim=2] cont,temp_data
    cdef int cont1,cont2

    if len((<object> data).shape) != 2:
        raise Exception('data must 2D array.')

    if np.min(data) < 0:
        raise Exception('data must be positive.')

    max_cont1 = data.shape[0]
    max_cont2 = data.shape[1]

    cont = np.zeros((max_cont1,max_cont2))    
    for cont1 in range(1,max_cont1+1):
        for cont2 in range(1,max_cont2+1):
            temp_data = np.zeros((max_cont1 + 1 - cont1,max_cont2 + 1 - cont2))
            for index1 in range(max_cont1 - cont1):
                for index2 in range(max_cont2 - cont2):
                        temp_data[index1,index2] = min(data[index1:index1+cont1,index2:index2+cont2].flatten())
         
            cont[cont1-1,cont2-1]=np.mean(temp_data)
        
    return cont

cpdef np.ndarray[DTYPE_d_t, ndim=3] continuity_3d(np.ndarray[DTYPE_d_t, ndim=3] data):

    cdef int max_cont1,max_cont2,max_cont3
    cdef np.ndarray[DTYPE_d_t, ndim=3] cont,temp_data
    cdef int cont1,cont2,cont3

    if len((<object> data).shape) != 3:
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
