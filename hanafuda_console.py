from hanafuda_card import Card, deck
from hanafuda_yaku import check_all_yakus
import random

class Koikoi:
    PLAYER_1 = 0
    PLAYER_2 = 1

    def __init__(self):
        self.player_hands = [[], []]
        self.player_point_piles = [[], []]
        self.field = []
        self.deck = deck.copy()
        random.shuffle(self.deck)
        self.current_player = self.PLAYER_1
        self.current_opponent = self.PLAYER_2
        # append player hands and field
        self.player_hands[0] = self.deck[:8]
        self.player_hands[1] = self.deck[8:16]
        self.field = self.deck[16:24]
        self.deck = self.deck[24:]
        # sort hands fields and point piles
        self.sort_piles()
        # init yaku arrays
        self.player_yakus = [[],[]]
        self.player_yaku_points = [0, 0]
        self.player_koikoied = [False, False]
        
    
    def sort_piles(self):
        self.player_hands[0].sort(key=lambda card: card.month)
        self.player_hands[1].sort(key=lambda card: card.month)
        self.field.sort(key=lambda card: card.month)
        self.player_point_piles[0].sort(key=lambda card: card.category)
        self.player_point_piles[1].sort(key=lambda card: card.category)

    def print_game_state(self):
        print('Opponent pile:', self.player_point_piles[self.current_opponent])
        print('Opponent hand count:', len(self.player_hands[self.current_opponent]))
        print('Field:  ', self.field)
        print('Your hand:', self.player_hands[self.current_player])
        print('Your pile:', self.player_point_piles[self.current_player])


    def match_field_card(self, played_card:Card):
        valid_field_card_ids = [
            id for id, card in enumerate(self.field)
            if card.month == played_card.month
        ]
        if len(valid_field_card_ids):
            if len(valid_field_card_ids) == 1:
                choosen_field_id = valid_field_card_ids[0]
            elif len(valid_field_card_ids) == 2:
                print('Multiple valid target exists on field:')
                for id in valid_field_card_ids:
                    print(id, self.field[id])
                choosen_field_id = int(input('Get:'))
                while choosen_field_id not in valid_field_card_ids:
                    print('Invalid Input!')
                    choosen_field_id = int(input('Get:'))
            elif len(valid_field_card_ids) == 3:
                choosen_field_id = valid_field_card_ids[0]
                bonus_field_card_1 = self.field[valid_field_card_ids[1]]
                bonus_field_card_2 = self.field[valid_field_card_ids[2]]
                self.player_point_piles[self.current_player].append(bonus_field_card_1)
                self.player_point_piles[self.current_player].append(bonus_field_card_2)
                self.field.remove(bonus_field_card_1)
                self.field.remove(bonus_field_card_2)
            
            choosen_field_card = self.field[choosen_field_id]
            print('Got:', choosen_field_card)
            self.field.remove(choosen_field_card)
            self.player_point_piles[self.current_player].append(played_card)
            self.player_point_piles[self.current_player].append(choosen_field_card)
        else:
            print('No match')
            self.field.append(played_card)


        
    def turn(self) -> bool:
        print('*' * 20)
        print(f'It\'s player {self.current_player+1}\'s turn!')
        self.print_game_state()

        print('*' * 20)
        # Choose card to play
        field_months = [
            card.month for card in self.field
        ]
        valid_hand_card_ids = [
            id for id, card in enumerate(self.player_hands[self.current_player] )
            if card.month in field_months
        ]
        print('Your hand:')
        for id in range(len(self.player_hands[self.current_player])):
            print(id, self.player_hands[self.current_player][id], 'Exist' if id in valid_hand_card_ids else '')

        choosen_card_id = int(input('Play:'))
        while choosen_card_id not in range(len(self.player_hands[self.current_player])):
            print('Invalid Input!')
            choosen_card_id = int(input('Play:'))

        choosen_hand_card:Card = self.player_hands[self.current_player][choosen_card_id]
        print('Played:', choosen_hand_card)
        self.player_hands[self.current_player].remove(choosen_hand_card)


        print('*' * 20)
        # Choose field card to get
        self.match_field_card(choosen_hand_card)

        print('*' * 20)
        # Flip one card on top of deck and match field
        top_deck_card, self.deck =  self.deck[0], self.deck[1:]
        print('Top deck:', top_deck_card)
        self.match_field_card(top_deck_card)

        print('*' * 20)
        self.print_game_state()
        # check yakus
        yaku_point, yakus = check_all_yakus(self.player_point_piles[self.current_player])
        if yaku_point != self.player_yaku_points[self.current_player]:
            print('*' * 20)
            print('YAKU!')
            print(yakus)
            koikoi = input('Koikoi (y/n)?')
            while koikoi not in ['y', 'n']:
                print('Invalid input!')
                koikoi = input('Koikoi (y/n)?')
            if koikoi == 'n':
                print(f'AGARI! Player {self.current_player+1} won {yaku_point} point{"s" if yaku_point > 1 else ""}')
                print('Yakus:', yakus)
                return True
            else:
                print('Koikoi!')
                self.player_koikoied[self.current_player] = True
            self.player_yaku_points[self.current_player], self.player_yakus[self.current_player] = yaku_point, yakus

        self.current_player, self.current_opponent = self.current_opponent, self.current_player
        return False


    def game(self) -> int:
        game_end = self.turn()
        while not game_end:
            game_end = self.turn()



# koikoi_game = Koikoi()

# koikoi_game.game()

# print(Month.__dict__)
