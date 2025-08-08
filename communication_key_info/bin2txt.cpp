#include <iostream>
#include <fstream>
#include <bitset>
#include <array>
#include <string>

template <std::size_t Bit_length, std::size_t Base_num>
struct BinaryDatas {
    std::array<std::bitset<Bit_length>, Base_num> bases;

    // バイナリ読み込み
    bool loadBinary(std::ifstream &ifs) {
        size_t bytes = (Bit_length + 7) / 8;
        for (std::size_t r = 0; r < Base_num; r++) {
            unsigned long long val = 0;
            ifs.read(reinterpret_cast<char*>(&val), bytes);
            if (!ifs) return false; // 読み込み失敗
            bases[r] = std::bitset<Bit_length>(val);
        }
        return true;
    }

    // テキスト出力
    void saveText(std::ofstream &ofs) const {
        for (std::size_t r = 0; r < Base_num; r++) {
            ofs << bases[r] << "\n";
        }
        ofs << "----\n";
    }
    // テキスト出力（整数に変換して出力）
    void saveInt(std::ofstream &ofs) const {
        ofs << bases[0].to_ullong();
        for (std::size_t r = 1; r < Base_num; r++) {
            ofs << "," << bases[r].to_ullong() ;  // 数字に変換して出力
        }
        ofs << "\n";
    }
};

int main() {
    const int baseCount = 6;
    const int length = 13;
    std::string bin_file = "pair" + std::to_string(baseCount) +
                           "_length" + std::to_string(length) + "_from_bin.dat";
    std::string txt_file = "pair" + std::to_string(baseCount) +
                           "_length" + std::to_string(length) + "_from_bin2txt.txt";

    using bases_data = BinaryDatas<length, baseCount>;
    bases_data bases;

    std::ifstream ifs(bin_file, std::ios::binary);
    if (!ifs) {
        std::cerr << "ファイルが開けません: " << bin_file << "\n";
        return 1;
    }

    std::ofstream ofs(txt_file);
    // ヘッダの出力
    ofs << "base1";
    for(int i = 1 ; i < baseCount ; i++){
        ofs << ",base" << std::to_string(i+1);
    }
    ofs << "\n";

    // ループでペアごとに読む
    while (bases.loadBinary(ifs)) {
        //bases.saveText(ofs);
        bases.saveInt(ofs);
    }

    std::cout << "変換完了: " << txt_file << " に出力しました\n";
    return 0;
}
