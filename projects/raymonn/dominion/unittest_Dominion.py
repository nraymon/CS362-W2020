import random
from collections import Counter, OrderedDict, defaultdict
from operator import itemgetter
import re
import unittest
import pandas
import Dominion
import testUtility





class testActionCard(unittest.TestCase):

    #This tests the initialization of an action card
    #This makes an action card called 'actionCard' with a name of 'Testing'
    #a cost of '50', actions of '0', number of cards is '6', '30' buys, and '24' coins
    #This then asserts the initialized values to the variable's properties
    def testInitialization(self):
        actionCard = Dominion.Action_card("Testing", 50, 0, 6, 30, 24)
        self.assertEqual("Testing", actionCard.name)
        self.assertEqual(50, actionCard.cost)
        self.assertEqual(0, actionCard.actions)
        self.assertEqual(6, actionCard.cards)
        self.assertEqual(30, actionCard.buys)
        self.assertEqual(24, actionCard.coins)

    #This tests the use method of the action card class
    #It defines an action card, a player, and a trash array
    #It then adds the defined action card to the player's hand, then uses the action card use method
    #This checks to see whether or not the use method properly romoves itself from the player's hand and
    # makes it into the player.played list
    #This then asserts that player.played does have the card and player.hand does not have the card
    def testUse(self):
        actionCard = Dominion.Action_card("Testing", 50, 0, 6, 30, 24)
        player = Dominion.Player("Tester")
        trash = []
        player.hand.append(actionCard)
        actionCard.use(player, trash)
        self.assertEqual(True, player.played.__contains__(actionCard))
        self.assertEqual(False, player.hand.__contains__(actionCard))

    #This test defines a player and an action card to test the augment method
    #It then also sets up a mini game in order for the player to have some of its properties to be initialized
    #Then asserts the player's 'actions', 'buys', and 'purse' based on happens in the turn
    def testAugment(self):
        player = Dominion.Player("Tester")
        actionCard = Dominion.Action_card("Testing", 50, 0, 6, 30, 24)

        player_names = ["Annie", "*Ben", "*Carla"]

        # number of curses and victory cards
        if len(player_names) > 2:
            nV = 12
        else:
            nV = 8
        nC = -10 + 10 * len(player_names)

        box = testUtility.GetBoxes(nV)

        # Pick 10 cards from box to be in the supply.
        boxlist = [k for k in box]
        random.shuffle(boxlist)
        random10 = boxlist[:10]
        supply = defaultdict(list, [(k, box[k]) for k in random10])

        supply = testUtility.SupplySetup(supply, nV, nC, player_names)

        trash = []

        players = []
        for name in player_names:
            if name[0] == "*":
                players.append(Dominion.ComputerPlayer(name[1:]))
            elif name[0] == "^":
                players.append(Dominion.TablePlayer(name[1:]))
            else:
                players.append(Dominion.Player(name))
        player.turn(players, supply, trash)
        actionCard.augment(player)
        actions = player.actions
        buys = player.buys
        coins = player.purse
        self.assertEqual(actions, player.actions)
        self.assertEqual(buys, player.buys)
        self.assertEqual(coins, player.purse)



class testPlayer(unittest.TestCase):

    #This tests the action balance method from the player class
    #This defines a new player and sets the deck to have 10 copper, 3 estates, and 6 min cards
    #This asserts this deck should have an action balance of -18
    #It then adds more cards that have more than 0 actions according to their class in Dominion.py
    #It adds 20 spy cards, 1000 laboratory cards and 600 cellar cards to put a strain on the deck as well
    # it asserts that the action balance of with those cards added to the deck should be -1
    def testActionBalance(self):
        test = Dominion.Player("balance")
        test.deck = ([Dominion.Copper()] * 10) + ([Dominion.Estate()] * 3) + ([Dominion.Mine()] * 6)
        self.assertEqual(-18, test.action_balance())
        test.deck += [Dominion.Spy()] * 20
        test.deck += [Dominion.Laboratory()] * 1000
        test.deck += [Dominion.Cellar()] * 600
        self.assertEqual(-1, test.action_balance())

    #This tests the calcpoints method of the player class that adds together all the victory card values
    # in the player's deck. It calculates the victory points of a new player's deck, a new player's deck
    # with a province added and asserts them to be equal to '3' and '9' respectively as well as adding 11
    # province cards to the player's deck which is asserted to be equal to 75
    def testCalcpoints(self):
        test = Dominion.Player("calc")
        self.assertEqual(3, test.calcpoints())
        test.deck += [Dominion.Province()] * 1
        self.assertEqual(9, test.calcpoints())
        test.deck += [Dominion.Province()] * 11
        self.assertEqual(75, test.calcpoints())

    #this tests the draw method of the player class by defining a new character and checking the amount of
    # cards in the player's hand before and after the player draws a card.
    # a new player should have 5 cards at the start then 6 cards once it draws a card
    def testDraw(self):
        test = Dominion.Player("draw")
        self.assertEqual(5, len(test.hand))
        test.draw(dest=None)
        self.assertEqual(6, len(test.hand))

    #This tests the card summary function of the player class
    # this defines a new player and asserts what cards the player should have at the start of a game
    # and what cards the player should have after adding a province card and the number of points
    # the player should have
    def testSumm(self):
            test = Dominion.Player("summ")
            self.assertEqual({'Copper': 7, 'Estate': 3, 'VICTORY POINTS': 3}, test.cardsummary())
            test.deck += [Dominion.Province()] * 1
            self.assertEqual({'Copper': 7, 'Estate': 3, 'Province': 1, 'VICTORY POINTS': 9}, test.cardsummary())

    #This test also sets up a mini version of the game by creating a list of the players and setting up
    # the game's supply. It start off by asserting when there are 0 province cards, the game should be over
    #When there are province cards in the supply it asserts that game over should be false
    #It then sets the number of copper, silver, gold, and estate cards to 0 and asserts that the game
    # should be over with 3 or more supply cards being gone.
    def testOver(self):
        player_names = ["Annie", "*Ben", "*Carla"]

        # number of curses and victory cards
        if len(player_names) > 2:
            nV = 12
        else:
            nV = 8
        nC = -10 + 10 * len(player_names)

        box = testUtility.GetBoxes(nV)

        supply_order = testUtility.Supplies()

        # Pick 10 cards from box to be in the supply.
        boxlist = [k for k in box]
        random.shuffle(boxlist)
        random10 = boxlist[:10]
        supply = defaultdict(list, [(k, box[k]) for k in random10])

        supply = testUtility.SupplySetup(supply, nV, nC, player_names)

        supply["Province"] = [Dominion.Province()] * 0
        self.assertEqual(True, Dominion.gameover(supply))
        supply["Province"] = [Dominion.Province()] * 2
        self.assertEqual(False, Dominion.gameover(supply))
        supply["Copper"] = [Dominion.Copper()] * 0
        supply["Silver"] = [Dominion.Silver()] * 0
        supply["Gold"] = [Dominion.Gold()] * 0
        supply["Estate"] = [Dominion.Estate()] * 0
        supply["Duchy"] = [Dominion.Duchy()] * nV
        supply["Province"] = [Dominion.Province()] * nV
        supply["Curse"] = [Dominion.Curse()] * nC
        self.assertEqual(True, Dominion.gameover(supply))
