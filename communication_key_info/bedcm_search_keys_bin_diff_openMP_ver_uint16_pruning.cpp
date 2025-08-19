#include <stdio.h>
#include <array>
#include <math.h>
#include <chrono>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <array>
#include <cstdint>
#include <vector>
#include <omp.h>

// 固定長バイナリを持つ構造体
template <std::size_t Bases_num>
struct BinaryDatas {
	std::array<uint16_t, Bases_num> bases;
    // baseの値セット
    void set_base(uint16_t num, int i){
        bases[i] = num;
    };

    // baseの値セット
    uint16_t get_base(uint16_t i){
        return bases[i];
    };

    // 調査中の基底以外の論理和をとった場合
    uint16_t pre_logical_or() {
        uint16_t acc = 0;
        for (int num_of_base = 0 ; num_of_base < Bases_num - 1 ; num_of_base++) {
            acc |= bases[num_of_base];   // OR演算を積み重ねる
        }
        return acc;
    }

    // 全ての論理和をとった場合
    uint16_t logical_or(uint16_t pre_data) {
        uint16_t acc = 0;
        acc = pre_data | bases[Bases_num-1];
        return acc;
    }

    // 調査中の基底以外の論理和をとった場合
    uint16_t logical_all_or() {
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
	const int baseCount = 4;
	const int length = 14;
    std::string baseCount_output_str = std::to_string(baseCount);
    std::string baseCount_input_str = std::to_string(baseCount-1);
    std::string n_str = std::to_string(length);
    std::string output_file_name = "pair"+baseCount_output_str+"_length"+n_str+"_from_bin_pruning.dat";
    std::string input_file_name = "pair"+baseCount_input_str+"_length"+ n_str + "_from_bin_pruning.dat";

    std::ifstream ifs(input_file_name, std::ios::binary);
    if (!ifs) {
        std::cerr << "ファイルが開けません: " << input_file_name << "\n";
        return 1;
    }
    ifs.seekg(0, std::ios::end);
    std::streampos filesize = ifs.tellg();
    uint16_t seq=0;
    size_t total = filesize /  sizeof(seq) / (baseCount-1);
    ifs.seekg(0, std::ios::beg);
    std::cout << "入力ファイルの行数: " << total << " 組" << std::endl;

    using bases_data = BinaryDatas<baseCount>;
    bases_data bases;
    //uint16_t last_num,pre_logical_or_data;    
    int max_length = int(pow(2,length));
    // 枝切りパラメータ
    int base_ul,base_ll;
    base_ul = 6;
    base_ll = 4;
    size_t done = 0;
    auto start = std::chrono::steady_clock::now();

    // まず全部読み込んでメモリに持ってしまう
    std::vector<bases_data> all_data;
    while (bases.loadBinary(ifs)) {
        all_data.push_back(bases);
    }

    #pragma omp parallel
    {
        std::ofstream local_ofs; // スレッドごとの一時出力
        std::string fname = "tmp_" + std::to_string(omp_get_thread_num()) + ".bin";
        local_ofs.open(fname, std::ios::binary);

        #pragma omp for schedule(dynamic)
        for (size_t idx = 0; idx < all_data.size(); idx++) {
            auto bases = all_data[idx];  // コピーしてスレッドごとに使う
            uint16_t last_num,pre_logical_or_data;
            int bitcnt_i;
            last_num = bases.get_base(baseCount-2);
            pre_logical_or_data = bases.pre_logical_or();
            for(uint16_t i = last_num+1; i < max_length; i++){
                bitcnt_i = __builtin_popcount(i);
                // 枝切り
                if(bitcnt_i < base_ll || bitcnt_i > base_ul) continue;
                bases.set_base(i,baseCount-1);
                bool flag = true;
                uint16_t cor_data;
                uint16_t cor_result;
                for(int k = 0; k < baseCount ; k++){
                    cor_data = bases.logical_or(pre_logical_or_data);

                    cor_result = bases.cyclic_correlation(cor_data,k,length);
                    if(cor_result == 1u){
                        cor_data = bases.logical_or_excluide_i(length,k);
                        cor_result = bases.cyclic_correlation(cor_data,k,length);
                        if(cor_result == 0){
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
                    bases.saveBinary(local_ofs);
                }
            }
 

            // 進捗更新
            size_t current = ++done;
            if (current % (all_data.size()/100 == 0 ? 1 : all_data.size()/100) == 0) {
                auto now = std::chrono::steady_clock::now();
                double elapsed = std::chrono::duration<double>(now - start).count();
                double progress = 100.0 * current / all_data.size();
                #pragma omp critical
                {
                    std::cout << "\r進捗: " << progress << "% (" 
                            << current << "/" << all_data.size() << ") "
                            << "経過: " << elapsed << " 秒"
                            << std::flush;
                }
            }
        }

        local_ofs.close();
    }

    // 最後にスレッドごとの一時ファイルを結合
    std::ofstream ofs(output_file_name, std::ios::binary);
    for (int t = 0; t < omp_get_max_threads(); t++) {
        std::ifstream tmp("tmp_" + std::to_string(t) + ".bin", std::ios::binary);
        ofs << tmp.rdbuf();
        tmp.close();
        std::remove(("tmp_" + std::to_string(t) + ".bin").c_str());
    }

	return 0;
};