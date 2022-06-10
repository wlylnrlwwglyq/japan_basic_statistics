import math
import sys


CSV_FILE = "FEH_00200521_220610143730.csv"


def load_csv(csv_file):
    csv_data = []
    #csvファイルを読み込む
    with open(csv_file,"r",encoding="utf-8") as f:
        csv_text = f.read()
    #csvファイルを1行ずつ解析して値を配列に格納していく
    line_number = 0
    for line in csv_text.split("\n"):
        line_number += 1
        #ヘッダは飛ばす
        if line_number == 1: #ヘッダは飛ばす
            continue
        #数値の区切り文字を削除する
        formatted_line = ""
        col_number = 0
        for data in line.split("\""):
            col_number += 1
            if col_number % 2 == 1:
                formatted_line += data
            else:
                formatted_line += data.replace(",","")
        #データを格納する
        formatted_data = formatted_line.split(",")
        prefecture_code = int(formatted_data[0][:2])
        city_code = formatted_data[0][2:]
        try:
            csv_data.append([prefecture_code,city_code,formatted_data[1],int(formatted_data[2]),int(formatted_data[3]),int(formatted_data[4])])
        except ValueError:
            csv_data.append([prefecture_code,city_code,formatted_data[1],-1,-1,-1])
    #県コード,市町村コード,名称,総数,男,女
    return csv_data


def get_prefecture_data(csv_data):
    prefecture_data = []
    for i in csv_data:
        if i[0] != 0 and i[1] == "000":
            prefecture_data.append([i[2],i[3]])
    return prefecture_data


if __name__ == "__main__":
    #データを取得する
    csv_data = load_csv(CSV_FILE)
    prefecture_data = get_prefecture_data(csv_data)
    if len(prefecture_data) == 0:
        print("データの読み込みに失敗");
        sys.exit(1)

    #データを昇順にソートする
    prefecture_data = sorted(prefecture_data,key=lambda x:x[1])

    #平均値を計算する
    total = 0
    for i in prefecture_data:
        total += i[1]
    average = total/len(prefecture_data)

    #中央値を計算する
    if len(prefecture_data)%2 == 1:
        median = prefecture_data[int(len(prefecture_data)/2)][1]
        median_prefecture = "( "+prefecture_data[int(len(prefecture_data)/2)][0]+" )"
    else: #今後、県の個数が変動する可能性を考慮する
        median = (prefecture_data[int(len(prefecture_data)/2)-1][1]+prefecture_data[int(len(prefecture_data)/2)][1])/2
        median_prefecture = ""

    #最大値を計算する
    max_value = prefecture_data[-1]

    #最小値を計算する
    min_value = prefecture_data[0]

    #分散を計算する
    total = 0
    for i in prefecture_data:
        total += pow(i[1]-average,2)
    variance = total/len(prefecture_data)

    #標準偏差を計算する
    standard_deviation = math.sqrt(variance)

    #結果を表示する
    print("平均値:",average)
    print("中央値:",median,median_prefecture)
    print("最大値:",max_value[1],"(",max_value[0],")")
    print("最小値:",min_value[1],"(",min_value[0],")")
    print("分散:",variance)
    print("標準偏差:",standard_deviation)

