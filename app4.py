import time

def start_game():
    print("--- げぇむ『てんびん』を開始します ---")
    print("ルール: 0〜100の中から数字を選んでください。")
    print("勝者: 全員の平均値に『0.8』を掛けた値に最も近い人。")
    print("脱落: ポイントが -10 になると『秤』から水が溢れます。\n")

    # プレイヤー設定
    num_players = int(input("参加人数を入力してください: "))
    players = {}
    for i in range(num_players):
        name = input(f"プレイヤー{i+1}の名前: ")
        players[name] = 0  # 初期ポイント

    round_count = 1

    while len(players) > 1:
        print(f"\n--- 第 {round_count} 回戦 ---")
        choices = {}

        # 入力フェーズ
        for name in players.keys():
            while True:
                try:
                    val = float(input(f"[{name}] 0〜100の数字を入力: "))
                    if 0 <= val <= 100:
                        choices[name] = val
                        break
                    print("0から100の間で入力してください。")
                except ValueError:
                    print("数字を入力してください。")

        # 計算フェーズ
        average = sum(choices.values()) / len(choices)
        target = average * 0.8
        print(f"\n集計中...")
        time.sleep(1)
        print(f"平均値: {average:.2f}")
        print(f"設定数値 (平均×0.8): {target:.2f}")

        # 勝敗判定
        winner = min(choices, key=lambda x: abs(choices[x] - target))
        print(f"このラウンドの勝者: {winner} (選択値: {choices[winner]})")

        # 敗者にペナルティ (-1ポイント)
        for name in list(players.keys()):
            if name != winner:
                players[name] -= 1
                print(f"{name}: {players[name]}ポイント")

        # 脱落チェック
        eliminated = [name for name, score in players.items() if score <= -10]
        for name in eliminated:
            print(f"!!! {name} が脱落しました (溶解) !!!")
            del players[name]

        if len(players) == 1:
            final_winner = list(players.keys())[0]
            print(f"\n🎉 げぇむくりあ：勝者は {final_winner} です！")
            break

        round_count += 1

if __name__ == "__main__":
    start_game()
