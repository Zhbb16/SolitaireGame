import pygame
import pygame.mixer
from Deck import Deck
from Waste import Waste
from Foundation import Foundation
from Table import Table
import random

random.seed()
pygame.init()
window_size = (1080, 720)  # 1080, 720
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Solitaire Game")
logo = pygame.image.load("solitaire_logo.png")
pygame.display.set_icon(logo)
game_is_running = True

backgroundImage = pygame.image.load("assets/background3.png")

deck = Deck()
deck.shuffle()

waste = Waste()

clock = pygame.time.Clock()

holding_cards = []
holding_card_group = None
mouse_cords = ()

moves = 0
score = 0
frame = 0
time = 0

place_sound = pygame.mixer.Sound('assets/flip.wav')
shuffle_sound = pygame.mixer.Sound('assets/shuffle.wav')
# shuffle_sound.play()

cards_in_foundations = {}  # Initialize the dictionary


def clicked_new_card(mouse_x, mouse_y):
    global moves
    if mouse_x > 129 and mouse_x < 226 and mouse_y > 14 and mouse_y < 155:
        if len(deck.get_deck()) <= 0:
            deck.add_cards(list(reversed(waste.get_waste_pile().copy())))
            waste.empty()
            shuffle_sound.play()
        else:
            moves += 1
            waste.add_card(deck.remove_card())
            place_sound.play()


def check_holding_card(mouse_x, mouse_y):
    global holding_card_group, holding_cards, mouse_cords
    possible_cards = []

    mouse_cords = (mouse_x, mouse_y)

    for table in tables:
        for table_card in table.get_table():
            if table_card.is_front_showing():
                possible_cards.append((table_card, table))

    for foundation in foundations:
        foundation_card = foundation.get_top_card()
        if foundation_card != None:
            possible_cards.append((foundation_card, foundation))

    waste_card = waste.get_top_card()
    if waste_card != None:
        possible_cards.append((waste_card, waste))

    for card in possible_cards:
        card_x = card[0].get_coordinates()[0]
        card_y = card[0].get_coordinates()[1]
        if mouse_x > card_x and mouse_x < card_x + 100 and mouse_y > card_y and mouse_y < card_y + 145:
            holding_card_group = card[1]
            if holding_card_group in tables:
                holding_cards = holding_card_group.get_cards_below(card[0])
            else:
                holding_cards = [card[0]]


def place_card(mouse_x, mouse_y):
    global holding_card_group, holding_cards, mouse_cords, tables, moves, score

    # Check if the cards are kings and are being moved to an empty pile
    if len(holding_cards) > 1 and all(
            card.get_value() == 13 for card in holding_cards) and holding_card_group.bottom_card() is None:
        holding_card_group.add_cards(holding_cards)
        for card in holding_cards:
            holding_card_group.remove_card()
            place_sound.play()
            moves += 1
        return

    # Autofill with click
    if mouse_cords == (mouse_x, mouse_y):
        if len(holding_cards) == 1:
            for foundation in foundations:
                if foundation.get_suit() == holding_cards[0].get_suit():
                    foundation_card = foundation.get_top_card()
                    if foundation_card is not None:
                        if foundation_card.get_value() + 1 == holding_cards[0].get_value():
                            foundation.add_card(holding_cards[0])
                            holding_card_group.remove_card()
                            place_sound.play()
                            moves += 1
                            if holding_cards[0] not in cards_in_foundations:
                                score += 5
                                cards_in_foundations[holding_cards[0]] = True
                            return
                    else:
                        if holding_cards[0].get_value() == 1:
                            foundation.add_card(holding_cards[0])
                            holding_card_group.remove_card()
                            place_sound.play()
                            moves += 1
                            if holding_cards[0] not in cards_in_foundations:
                                score += 5
                                cards_in_foundations[holding_cards[0]] = True
                            return

    for table in tables:
        bottom_card = table.bottom_card()
        if bottom_card is None and holding_cards[0].get_value() == 13:
            table.add_cards(holding_cards)
            for card in holding_cards:
                holding_card_group.remove_card()
                place_sound.play()
                moves += 1
            return
        elif bottom_card is not None:
            value = bottom_card.get_value()
            if bottom_card.get_color() != holding_cards[0].get_color() and value - 1 == holding_cards[0].get_value():
                table.add_cards(holding_cards)
                for card in holding_cards:
                    holding_card_group.remove_card()
                    place_sound.play()
                    moves += 1
                return
    else:
        for idx, table in enumerate(tables):
            # Adjust the positions based on the number of piles you want
            # You can add or remove elements in the positions list to change the number of piles
            positions = [950, 825, 710, 590, 470, 355, 242, 120]

            # Change the width and height of the drop zone
            drop_zone_width = 145
            drop_zone_height = 600

            # Check if the mouse is within the drop zone of a table pile
            if mouse_x > table.get_x() and mouse_x < table.get_x() + drop_zone_width and mouse_y > table.get_y() and mouse_y < table.get_y() + drop_zone_height:
                bottom_card = table.bottom_card()
                if bottom_card is None and holding_cards[0].get_value() == 13:
                    table.add_cards(holding_cards)
                    for card in holding_cards:
                        holding_card_group.remove_card()
                        place_sound.play()
                        moves += 1
                    return
                elif bottom_card is not None and (
                        bottom_card.get_color() != holding_cards[0].get_color() and bottom_card.get_value() - 1 ==
                        holding_cards[0].get_value()):
                    table.add_cards(holding_cards)
                    for card in holding_cards:
                        holding_card_group.remove_card()
                        place_sound.play()
                        moves += 1
                    return
            elif mouse_x > table.get_x() and mouse_x < table.get_x() + drop_zone_width and mouse_y > table.get_y() and mouse_y < table.get_y() + drop_zone_height:
                if holding_cards[0].get_value() == 1:  # Check if the card is an Ace
                    table.add_cards(holding_cards)
                    for card in holding_cards:
                        holding_card_group.remove_card()
                        place_sound.play()
                        moves += 1
                    return
        else:
            for foundation in foundations:
                if foundation.get_suit() == holding_cards[0].get_suit():
                    foundation_card = foundation.get_top_card()
                    if foundation_card is not None:
                        if foundation_card.get_value() + 1 == holding_cards[0].get_value():
                            foundation.add_card(holding_cards[0])
                            holding_card_group.remove_card()
                            place_sound.play()
                            moves += 1
                            score += 5
                            return
                    else:
                        if holding_cards[0].get_value() == 1:
                            foundation.add_card(holding_cards[0])
                            holding_card_group.remove_card()
                            place_sound.play()
                            moves += 1
                            score += 5
                            return

    holding_card_group.set_cards()


