import json
from collections.abc import Iterable
from datetime import datetime

class MyLogger:
    ## constructor
    # @parm output bolean write to file - true default false
    # @parm path path for logger file defaul curent working
    def __init__(self, output=False, path = "") -> None:
        self.output = output
        self.file = None
        if self.output:
            self.OpenFile(path)

    ## destructor
    # write line to file and close it
    def __del__(self):
        if self.file:
            self.file.write("\n"+10*"-" +"\n")
            self.CloseFile()

    ## Log
    # logging function - write data to output
    # @param data can be anything
    def Log(self, data):
        # if data is Iterable (it means array) convert it to json
        if isinstance(data, Iterable):
            data = self.JsonEncode(data)
        # else conver to string
        else:
            data = str(data)
        #write data to file or concole
        if self.output:
            self.LogFileWrite(data)
        else:
            self.ConsoleLogWrite(data)
        return 0
    
    ## Save Log
    # write data to only to file
    # @param data can be anything
    def SaveLog(self, data):
        # if data is Iterable (it means array) convert it to json
        if isinstance(data, Iterable):
            data = self.JsonEncode(data)
        # else conver to string
        else:
            data = str(data)
        if self.output:
            self.LogFileWrite(data)

    ## Json Encode
    # encode data to JSON
    # @param data can be anything
    # @return string in JSON format
    def JsonEncode(self, data):
        return json.dumps(data)
    
    ## Open File
    # open file (or make it if doesnt exist), write curent date to it
    # @param path string path for file 
    def OpenFile(self, path):
        # edit path
        if len(path)>0 and path[-1]!= "/":
            path += "/"
        path += "game.log"
        self.file = open(path,"a+",encoding="utf-8")
        self.file.write (str(datetime.now())+"\n\n")

    ## Close file
    def CloseFile(self):
        self.file.close()

    ## Log File Write
    # write string to file and add new line
    # @param string string
    def LogFileWrite(self, string:str):
        self.file.write(string +"\n")

    ## Console Log Write
    # write string to console
    # @param string string
    def ConsoleLogWrite(self, string:str):
        print(string)