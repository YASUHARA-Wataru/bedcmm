#include <iostream>
#include <fstream>
#include <stdio.h>
#include <array>
#include <math.h>
#include <cstdint>
#include <bitset>

// 固定長バイナリを持つ構造体
template <std::size_t Bases_num>
struct BinaryDatas {
	std::array<uint16_t, Bases_num> bases;
    void set_base(uint16_t num, int i){
        bases[i] = num;
    };

    // 全ての論理和をとった場合
    uint16_t logical_or(int Bit_length) {
        uint16_t acc = 0;
        for (int num_of_base = 0 ; num_of_base < Bases_num ; num_of_base++) {
            acc |= bases[num_of_base];   // OR演算を積み重ねる
        }
        return acc;
    }
    // i番目の基底以外の論理和
    uint16_t logical_or_excluide_i(int Bit_length,int i) {
        uint16_t acc = 0;
        for (int num_of_base = 0 ; num_of_base < Bases_num ; num_of_base++) {
            if(num_of_base != i){
                acc |= bases[num_of_base];   // OR演算を積み重ねる
            }
        }
        return acc;
    }
    // base: 既存系列のうち i番目
    // cor_data: 論理和した系列
    // return の意味：
    //  - 0                = 全滅
    //  - (1u << (Bit_length-1)) = MSBだけが1
    //  - その他            = 判定ベクトル
    uint16_t cyclic_correlation(uint16_t cor_data,int i, int Bit_length) {
        uint16_t mask = (1u << Bit_length) - 1;
        uint16_t result = 0;
        uint16_t base = bases[i];

        for (int shift = 0; shift < Bit_length; shift++) {
            uint16_t shifted = ((cor_data << shift) | (cor_data >> (Bit_length - shift))) & mask;
            //std::cout << "shift=" << shift << " shifted=" << std::bitset<16>(shifted)
            //  << " base=" << std::bitset<16>(base)
            // << " res=" << ((base & ~shifted) == 0) << "\n";
            // 衝突なければ、その shift ビットを立てる
            if ((base & ~shifted) == 0) {
                result |= (1u << shift);
            }
        }
        return result;
    }

    // バイナリ保存（appendモード）
    void saveBinary(std::ofstream &ofs) const {
        for (std::size_t r = 0; r < Bases_num; r++) {
            uint16_t seq;
            seq = bases[r];
            ofs.write(reinterpret_cast<char*>(&seq), sizeof(seq));
        }
    };

    // 1つ前のバイナリ読み込み
    bool loadBinary(std::ifstream &ifs) {
        for (std::size_t r = 0; r < Bases_num-1; r++) {
            uint16_t seq;
            ifs.read(reinterpret_cast<char*>(&seq), sizeof(seq)); 
            if (!ifs) return false; // 読み込み失敗
            bases[r] = seq;
        }
        return true;
    }

};

    

int main(void)
{
    //std::cout << 'test1' << std::endl;
	const int baseCount = 2; // baseCountは、2で固定
	const int length = 13;
    std::string baseCount_output_str = std::to_string(baseCount);
    std::string n_str = std::to_string(length);
    std::string output_file_name = "pair"+baseCount_output_str+"_length"+n_str+"_from_bin.dat";

    std::ofstream ofs(output_file_name, std::ios::binary);

    using bases_data = BinaryDatas<baseCount>;
    bases_data bases;
    int max_length = int(pow(2,length));
    for(uint16_t i = 1; i < max_length; i++){
        bases.set_base(i,0);
        for(uint16_t j = i+1 ; j < max_length;j++){
            bases.set_base(j,1);
            bool flag = true;
            uint16_t cor_data;
            uint16_t cor_result;
            for(int k = 0; k < baseCount ; k++){
                cor_data = bases.logical_or(length);
                cor_result = bases.cyclic_correlation(cor_data,k,length);
                
                //if(cor_result == (1u << (length - 1))){
                if(cor_result == 1u){
                    //std::cout << "all_success" << std::endl;
                    cor_data = bases.logical_or_excluide_i(length,k);
                    //std::cout << k << ":" << i << ":" << j <<":" << cor_data << std::endl;
                    cor_result = bases.cyclic_correlation(cor_data,k,length);
                    //std::cout << cor_result << std::endl;
                    //std::cout << (1u << (length - 1)) << std::endl;
                    if(cor_result == 0){
                        //std::cout << "ex_i_success" << std::endl;
                        flag = true;
                    }else{
                        flag = false;
                    }

                }else{
                    flag = false;
                }
                if(!flag){
                    break;
                }
            }
            
            if(flag){
                bases.saveBinary(ofs);
                //std::cout << "保存: " << i << "," << j << std::endl; // デバッグ出力
            }
        }
    }

	return 0;
};