def card_follow_mouse(mouse_x, mouse_y):
    if holding_cards != []:
        # card_cords = holding_card.get_coordinates()
        # dif1 = mouse_x - card_cords[0]
        # dif2 = mouse_y - card_cords[1]
        x = mouse_x - 50
        y = mouse_y - 50
        pos = 0
        for card in holding_cards:
            card.set_coordinates(x, y + (pos * 40))
            pygame.sprite.GroupSingle(card).draw(screen)
            pos += 1


def create_tables():
    tables = []
    x = 135
    card_amount = 1
    for i in range(0, 7):
        tables.append(Table(x, deck, card_amount))
        x += 135
        card_amount += 1
    return tables


def create_foundations():
    foundations = []
    x = 540
    suits = ["hearts", "diamonds", "spades", "clubs"]
    for i in range(0, 4):
        foundations.append(Foundation(x, suits[i]))
        x += 135
    return foundations


tables = create_tables()
foundations = create_foundations()


def message_display(text, cords, color=(255, 255, 255), font_size=17):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=cords)
    screen.blit(text_surface, text_rect)


def restart_game():
    global deck, waste, tables, foundations, moves
    deck = Deck()
    deck.shuffle()
    waste = Waste()
    tables = create_tables()
    foundations = create_foundations()
    moves = 0


def check_if_game_won():
    for foundation in foundations:
        if len(foundation.get_foundation()) != 13:  # Assuming 13 cards in each foundation pile
            return False
    return True


selected_mode = "Classic Mode"  # Initialize the selected mode


