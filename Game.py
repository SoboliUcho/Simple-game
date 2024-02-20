
import argparse
from itertools import product
import math

from stone import *
from players import *
from loger import *


class Game:
    ## constructor
    # @parm dimensionOfGame int size of game field
    # @parm dificulty int 0 is random play, 1 is AI play
    # @parm output bolean for logger True - write to file
    # @parm path path for logger file defaul curent working
    def __init__(self, dimensionOfGame, dificulty, output=False, path = "") -> None:
        self.dimensionOfGame = dimensionOfGame
        self.dificulty = dificulty
        self.logger = MyLogger(output, path)
        # read arument
        parser = argparse.ArgumentParser()
        parser.add_argument("--player1", action="store_true",default=False)
        argument = parser.parse_args()
        self.player1 = argument.player1

        # make board
        self.board= Board(self.dimensionOfGame)

        # make stones for placing 
        self.freeStones = []
        self.MakeStones(self.dimensionOfGame)
        self.gameStatus = ["computer wins","player wins", "no winner","playing"]
        self.curentGameStatus = 3

        # define players order and make players
        if self.player1:
            self.players = [PcPlayer(self), Player(self)]
        else:
            self.players = [Player(self),PcPlayer(self)]
            # self.players = [PcPlayer(self), PcPlayer(self)]

    ## Print Free Stones
    # print free stones to console
    def PrintFreeStones(self):
        self.logger.Log("Free stones are:")
        for stone in self.freeStones:
            self.logger.Log(stone)

    def GetFreeStones(self):
        return self.freeStones
    
    def ChangeGameStatus(self, number):
        self.curentGameStatus = number
    
    def GetBoard(self):
        return self.board
    
    def GetDificulty(self):
        return self.dificulty
    
    def GetLoger(self):
        return self.logger
    
    ## Make Stones
    # make all cobnination of stones characteristic for game
    # @param nStone int number os stone to make
    def MakeStones(self, nStone):
        # for i in range (2):
        #     for j in range(2):
        #         for k in range(2):
        #             for l in range (2):
        #                 self.freeStones.append(Stone([i,j,k,l]))
        for combination in product([0, 1], repeat=nStone):
            self.freeStones.append(Stone(list(combination)))
    
    ## Status Anouncment
    # print game status 
    def StatusAnouncment(self):
        data = {
            "status":self.gameStatus[self.curentGameStatus]
        }
        self.logger.Log (data)
        # print (self.board)
    
    ## Play Game
    # game engine
    # @return int 0 of game end noramly else 1 
    def PlayGame(self):
        nPlayers = len(self.players)
        # the game runs as long as there are free stones, number of stones is same as number of fields
        while len(self.freeStones)>0:
            # player rotation
            for i in range (nPlayers):
                # checking the number of stones, with two player it shouldn't happen but for sure
                if len(self.freeStones)==0:
                    self.ChangeGameStatus(3)
                    self.StatusAnouncment()
                    return 0
                
                currentPlayer = self.players[i]
                nextPlayer = self.players[(i + 1) % nPlayers]

                # requests a stone from the next player
                try:
                    stone = nextPlayer.SelectStone()
                except ValueError as e:
                    self.logger.Log (e)
                    return 1
                
                # gives stone to current player, requests location
                try:
                    location = currentPlayer.GetStone(stone)
                except ValueError as e:
                    self.logger.Log (e)
                    return 1
                
                # placing ston on board
                try:
                    result = self.board.PlaceStone(stone,location)
                except ValueError as e:
                    self.logger.Log (e)
                    return 1
                # check game status 
                if self.board.CheckBoard():
                    self.players[i].winner()
                    self.StatusAnouncment()
                    return 0
                # remove used stone from free stones
                self.freeStones.remove(stone)
                self.StatusAnouncment()

        # if there isnt free stone end game with no winner status
        self.ChangeGameStatus(4)
        self.StatusAnouncment()
        # self.end()
        return 0
    
class Board:
    ## constructor 
    # @param size x and y dimension of game field
    def __init__(self, size) -> None:
        self.size=size
        self.field = [[None for _ in range(size)] for _ in range(size)]
    
    ## __str__
    # convert Board to string for printing
    # @return string
    def __str__(self) -> str:
        text = ""
        for line in self.field:
            # first two number from stone or ** if there isnt stone
            for elm in line:
                if elm != None:
                    text += ''.join(map(str, elm.GetType()[:2]),)+ " "
                else:
                    text +="** "
            text += "\n"
            # seconf two number from stone or ** if there isnt stone
            for elm in line:
                if elm != None:
                    text += ''.join(map(str, elm.GetType()[2:]),)+ " "
                else:
                    text += "** "
            text += "\n\n"
            # text+=' '.join(map(str, line),)+"\n"
        return text
    
    ## PlaceStone
    # place stone to game field
    # @param newStone Stone class element to be inserted to board
    # @param pozition int reprezation of pozicion
    # return bolean
    def PlaceStone(self, newStone:Stone, pozition:int):
        # separete x and y pozition base on size of board
        divisor = (int(math.log10(self.size)) + 1)*10
        xPozition = pozition // divisor -1
        yPozition = pozition % divisor -1
        # print (xPozition,yPozition)
        # check condition for placing stone
        if xPozition >= self.size or yPozition >= self.size:
            raise ValueError ("Error: Placing stone out of desk")
        if self.field[xPozition][yPozition] != None:
            raise ValueError("Error: Field already contains a stone")
        
        # if coordinates are correct place stone
        self.field[xPozition][yPozition] = newStone
        return True

    ## Check Line
    #@parm stone Stone class element 
    # checking list of stone if there are four stones with at least one same characteristic
    # @return bolean
    def CheckLine(self, stones):
        for i in range (self.size):
            if stones[i] is None:
                return False
            for j in range (i+1,self.size):
                if stones[j] is None:
                    return False
                if stones[i].Comperation(stones[j])==False:
                    return False
        return True
    
    ## Check Board
    # checking all board if there is row/column/diagona of four stones with at least one same characteristic
    # @return bolean
    def CheckBoard(self):
        # row
        for line in self.field:
            if self.CheckLine(line):
                return True

        # column
        for i in range(self.size):
            column = []
            for j in range(self.size):
                column.append(self.field[j][i])
            if self.CheckLine(column):
                return True
            
        #diagonal
        diagonal1=[]
        diagonal2=[]
        for i in range(self.size):
            diagonal1.append(self.field[i][i])
            diagonal2.append(self.field[i][-(i+1)])

        if self.CheckLine(diagonal1) or self.CheckLine(diagonal2):
            return True
        return False
    
    ## check Board2
    # "diferent" implementation of checkBoard, in some cases is faster, it was experimet (not used)
    # @return bolean
    def checkBoard2(self):
        diagonal1=[]
        diagonal2=[]
        for i in range(self.size):
            # row
            if self.checkLine(self.field[i]):
                return True
            # column
            column = []
            for j in range(self.size):
                column.append(self.field[j][i])
            if self.checkLine(column):
                return True
            
            diagonal1.append(self.field[i][i])
            diagonal2.append(self.field[i][-(i+1)])
            
        #diagonal
        if self.checkLine(diagonal1) or self.checkLine(diagonal2):
            return True
        return False
    
    ## Get Game Board
    def GetGameBoard(self):
        return self.field
    
    ## Get Size
    def GetSize(self):
        return self.size


def main():
    NewGame = Game(4, 1)
    return NewGame.PlayGame()

if __name__=="__main__": 
    main() 