class Stone:
    ## constructor
    # @parm TypeOfStone list of stone characteristic
    def __init__(self, TypeOfStone:list) -> None:
        self.TypeOfStone = TypeOfStone

    ## string 
    # make string from stone for print in format
    # 11
    # 11
    # @return string
    def __stdr__(self) -> str:
        text = ""
        for i in range(0, len(self.TypeOfStone), 2):
            text += str(self.TypeOfStone[i]) + str(self.TypeOfStone[i+1]) + "\n"
        return text[:-1]
    
    ## Int Value
    # make number from stone type (not used) 
    # @return int
    def IntValue(self):
        value = 0
        for i in range(len(self.TypeOfStone)):
            value += self.TypeOfStone[i] * 10**(len(self.TypeOfStone)-i-1)
        return value
    ## String Value
    # make string from stone type in format 1111
    # @return string  
    def StringValue(self):
        text = "".join(map(str, self.TypeOfStone))+"\n"
        return text[:-1]
    
    ## Get Type
    # return list of characteristics
    # @return list 
    def GetType (self):
        return self.TypeOfStone
    
    ## ComperationString
    # compare two stone in string form
    # @return bolean
    def ComperationString(self, string):
        if self.StringValue()==string:
            return True
        return False
    ## Comperation
    # compare two stone (this and other) if they have anything in common
    # @param Stone stone class type 
    # @return bolean
    def Comperation(self, Stone):
        if Stone == self:
            return False
        for IdS1, IdS2 in zip (self.TypeOfStone, Stone.GetType()):
            if IdS1 == IdS2:
                return True
        return False

