#include <iostream>
#include <vector>
#include <fstream>

class Correlator {
public:
    void corr_binary(const std::vector<bool>& data, const std::vector<bool>& base, std::vector<bool>& result) {
        int data_size = data.size();
        int base_size = base.size();
        for (int i = 0; i <= data_size + 1 - base_size; ++i) {
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

// インクリメント（2進数加算）
bool increment(std::vector<bool>& bits) {
    for (int i = bits.size() - 1; i >= 0; --i) {
        if (!bits[i]) {
            bits[i] = true;
            return true;
        }
        bits[i] = false;
    }
    return false; // overflow
}

// ビット列を整数に変換
int toDecimal(const std::vector<bool>& binary) {
    int result = 0;
    for (bool bit : binary) {
        result = (result << 1) | bit;
    }
    return result;
}

void printBits(const std::vector<bool>& bits) {
    for (bool b : bits) std::cout << b;
}

void enumerate(
    int level,
    int baseCount,
    int n,
    std::vector<std::vector<bool>>& bases,
    std::vector<bool>& send_sig,
    std::vector<std::vector<bool>>& send_sig2,
    std::vector<std::vector<bool>>& cor_results,
    std::vector<std::vector<bool>>& cor_results2,
    Correlator& corr,
    std::vector<std::vector<int>>& base_decimals,
    std::ofstream& outputfile
) {
    if (level == baseCount) {
        // send_sig の作成（OR 合成）
        std::fill(send_sig.begin(), send_sig.end(), false);
        for (int i = 0; i < 2*n; ++i) {
            for (int j = 0; j < baseCount; ++j) {
                send_sig[i] = send_sig[i] | bases[j][i%n];
            }
        }

        // 自己相関計算
        for (int j = 0; j < baseCount; ++j) {
            corr.corr_binary(send_sig, bases[j], cor_results[j]);
        }
        // 相関結果を確認（位置1以降に重なりがあれば除外）
        bool valid = true;
        for (int i = 1; i < n; ++i) {
            for (int j = 0; j < baseCount; ++j) {
                if (cor_results[j][i]) {
                    valid = false;
                    break;
                }
            }
            if (!valid) break;
        }

        if (valid) {

            for (int j = 0; j < baseCount; ++j) {
                std::fill(send_sig2[j].begin(), send_sig2[j].end(), false);  // 初期化
                for (int i = 0; i < 2*n; ++i) {
                    for (int j2 = 0; j2 < baseCount ;++j2){
                        if (j != j2){
                            send_sig2[j][i] = send_sig2[j][i] | bases[j2][i%n];
                        }
                    }
                }
            }
            
            // 自己相関計算
            for (int j = 0; j < baseCount; ++j) {
                corr.corr_binary(send_sig2[j], bases[j], cor_results2[j]);
            }

            // 相関結果を確認（1が一つでもあれば除外）
            bool valid2 = true;
            for (int i = 0; i < n; ++i) {
                for (int j = 0; j < baseCount; ++j) {
                    if (cor_results2[j][i]) {
                        valid2 = false;
                        break;
                    }
                }
                if (!valid2) break;
            }

            if(valid2){
                // 結果出力
                for (int j = 0; j < baseCount; ++j) {
                    int val = toDecimal(bases[j]);
                    base_decimals[j].push_back(val);
                    outputfile << val;
                    if (j < baseCount - 1) outputfile << ",";
                }
                outputfile << "\n";
            }
        }

        return;
    }

    // 次のベース配列を前のより大きいところから始める
    std::vector<bool>& prev = bases[level - 1];
    std::vector<bool>& current = bases[level];
    current = prev;
    // base[0]を7に制限して回す
    while (increment(current)) {
        bool calc_flag = false;
        //if( toDecimal(bases[0]) == 7 | toDecimal(bases[0]) == 15 | toDecimal(bases[0]) == 31){
        if( toDecimal(bases[0]) == 7){
                calc_flag = true;
            }
        if (!calc_flag){continue;} 
        
        enumerate(level + 1, baseCount, n, bases, send_sig,send_sig2, cor_results,cor_results2, corr, base_decimals, outputfile);
    }
}

int main() {
    //int baseCount = 2; // 基底数
    //int n = 9;         // ビット長
    int n;
    int baseCount; // 基底数
    std::cout << "Input length of array: ";
    std::cin >> n;    
    std::cout << "Input baseCount: ";
    std::cin >> baseCount;    
    
    std::cout << "length of array: " << n << ", num of base: " << baseCount << std::endl;
    // std::format(フォーマット文字列, 値...)
    std::string baseCount_str = std::to_string(baseCount);
    std::string n_str = std::to_string(n);
    std::string output_file_name = "pair"+baseCount_str+"_length"+n_str+"_limted.csv";

    std::ofstream outputfile(output_file_name);
    Correlator corr;
    std::vector<std::vector<bool>> bases(baseCount, std::vector<bool>(n, false));
    std::vector<std::vector<bool>> cor_results(baseCount, std::vector<bool>(n+1));
    std::vector<std::vector<bool>> cor_results2(baseCount, std::vector<bool>(n+1));
    std::vector<bool> send_sig(2 * n, false);
    std::vector<std::vector<bool>> send_sig2(baseCount,std::vector<bool>(2 * n, false));
    std::vector<std::vector<int>> base_decimals(baseCount);


    outputfile << "base1";
    for (int i = 2; i <= baseCount; ++i) outputfile << ",base" << i;
    outputfile << "\n";

    // A をインクリメントしてルートとして使う
    while (increment(bases[0])) {
        enumerate(1, baseCount, n, bases, send_sig,send_sig2, cor_results,cor_results2, corr, base_decimals, outputfile);
    }

    outputfile.close();
    std::cout << "end output: " << output_file_name << std::endl;
    return 0;
}
