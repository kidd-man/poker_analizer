import errors as err


class Hand(set):
    def __init__(self, cards):
        super().__init__(cards)
        self.hand = cards

    def count(self, x):
        if type(x) is int:
            numbers = [i[0] for i in self.hand]
            return numbers.count(x)
        elif type(x) is str:
            suits = [i[1] for i in self.hand]
            return suits.count(x)

    def filter(self, x):
        result = set()
        cards = list(self.hand)
        if type(x) is int:
            for l in cards:
                if l[0] == x:
                    result.add(l)
        elif type(x) is str:
            for l in cards:
                if l[1] == x:
                    result.add(l)
        return result

    def n_degrees(self):
        result = [0]*13
        for c in self.hand:
            result[c[0]] += 1
        return result

    def s_digrees(self):
        result = {'spade': 0, 'heart': 0, 'diamond': 0, 'club': 0}
        for c in self.hand:
            result[c[1]] += 1
        return result

    def is_straight_flush(self):
        st = Hand(self.hand).is_straight()
        fl = Hand(self.hand).is_flush()
        if st[0] and fl[0]:
            return True, st[1]
        else:
            return False, (-1,)

    def is_4_of_a_kind(self):
        n_degrees = Hand(self.hand).n_degrees()
        n_degrees.reverse()
        quads = n_degrees.count(4)
        if quads > 0:
            result = ()
            for i, x in enumerate(n_degrees):
                if x >= 4:
                    result += (12-i,)
                    n_degrees[i] -= 4
                    break
            for i, x in enumerate(n_degrees):
                if x > 0:
                    result += (12-i,)
                    break
            return True, result
        else:
            return False, (-1,)

    def is_full_house(self):
        n_degrees = Hand(self.hand).n_degrees()
        n_degrees.reverse()

        degree4 = n_degrees.count(4)
        degree3 = n_degrees.count(3)
        degree2 = n_degrees.count(2)

        if (degree3 + degree4) > 0 and (degree2 + degree3 + degree4 - 1) > 0:
            result = ()
            for i, x in enumerate(n_degrees):
                if x >= 3:
                    result += (12-i,)
                    n_degrees[i] -= 3
                    break
            for i, x in enumerate(n_degrees):
                if x >= 2:
                    result += (12-i,)
                    break
            return True, result
        else:
            return False, (-1,)

    def is_flush(self):
        s_degrees = Hand(self.hand).s_digrees()
        sp_d = s_degrees['spade']
        dm_d = s_degrees['diamond']
        ht_d = s_degrees['heart']
        cl_d = s_degrees['club']
        if sp_d >= 5 or dm_d >= 5 or ht_d >= 5 or cl_d >= 5:
            result = ()
            for i, x in enumerate(s_degrees):
                if s_degrees[x] >= 5:
                    hand = Hand(self.hand).filter(x)
                    result += max(hand, key=lambda c: c[0])
                    break
            return True, result
        else:
            return False, (-1)

    def is_straight(self):
        hand = Hand(self.hand).copy()
        pre_card = min(hand, key=lambda x: x[0])
        hand.remove(pre_card)
        while True:
            if len(hand) == 0:
                return True, (pre_card[0],)
            minimum = min(hand, key=lambda x: x[0])
            hand.remove(minimum)
            if pre_card[0] == minimum[0] - 1:
                pre_card = minimum
                continue
            elif len(hand) == 1:
                last = hand.pop()
                if pre_card[0] == '5' and last[0] == 'A':  # A2345
                    return True, (pre_card[0],)
                else:
                    return False, (-1,)
            else:
                return False, (-1,)

    def is_3_of_a_kind(self):
        n_degrees = Hand(self.hand).n_degrees()
        n_degrees.reverse()
        triples = n_degrees.count(3) + n_degrees.count(4)
        if triples > 0:
            result = ()
            for i, x in enumerate(n_degrees):
                if x >= 3:
                    result += (12-i,)
                    n_degrees[i] -= 3
                    break
            for i, x in enumerate(n_degrees):
                if x > 0:
                    result += (12-i,)
                    break
            return True, result
        else:
            return False, (-1,)

    def is_2_pair(self):
        n_degrees = Hand(self.hand).n_degrees()
        n_degrees.reverse()
        pairs = n_degrees.count(2) + n_degrees.count(3) + n_degrees.count(4)
        result = ()
        if pairs >= 2:
            for i, x in enumerate(n_degrees):
                if len(result) < 2 and x > 1:
                    result += (12 - i,)
                    n_degrees[i] -= 2
            for i, x in enumerate(n_degrees):
                if x > 0:
                    result += (12-i,)
                    break
            return True, result
        else:
            return False, (-1,)

    def is_1_pair(self):
        n_degrees = Hand(self.hand).n_degrees()
        n_degrees.reverse()
        pairs = n_degrees.count(2) + n_degrees.count(3) + n_degrees.count(4)
        result = ()
        if pairs > 0:
            for i, x in enumerate(n_degrees):
                if x > 1:
                    result += (12 - i,)
                    n_degrees[i] -= 2
                    break
            for i, x in enumerate(n_degrees):
                if x > 0:
                    for j in range(x):
                        result += (12 - i,)
                        if len(result) >= 4:
                            break
                    if len(result) >= 4:
                        break
            return True, result
        else:
            return False, (-1,)

    def is_high_card(self):
        n_degrees = Hand(self.hand).n_degrees()
        n_degrees.reverse()
        result = ()
        for i, x in enumerate(n_degrees):
            if x > 0:
                for j in range(x):
                    result += (12 - i,)
                    if len(result) >= 5:
                        break
                if len(result) >= 5:
                    break
        return True, result


def eval_hand(hand: Hand):
    return [hand.is_straight_flush(),
            hand.is_4_of_a_kind(),
            hand.is_full_house(),
            hand.is_flush(),
            hand.is_straight(),
            hand.is_3_of_a_kind(),
            hand.is_2_pair(),
            hand.is_1_pair(),
            hand.is_high_card()]


def judge_two_hands(hand1, hand2):
    ev1, ev2 = eval_hand(hand1), eval_hand(hand2)
    for x, y in zip(ev1, ev2):
        if x[0] and (not y[0]):
            return True, False
        elif (not x[0]) and y[0]:
            return False, True
        elif x[0] and y[0]:
            for i, j in zip(x[1], y[1]):
                if i > j:
                    return True, False
                elif i < j:
                    return False, True
            return True, True
    return True, True
