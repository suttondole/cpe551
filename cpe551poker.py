import sys, random

class Card (object):
  #sets to hold different ranks and suits
  RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

  SUITS = ('C', 'D', 'H', 'S')

  # constructor
  def __init__ (self, rank = 12, suit = 'S'):
    if (rank in Card.RANKS):
      self.rank = rank
    else:
      self.rank = 12

    if (suit in Card.SUITS):
      self.suit = suit
    else:
      self.suit = 'S'

  # string representation of a Card object
  def __str__ (self):
    if (self.rank == 14):
      rank = 'A'
    elif (self.rank == 13):
      rank = 'K'
    elif (self.rank == 12):
      rank = 'Q'
    elif (self.rank == 11):
      rank = 'J'
    else:
      rank = str (self.rank)
    return rank + self.suit

  # equality tests

  #equal
  def __eq__ (self, other):
    return self.rank == other.rank

  #not equal
  def __ne__ (self, other):
    return self.rank != other.rank

  #less than
  def __lt__ (self, other):
    return self.rank < other.rank

  #less than or equal to
  def __le__ (self, other):
    return self.rank <= other.rank

  #greater than
  def __gt__ (self, other):
    return self.rank > other.rank

  #greater than or equal to
  def __ge__ (self, other):
    return self.rank >= other.rank

class Deck (object):
  # constructor
  def __init__ (self, num_decks = 1):
    self.deck = []
    for i in range (num_decks):
      for suit in Card.SUITS:
        for rank in Card.RANKS:
          card = Card (rank, suit)
          self.deck.append (card)

  # shuffle the deck
  def shuffle (self):
    random.shuffle (self.deck)

  # deal a card
  def deal (self):
    if (len(self.deck) == 0):
      return None
    else:
      return self.deck.pop(0)

