import config
import random
from codename_card import *
from map_card import *

class CodenameGame(object):
    def __init__(self):
        # An array of Card objects
        self.deck = self._gen_cards()
        self.map_card = MapCard()
        self.red_count = 0
        self.blue_count = 0
        self.current_turn = self.map_card.get_starting_color()
        self.current_clue = {"Word" : None, "Number" : None}

    # Generate a new deck of cards, chosing a set of cards randomly from the set
    # of all cards.
    def _gen_cards(self):
        words = random.sample(config.WORDS, config.NUM_CARDS)
        cards = []
        position = 0
        for word in words:
            cards.append(Card(word, position))
            position += 1
        return cards

    def mark_card(self, card, new_status):
        card.set_status(new_status)

    def get_card_by_word(self, word):
        for card in self.deck:
            if (card.get_word() == word):
                return card
        return None

    def set_current_clue(self, word, number):
        assert(int(number) == number), "Not a valid number"

        self.current_clue["Word"] = word
        self.current_clue["Number"] = number

    # Makes a guess, and returns boolean based on correctness of guess
    def make_guess(self, word):
        if (self.current_clue["Number"] == 0):
            raise Exception("No more guesses left!")

        card = self.get_card_by_word(word)
        if (not card):
            raise Exception("Invalid word")

        position_type = self.map_card.get_card_type_at_position(card.get_position())
        if (self.current_turn == position_type):
            card.set_status(position_type)
            self.current_clue["Number"] -= 1
            return True
        else:
            # Incorrect guess ends the turn
            card.set_status(position_type):
            self.current_clue["Number"] = 0
            return False

    def switch_turns(self, word, number):
        self.current_turn = config.RED if self.current_turn == config.BLUE else config.BLUE
        self.set_current_clue(word, number)

    def is_game_over(self):
        # Game over condition is that red or blue meets their total possible or the bomb has been hit

        # Check if bomb has been uncovered
        bomb_location = self.map_card.get_bomb_location()
        if (self.deck[bomb_location].get_status() == config.BOMB):
            return True

        # Check if red or blue is at winning count
        if (self.red_count == self.map_card.get_num_card_by_type(config.RED)):
            return True
        elif (self.blue_count == self.map_card.get_num_card_by_type(config.BLUE)):
            return True

        return False


    def __repr__(self):
        output = str(self.map_card) + "\n"
        max_len = 15
        spacer = lambda x: str(x) + " "*(max_len - len(str(x)))
        for x in range(5):
            output += "".join(map(spacer, self.deck[5*x:5*x+5]))
            output += "\n"
        output += "\n"
        status_spacer = lambda x: str(x.status) + " "*(max_len - len(x.status))
        for x in range(5):
            output += "".join(map(status_spacer, self.deck[5*x:5*x+5]))
            output += "\n"
        return output


if __name__ == "__main__":
    cg = CodenameGame()
    #cg.mark_card(cg.deck[0], config.RED)
    print cg
