#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>

class Correlator {
public:
    void corr_binary(const std::vector<bool>& data, const std::vector<bool>& base, std::vector<bool>& result) {
        int data_size = data.size();
        int base_size = base.size();
        for (int i = 0; i <= data_size - base_size; ++i) {
            bool flag = true;
            for (int j = 0; j < base_size; ++j) {
                if (base[j] && !data[i + j]) {
                    flag = false;
                    break;
                }
            }
            result[i] = flag;
        }
    }
};

bool increment(std::vector<bool>& bits) {
    for (int i = bits.size() - 1; i >= 0; --i) {
        if (!bits[i]) {
            bits[i] = true;
            return true;
        }
        bits[i] = false;
    }
    return false;
}

int toDecimal(const std::vector<bool>& binary) {
    int result = 0;
    for (bool bit : binary) {
        result = (result << 1) | bit;
    }
    return result;
}

std::vector<bool> fromDecimal(int num, int n) {
    std::vector<bool> bits(n, false);
    for (int i = n - 1; i >= 0; --i) {
        bits[i] = num & 1;
        num >>= 1;
    }
    return bits;
}

void extendAndCheck(
    const std::vector<std::vector<bool>>& base_prefix,
    int baseCount,
    int n,
    Correlator& corr,
    std::ofstream& outputfile
) {
    static bool header_written = false;

    if (!header_written) {
        // ヘッダー出力
        outputfile << "base1";
        for (int i = 2; i <= baseCount; ++i) {
            outputfile << ",base" << i;
        }
        outputfile << "\n";
        header_written = true;
    }

    std::vector<std::vector<bool>> bases = base_prefix;
    bases.emplace_back(n, false); // 新しい base 用

    std::vector<std::vector<bool>> cor_results(baseCount, std::vector<bool>(n+1));
    std::vector<std::vector<bool>> cor_results2(baseCount, std::vector<bool>(n+1));
    std::vector<bool> send_sig(2 * n, false);
    std::vector<std::vector<bool>> send_sig2(baseCount, std::vector<bool>(2 * n, false));

    std::vector<bool>& new_base = bases.back();
    std::vector<bool>& prev_base = bases[bases.size() - 2];
    bool calc_flag = false; 
    new_base = prev_base;

    while (increment(new_base)) {
        // keyの制限
        //if( toDecimal(bases[0]) == 7 | toDecimal(bases[0]) == 15 | toDecimal(bases[0]) == 31){
        if( toDecimal(bases[0]) == 7){
            calc_flag = true;
        }
        if (!calc_flag){continue;} 
        // 合成信号
        std::fill(send_sig.begin(), send_sig.end(), false);
        for (int i = 0; i < 2 * n; ++i) {
            for (int j = 0; j < baseCount; ++j) {
                send_sig[i] = send_sig[i] | bases[j][i % n];
            }
        }

        // 自己相関（合成）
        bool valid = true;
        for (int j = 0; j < baseCount; ++j) {
            corr.corr_binary(send_sig, bases[j], cor_results[j]);
            for (int i = 1; i < n; ++i) {
                if (cor_results[j][i]) {
                    valid = false;
                    break;
                }
            }
            if (!valid) break;
        }

        if (!valid) continue;

        // 自分以外の合成信号との相関
        for (int j = 0; j < baseCount; ++j) {
            std::fill(send_sig2[j].begin(), send_sig2[j].end(), false);
            for (int i = 0; i < 2 * n; ++i) {
                for (int j2 = 0; j2 < baseCount; ++j2) {
                    if (j != j2) {
                        send_sig2[j][i] = send_sig2[j][i] | bases[j2][i % n];
                    }
                }
            }
        }

        bool valid2 = true;
        for (int j = 0; j < baseCount; ++j) {
            corr.corr_binary(send_sig2[j], bases[j], cor_results2[j]);
            for (int i = 0; i < n; ++i) {
                if (cor_results2[j][i]) {
                    valid2 = false;
                    break;
                }
            }
            if (!valid2) break;
        }

        if (valid2) {
            for (int j = 0; j < baseCount; ++j) {
                outputfile << toDecimal(bases[j]);
                if (j < baseCount - 1) outputfile << ",";
            }
            outputfile << "\n";
        }
    }
}

int main() {
    //int baseCount = 3;
    //int n = 8;
    int n;
    int baseCount; // 基底数
    std::cout << "Input length of array: ";
    std::cin >> n;    
    std::cout << "Input baseCount: ";
    std::cin >> baseCount;    

    std::cout << "Extend base from baseCount=" << (baseCount - 1) << " to baseCount=" << baseCount << " (n=" << n << ")" << std::endl;

    std::string baseCount_input_str = std::to_string(baseCount-1);
    std::string baseCount_output_str = std::to_string(baseCount);
    std::string n_str = std::to_string(n);
    std::string input_file_name = "pair"+baseCount_input_str+"_length"+n_str+"_limted.csv";
    std::string output_file_name = "pair"+baseCount_output_str+"_length"+n_str+"_limted.csv";

    std::ifstream infile(input_file_name);
    std::ofstream outfile(output_file_name);

    Correlator corr;

    std::string line;

    // ヘッダー行を読み飛ばす
    std::getline(infile, line); // ← これが大事

    while (std::getline(infile, line)) {
        if (line.empty()) continue;  // ← 空行スキップ
        std::stringstream ss(line);
        std::string cell;
        std::vector<std::vector<bool>> base_prefix;
        while (std::getline(ss, cell, ',')) {
            if (cell.empty()) continue; // ← ここで空文字は無視
            int num = std::stoi(cell);
            base_prefix.push_back(fromDecimal(num, n));
        }

        if (base_prefix.size() != baseCount - 1) continue;

        extendAndCheck(base_prefix, baseCount, n, corr, outfile);
    }

    std::cout << "Finished extending bases. Output: "<< output_file_name << std::endl;
    return 0;
}
