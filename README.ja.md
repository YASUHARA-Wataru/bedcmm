# 特許アルゴリズムの公開実装（日本国内特許）

このリポジトリでは、特許（日本）として登録された基底抽出割算最小法(bedcmm)の実装を公開しています。

- 本実装は研究・検証・評価用途での利用を目的としています
- 商用利用・再配布にはライセンスの取得が必要です（下記参照）

bedcmmは、ロバストなパターン抽出、周期性解析、連続性解析、そしてバターン抽出を基づいた通信多重化方法です。

## 特徴
インパルスノイズや外れ値に強い、パターン抽出、周期性解析の手法です。

- 定量的なパターンの抽出
- 定量的な周期性の計算
  - スパイクノイズに強いピッチ検出への応用(https://github.com/YASUHARA-Wataru/bedcmmPitch)
  - 外れ値に強い周期性解析(```example_temperature_priod_ana.py```)
  - 欠損値（NaN）を含むデータへの対応（特許アルゴリズムの拡張的実装）
    - 補間を行わず、そのまま周期性を計算可能
    - 有効データ率（valid_ratio）を同時に出力し、結果の信頼度を評価可能
    - 完全データに対しては自己相関に近い挙動を示すが、欠損を含む場合でも一貫した評価が可能
- 定量的な連続性の計算
- M系列使用時より短く、量子化1bitのみでの通信の多重化。
  ただし、同期(送信のみ)が必要で乱数性は確保されず、SN比は向上しません。
- 相互周期性解析（特許のコアクレームには含まれない実装）
  - 自己相関と相互相関の関係のように、周期性解析をデータ比較に用いる手法

  ※ 同一のデータを入力した場合、自己周期性（auto-periodicity）に相当する結果が得られます。

## Install
```bash
pip install bedcmm
```
## Example
- pattern
```python
import numpy as np
import bedcmm

np.random.seed(0)

# 周期 + ノイズ
base = np.tile([1, 0, 0, 0], 25)
noise = np.random.randint(0, 2, len(base)) * 0.1

x = base + noise

score = bedcmm.pattern.periodicity(x)

print("periodicity score:", score)
```
- communication
```python
import numpy as np
import bedcmm

base1 = [False, False, False, False, False, True, True, True]
base2 = [False, False, False, True, False, False, True, True]
base3 = [False, True, False, False, False, False, True, True]
tx1 = np.tile(base1, 5)
tx2 = np.tile(base2, 5)
tx3 = np.tile(base3, 5)

tx = np.array([tx1,tx2,tx3])

send_signal = bedcmm.communication.multiplexing(tx)
print(send_signal)

demod_signal1 = bedcmm.communication.demodulate(send_signal,base1)
demod_signal2 = bedcmm.communication.demodulate(send_signal,base2)
demod_signal3 = bedcmm.communication.demodulate(send_signal,base3)

print("demod_signal1:", demod_signal1)
print("demod_signal2:", demod_signal2)
print("demod_signal3", demod_signal3)
```

## デモ

`pattern_demo.ipynb`,`communication_demo.ipynb` を実行することで、簡単なサンプル結果を得られます：

簡単な説明が、`doc`内に入っています。

## 高速化について
```python setup.py build_ext --inplace```
cython実装になります(pattern modules)

## 計算速度
計算時間の検証スクリプトは、```speed_test.py```です。

### Cython
```
       mode      N  time_msec
0    random   1000     2.6160
1    random   5000    61.1024
2    random  10000   245.1453
3  periodic   1000     1.2297
4  periodic   5000    28.6166
5  periodic  10000   110.1707
6     spike   1000     1.3126
7     spike   5000    27.9070
8     spike  10000   113.7231
```
### Python only
```
       mode      N   time_msec
0    random   1000    188.5421
1    random   5000   4593.9274
2    random  10000  19079.0753
3  periodic   1000    196.6179
4  periodic   5000   4723.4922
5  periodic  10000  18833.8787
6     spike   1000    206.1020
7     spike   5000   4802.0938
8     spike  10000  19601.9191
```

## 特許情報

このアルゴリズムは、以下の日本国特許に基づいています：

- 特許番号：特許第7537807号
- 発明の名称：パターン抽出及び通信多重化方法
- 登録日：2024年8月13日
- 内容：パターン抽出方法、周期性の計算方法、連続性の計算方法、通信の多重化方法

## 特許範囲と非特許実装について

本リポジトリには、特許に基づく実装と、それとは独立した補助的・拡張的な実装が含まれています。

- 特許対象：
  - 基底抽出割算最小法に基づくパターン抽出および周期性解析のコアアルゴリズム

- 拡張実装：
  - 欠損値（NaN）対応

- 特許対象外の実装：
  - 相互周期性解析（cross_periodicity など）

これらの実装の特許適用範囲は、具体的な利用方法や構成に依存する場合があります。

## 連絡先
fapow.contact[at]gmail.com