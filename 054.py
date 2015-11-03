#!/usr/bin/python

import os, sys


from itertools import groupby
from operator import itemgetter

# game constants
ROUNDS = 1000
HANDS_FILE = '054.txt'
PLAYER_ONE = PLAYER_TWO = 0
HAND_SIZE = 5

# scores
HighCard = 1
OnePair = 2
TwoPairs = 3
ThreeKind = 4
Straight = 5
Flush = 6
FullHouse = 7
FourKind = 8
StraightFlush = 9
RoyalFlush = 10

mapping = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
}
for i in range(2, 10):
    mapping.update({str(i): i})


def read_rounds():
    lines = []
    with open(HANDS_FILE, 'r') as f:
        for line in f:
            lines.append(line.rstrip('\n').split(' '))
            print 'Read %s' % line.rstrip('\n')
    return lines


class Hand:

    def __init__(self, player, hand, *args, **kwargs):
        # reverse-ordered so we always give priority to the best score
        self.player = player
        self.functions = [
            '_royal_flush', '_straight_flush', '_four_kind', '_full_house', '_flush',
            '_straight', '_three_kind', '_two_pairs', '_one_pair', '_high_card']
        self.hand = self._convert_hand(hand)
        self.message = '%s: %s'
        self.score_name = 'HighCard'

    def _convert_hand(self, hand):
        # converts the hand into a readable list of tuples
        converted = []
        for card in hand:
            value, seed = list(card)
            converted.append((mapping[value], seed))
        return converted

    def score(self):
        points, obj = self._high_card()  # everyone has one

        for func in self.functions:
            p, o = getattr(self, func)()
            if p:
                points, obj = (p, o)
                break

        return points, obj

    @property
    def result(self):
        return self.message % (self.player, self.score_name)

    def _get_hand_by_(self, i=0, reverse=True):
        return sorted(self.hand, key=lambda x: x[i], reverse=reverse)

    def get_hand_by(self, param='value'):
        if param == 'value':
            return self._get_hand_by_(0)
        if param == 'seed':
            return self._get_hand_by_(1)
        return self.hand

    def _high_card(self):
        card = self.get_hand_by('value')[0]
        obj = {'card_values': [card[0]]}
        score = HighCard
        return score, obj

    def _one_pair(self):
        obj, score = (None, 0)
        hand = self.get_hand_by('value')
        groups = groupby(hand, itemgetter(0))
        pairs = [[item for item in data] for (_, data) in groups]
        for p in pairs:
            if len(p) == 2:
                obj = {'card_values': list(set([v[0] for v in p]))}
                score = OnePair
                self.score_name = 'OnePair'
                break
        return score, obj

    def _two_pairs(self):
        obj, score = (None, 0)
        hand = self.get_hand_by('value')
        groups = groupby(hand, itemgetter(0))
        pairs = [[item for item in data] for (_, data) in groups]
        found, temp = (0, [])
        for p in pairs:
            if len(p) == 2:
                found += 1
                temp.append(p[0][0])
                if found == 2:
                    obj = {}
                    obj.update({'card_values': temp})
                    score = TwoPairs
                    self.score_name = 'TwoPairs'
                    break
        return score, obj

    def _three_kind(self):
        obj, score = (None, 0)
        return score, obj

    def _straight(self):
        obj, score = (None, 0)
        groups = []
        for k, g in groupby(enumerate([c[0] for c in self.hand]), lambda (i, x): i-x):
            groups.append(map(itemgetter(1), g))
        if len(groups) == 1:
            if len(groups[0]) == HAND_SIZE:
                obj = {}
                obj.update({'card_values': groups[0]})
                score = Straight
                self.score_name = 'Straight'
        return score, obj

    def _flush(self):
        score = 0
        seed = [c[1] for c in self.hand]
        if len(set(seed)) == 1:
            score = Flush
            self.score_name = 'Flush'
        return score, None

    def _full_house(self):
        obj, score = (None, 0)
        return score, obj

    def _four_kind(self):
        obj, score = (None, 0)
        groups = []
        for k, g in groupby(enumerate([c[0] for c in self.hand]), lambda (i, x): i-x):
            groups.append(map(itemgetter(1), g))
        for group in groups:
            if len(group) == 4:
                obj = {}
                obj.update({'card_values': group})
                score = FourKind
                self.score_name = 'Four of a Kind'
        return score, obj

    def _straight_flush(self):
        obj, score = (None, 0)
        seed = [c[1] for c in self.hand]
        groups = []
        if len(set(seed)) == 1:
            for k, g in groupby(enumerate([c[0] for c in self.hand]), lambda (i, x): i-x):
                groups.append(map(itemgetter(1), g))
            if len(groups) == 1:
                if len(groups[0]) == HAND_SIZE:
                    obj = {}
                    obj.update({'card_values': groups[0]})
                    score = StraightFlush
                    self.score_name = 'StraightFlush'

        return score, obj

    def _royal_flush(self):
        score = 0
        values = [c[0] for c in self.hand]
        seed = [c[1] for c in self.hand]
        if len(set(seed)) == 1 and sorted(values) == sorted([10, 11, 12, 13, 14]):
            score = RoyalFlush
            self.score_name = 'RoyalFlush'
        return score, None


class Game:

    def __init__(self, *args, **kwargs):
        self.HAND = 0
        self.ROUNDS = read_rounds()

    def _load_hand(self):
        return self.ROUNDS[self.HAND]

    def _split_hands(self, hand):
        p1, p2 = (hand[:HAND_SIZE], hand[HAND_SIZE:])
        print 'P1: %s, P2: %s' % (','.join(p1), ','.join(p2))
        return p1, p2

    def _next_hand(self):
        self.HAND += 1

    def _compare_hands(self, h1, h2):
        s1 = s2 = 0

        p1, o1 = h1.score()
        p2, o2 = h2.score()

        if p1 == p2:
            hand_range = HAND_SIZE
            # compare high cards
            cards1 = cards2 = None
            if o1 and o2:
                cards1 = o1.get('card_values', None)
                cards2 = o2.get('card_values', None)

            if cards1 and cards2:
                hand_range = len(cards1)
                high1 = sorted(cards1, reverse=True)
                high2 = sorted(cards2, reverse=True)
            else:
                high1 = [c[0] for c in h1.get_hand_by('value')]
                high2 = [c[0] for c in h2.get_hand_by('value')]

            for i in range(hand_range):
                if not high1[i] == high2[i]:
                    s1, s2 = (1, 0) if high1[i] > high2[i] else (0, 1)
                    break
        else:
            # check scores
            s1, s2 = (1, 0) if p1 > p2 else (0, 1)

        return s1, s2

    def run(self):
        global PLAYER_ONE
        global PLAYER_TWO
        while self.HAND < ROUNDS:
            print 'Dealing hand %d' % self.HAND

            hand = self._load_hand()
            p1, p2 = self._split_hands(hand)

            h1 = Hand('P1', p1)
            h2 = Hand('P2', p2)
            s1, s2 = self._compare_hands(h1, h2)

            PLAYER_ONE += s1
            PLAYER_TWO += s2

            print '%s, %s' % (h1.result, h2.result)
            print 'P1 %d (%d), P2 %d (%d)' % (PLAYER_ONE, s1, PLAYER_TWO, s2)
            print ''

            self._next_hand()
        return PLAYER_ONE


def solve():
    print '''
        Problem 54

        Poker Hands
        https://projecteuler.net/problem=54
    '''

    g = Game()
    res = g.run()

    return res


def main():
	res = solve()
	print "Solution: %s " % (str(res))

if __name__=="__main__":
	main()
