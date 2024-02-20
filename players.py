import math
import random
from stone import Stone
import json


class Player:
    def __init__(self, game) -> None:
        self.game = game
        self.type = 1
        self.logger = game.GetLoger()

    
    ## GetStone
    # selecting stone pozition
    # @param Stone Stone class object
    # @return int pozicion of stone
    def GetStone(self, Stone:Stone):
        #output of the given stone
        data = {"chosen_stone":Stone.StringValue()}
        self.logger.Log(data)

        #input pozition
        pozition = input() #{"stone":"1111", "field":12}
        self.logger.SaveLog(pozition)
        pozition = json.loads(pozition)

        #check if return stone is correct 
        if pozition["stone"] == Stone.StringValue():
            return pozition["field"]
        raise ValueError("Error: Trying placing non chosen stone")
    
    ## SelectStone
    # return select stone to game engine
    # @return Stone if is in free stones
    def SelectStone(self):
        # input stone and decode 
        stoneInput = input() #{ "chosen_stone": "0010" }
        self.logger.SaveLog(stoneInput)
        stoneInput = json.loads(stoneInput)

        # find selected stone in free stones (for better manipulation)
        for stone in self.game.GetFreeStones():
            if stone.ComperationString(stoneInput["chosen_stone"]):
                return stone
        raise ValueError ("Error: chosen stone is not available")

    def winner(self):
        self.game.ChangeGameStatus(self.type)

class PcPlayer(Player):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.type = 0
        self.board = self.game.GetBoard()
        self.dificulty = self.game.GetDificulty()
    ## Get Stone
    # select dificulty of pc player random / ai 
    # @param Stone
    # @return int
    def GetStone(self, stone:Stone):
        if self.dificulty == 0:
            response =  self.GetStoneRandom()
        if self.dificulty == 1:
            response = self.GetStoneAi(stone)

        data = {
            "stone":stone.StringValue(),
            "field":response
        }
        self.logger.Log(data)
        return response
    
    ## Get Stone Random
    # random placing stone
    # @return int pozition
    def GetStoneRandom(self):
        # print ("random")
        size = self.board.GetSize()
        # until it finds a free field
        while True:
            x = random.randint(0,size-1)
            y = random.randint(0,size-1)
            # if field is free return pozition
            if self.board.field[y][x]==None:
                multiple = (int(math.log10(size)) + 1)*10
                pozition = (x+1)*multiple+y+1
                return pozition
    
    ## Get Stone Ai
    # smart placing stone 
    # selecting stone pozition
    # @param Stone Stone class object
    # @return int pozicion of stone
    def GetStoneAi(self, Stone:Stone):
        size = self.board.GetSize()
        gameField = self.board.GetGameBoard()
        # for every column
        for y in range (size):
            # for every row
            for x in range(size):
                # if field is free
                if gameField[y][x]==None:
                    # find row with stone with same characteristic
                    for stoneOnBoard in gameField[y]:
                        if stoneOnBoard is not None:
                            # print (stoneOnBoard)
                            if Stone.Comperation(stoneOnBoard):
                                # print ("line true")
                                return self.pozicion(y,x)
                            else:
                                break
                     # find column with stone with same characteristic
                    for i in range(size):
                        if gameField[i][x] is not None:
                            # print (gameField[i][x])
                            if Stone.Comperation(gameField[i][x]):
                                # print ("colum true")
                                return self.pozicion(y, x)
                            else:
                                break
        # if there arent any same stone place it random
        return self.GetStoneRandom()
    
    ## pozicion
    # counting pozition as numeber 
    # @param xPozition int x pozition of stone
    # @param yPozition int y pozition of stone
    # @return int 
    def pozicion(self, xPozition, yPozition):
        size = self.board.GetSize()
        multiple = (int(math.log10(size)) + 1)*10
        pozition = (xPozition+1)*multiple+(yPozition+1)
        return pozition
    
    ## SelectStone
    # select random stone from free stones
    # @return Stone
    def SelectStone(self):
        stone = random.choice(self.game.GetFreeStones())
        return stone
