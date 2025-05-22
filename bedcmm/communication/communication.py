# -*- coding: utf-8 -*-
"""
bedcmm communication method class

Author: YASUHARA Wataru
Copyright (c) 2025, Feel a Piece of the World
"""

import numpy as np

# modulate function
def modulate(binary_data,main_key):
    """
    Parameters
    ----------
    binary_data : 1D-array
        1D-array (bool) send Data
    main_key : 1D-array
        1D-array (bool) key

    Returns
    -------
    mod_data : list
        modulated data
    """
    data_length = len(binary_data)
    key_length = len(main_key)
    mod_data = np.zeros(data_length*key_length,dtype=bool)
    for i,bit in enumerate(binary_data):
        if bit > 0:
            mod_data[i*key_length:(i+1)*key_length] = main_key
        elif bit == 0:
            mod_data[i*key_length:(i+1)*key_length] = 0
    
    return mod_data

# multiplexing
def multiplexing(mod_data_array):
    """
    Parameters
    ----------
    mod_data_array : 2D-array
        2D array (bool) send Data
        1D length is number of data
        2D length is data length

    Returns
    -------
    mod_list : list
        multiplexing modulated data
    """

    multiplexing_data = np.zeros(mod_data_array.shape[1],dtype=bool)
    temp_list = np.sum(mod_data_array,axis=0)
    # get or sum
    multiplexing_data[temp_list>0] = True
    return multiplexing_data

# bedcm for binary data
def _bedcm_binary(binary_data,key):
    """
    Parameters
    ----------
    binary_data : 1D-array
        1D-array (bool) recived Data
    key : 1D-array
        1D-array (bool) key


    Returns
    -------
    cor_data : list
        after bedcm data
    """
    cor_data = np.zeros_like(binary_data)
    data_len = len(binary_data)
    key_len = len(key)
    for i in range(data_len+1-key_len):
        temp_data = binary_data[i:i+key_len]
        cor_data[i] = np.all(temp_data[key])
    return cor_data

# demodulate function
def demodulate(binary_data,key):
    """
    Parameters
    ----------
    binary_data : 1D-array
        1D-array (bool) recived Data
    key : 1D-array
        1D-array (bool) key


    Returns
    -------
    cor_data : list
        demod data
    """
    cor_data = _bedcm_binary(binary_data,key)

    return cor_data

def demodulate_logical_operations(binary_data,key):
    """
    Parameters
    ----------
    binary_data : 1D-array
        1D-array (bool) recived data(key length) 
    key : 1D-array
        1D-array (bool) key


    Returns
    -------
    demod_data : list
        demod data
    """
    if len(binary_data) != len(key):
        raise Exception('length of binary data and key is must be same in this function.')

    temp_data = []
    for bit_data,bit_key in zip(binary_data,key):
        if bit_key:
            temp_data.append(bit_data and True)
        else:
            temp_data.append(bit_data or True)

    demod_data = np.all(temp_data)

    return demod_data

def main():
    send_data1 = np.array([1,0,0,1,1,1,1],dtype=bool)
    send_data2 = np.array([0,1,0,1,1,0,1],dtype=bool)
    send_data3 = np.array([1,0,1,1,1,0,1],dtype=bool)
    print(f'send data1:{send_data1}')
    print(f'send data2:{send_data2}')
    print(f'send data3:{send_data3}')
    key1 = np.array([0,0,0,0,0,1,1,1],dtype=bool)
    key2 = np.array([0,0,0,1,0,0,1,1],dtype=bool)
    key3 = np.array([0,1,0,0,0,0,1,1],dtype=bool)
    key1_mod_data = modulate(send_data1,key1)
    key2_mod_data = modulate(send_data2,key2)
    key3_mod_data = modulate(send_data3,key3)
    all_mod_data = np.array([key1_mod_data,key2_mod_data,key3_mod_data],dtype=bool)
    send_signal = multiplexing(all_mod_data)

    key1_demod_signal = demodulate(send_signal,key1)
    key2_demod_signal = demodulate(send_signal,key2)
    key3_demod_signal = demodulate(send_signal,key3)
    filt = np.ones(len(key1))
    filtered_data1 = np.convolve(key1_demod_signal,filt,mode='same')
    demod_data1 = np.array(filtered_data1[::len(key1)],dtype=bool)
    filtered_data2 = np.convolve(key2_demod_signal,filt,mode='same')
    demod_data2 = np.array(filtered_data2[::len(key1)],dtype=bool)
    filtered_data3 = np.convolve(key3_demod_signal,filt,mode='same')
    demod_data3 = np.array(filtered_data3[::len(key1)],dtype=bool)

    print(f'demod data1:{demod_data1}')
    print(f'demod data2:{demod_data2}')
    print(f'demod data3:{demod_data3}')

    l_o_esult1 = []
    l_o_esult2 = []
    l_o_esult3 = []

    for i in range(len(send_signal)-len(key1)+1):
        calc_data = send_signal[i:i+len(key1)]
        l_o_esult1.append(demodulate_logical_operations(calc_data,key1))
        l_o_esult2.append(demodulate_logical_operations(calc_data,key2))
        l_o_esult3.append(demodulate_logical_operations(calc_data,key3))

    filt = np.ones(len(key1))
    filtered_data1 = np.convolve(l_o_esult1,filt,mode='same')
    l_o_esult1 = np.array(filtered_data1[::len(key1)],dtype=bool)
    filtered_data2 = np.convolve(l_o_esult2,filt,mode='same')
    l_o_esult2 = np.array(filtered_data2[::len(key1)],dtype=bool)
    filtered_data3 = np.convolve(l_o_esult3,filt,mode='same')
    l_o_esult3 = np.array(filtered_data3[::len(key1)],dtype=bool)

    print(f'lo demod data1:{l_o_esult1}')
    print(f'lo demod data2:{l_o_esult2}')
    print(f'lo demod data3:{l_o_esult3}')
    pass

if __name__ == "__main__":
    main()
