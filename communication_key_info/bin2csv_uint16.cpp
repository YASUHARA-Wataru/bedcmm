#include <iostream>
#include <fstream>
#include <array>
#include <string>
#include <cstdint>

template <std::size_t Bases_num>
struct BinaryDatas {
    std::array<uint16_t, Bases_num> bases;

    // 1つ前のバイナリ読み込み
    bool loadBinary(std::ifstream &ifs) {
        for (std::size_t r = 0; r < Bases_num; r++) {
            uint16_t seq;
            ifs.read(reinterpret_cast<char*>(&seq), sizeof(seq)); 
            if (!ifs) return false; // 読み込み失敗
            bases[r] = seq;
        }
        return true;
    }

    // テキスト出力
    void saveText(std::ofstream &ofs) const {
        for (std::size_t r = 0; r < Bases_num; r++) {
            ofs << bases[r] << "\n";
        }
        ofs << "----\n";
    }
    // テキスト出力（整数に変換して出力）
    void saveInt(std::ofstream &ofs) const {
        ofs << bases[0];
        for (std::size_t r = 1; r < Bases_num; r++) {
            ofs << "," << bases[r] ;  // 数字に変換して出力
        }
        ofs << "\n";
    }
};

int main() {
    const int baseCount = 6;
    const int length = 12;
    std::string bin_file = "pair" + std::to_string(baseCount) +
                           "_length" + std::to_string(length) + "_from_bin.dat";
    std::string txt_file = "pair" + std::to_string(baseCount) +
                           "_length" + std::to_string(length) + "_from_bin2.csv";

    using bases_data = BinaryDatas<baseCount>;
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
