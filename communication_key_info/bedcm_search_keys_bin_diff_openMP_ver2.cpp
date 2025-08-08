#include <iostream>
#include <fstream>
#include <stdio.h>
#include <bitset>
#include <array>
#include <math.h>
#include <chrono>
#include <vector>
#include <omp.h>

// 固定長バイナリを持つ構造体
template <std::size_t Bit_length,std::size_t Base_num>
struct BinaryDatas {
	std::array<std::bitset<Bit_length>, Base_num> bases;
	std::bitset<2*Bit_length> cor_data;
	std::bitset<Bit_length> presave_all_cor_data;
	std::bitset<Bit_length> cor_result;

    // intを指定行に設定
    void set_base(std::size_t row, int value) {
        if (row < Base_num) {
            bases[row] = std::bitset<Bit_length>(value);
        }
    };

    // 指定行の値を取得
    int get_base(std::size_t row) {
        if (row < Base_num) {
            return bases[row].to_ullong();
        } else{
            return 0;
        }
    };
    // 指定行のインクリメント
    void increment_row(std::size_t row) {
        if (row < Base_num) {
            unsigned long long val = bases[row].to_ullong();
            val++;  
            bases[row] = std::bitset<Bit_length>(val);
        }
    };
    //*
    // すべてのor和の取得の前準備
    void pre_all_or_data(){
        std::bitset<Bit_length> result;
        for (std::size_t r = 0; r < Base_num-1; r++) {
            result |= bases[r];
        }
        presave_all_cor_data = result;
	};
    // すべてのor和の取得(前準備後)
    void all_or_data(){
        std::bitset<Bit_length> result;
        result = presave_all_cor_data | bases[Base_num-1];
		for(std::size_t c = 0; c < 2*Bit_length; c++){
			cor_data[c] = result[c%Bit_length];
		}
	};
    // 指定のbase以外のor和の取得
    void exclude_i_or_data(std::size_t ex_base_num) {
        std::bitset<Bit_length> result;
        for (std::size_t r = 0; r < Base_num; r++) {
			if(r != ex_base_num){
	            result |= bases[r];
			}
        }
		for(std::size_t c = 0; c < 2*Bit_length; c++){
			cor_data[c] = result[c%Bit_length];
		}
	};
	// bedcm相関を取得する
    void corr_binary_base_i_prev(std::size_t cor_base_num) {
        for (int i = 0; i < Bit_length; ++i) {
            bool flag = true;
            for (int j = 0; j < Bit_length; ++j) {
                if (bases[cor_base_num][j] && !cor_data[i + j]) {
                    flag = false;
                    break;
                }
            }
            cor_result[i] = flag;
        }
	};

    // bedcm相関を取得するver2
    void corr_binary_base_i(std::size_t cor_base_num) {
        uint64_t base = bases[cor_base_num].to_ullong();
        for (int shift = 0; shift < Bit_length; shift++) {
            uint64_t mask = (cor_data.to_ullong() >> shift);
            cor_result[shift] = ((base & ~mask) == 0);
        }
	};

    bool corresult_all_zero() {
        for (std::size_t r = 0; r < Bit_length; r++) {
            if (cor_result[r]) {
                return false; // 1が見つかったら false
            }
        }
        return true; // 全部0なら true
    };
    bool corresult_first_one_other_zero() {
		if (cor_result[0]){
			for (std::size_t r = 1; r < Bit_length; r++) {
				if (cor_result[r]) {
					return false; // 1が見つかったら false
				}
 	      }
 		}else{
			return false;
		}
        return true; // 全部0なら true
    };	

    // バイナリ保存（appendモード）
    void saveBinary(std::ofstream &ofs) const {
        size_t bytes = (Bit_length + 7) / 8;
        for (std::size_t r = 0; r < Base_num; r++) {
            unsigned long long val = bases[r].to_ullong();
            ofs.write(reinterpret_cast<const char*>(&val), bytes);
        }
    };

    // 1つ前のバイナリ読み込み
    bool loadBinary(std::ifstream &ifs) {
        size_t bytes = (Bit_length + 7) / 8;
        for (std::size_t r = 0; r < Base_num-1; r++) {
            unsigned long long val = 0;
            ifs.read(reinterpret_cast<char*>(&val), bytes);
            if (!ifs) return false; // 読み込み失敗
            bases[r] = std::bitset<Bit_length>(val);
        }
        return true;
    }

};


int main(void)
{
	const int baseCount = 4;
	const int length = 13;
    std::string baseCount_output_str = std::to_string(baseCount);
    std::string baseCount_input_str = std::to_string(baseCount-1);
    std::string n_str = std::to_string(length);
    std::string output_file_name = "pair"+baseCount_output_str+"_length"+n_str+"_from_bin.dat";
    std::string input_file_name = "pair"+baseCount_input_str+"_length"+ n_str + "_from_bin.dat";

    std::ifstream ifs(input_file_name, std::ios::binary);
    if (!ifs) {
        std::cerr << "ファイルが開けません: " << input_file_name << "\n";
        return 1;
    }
    ifs.seekg(0, std::ios::end);
    std::streampos filesize = ifs.tellg();
    size_t bytes_per_row = ((length + 7)/8) * (baseCount-1);
    size_t total = filesize / bytes_per_row;
    ifs.seekg(0, std::ios::beg);
    std::cout << "入力ファイルの行数: " << total << " 組" << std::endl;

    //std::ofstream ofs(output_file_name, std::ios::binary);

    using bases_data = BinaryDatas<length,baseCount>;
    bases_data bases;
    int last_num;
    int max_length = int(pow(2,length));
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
            int last_num = bases.get_base(baseCount-2);
            bases.pre_all_or_data();

            for(int i = last_num+1; i < max_length; i++){
                bases.set_base(baseCount-1, i);
                bool flag = true;
                for(int k = 0; k < baseCount; k++){
                    bases.all_or_data();
                    bases.corr_binary_base_i(k);
                    if(bases.corresult_first_one_other_zero()){
                        bases.exclude_i_or_data(k);
                        bases.corr_binary_base_i(k);
                        if(!bases.corresult_all_zero()){
                            flag = false;
                            break;
                        }
                    } else {
                        flag = false;
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