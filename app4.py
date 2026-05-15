import random

class EnterpriseGame:
    def __init__(self):
        self.money = 5000
        self.debt = 0           # 借金
        self.staff = {"平社員": 0, "部長": 0, "役員": 0}
        self.market_share = 5
        self.is_listed = False  # 上場しているか
        self.turn = 1

    def calculate_income(self):
        # 基礎収益
        base = (self.staff["平社員"]*50 + self.staff["部長"]*300 + self.staff["役員"]*1500)
        share_bonus = 1 + (self.market_share / 100)
        return int(base * share_bonus)

    def handle_taxes(self, profit):
        """税金システム：利益の30%を徴収"""
        if profit > 0:
            tax = int(profit * 0.3)
            self.money -= tax
            return tax
        return 0

    def run_bank(self):
        """銀行融資：お金を借りるが利息が発生"""
        print(f"\n--- 銀行窓口 (現在の借金: {self.debt}円) ---")
        print("1: 10,000円借りる (利息10%)  2: 借金を全額返済する")
        choice = input("選択: ")
        if choice == "1":
            self.money += 10000
            self.debt += 11000 # 利息込み
            return "10,000円を借りました。返済義務は11,000円です。"
        elif choice == "2":
            if self.money >= self.debt:
                self.money -= self.debt
                self.debt = 0
                return "借金を完済しました！"
            else:
                return "返済資金が足りません。"
        return "戻ります。"

    def run_ipo(self):
        """株式上場：厳しい条件をクリアして大金を得る"""
        if self.is_listed: return "既に上場しています。"
        
        print("\n--- 証券取引所 (IPO審査) ---")
        print("条件: 資産50,000円以上 かつ シェア30%以上")
        if self.money >= 50000 and self.market_share >= 30:
            choice = input("上場しますか？ (y/n): ")
            if choice == "y":
                ipo_fund = 200000
                self.money += ipo_fund
                self.is_listed = True
                return f"祝・上場！ 上場益として {ipo_fund}円 が払い込まれました！"
        else:
            return "条件を満たしていません。"
        return "上場を見送りました。"

    def show_status(self):
        print(f"\n{'='*40}")
        print(f"第 {self.turn} 期 {' [上場企業]' if self.is_listed else ''}")
        print(f"【資産】 {self.money}円  【借金】 {self.debt}円")
        print(f"【シェア】 {self.market_share}%  【人員】 {sum(self.staff.values())}名")
        print(f"{'='*40}")

    def play(self):
        while True:
            self.show_status()
            print("1:人員 2:営業/開発 3:銀行(融資) 4:IPO(上場) 5:次へ q:終了")
            cmd = input("アクションを選択: ")

            if cmd == "q": break
            
            # メインアクション処理
            if cmd == "3": print(self.run_bank())
            elif cmd == "4": print(self.run_ipo())
            # (省略：1と2はこれまでの雇用や営業のコードが入るイメージ)

            # 期末処理
            income = self.calculate_income()
            tax = self.handle_taxes(income)
            self.money += (income - tax)
            
            if income > 0:
                print(f"今期の利益: {income}円 (うち税金: {tax}円) を計上しました。")
            
            self.turn += 1
            if self.money < 0:
                print("【破産】 資金が底をつきました。ゲームオーバー。")
                break

# ゲーム開始
# EnterpriseGame().play() 
