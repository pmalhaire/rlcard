# -*- coding: utf-8 -*-
''' Implement Limit Texas Hold'em Round class
'''

import random

from rlcard.core import Round
from rlcard.games.limitholdem.player import LimitholdemPlayer as Player



class LimitholdemRound(Round):
    ''' Round can call other Classes' functions to keep the game running
    '''

    def __init__(self, raise_amount, allowed_raise_num):
        ''' Currently, it is designed for two players.

        Args:
            button (int): The first play to take actions
            raise_amount (int): the raise amount for each raise
            allowed_raise_num (int): The number of allowed raise num

        The round will be over when the when either  
        '''
        
        self.button = None
        self.raise_amount = raise_amount
        self.allowed_raise_num = allowed_raise_num

        self.num_players = 2

        # Count the number of raise
        self.have_raised = 0

        # Count the number without raise
        # In two player version, if two consecutive call/check is performed,
        # the round is over
        self.not_raise_num = 0

        # Raised amount for each player
        self.raised = [0 for _ in range(self.num_players)]

    def start_new_round (self, button, raised=None):
        ''' Start a new bidding round

        Args:
            rasied (list): Initialize the chips for each player

        Note: For the first round of the game, we need to setup the big/small blind
        '''
        
        self.button = button
        self.have_raised = 0
        self.not_raise_num = 0
        if raised:
            self.raised = raised
        else:
            self.raised = [0 for _ in range(self.num_players)] 

    def proceed_round(self, player, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            player (object): object of DoudizhuPlayer
            action (str): string of legal specific action

        Returns:
            The button that indicates the next player
        '''
        
        if action not in self.get_legal_actions():
            raise Exception('{} is not legal acyion. Legal actions: {}', action, self.get_legal_actions())

        if action == 'call':
            diff = max(self.raised) - self.raised[self.button]
            self.raised[self.button] = max(self.raised)
            player.in_chips += diff
            self.not_raise_num += 1
            

        elif action == 'raise':
            diff = max(self.raised) - self.raised[self.button] + self.raise_amount
            self.raised[self.button] = max(self.raised) + self.raise_amount
            player.in_chips += diff
            self.have_raised += 1
            self.not_raise_num = 1

        elif action == 'fold':
            player.status = 'folded'
            self.player_folded = True

        elif action == 'check':
            self.not_raise_num += 1

        self.button = (self.button + 1) % self.num_players

        return self.button

    def get_legal_actions(self):
        ''' Obtain the leagal action for the curent player

        Returns:
            A list of legal actions
        '''

        full_actions = ['call', 'raise', 'fold', 'check']
        
        # If the the number of raises already reaches the maximum number raises, we can not raise any more
        if self.have_raised >= self.allowed_raise_num:
            full_actions.remove('raise')

        # If the current chips are less than that of the highest one in the round, we can not check
        if self.raised[self.button] < max(self.raised):
            full_actions.remove('check')

        # If the current player has put in the chips that are more than others, we can not call

        if self.raised[self.button] == max(self.raised):
            full_actions.remove('call')

        return full_actions

    def is_over(self):
        ''' Check whether the round is over

        Returns:
            A boolean. True if the current round is over
        '''
        #print(self.not_raise_num)
        #print(self.num_players)

        if self.not_raise_num >= self.num_players:
            return True
        return False
            
if __name__ == '__main__':
    players = [Player(0), Player(1)]
    button = 0
    r = LimitholdemRound(button, 2, 4)
    r.start_new_round(raised=[1, 2])
    print(r.raised, r.have_raised, r.not_raise_num)

    while not r.is_over():
        legal_actions = r.get_legal_actions()
        action = random.choice(legal_actions)
        print(button, action, legal_actions)
        button = r.proceed_round(players[button], action)
        print(r.raised, r.have_raised, r.not_raise_num)