class Poker (object):
  # constructor
  def __init__ (self, num_players = 2, num_cards = 5):
    self.deck = Deck()
    self.deck.shuffle()
    self.all_hands = []
    self.numCards_in_Hand = num_cards

    # deal the cards to the players
    for i in range (num_players):
      hand = []
      for j in range (self.numCards_in_Hand):
        hand.append (self.deck.deal())
      self.all_hands.append (hand)
   
  # simulate the play of poker
  def play (self):
    # sort the hands of each player and print
    for i in range (len(self.all_hands)):
      sorted_hand = sorted (self.all_hands[i], reverse = True)
      self.all_hands[i] = sorted_hand
      hand_str = ''
      for card in sorted_hand:
        hand_str = hand_str + str (card) + ' '
      print ('Player ' + str(i + 1) + ' : ' + hand_str)
    print("")
    # determine the type of each hand and print
    hand_type = [] # create a list to store type of hand
    hand_points = [] # create a list to store points for hand

    #decide what kind of hand the cards have
    #returns 0 if not hand, else returns point value
    for i in range (len(self.all_hands)):
      sorted_hand = sorted (self.all_hands[i], reverse = True)
     
      result = self.is_royal(sorted_hand)
      if result[0]:
          hand_points.append(result[0])
          hand_type.append(result[1])
          continue
      result = self.is_straight_flush(sorted_hand)
      if result[0] != 0:
          hand_points.append(result[0])
          hand_type.append(result[1])
          continue
      result = self.is_four_kind(sorted_hand)
      if result[0]:
          hand_points.append(result[0])
          hand_type.append(result[1])
          continue
      result = self.is_full_house(sorted_hand)
      if result[0]:
          hand_points.append(result[0])
          hand_type.append(result[1])
          continue
      result = self.is_flush(sorted_hand)
      if result[0]:
          hand_points.append(result[0])
          hand_type.append(result[1])
          continue
      result = self.is_straight(sorted_hand)
      if result[0]:
          hand_points.append(result[0])
          hand_type.append(result[1])
          continue
      result = self.is_three_kind(sorted_hand)
      if result[0]:
          hand_points.append(result[0])
          hand_type.append(result[1])
          continue
      result = self.is_two_pair(sorted_hand)
      if result[0]:
          hand_points.append(result[0])
          hand_type.append(result[1])
          continue
      result = self.is_one_pair(sorted_hand)
      if result[0]:
          hand_points.append(result[0])
          hand_type.append(result[1])
          continue
      result = self.is_high_card(sorted_hand)
      hand_points.append(result[0])
      hand_type.append(result[1])
          
  


    #calculating best hand
    #does not consider if one hand of same type is more points than another
    current_max = 0
    current_winning_hand = ""
    current_winner = ""
    current_ties = {}
    for player in range(len(self.all_hands)):
        print("Player " + str(player + 1) + ": " + hand_type[player])
        if hand_type[player] == current_winning_hand:
            current_ties[player] = hand_points[player]
        elif current_max < hand_points[player]:
            current_max = hand_points[player]
            current_winner = str(player + 1)
            current_winning_hand = hand_type[player]
            current_ties = {}
            current_ties[player] = hand_points[player]
    print("")
    if len(current_ties) == 1:
        print("Player " + current_winner + " wins.")
    else:
        current_ties = dict(sorted(current_ties.items(), key = lambda item: item[1]))
        current_ties = dict(reversed(list(current_ties.items())))
        for player in current_ties:
            print("Player " + str(player + 1) + " ties.")
        
        

        
  def print_hands(self):
    for i in range (len(self.all_hands)):
      sorted_hand = sorted (self.all_hands[i], reverse = True)
      self.all_hands[i] = sorted_hand
      hand_str = ''
      for card in sorted_hand:
        hand_str = hand_str + str (card) + ' '
      print ('Player ' + str(i + 1) + ' : ' + hand_str)
          
    



  
        
  # determine if a hand is a royal flush
  # takes as argument a list of 5 Card objects
  # returns a number (points) for that hand
  def is_royal (self, hand):
    same_suit = True
    for i in range (len(hand) - 1):
      same_suit = same_suit and (hand[i].suit == hand[i + 1].suit)

    if (not same_suit):
      return 0, ''

    rank_order = True
    for i in range (len(hand)):
      rank_order = rank_order and (hand[i].rank == 14 - i)

    if (not rank_order):
      return 0, ''

    points = 10 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3
    points = points + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1
    points = points + (hand[4].rank)

    return points, 'Royal Flush'

  def is_straight_flush (self, hand):
    same_suit = True
    for i in range (len(hand) - 1):
      same_suit = same_suit and (hand[i].suit == hand[i + 1].suit)
    
    if (not same_suit):
      return 0, ''
    rank_order = True
    
    for i in range (len(hand) - 1):
      rank_order = rank_order and (hand[i].rank - hand[i+1].rank == 1)
      
    if (not rank_order):
      return 0, ''

    points = 9 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3 + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1 + (hand[4].rank)

    return points, "Straight Flush"

  def is_four_kind (self, hand):
    start = -1
    if hand[0].rank == hand[1].rank and hand[1].rank == hand[2].rank and hand[2].rank == hand[3].rank:
        start = 0
    elif hand[1].rank == hand[2].rank and hand[2].rank == hand[3].rank and hand[3].rank == hand[4].rank:
        start = 1
    else:
      return 0, ''
    
    
    points = 0
    if start == 0:
      points = 8 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3 + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1 + (hand[4].rank)
    else:
      points = 8 * 15 ** 5 + (hand[1].rank) * 15 ** 4 + (hand[2].rank) * 15 ** 3 + (hand[3].rank) * 15 ** 2 + (hand[4].rank) * 15 ** 1 + (hand[0].rank)

    return points, "Four of a Kind"

  def is_full_house (self, hand):
    #checking first the cards are equal
    start_of_three = -1
    if hand[0].rank == hand[1].rank and hand[1].rank == hand[2].rank:
        if hand[3].rank == hand[4].rank:
            start_of_three = 0
    elif hand[2].rank == hand[3].rank and hand[3].rank == hand[4].rank:
        if hand[0].rank == hand[1].rank:
            start_of_three = 2

    if start_of_three == -1:
        return 0, ''
    
    points = 0
    if start_of_three == 0:
      points = 7 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3 + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1 + (hand[4].rank)
    else:
      points = 7 * 15 ** 5 + (hand[2].rank) * 15 ** 4 + (hand[3].rank) * 15 ** 3 + (hand[4].rank) * 15 ** 2 + (hand[0].rank) * 15 ** 1 + (hand[1].rank)
    return points, "Full House"

  def is_flush (self, hand):
    same_suit = True
    for i in range (len(hand) - 1):
      same_suit = same_suit and (hand[i].suit == hand[i + 1].suit)
    
    if (not same_suit):
      return 0, ''

    points = 6 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3 + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1 + (hand[4].rank)

    return points, "Flush"

  def is_straight (self, hand):
    rank_order = True
    for i in range (len(hand) - 1):
      rank_order = rank_order and (hand[i].rank - hand[i+1].rank == 1)
      
    if (not rank_order):
      return 0, ''

    points = 5 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3 + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1 + (hand[4].rank)

    return points, "Straight"

  def is_three_kind (self, hand):
    
    three_kind_start = -1
    for end_index in range(len(hand) - 2):
        if hand[end_index].rank == hand[end_index + 1].rank and hand[end_index].rank == hand[end_index + 2].rank:
            three_kind_start = end_index
            break
    if three_kind_start == -1:
        return 0, ''
    points = 0
    if three_kind_start == 0:
        points = 4 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3 + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1 + (hand[4].rank)
    elif three_kind_start == 1:
        points = 4 * 15 ** 5 + (hand[1].rank) * 15 ** 4 + (hand[2].rank) * 15 ** 3 + (hand[3].rank) * 15 ** 2 + (hand[0].rank) * 15 ** 1 + (hand[4].rank)
    else:
        points = 4 * 15 ** 5 + (hand[2].rank) * 15 ** 4 + (hand[3].rank) * 15 ** 3 + (hand[4].rank) * 15 ** 2 + (hand[0].rank) * 15 ** 1 + (hand[1].rank)
    return points, "Three of a Kind"

  def is_two_pair (self, hand):
    first_pair = -1
    second_pair = -1
    
    
    if hand[0].rank == hand[1].rank:
        first_pair = 0
    if hand[1].rank == hand[2].rank:
        first_pair = 1
    if hand[2].rank == hand[3].rank:
        second_pair = 2
    if hand[3].rank == hand[4].rank:
        second_pair = 3
    points = 0
    if first_pair == 0 and second_pair == 2:
        points = 3 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3 + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1 + (hand[4].rank)
    elif first_pair == 0 and second_pair == 3:
        points = 3 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3 + (hand[3].rank) * 15 ** 2 + (hand[4].rank) * 15 ** 1 + (hand[2].rank)
    elif first_pair == 1 and second_pair == 3:
        points = 3 * 15 ** 5 + (hand[1].rank) * 15 ** 4 + (hand[2].rank) * 15 ** 3 + (hand[3].rank) * 15 ** 2 + (hand[4].rank) * 15 ** 1 + (hand[0].rank)
    else:
        return 0, ''


    return points, "Two Pair"

  # determine if a hand is one pair
  # takes as argument a list of 5 Card objects
  # returns the number of points for that hand
  def is_one_pair (self, hand):
    
    pair_start = -1
    for i in range (len(hand) - 1):
      if (hand[i].rank == hand[i + 1].rank):
        pair_start = i
        break
    if pair_start == -1:
      return 0, ''

    points = 0
    if pair_start == 0:
      points = 2 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3 + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1 + (hand[4].rank)
    if pair_start == 1:
      points = 2 * 15 ** 5 + (hand[1].rank) * 15 ** 4 + (hand[2].rank) * 15 ** 3 + (hand[0].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1 + (hand[4].rank)
    if pair_start == 2:
      points = 2 * 15 ** 5 + (hand[2].rank) * 15 ** 4 + (hand[3].rank) * 15 ** 3 + (hand[0].rank) * 15 ** 2 + (hand[1].rank) * 15 ** 1 + (hand[4].rank)
    if pair_start == 3:
      points = 2 * 15 ** 5 + (hand[3].rank) * 15 ** 4 + (hand[4].rank) * 15 ** 3 + (hand[0].rank) * 15 ** 2 + (hand[1].rank) * 15 ** 1 + (hand[2].rank)

    return points, 'One Pair'
  def is_high_card (self,hand):
    
    points = 1 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3 + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1 + (hand[4].rank)
    return points, "High Card"
def main():
  # read number of players from stdin
  
  num_players = int(input("Enter the number of players: "))

  # create the Poker object
  game = Poker (num_players)

  # play the game
  game.play()

main()
