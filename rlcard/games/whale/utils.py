import os
import json
import numpy as np
from collections import OrderedDict

import rlcard

from rlcard.games.whale.card import WhaleCard as Card

# Read required docs
ROOT_PATH = rlcard.__path__[0]

# a map of trait to its index
CARD_MAP = {'water': 0, 'wave': 1, 'double_wave': 2}

# a map of abstract action to its index and a list of abstract action
with open(os.path.join(ROOT_PATH, 'games/whale/jsondata/action_space.json'), 'r') as file:
    ACTION_SPACE = json.load(file, object_pairs_hook=OrderedDict)
    ACTION_LIST = list(ACTION_SPACE.keys())


def init_deck():
    ''' Generate whale deck of 108 cards
    '''
    deck = []

    # init wave cards
    for _ in range(1, 32):
        deck.append(Card('wave'))

    # init double_wave cards
    for _ in range(1, 8):
        deck.append(Card('double_wave'))

    # init water cards
    for _ in range(1, 40):
        deck.append(Card('water'))

    return deck


def cards2list(cards):
    ''' Get the corresponding string representation of cards

    Args:
        cards (list): list of WhaleCards objects

    Returns:
        (string): string representation of cards
    '''
    cards_list = []
    for card in cards:
        cards_list.append(card.get_str())
    return cards_list


def hand2dict(hand):
    ''' Get the corresponding dict representation of hand

    Args:
        hand (list): list of string of hand's card

    Returns:
        (dict): dict of hand
    '''
    hand_dict = {}
    for card in hand:
        if card not in hand_dict:
            hand_dict[card] = 1
        else:
            hand_dict[card] += 1
    return hand_dict


def encode_hand(hand):
    ''' Encode hand and represerve it into plane

    Args:
        hand (list): list of string of hand's card

    Returns:
        (array): 3 numpy array
    '''
    # plane = np.zeros((3, 4, 3), dtype=int)
    plane = np.ones((3), dtype=int)
    hand = hand2dict(hand)
    for card in hand.items():
        # print(f'card{card}')
        card_info = CARD_MAP[card[0]]
        plane[card_info] = 1
    return plane
