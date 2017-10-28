# ←これで始まる行はコメント。プログラムと関係なくて、動かすときには無視される

# 参考 イロレーティング
# https://ja.wikipedia.org/wiki/%E3%82%A4%E3%83%AD%E3%83%AC%E3%83%BC%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0

# このプログラムを理解するのに必要な知識
# - for文 https://docs.python.jp/3/tutorial/controlflow.html#for-statements
# - if文 https://docs.python.jp/3/tutorial/controlflow.html#if-statements
# - 辞書型 (dictionary) https://docs.python.jp/3/tutorial/datastructures.html#dictionaries
# ファイルの読み込みとかもあるが、一旦スルーしといていい。

# CSVファイル操作の関数を使う
import csv

# 選手ごとのレートを持っておく辞書
rate_dict = {}

# 戦績CSVファイルを読み込む
with open('records.csv') as csv_file:
    # CSVファイルから各行を読み取るreaderを作成
    reader = csv.reader(csv_file)
    # readerから各行を行番号と一緒に読み出す
    for row_num, row in enumerate(reader):
        # 処理中の行番号と行の内容を出力して確認
        print('行番号:', row_num)
        print('行の中身:', row)

        # 先頭の行は列名なので無視
        if row_num == 0:
            # なにもしない
            pass
        else:
            # プレーヤーふたりの名前を取得
            name_a = row[1]
            name_b = row[8]
            # プレーヤー名を出力して確認
            print('プレーヤーA:', name_a, 'プレーヤーB:', name_b)

            # 各プレーヤーのレート。一旦初期値の1500にする
            rate_a = 1500
            rate_b = 1500
            # 各プレーヤーのレート辞書にレートがあればそれを使う
            if name_a in rate_dict:
                rate_a = rate_dict[name_a]
            if name_b in rate_dict:
                rate_b = rate_dict[name_b]
            # レートを出力して確認
            print('プレーヤーAのレート:', rate_a, 'プレーヤーBのレート:', rate_b)

            # プレーヤーAがプレーヤーBに勝利する確率e_aを計算
            e_a = 1 / (1 + 10 ** ((rate_b - rate_a) / 400))
            # プレーヤーBがプレーヤーAに勝利する確率e_bを計算
            e_b = 1 / (1 + 10 ** ((rate_a - rate_b) / 400))
            # 勝利する確率を出力して確認
            print('e_a:', e_a, 'e_b:', e_b)

            # プレーヤーAの試合結果を取得
            result_a = row[3]
            # プレーヤーAの試合結果を出力して確認
            print('プレーヤーAの試合結果:', result_a)

            # 各プレーヤーの勝利数。1試合ごとにレート計算するので0か1のいずれか
            s_a = 0
            s_b = 0
            # プレーヤーAが勝っていたらs_aに1を、負けていたらs_bに1を代入する
            if result_a == 'WIN':
                s_a = 1
            else:
                s_b = 1
            # 勝利数を出力して確認
            print('プレーヤーAの勝利数:', s_a, 'プレーヤーBの勝利数:', s_b)

            # それぞれのレートを補正(K=32)
            rate_a = rate_a + 32 * (s_a - e_a)
            rate_b = rate_b + 32 * (s_b - e_b)
            # レートを出力して確認
            print('プレーヤーAのレート:', rate_a, 'プレーヤーBのレート:', rate_b)

            # rate_dictに持っているレートと勝利数を更新
            rate_dict[name_a] = rate_a
            rate_dict[name_b] = rate_b

# 最終的な計算結果の表示
print('=== 最終結果 ===')
for name in rate_dict:
    print(name, rate_dict[name])
