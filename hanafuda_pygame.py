import pygame
import os
from hanafuda_card import Card, deck
from hanafuda_yaku import check_all_yakus
from enum import Enum
import random

display_width = 1200
display_height = 800
DEFAULT_CARD_SIZE = (90, 150)
DEFAULT_CARD_SIZE_SMOL = (72, 129)
DEFAULT_CARD_SIZE_EXTRA_SMOL = (30, 50)

class CardSprite(pygame.sprite.Sprite):
    def __init__(self, card, pos=(0,0), card_size=DEFAULT_CARD_SIZE):
        super().__init__()
        if card:
            self.card = card
            card_img = pygame.image.load(os.path.join('card_images', card.image_name))
        else:
            self.card = None
            card_img = pygame.image.load(os.path.join('card_images', 'sm_Hana-cardback.jpg'))

        self.image = pygame.transform.scale(card_img, card_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.card = card

    def set_pos(self, pos):
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pick(self):
        card_img = pygame.image.load(os.path.join('card_images', self.card.image_name))
        self.image = pygame.transform.scale(card_img, DEFAULT_CARD_SIZE_SMOL)
    
    def unpick(self):
        card_img = pygame.image.load(os.path.join('card_images', self.card.image_name))
        self.image = pygame.transform.scale(card_img, DEFAULT_CARD_SIZE)
    
    def point_pile(self):
        card_img = pygame.image.load(os.path.join('card_images', self.card.image_name))
        self.image = pygame.transform.scale(card_img, DEFAULT_CARD_SIZE_EXTRA_SMOL)


class KoikoiGameState(Enum):
    CHOOSE_HAND = 1
    CHOOSE_FIELD_HAND = 2
    DRAW_CARD = 3
    DREW_CARD = 4
    CHOOSE_FIELD_DRAW = 5
    CHOOSE_KOIKOI = 6
    GAME_END = 7

class Koikoi:
    PLAYER_1 = 0
    PLAYER_2 = 1

    def __init__(self, display):
        self.display = display
        self.player_hands = [[], []]
        self.player_point_piles = [[], []]
        self.field = []
        self.deck = deck.copy()
        random.shuffle(self.deck)
        self.current_player = self.PLAYER_1
        self.current_opponent = self.PLAYER_2
        # append player hands and field
        self.player_hands[0] = [CardSprite(card) for card in self.deck[:8]]
        self.player_hands[1] = [CardSprite(card) for card in self.deck[8:16]]
        self.field = [CardSprite(card) for card in self.deck[16:24]]
        self.deck = [CardSprite(card) for card in self.deck[24:]]
        # sort hands fields and point piles
        self.sort_piles()
        # init yaku arrays
        self.player_yakus = [[],[]]
        self.player_yaku_points = [0, 0]
        self.player_koikoied = [False, False]
        self.game_state = KoikoiGameState.CHOOSE_HAND
        self.choosen_card = None
        self.top_deck_card = None
        self.koikoi_menu_flag = False
        self.agari_popup_flag = False
        
        
    def sort_piles(self):
        self.player_hands[0].sort(key=lambda card_sprite: card_sprite.card.month)
        self.player_hands[1].sort(key=lambda card_sprite: card_sprite.card.month)
        self.field.sort(key=lambda card_sprite: card_sprite.card.month)
        self.player_point_piles[0].sort(key=lambda card: card.month)
        self.player_point_piles[1].sort(key=lambda card: card.month)
    
    def display_field(self):
        render_group = pygame.sprite.RenderPlain()
        # top deck card (if exists)
        if self.top_deck_card:
            pos = (int(display_width//2) + 350, int(display_height//2))
            self.top_deck_card.set_pos(pos)
            render_group.add(self.top_deck_card)
        
        # deck
        if self.deck:
            pos = (int(display_width//2) + 450, int(display_height//2))
            deck_back = CardSprite(None, pos)
            render_group.add(deck_back)

        # player 1 hand
        player_1_x = int((display_width - len(self.player_hands[self.current_player]) * 100) // 2)
        for i, card_sprite in enumerate(self.player_hands[self.current_player]):
            pos = (i * (90 + 10) + player_1_x, display_height-90)
            card_sprite.set_pos(pos)
            render_group.add(card_sprite)
        
        # player 1 point pile
        for i, card in enumerate(self.player_point_piles[self.current_player]):
            pos = (i * (16) + 50, int(display_height//2)+250)
            card_sprite = CardSprite(card, pos)
            card_sprite.point_pile()
            render_group.add(card_sprite)

        # player 2 hand
        player_2_x = int((display_width - len(self.player_hands[self.current_opponent]) * 100) // 2)
        # for i, card_sprite in enumerate(self.player_hands[self.current_opponent]):
        #     pos = (i * (90 + 10) + player_2_x, 90)
        #     card_sprite.set_pos(pos)
        #     render_group.add(card_sprite)
        for i in range(len(self.player_hands[self.current_opponent])):
            pos = (i * (90 + 10) + player_2_x, 90)
            card_sprite = CardSprite(None, pos)
            render_group.add(card_sprite)

        
        # player 2 point pile
        for i, card in enumerate(self.player_point_piles[self.current_opponent]):
            pos = (i * (16) + 50, int(display_height//2)-150)
            card_sprite = CardSprite(card, pos)
            card_sprite.point_pile()
            render_group.add(card_sprite)

        # field
        if len(self.field) <= 6:
            field_x = int((display_width - len(self.field) * 100) // 2)
            for i, card_sprite in enumerate(self.field):
                pos = (i * (90 + 10) + field_x, int(display_height // 2))
                card_sprite.set_pos(pos)
                render_group.add(card_sprite)
        else:
            top_row_len = int(round(len(self.field) / 2))
            field_x1 = int((display_width - top_row_len * 100) // 2)
            field_x2 = int((display_width - (len(self.field)-top_row_len) * 100) // 2)
            for i, card_sprite in enumerate(self.field):
                if i < top_row_len:
                    pos = ( i * (90 + 10) + field_x1, int(display_height // 2) - 80)
                else:
                    pos = ( (i-top_row_len) * (90 + 10) + field_x2, int(display_height // 2) + 80)
                card_sprite.set_pos(pos)
                render_group.add(card_sprite)
        if self.koikoi_menu_flag:
            render_group.add(koikoi_menu_popup)
        if self.agari_popup_flag:
            points = self.player_yaku_points[self.current_player] * (2 if self.player_koikoied[self.current_opponent] else 1)
            agari_popup = PopupSprite([
                f'Player {self.current_player + 1} won!', 
                f'Points: {points}',
                f'Yaku:{self.player_yakus[self.current_player]}'])
            render_group.add(agari_popup)
        render_group.draw(self.display)
        pygame.display.update()

    def prepare_match(self, played_card):
        valid_field_card_ids = [
            id for id, card_sprite in enumerate(self.field)
            if card_sprite.card.month == played_card.card.month
        ]

        if valid_field_card_ids:
            # if two card of the same month exist on field prompt user to choose
            if len(valid_field_card_ids) == 2:
                self.choosen_card = played_card
                self.choosen_card.pick()
                for id in valid_field_card_ids:
                    self.field[id].pick()
                if KoikoiGameState.CHOOSE_HAND:
                    self.game_state = KoikoiGameState.CHOOSE_FIELD_HAND
                elif KoikoiGameState.DREW_CARD:
                    self.game_state = KoikoiGameState.CHOOSE_FIELD_DRAW
                return
            # if theres only one, then player gets that card
            elif len(valid_field_card_ids) == 1:
                choosen_field_id = valid_field_card_ids[0]
            # if theres all three, then player gets all three
            elif len(valid_field_card_ids) == 3:
                choosen_field_id = valid_field_card_ids[0]
                bonus_field_card_1 = self.field[valid_field_card_ids[1]]
                bonus_field_card_2 = self.field[valid_field_card_ids[2]]
                self.player_point_piles[self.current_player].append(bonus_field_card_1.card)
                self.player_point_piles[self.current_player].append(bonus_field_card_2.card)
                self.field.remove(bonus_field_card_1)
                self.field.remove(bonus_field_card_2)
            
            choosen_field_card = self.field[choosen_field_id]
            self.field.remove(choosen_field_card)

            if played_card in self.player_hands[self.current_player]:
                self.player_hands[self.current_player].remove(played_card)
            
            self.player_point_piles[self.current_player].append(played_card.card)
            self.player_point_piles[self.current_player].append(choosen_field_card.card)
        else:
            self.field.append(played_card)

            if played_card in self.player_hands[self.current_player]:
                self.player_hands[self.current_player].remove(played_card)
        
        if self.game_state == KoikoiGameState.CHOOSE_HAND:
            self.game_state = KoikoiGameState.DRAW_CARD

        elif self.game_state == KoikoiGameState.DREW_CARD:
            self.game_state = KoikoiGameState.CHOOSE_HAND
            
    def switch_player(self):
        yaku_point, yakus = check_all_yakus(self.player_point_piles[self.current_player])
        if yaku_point != self.player_yaku_points[self.current_player]:
            print(f'Player {self.current_player+1}',yaku_point, yakus)
            self.game_state = KoikoiGameState.CHOOSE_KOIKOI
            self.koikoi_menu_flag = True
            return
        self.player_yaku_points[self.current_player], self.player_yakus[self.current_player] = yaku_point, yakus
        self.current_player, self.current_opponent = self.current_opponent, self.current_player


    def mouse_event(self, mouse_pos):
        if self.game_state == KoikoiGameState.CHOOSE_HAND:
            # initialize choosen id as None
            choosen_hand_card_id = None
            # if player clicked on a hand card, then cache its id
            for id_hand in range(len(self.player_hands[self.current_player])):
                if self.player_hands[self.current_player][id_hand].rect.collidepoint(mouse_pos):
                    choosen_hand_card_id = id_hand
                    break
            # if an id is cached, match the card, 
            if choosen_hand_card_id is not None:
                choosen_hand_card = self.player_hands[self.current_player][choosen_hand_card_id]
                self.prepare_match(choosen_hand_card) # -> Choose Field or Draw card
        
        elif self.game_state == KoikoiGameState.CHOOSE_FIELD_HAND or self.game_state == KoikoiGameState.CHOOSE_FIELD_DRAW:
            # first filter to see all card that can be choosed on field
            valid_field_card_ids = [
                    id for id, card_sprite in enumerate(self.field)
                    if card_sprite.card.month == self.choosen_card.card.month
            ]
            # if user selected the handcard again, then go back to choose hand
            if self.game_state == KoikoiGameState.CHOOSE_FIELD_HAND and self.choosen_card.rect.collidepoint(mouse_pos):
                self.choosen_card.unpick()
                self.choosen_card = None
                for id in valid_field_card_ids:
                    self.field[id].unpick()
                self.game_state = KoikoiGameState.CHOOSE_HAND
                return
            # otherwise if the user clicked a valid field card, unscale all the other unpicked cards
            # then save both the choosen card and matched field card to the point pile, and remove the
            # card from the player's hand
            for id in valid_field_card_ids:
                card_sprite_field = self.field[id]
                if card_sprite_field.rect.collidepoint(mouse_pos):
                    for id_field in valid_field_card_ids:
                        self.field[id_field].unpick()
                    
                    self.player_point_piles[self.current_player].append(self.choosen_card.card)
                    self.player_point_piles[self.current_player].append(card_sprite_field.card)
                    self.field.remove(card_sprite_field)
                    if self.choosen_card in self.player_hands[self.current_player]:
                        self.player_hands[self.current_player].remove(self.choosen_card)
                    self.choosen_card = None

                    if self.game_state == KoikoiGameState.CHOOSE_FIELD_HAND:
                        self.game_state = KoikoiGameState.DRAW_CARD

                    elif self.game_state == KoikoiGameState.CHOOSE_FIELD_DRAW:
                        self.game_state = KoikoiGameState.CHOOSE_HAND
                        self.switch_player()
        
        elif self.game_state == KoikoiGameState.DRAW_CARD:
            self.top_deck_card, self.deck =  self.deck[0], self.deck[1:]
            self.display_field()
            self.game_state = KoikoiGameState.DREW_CARD

        elif self.game_state == KoikoiGameState.DREW_CARD:
            self.prepare_match(self.top_deck_card) 
            self.top_deck_card = None
            if self.game_state == KoikoiGameState.CHOOSE_HAND:
                self.switch_player()

        elif self.game_state == KoikoiGameState.CHOOSE_KOIKOI:
            self.koikoi_menu_flag = True
            koikoi_rect = pygame.rect.Rect(475, 290, 250, 65)
            agari_rect = pygame.rect.Rect(500, 440, 200, 80)
            print(mouse_pos)
            if koikoi_rect.collidepoint(mouse_pos):
                print('KOIKOI')
                self.player_koikoied[self.current_player] = True
                self.koikoi_menu_flag = False
                self.player_yaku_points[self.current_player], self.player_yakus[self.current_player] = check_all_yakus(self.player_point_piles[self.current_player])
                self.current_player, self.current_opponent = self.current_opponent, self.current_player
                self.game_state = KoikoiGameState.CHOOSE_HAND
            elif agari_rect.collidepoint(mouse_pos):
                print('AGARI')
                self.koikoi_menu_flag = False
                self.player_yaku_points[self.current_player], self.player_yakus[self.current_player] = check_all_yakus(self.player_point_piles[self.current_player])
                self.agari_popup_flag = True
                self.game_state = KoikoiGameState.GAME_END
                

        elif self.game_state == KoikoiGameState.GAME_END:
            pass
            # points = self.player_yaku_points[self.current_player] * (2 if self.player_koikoied[self.current_opponent] else 1)
            # print(f'Player {self.current_player+1} won!')
            # print('Points:', points)
            # print('Yaku:', self.player_yakus[self.current_player])
            # TODO: make window for game end

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
koikoi_game = Koikoi(gameDisplay)
pygame.display.set_caption('Py Koikoi')
background = Background('other_images/tatami_bg.jpg', (0,0))
black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()

class PopupSprite(pygame.sprite.Sprite):
    def __init__(self, options) -> None:
        super().__init__()
        popupSurf = pygame.Surface((int(display_width * 0.5), int(display_height * 0.5)))
        popupSurf.fill((255,255,255,125))
        # options = ['Koikoi', 'Agari']
        text_y_shifts = [-1, 1, 0]
        text_font_sizes = [100,100,25]
        for i in range(len(options)):
            pygame.font.get_default_font()
            font = pygame.font.SysFont(None, text_font_sizes[i])
            textSurf = font.render(options[i], 1, (255,0,0))
            textRect = textSurf.get_rect()
            textRect.centerx = display_width * 0.25
            textRect.centerx = display_width * 0.25
            textRect.centery = display_height * 0.25 + pygame.font.Font.get_linesize(font) * text_y_shifts[i]

            popupSurf.blit(textSurf, textRect)
            # print(options[i], textRect)
        popupRect = popupSurf.get_rect()
        popupRect.centerx = display_width * 0.5
        popupRect.centery = display_height * 0.5
        self.image = popupSurf
        self.rect = popupRect


koikoi_menu_popup = PopupSprite(['Koikoi', 'Agari'])


crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.MOUSEBUTTONDOWN:    
            mouse_pos = pygame.mouse.get_pos()
            koikoi_game.mouse_event(mouse_pos)
        # elif event.type == pygame.KEYDOWN:
        #     koikoi_game.game_state = KoikoiGameState.CHOOSE_KOIKOI
        #     koikoi_game.koikoi_menu_flag = not koikoi_game.koikoi_menu_flag
            
    
    gameDisplay.fill(white)
    gameDisplay.blit(background.image, background.rect)
    koikoi_game.display_field()
    
    clock.tick(60)

pygame.quit()
quit()