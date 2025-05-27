#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
//#include <unistd.h>
#include <stdio.h>
#include <math.h>
#include <vector>
//using namespace std;         //  名前空間指定

class bedcmm{
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

void toBinary(int n,int dig,std::vector<bool>& r)
{
    for (int i = 0;i < dig ;i++){
        if(n % 2 == 0 ){
			r[i] = false;
		}else{
			r[i] = true;
		}
        n /= 2;
    }

    return;
};

int toDecimal(const std::vector<bool>& binary,int dig){
  	int decimal = 0;
  	int base = 1;

	for(int i = 0; i < dig ; ++i){
		decimal = decimal + ( binary[i] % 10 ) * base;
		base = base * 2;
	}

	return decimal;
}

std::vector<std::string> split(std::string& input, char delimiter)
{
    std::istringstream stream(input);
    std::string field;
    std::vector<std::string> result;
    while (getline(stream, field, delimiter)) {
        result.push_back(field);
    }
    return result;
}


int main(void)
{

    int n;
    const int baseCount = 3; // 基底数
	const int limit_num = 7;
    std::cout << "Input length of array: ";
    std::cin >> n;
    //std::cout << "Input baseCount: ";
    //std::cin >> baseCount;    
    std::cout << "Extend base from baseCount=" << (baseCount - 1) << " to baseCount=" << baseCount << " (n=" << n << ")" << std::endl;

	std::string baseCount_input_str = std::to_string(baseCount-1);
    std::string baseCount_output_str = std::to_string(baseCount);
    std::string n_str = std::to_string(n);
    std::string limit_base_str = std::to_string(limit_num);
    std::string input_file_name = "pair"+baseCount_input_str+"_length"+n_str+"_limited"+limit_base_str+".csv";
    std::string output_file_name = "pair"+baseCount_output_str+"_length"+n_str+"_limited"+limit_base_str+".csv";

	bedcmm bedcmm;
	std::ofstream outputfile(output_file_name);
	outputfile << "base1";
	for (int i = 2; i <= baseCount; ++i) {
		outputfile << ",base" << i;
	}
	outputfile << std::endl;
	std::ifstream readingfile;
	readingfile.open(input_file_name, std::ios::in);
	if (!readingfile.is_open()) {
		std::cerr << "does not open file: " << input_file_name << std::endl;
		return 1;
	}
	int max_number = pow(2,n) - 1;

    std::vector<std::vector<bool>> bases(baseCount, std::vector<bool>(n, false));
    std::vector<int> bases_num(baseCount-1, 0);
    std::vector<std::vector<bool>> cor_results1(baseCount, std::vector<bool>(n,false));
    std::vector<std::vector<bool>> cor_results2(baseCount, std::vector<bool>(n,false));
    std::vector<bool> send_sig1(2 * n, false);
    std::vector<std::vector<bool>> send_sig2(baseCount, std::vector<bool>(2 * n, false));

	std::string raeding_line_buffer;
	int line_cnt = 0;
	while(std::getline(readingfile, raeding_line_buffer)){
		line_cnt+=1;
		if (line_cnt ==1){
			continue;
		}
		//std::cout << raeding_line_buffer << std::endl;
		std::vector<std::string> strvec = split(raeding_line_buffer, ',');
		// get bases
		for(int i =0;i < baseCount-1;++i){
			bases_num[i] = std::stoi(strvec[i]);
			toBinary(bases_num[i],n,bases[i]);
		}

		for(int i=bases_num[baseCount-2]+1;i<max_number+1;++i){
			int base3_num = 0;
			base3_num = i;
			toBinary(base3_num,n,bases[baseCount-1]);

			// get corr data
			for (int j = 0; j < 2 * n; ++j) {
				send_sig1[j] = bases[0][j % n] | bases[1][j % n] | bases[2][j % n];
			}
			
			for (int j = 0 ; j < baseCount ; ++j){
				bedcmm.corr_binary(send_sig1,bases[j],cor_results1[j]);
			}

			// 相関結果を確認（位置1以降に重なりがあれば除外）
			bool valid = true;
			for (int j = 1; j < n; ++j) {
				for (int k = 0; k < baseCount; ++k) {
					if (cor_results1[k][j]) {
						valid = false;
						break;
					}
				}
				if (!valid) break;
			}

			if (valid) {
				// 自分以外の合成信号との相関
				for (int j = 0 ; j < baseCount;++j){
					std::fill(send_sig2[j].begin(), send_sig2[j].end(), false);
				}
				for (int j = 0; j < 2 * n; ++j) {
					send_sig2[0][j] = bases[1][j%n] | bases[2][j%n];
					send_sig2[1][j] = bases[0][j%n] | bases[2][j%n];
					send_sig2[2][j] = bases[0][j%n] | bases[1][j%n];
				}

				bool valid2 = true;
				for (int j = 0 ; j < baseCount;++j){
					bedcmm.corr_binary(send_sig2[j],bases[j],cor_results2[j]);
					for (int k = 0; k < n; ++k) {
						if (cor_results2[j][k]) {
							valid2 = false;
							break;
						}
					}
					if (!valid2) break;
				}
				if (valid2) {
					for (int j = 0; j < baseCount; ++j) {
						outputfile << toDecimal(bases[j],n);
						if (j < baseCount - 1) outputfile << ",";
					}
					outputfile << std::endl;
				}
			}
		}

	}

	outputfile.close();	

	bases.clear();
	bases_num.clear();
    cor_results1.clear();
    cor_results2.clear();
    send_sig1.clear();
    send_sig2.clear();
	return 0;
};