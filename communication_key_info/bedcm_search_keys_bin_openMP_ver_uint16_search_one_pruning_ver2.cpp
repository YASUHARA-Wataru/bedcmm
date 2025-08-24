#include <iostream>
#include <vector>
#include <cstdint>
#include <fstream>
#include <omp.h>
#include <bitset>

// 固定長バイナリを持つ構造体
struct BinaryDatas {
    std::vector<uint16_t> bases;

    BinaryDatas(int baseCount) {
        bases.resize(baseCount,0);
    }
    
    void set_base(uint16_t num, int i){
        bases[i] = num;
    };

    // i番目を除いた論理和
    uint16_t logical_or_excluide_i(int Bit_length,int i) const {
        uint16_t acc = 0;
        for (int num_of_base = 0 ; num_of_base < (int)bases.size(); num_of_base++) {
            if(num_of_base != i){
                acc |= bases[num_of_base];
            }
        }
        return acc;
    }

    // 全ての論理和
    uint16_t logical_all_or() const {
        uint16_t acc = 0;
        for (int num_of_base = 0 ; num_of_base < (int)bases.size(); num_of_base++) {
            acc |= bases[num_of_base];
        }
        return acc;
    }

    // 相関判定
    uint16_t cyclic_correlation(uint16_t cor_data,int i, int Bit_length) const {
        uint16_t mask = (1u << Bit_length) - 1;
        uint16_t result = 0;
        uint16_t base = bases[i];

        for (int shift = 0; shift < Bit_length; shift++) {
            uint16_t shifted = ((cor_data << shift) | (cor_data >> (Bit_length - shift))) & mask;
            if ((base & ~shifted) == 0) {
                result |= (1u << shift);
            }
        }
        return result;
    }

    // テキスト形式で保存
    void saveText(std::ofstream &ofs, int length) const {
        //ofs << "代表解 (baseCount=" << bases.size() << ", length=" << length << ")\n";
        //for (int r = 0; r < (int)bases.size(); r++) {
        //    ofs << "base[" << r << "] = "
        //        << bases[r] << " (bin: " << std::bitset<16>(bases[r]) << ")\n";
        //}
        ofs << "base1";
        for(int r = 1; r < (int)bases.size();r++){
            ofs << "," << "base" << r+1;
        }
        ofs << "\n";
        ofs << bases[0];
        for (int r = 1; r < (int)bases.size(); r++) {
            ofs <<","<< bases[r];
        }
    }
};

// 再帰的に組合せ探索
bool dfs(int idx, int baseCount, int length , int base_ll , int base_ul , BinaryDatas &bases, bool &saved, std::ofstream &ofs) {
    if ((idx > 0) && (idx <= baseCount)) {
        // 判定
        bool flag = true;
        for(int k = 0; k < idx ; k++){
            uint16_t cor_data = bases.logical_all_or();
            uint16_t cor_result = bases.cyclic_correlation(cor_data,k,length);
            if(cor_result == 1u){
                cor_data = bases.logical_or_excluide_i(length,k);
                cor_result = bases.cyclic_correlation(cor_data,k,length);
                if(cor_result == 0) flag = true;
                else flag = false;
            } else flag = false;
            if(!flag) break;
        }

        if(flag && !saved && (idx == baseCount)) {
            #pragma omp critical
            {
                if (!saved) {
                    bases.saveText(ofs, length);
                    saved = true;
                    std::cout << "\nsave one pair";
                }
            }
        }

        if(idx == baseCount) return flag;
    }

    uint32_t max_val = (1u << length);
    for (uint32_t v = (idx==0 ? 1 : bases.bases[idx-1]+1); v < max_val; v++) {
        if (saved) continue; // すでに保存済みならスキップ
        int bitcnt_v = __builtin_popcount(v);
        // 枝切り
        if(bitcnt_v < base_ll || bitcnt_v > base_ul) continue;
        bases.set_base(v, idx);
        if (dfs(idx+1, baseCount, length, base_ll, base_ul , bases, saved, ofs)) {
            return true; // 見つけたら枝刈り
        }
    }
    return false;
}

int main(int argc, char* argv[])
{
    if (argc < 5) {
        std::cerr << "Usage: " << argv[0] << " <length> <baseCount> <basell> <baseul>\n";
        return 1;
    }
    int length = std::stoi(argv[1]);
    int baseCount = std::stoi(argv[2]);
    int base_ll = std::stoi(argv[3]);
    int base_ul = std::stoi(argv[4]);

    std::ofstream ofs("pair"+std::to_string(baseCount)+"_length"+std::to_string(length)+"_p"+std::to_string(base_ll)+"_"+std::to_string(base_ul)+"_one_solution.csv");
    bool saved = false;

    uint64_t total = (1ULL << length) - 1;
    uint64_t done = 0;

    // 外側ループを並列化
    #pragma omp parallel for schedule(dynamic)
    for (uint32_t v = 1; v < (1u << length); v++) {
        if (saved) continue; // すでに保存済みならスキップ

        // --- 進捗更新 ---
        //*
        #pragma omp atomic
        done++;

        if (done % (total/10000 == 0 ? 1 : total/10000) == 0) {
            double progress = 100.0 * done / total;
            #pragma omp critical
            {
                std::cout << "\rprogress: " << progress << "% (" 
                        << done << "/" << total << ")" 
                        << std::flush;
            }
        }
        //*/
        int bitcnt_v = __builtin_popcount(v);
        // 枝切り
        if(bitcnt_v < base_ll || bitcnt_v > base_ul) continue;

        BinaryDatas bases(baseCount);
        bases.set_base(v, 0);
        dfs(1, baseCount, length,base_ll,base_ul, bases, saved, ofs);
    }

    ofs.close();

    if (saved) {
        std::cout << "\nbaseCount=" << baseCount << " exist\n";
    } else {
        std::cout << "\nbaseCount=" << baseCount << " do not exist\n";
    }

    return 0;
}
