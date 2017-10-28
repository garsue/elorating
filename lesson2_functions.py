# ←これで始まる行はコメント。プログラムと関係なくて、動かすときには無視される

# 参考 イロレーティング
# https://ja.wikipedia.org/wiki/%E3%82%A4%E3%83%AD%E3%83%AC%E3%83%BC%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0

# このプログラムを理解するのに必要な知識
# - functions https://docs.python.jp/3/tutorial/controlflow.html#defining-functions

# CSVファイル操作の関数を使う
import csv


def main():
    # メインの処理
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

            # 戦績が記録されている行(見出し行でない)場合に処理する
            if is_record_row(row_num):
                # プレーヤーふたりの名前を取得
                name_a = row[1]
                name_b = row[8]
                # プレーヤー名を出力して確認
                print('プレーヤーA:', name_a, 'プレーヤーB:', name_b)

                # 各プレーヤーのレート
                rate_a = get_rate(rate_dict, name_a)
                rate_b = get_rate(rate_dict, name_b)
                print('プレーヤーAのレート:', rate_a, 'プレーヤーBのレート:', rate_b)

                # プレーヤーAがプレーヤーBに勝利する確率e_aを計算
                e_a = calculate_win_probability(rate_a, rate_b)
                # プレーヤーBがプレーヤーAに勝利する確率e_bを計算
                e_b = calculate_win_probability(rate_b, rate_a)
                # 勝利する確率を出力して確認
                print('e_a:', e_a, 'e_b:', e_b)

                # プレーヤーAの試合結果を取得
                result_a = row[3]
                # プレーヤーAの試合結果を出力して確認
                print('プレーヤーAの試合結果:', result_a)
                # プレーヤーAが勝ったかどうか
                win_a = result_a == 'WIN'

                # それぞれのレートを補正(プレーヤーAが勝ってない=プレーヤーBが勝った)
                rate_a = calculate_rate(rate_a, win_a, e_a)
                rate_b = calculate_rate(rate_b, not win_a, e_b)
                # レートを出力して確認
                print('プレーヤーAのレート:', rate_a, 'プレーヤーBのレート:', rate_b)

                # rate_dictに持っているレートと勝利数を更新
                rate_dict[name_a] = rate_a
                rate_dict[name_b] = rate_b

    # 最終的な計算結果の表示
    show_result(rate_dict)


def is_record_row(row_num):
     # 列名の行(見出し行)でなければ戦績が記録されている行
    return row_num != 0

def get_rate(rate_dict, name):
    # rate_dictからプレーヤー名nameのプレーヤーのレートを取得する
    # プレーヤーのレート辞書にレートがあればそれを返す
    if name in rate_dict:
        return rate_dict[name]
    # 初期値の1500をレートとして返す
    return 1500


def calculate_win_probability(my_rate, other_rate):
    # 自分と相手のレートから勝利確率を計算する
    return 1 / (1 + 10 ** ((other_rate - my_rate) / 400))


def calculate_rate(rate, win, win_probability):
    # 自分のレート、勝敗、勝利確率から補正されたレートを計算する
    # プレーヤーの勝利数。1試合ごとにレート計算するので0か1のいずれか
    win_count = 0
    # 勝ってたら勝利数1に
    if win:
        win_count = 1
    # K=32
    return rate + 32 * (win_count - win_probability)


def show_result(rate_dict):
    # 最終的な計算結果の表示
    print('=== 最終結果 ===')
    for name in rate_dict:
        print(name, rate_dict[name])

# 処理開始
main()
