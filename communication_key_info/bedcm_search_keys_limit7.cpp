#include <iostream>
#include <fstream>
#include <stdio.h>
#include <math.h>
#include <vector>

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


int main(void)
{
    int n;
    const int baseCount = 2; // 基底数
	const int limit_num = 7;
    std::cout << "Input length of array: ";
    std::cin >> n;
    //std::cout << "Input baseCount: ";
    //std::cin >> baseCount;    

	std::string baseCount_input_str = std::to_string(baseCount-1);
    std::string baseCount_output_str = std::to_string(baseCount);
    std::string n_str = std::to_string(n);
    std::string limit_base_str = std::to_string(limit_num);
    std::string output_file_name = "pair"+baseCount_output_str+"_length"+n_str+"_limited"+limit_base_str+".csv";

	int max_number = pow(2,n);
	bedcmm bedcmm;
	std::ofstream outputfile(output_file_name);
    outputfile<<"base1,base2"<< std::endl;
	std::vector<int> base_numbers;

	for(int i=1; i < max_number;++i){
		// reject no pattern
		bool no_pattern_flag = false;
		for(int j=0; j < n ;++j){
			if (i == pow(2,j)){
				no_pattern_flag = true;
			}
		}
		if (!no_pattern_flag){
			base_numbers.push_back(i);
		}
	}

	int numbers_num = base_numbers.size();
	
	int output_cnt = 0;

    std::vector<std::vector<bool>> bases(baseCount, std::vector<bool>(n, false));
    std::vector<std::vector<bool>> cor_results1(baseCount, std::vector<bool>(n,false));
    std::vector<std::vector<bool>> cor_results2(baseCount, std::vector<bool>(n,false));
    std::vector<bool> send_sig1(2 * n, false);
    std::vector<std::vector<bool>> send_sig2(baseCount, std::vector<bool>(2 * n, false));

	std::cout << numbers_num << std::endl;
	for(int i=limit_num+1;i<numbers_num;++i){
		// get bases
		int base1_num = 0;
		base1_num = limit_num;
		bool base1[n]={};
		toBinary(base1_num,n,bases[0]);
		int base2_num = 0;
		base2_num = base_numbers[i];
		bool base2[n]={};
		toBinary(base2_num,n,bases[1]);


		// get corr data
        for (int j = 0; j < 2 * n; ++j) {
            send_sig1[j] = bases[0][j % n] | bases[1][j % n];
        }
		
		for (int j = 0 ; j < baseCount ; ++j){
			bedcmm.corr_binary(send_sig1,bases[j],cor_results1[j]);
		}

        // 相関結果を確認（位置1以降に重なりがあれば除外）
        bool valid = true;
        for (int i = 1; i < n; ++i) {
            for (int j = 0; j < baseCount; ++j) {
                if (cor_results1[j][i]) {
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
				send_sig2[0][j] = bases[1][j%n];
				send_sig2[1][j] = bases[0][j%n];
			}

			bool valid2 = true;
			for (int j = 0 ; j < baseCount;++j){
				bedcmm.corr_binary(send_sig2[j],bases[j],cor_results2[j]);
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
					outputfile << toDecimal(bases[j],n);
					if (j < baseCount - 1) outputfile << ",";
				}
				outputfile << std::endl;
			}
		}
	}
	std::cout << output_cnt << std::endl;
	base_numbers.clear();
    outputfile.close();	

    bases.clear();
    cor_results1.clear();
    cor_results2.clear();
    send_sig1.clear();
    send_sig2.clear();

	return 0;
};