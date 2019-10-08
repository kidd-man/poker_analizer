import sys
import random as rand
import errors as err
from functools import reduce
import poker as pk


# トランプ
class Deck:
    numbers = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8',
               7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A'}
    __suits = {'spade', 'heart', 'diamond', 'club'}

    def __init__(self):
        self.cards = [(i, j) for i in self.numbers for j in self.__suits]
        rand.shuffle(self.cards)

    def show_deck(self):
        return self.cards

    def shuffle_deck(self):
        rand.shuffle(self.cards)

    def islt(self, n, m):
        return self.numbers[n] < self.numbers[m]

    @staticmethod
    def count_n(cards: set, n: str):
        numbers = [i[0] for i in cards]
        return numbers.count(n)

    def open(self, n: int):
        e_m_about_deck = "Deck is empty."
        e_m_about_atr = "Invalid argument '{0}' as n. "
        try:
            if len(self.cards) == 0:
                raise(err.DeckError(e_m_about_deck))
            elif n < 1:
                raise(err.DeckError(e_m_about_atr.format(n) + "n must be greater than 0. "))
            elif n > len(self.cards):
                raise(err.DeckError(e_m_about_atr.format(n)
                                    + "n must be less than the size of deck {0}".format(len(self.cards))))
            else:
                opened = self.cards[:n]
                self.cards = self.cards[n:]
                return opened
        except err.DeckError as e:
            print('Deck Error: {0}'.format(e.message))

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips

    def get_chips(self, n):
        self.chips += n
        return

    def lose_chips(self, n):
        self.chips -= n
        return


class Poker:
    def __init__(self, n, chips):
        self.p_num = n
        self.players = [Player('player{0}'.format(i), chips) for i in range(self.p_num)]
        self.chips = [chips for _ in range(self.p_num)]
        self.hands = [set() for _ in range(self.p_num)]
        self.survivers = [True for _ in range(self.p_num)]
        self.bets = [None for _ in range(self.p_num)]  # None: no action, -1: fold
        self.sb = 25
        self.bb = 50
        self.dealer = self.p_num-1
        self.c_bet = 0
        self.pod = 0
        self.deck = object()
        self.nowplayer = (self.dealer + 1) % self.p_num

    def game(self):
        self.dealing()
        self.show_players_status()

        def is_call(x): return x == self.c_bet

        def is_fold(x): return x == -1

        def op_c_or_f(x): return not(is_call(x)) and not(is_fold(x))

        # ベット額が揃うまでループ(全員が即foldするケースをカバーしていない)
        while reduce(lambda x, y: x or y, map(op_c_or_f, self.bets)):
            print("bet is not satisfied?")
            print(list(map(op_c_or_f, self.bets)))
            self.input_action()
            self.show_betting_status()
        print("everyone betted.")

    # processings
    def dealing(self):
        self.deck = Deck()  # デッキの作成
        for i in range(2*self.p_num):
            self.hands[i % self.p_num].add(self.deck.open(1)[0])  # ハンドのディーリング

    def show_players_status(self):
        chips = ""
        hands = ""
        for p, c, h in zip(self.players, self.chips, self.hands):
            chips += " {0}({1})".format(p.name, c)
            hlist = list(h)
            hands += " {0}({1}, {2})".format(p.name, hlist[0], hlist[1])

        print("=== players status ===")
        print("chips:{0}".format(chips))
        print("dealer: {0}".format(self.players[self.dealer].name))
        print("hands:{0}".format(hands))
        print("==============")

    def show_betting_status(self):
        print("=== betting status ===")
        print("pod: {0}".format(self.pod))
        print("current bet: {0}".format(self.c_bet))
        print("==============")

    # actions
    def input_action(self):
        print("input action for {0}.".format(self.players[self.nowplayer].name))
        if self.c_bet == 0:
            action_list = input("< check / bet x / fold >: ").split()
        else:
            action_list = input("< call / raise x / fold >").split()
        print(">>>")

        if action_list[0] == "check":
            self.bets[self.nowplayer] = 0                      # プレイヤー毎のベット額の更新
        elif action_list[0] == "call":
            self.bets[self.nowplayer] = int(action_list[1])    # プレイヤー毎のベット額の更新
            self.chips[self.nowplayer] -= int(action_list[1])  # プレイヤーのチップ数の更新
            self.pod += int(action_list[1])                    # podの更新(未完全)
        elif action_list[0] == "bet":
            self.c_bet = action_list[1]                        # 場のベット額の更新
            self.bets[self.nowplayer] = int(action_list[1])    # プレイヤー毎のベット額の更新
            self.chips[self.nowplayer] -= int(action_list[1])  # プレイヤーのチップ数の更新
            self.pod += int(action_list[1])                    # podの更新(未完全)
        elif action_list[0] == "raise":
            self.c_bet = action_list[1]                        # 場のベット額の更新
            self.bets[self.nowplayer] = int(action_list[1])    # プレイヤー毎のベット額の更新
            self.chips[self.nowplayer] -= int(action_list[1])  # プレイヤーのチップ数の更新
        elif action_list[0] == "fold":
            self.bets[self.nowplayer] = -1                     # プレイヤー毎のベット額の更新

        self.nowplayer = (self.nowplayer + 1) % self.p_num  # 手番プレイヤーの更新

    # def get_seat(self):


def main(argv):
    n = int(argv[1])  # 人数
    c = int(argv[2])  # チップ数

    p = Poker(n, c)

    p.game()


if __name__ == "__main__":
    main(sys.argv)