def game_loop():
    global holding_cards, moves, score, selected_mode

    deck = Deck()
    deck.shuffle()

    restart_button = pygame.Rect(15, 25, 95, 40)  # (30, 480, 95, 40)
    restart_text = "Classic"

    vegas_button = pygame.Rect(15, 85, 95, 40)
    vegas_text = "Vegas"

    # mute_button = pygame.Rect(15, 145, 95, 40)
    # mute_text = "Mute" if not pygame.mixer.music.get_busy() else "Unmute"
    #
    # undo_button = pygame.Rect(15, 205, 95, 40)
    # undo_text = "Undo"

    def restart_game_with_negative_score():
        global deck, waste, tables, foundations, moves, score, start_time
        deck = Deck()
        deck.shuffle()
        waste = Waste()
        tables = create_tables()
        foundations = create_foundations()
        moves = 0
        score = -52  # Set initial score to -52
        start_time = pygame.time.get_ticks()  # Reset the timer

    # pygame.init()
    #
    # # Load the background music
    # pygame.mixer.music.load("background.mp3")
    #
    # # Start playing the background music on loop
    # pygame.mixer.music.play(-1)

    start_time = pygame.time.get_ticks()  # Get the start time

    game_running = True  # Flag to control the game loop

    while game_running:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_new_card(mouse_x, mouse_y)
                check_holding_card(mouse_x, mouse_y)

                # Check if the restart button is clicked
                if restart_button.collidepoint(mouse_x, mouse_y):
                    restart_game()
                    moves = 0
                    score = 0
                    start_time = pygame.time.get_ticks()  # Reset the timer
                    selected_mode = "Classic Mode"  # Update the selected mode

                # Check if the Vegas button is clicked
                if vegas_button.collidepoint(mouse_x, mouse_y):
                    restart_game_with_negative_score()
                    moves = 0
                    start_time = pygame.time.get_ticks()  # Reset the timer
                    selected_mode = "Vegas Mode"  # Update the selected mode

                # # Check if the mute button is clicked
                # if mute_button.collidepoint(mouse_x, mouse_y):
                #     if pygame.mixer.music.get_busy():
                #         pygame.mixer.music.pause()
                #         mute_text = "Unmute"
                #     else:
                #         pygame.mixer.music.unpause()
                #         mute_text = "Mute"

            if event.type == pygame.MOUSEBUTTONUP:
                if holding_cards != []:
                    place_card(mouse_x, mouse_y)
                    holding_cards = []
                    # set because if card is placed the new ones need to pop out
                    waste.set_cards()
            if event.type == pygame.QUIT:
                game_running = False  # Set the flag to exit the game loop

        # Draw background image to screen (behind everything)
        screen.blit(backgroundImage, (0, 0))

        # Draw all cards in tables to the screen
        for table in tables:
            for card in table.get_table():
                if not card in holding_cards:
                    pygame.sprite.GroupSingle(card).draw(screen)

        for foundation in foundations:
            card = foundation.get_top_card()
            if not card in holding_cards:
                pygame.sprite.GroupSingle(card).draw(screen)

        # Draw all cards in waste bin to the screen
        for card in waste.get_show_waste_pile():
            if not card in holding_cards:
                pygame.sprite.GroupSingle(card).draw(screen)

        # Draw cards picked up by mouse
        card_follow_mouse(mouse_x, mouse_y)

        # Draw restart button
        pygame.draw.rect(screen, (1, 1, 31), restart_button)
        message_display(restart_text, (restart_button.centerx, restart_button.centery), color=(255, 255, 255),
                        font_size=26)

        # Draw Vegas button
        pygame.draw.rect(screen, (1, 1, 31), vegas_button)
        message_display(vegas_text, (vegas_button.centerx, vegas_button.centery), color=(255, 255, 255), font_size=26)

        # Calculate and draw elapsed time
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Convert milliseconds to seconds
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_text = f"{minutes:02d}:{seconds:02d}"
        message_display("Time:", (40, 651), color=(255, 255, 255), font_size=28)
        message_display(time_text, (100, 651), color=(255, 255, 255), font_size=28)

        # Draw score
        message_display("Score:", (42, 611), color=(255, 255, 255), font_size=28)
        message_display(str(score), (88, 611), color=(255, 255, 255), font_size=28)

        # Draw current mode
        message_display(selected_mode, (65, 690), color=(255, 200, 0), font_size=26)

        # Check and display "You Win!" message if the game is won
        if check_if_game_won():
            message_display("You Win!", (window_size[0] // 2, window_size[1] // 2), color=(255, 255, 255), font_size=48)

        # Draw mute button
        # pygame.draw.rect(screen, (1, 1, 31), mute_button)
        # message_display(mute_text, (mute_button.centerx, mute_button.centery), color=(255, 255, 255), font_size=26)

        # Draw moves
        # message_display("Moves", (42, 571), color=(255, 255, 255), font_size=24)
        # message_display(str(moves), (88, 571), color=(255, 255, 255), font_size=24)

        # # Draw undo button
        # pygame.draw.rect(screen, (1, 1, 31), undo_button)
        # message_display(undo_text, (undo_button.centerx, undo_button.centery), color=(255, 255, 255), font_size=26)

        # Update the display
        pygame.display.update()
        clock.tick(60)

    # Clean up and quit pygame
    pygame.quit()


# Start the game loop
game_loop()
