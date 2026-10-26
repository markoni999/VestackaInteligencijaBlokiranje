from asyncio.windows_events import NULL
import functools
from msilib.schema import CheckBox
from multiprocessing.sharedctypes import Value
import time
import tkinter
from typing import List
import numpy as np
from tkinter import *
from collections import *
import copy

frameRed=NULL
greenXLeft=NULL
blueXLeft=NULL
frameYellow=NULL
greenOLeft=NULL
blueOLeft=NULL

class Board:
    
    def __init__(self,board, height, width, wallNum, pawnPosX1, pawnPosX2, pawnPosO1, pawnPosO2):

        self.board=board
        self.height=height
        self.width=width
        self.pawnPosX1=pawnPosX1
        self.pawnPosX2=pawnPosX2
        self.pawnPosO1=pawnPosO1
        self.pawnPosO2=pawnPosO2
        self.startPosX1=pawnPosX1
        self.startPosX2=pawnPosX2
        self.startPosO1=pawnPosO1
        self.startPosO2=pawnPosO2
        self.greenWallNumX=wallNum
        self.greenWallNumO=wallNum
        self.blueWallNumX=wallNum
        self.blueWallNumO=wallNum
        self.X1Id=0
        self.X2Id=0
        self.O1Id=0
        self.O2Id=0
        self.currentPlayer='X'
        self.wallPlayed=False

    def possibleDirection(self, startPos:list, endPosition:list ):

        #da li je krajnje polje zauzeto drugim pesakom
        if (endPosition==self.pawnPosX1) or (endPosition==self.pawnPosX2) or (endPosition==self.pawnPosO1) or (endPosition==self.pawnPosO2):
            return False
        #levo-desno
        
        if startPos[0]==endPosition[0]:
            if startPos[1]> endPosition[1]:
                if ("left" in self.board[startPos[0]-1][startPos[1]-1]) or ("left" in self.board[startPos[0]-1][startPos[1]-2]) :
                    return False
                if np.sqrt((endPosition[0]-startPos[0])**2+(endPosition[1]-startPos[1])**2)==1:  #provera da li moze da se krece jedno polje
                    if(([endPosition[0],endPosition[1]-1]) in (self.pawnPosO1, self.pawnPosO2, self.pawnPosX1, self.pawnPosX2))\
                        or (([endPosition[0],endPosition[1]]) in ( self.startPosO1, self.startPosO2, self.startPosX1, self.startPosX2)):
                        return True
                    else:
                        return False
            if startPos[1]< endPosition[1]:
                if ("right" in self.board[startPos[0]-1][startPos[1]-1]) or ("right" in self.board[startPos[0]-1][startPos[1]]) :
                    return False
                if np.sqrt((endPosition[0]-startPos[0])**2+(endPosition[1]-startPos[1])**2)==1:  #provera da li moze da se krece jedno polje
                    if(([endPosition[0],endPosition[1]+1]) in (self.pawnPosO1, self.pawnPosO2, self.pawnPosX1, self.pawnPosX2))\
                        or (([endPosition[0],endPosition[1]]) in ( self.startPosO1, self.startPosO2, self.startPosX1, self.startPosX2)):
                        return True
                    else:
                        return False
        #gore-dole
        if startPos[1]==endPosition[1]:
            if startPos[0]< endPosition[0]:
                if ("down" in self.board[startPos[0]-1][startPos[1]-1]) or ("down" in self.board[startPos[0]][startPos[1]-1]) :
                    return False
                if np.sqrt((endPosition[0]-startPos[0])**2+(endPosition[1]-startPos[1])**2)==1:  #provera da li moze da se krece jedno polje
                    if(([endPosition[0]+1,endPosition[1]]) in (self.pawnPosO1, self.pawnPosO2, self.pawnPosX1, self.pawnPosX2))\
                        or (([endPosition[0],endPosition[1]]) in ( self.startPosO1, self.startPosO2, self.startPosX1, self.startPosX2)):
                        return True
                    else:
                        return False
            if startPos[0]> endPosition[0]:
                if ("up" in self.board[startPos[0]-1][startPos[1]-1]) or ("up" in self.board[startPos[0]-2][startPos[1]-1]) :
                    return False
                if np.sqrt((endPosition[0]-startPos[0])**2+(endPosition[1]-startPos[1])**2)==1:  #provera da li moze da se krece jedno polje
                    if(([endPosition[0]-1,endPosition[1]]) in (self.pawnPosO1, self.pawnPosO2, self.pawnPosX1, self.pawnPosX2))\
                        or (([endPosition[0],endPosition[1]]) in ( self.startPosO1, self.startPosO2, self.startPosX1, self.startPosX2)):
                        return True
                    else:
                        return False
        #dijagonalno
        #gore levo
        if ((startPos[0] > endPosition[0]) and (startPos[1] > endPosition[1])):
            if ("up" in self.board[startPos[0]-1][startPos[1]-1]) or ("left" in self.board[startPos[0]-1][startPos[1]-1]) or ("down" in self.board[startPos[0]-2][startPos[1]-2]) or ("right" in self.board[startPos[0]-2][startPos[1]-2]):
                    return False
        #dole levo
        if ((startPos[0] < endPosition[0]) and (startPos[1] > endPosition[1])):
            if ("down" in self.board[startPos[0]-1][startPos[1]-1]) or ("left" in self.board[startPos[0]-1][startPos[1]-1]) or ("up" in self.board[startPos[0]][startPos[1]-2]) or ("right" in self.board[startPos[0]][startPos[1]-2]):
                    return False
        #gore desno            
        if ((startPos[0] > endPosition[0]) and (startPos[1] < endPosition[1])):
            if ("up" in self.board[startPos[0]-1][startPos[1]-1]) or ("right" in self.board[startPos[0]-1][startPos[1]-1]) or ("down" in self.board[startPos[0]-2][startPos[1]]) or ("left" in self.board[startPos[0]-2][startPos[1]]):
                    return False
        #dole desno
        if ((startPos[0] < endPosition[0]) and (startPos[1] < endPosition[1])):
            if ("down" in self.board[startPos[0]-1][startPos[1]-1]) or ("right" in self.board[startPos[0]-1][startPos[1]-1]) or ("up" in self.board[startPos[0]][startPos[1]]) or ("left" in self.board[startPos[0]][startPos[1]]):
                    return False
        return True

    def possibleDirection2(self, startPos:list, endPosition:list ):
        #levo-desno
        
        if startPos[0]==endPosition[0]:
            if startPos[1]> endPosition[1]:
                if ("left" in self.board[startPos[0]-1][startPos[1]-1]) or ("left" in self.board[startPos[0]-1][startPos[1]-2]) :
                    return False
            if startPos[1]< endPosition[1]:
                if ("right" in self.board[startPos[0]-1][startPos[1]-1]) or ("right" in self.board[startPos[0]-1][startPos[1]]) :
                    return False
        
        #gore-dole
        if startPos[1]==endPosition[1]:
            if startPos[0]< endPosition[0]:
                if ("down" in self.board[startPos[0]-1][startPos[1]-1]) or ("down" in self.board[startPos[0]][startPos[1]-1]) :
                    return False
            if startPos[0]> endPosition[0]:
                if ("up" in self.board[startPos[0]-1][startPos[1]-1]) or ("up" in self.board[startPos[0]-2][startPos[1]-1]) :
                    return False
        #dijagonalno
        #gore levo
        if ((startPos[0] > endPosition[0]) and (startPos[1] > endPosition[1])):
            if ("up" in self.board[startPos[0]-1][startPos[1]-1]) or ("left" in self.board[startPos[0]-1][startPos[1]-1]) or ("down" in self.board[startPos[0]-2][startPos[1]-2]) or ("right" in self.board[startPos[0]-2][startPos[1]-2]):
                    return False
        #dole levo
        if ((startPos[0] < endPosition[0]) and (startPos[1] > endPosition[1])):
            if ("down" in self.board[startPos[0]-1][startPos[1]-1]) or ("left" in self.board[startPos[0]-1][startPos[1]-1]) or ("up" in self.board[startPos[0]][startPos[1]-2]) or ("right" in self.board[startPos[0]][startPos[1]-2]):
                    return False
        #gore desno            
        if ((startPos[0] > endPosition[0]) and (startPos[1] < endPosition[1])):
            if ("up" in self.board[startPos[0]-1][startPos[1]-1]) or ("right" in self.board[startPos[0]-1][startPos[1]-1]) or ("down" in self.board[startPos[0]-2][startPos[1]]) or ("left" in self.board[startPos[0]-2][startPos[1]]):
                    return False
        #dole desno
        if ((startPos[0] < endPosition[0]) and (startPos[1] < endPosition[1])):
            if ("down" in self.board[startPos[0]-1][startPos[1]-1]) or ("right" in self.board[startPos[0]-1][startPos[1]-1]) or ("up" in self.board[startPos[0]][startPos[1]]) or ("left" in self.board[startPos[0]][startPos[1]]):
                    return False
        return True

    def possiblePawnMoves(self, startPos:list):
        moveList=[]
        moveList.append( [startPos[0]+2,startPos[1]])
        moveList.append( [startPos[0]+1,startPos[1]+1])
        moveList.append( [startPos[0]+1,startPos[1]-1])
        moveList.append( [startPos[0],startPos[1]+2])
        moveList.append( [startPos[0],startPos[1]-2])
        moveList.append( [startPos[0]-1,startPos[1]+1])
        moveList.append( [startPos[0]-1,startPos[1]-1])
        moveList.append( [startPos[0]-2,startPos[1]])

        moveList.append( [startPos[0]+1,startPos[1]])
        moveList.append( [startPos[0]-1,startPos[1]])
        moveList.append( [startPos[0],startPos[1]+1])
        moveList.append( [startPos[0],startPos[1]-1])

        return moveList

    def isLegal(self, player, pawnNum, move: list, wallColor, wallPosition):
        
        #provera da li je odgovarajuca distanca izmedju izvora i odtedista pesaka (2, -2 ili sqrt(2) i -sqrt(2) za dijagonalni potez) 
        if pawnNum not in [1,2]:
            return False
        if player not in ["X", "O"]:
            return False
        if player=="X":
            if pawnNum==1:
                playerPos=[self.pawnPosX1[0], self.pawnPosX1[1]]
                if np.sqrt((move[0]-self.pawnPosX1[0])**2+(move[1]-self.pawnPosX1[1])**2) not in [np.sqrt(2),2]:
                    return False 
                
                                       #distanca = sqrt((X2-X1)^2+(Y2-Y1)^2)     (X2,Y2) - koordinate odredista     (X1,Y1) - koordinate izvora

            if pawnNum==2:
                playerPos=[self.pawnPosX2[0], self.pawnPosX2[1]]
                if np.sqrt((move[0]-self.pawnPosX2[0])**2+(move[1]-self.pawnPosX2[1])**2) not in [np.sqrt(2),2]:           
                    return False


        if player=="O":
            if pawnNum==1:
                playerPos=[self.pawnPosO1[0], self.pawnPosO1[1]]
                if np.sqrt((move[0]-self.pawnPosO1[0])**2+(move[1]-self.pawnPosO1[1])**2) not in [np.sqrt(2),2]:                   
                    return False

            if pawnNum==2:
                playerPos=[self.pawnPosO2[0], self.pawnPosO2[1]]
                if np.sqrt((move[0]-self.pawnPosO2[0])**2+(move[1]-self.pawnPosO2[1])**2) not in [np.sqrt(2),2]:
                    return False
        

        if self.possibleDirection(playerPos, move)==False:
            return False
        
        x=wallPosition[0]
        y=wallPosition[1]
        if (x > self.height-1) or (y>self.width-1):
            return False
        if wallColor=="blue":
            
            if "down" in self.board[wallPosition[0]-1][wallPosition[1]-1]:
                return False
            if "down" in self.board[wallPosition[0]-1][wallPosition[1]]:
                return False
            if "up" in self.board[wallPosition[0]][wallPosition[1]-1]:  
                return False
            if "up" in self.board[wallPosition[0]][wallPosition[1]]:
                return False
            if ("right" in self.board[wallPosition[0]-1][wallPosition[1]-1]) and ("right" in self.board[wallPosition[0]][wallPosition[1]-1]):
                return False
        if wallColor=="green":
            if "right" in self.board[wallPosition[0]-1][wallPosition[1]-1]:
                return False
            if "left" in self.board[wallPosition[0]-1][wallPosition[1]]:
                return False
            if "right" in self.board[wallPosition[0]][wallPosition[1]-1]:  
                return False
            if "left" in self.board[wallPosition[0]][wallPosition[1]]:
                return False
            if ("down" in self.board[wallPosition[0]-1][wallPosition[1]-1]) and ("down" in self.board[wallPosition[0]-1][wallPosition[1]]):
                return False
        return True

    def isEnd(self):
        if (self.pawnPosX1==self.startPosO1) or (self.pawnPosX1==self.startPosO2) or (self.pawnPosX2==self.startPosO1) or (self.pawnPosX2==self.startPosO2):
            return "X"
        if (self.pawnPosO1==self.startPosX1) or (self.pawnPosO1==self.startPosX2) or (self.pawnPosO2==self.startPosX1) or (self.pawnPosO2==self.startPosX2):
            return "O"
        return False

    def wallMove(self, wallColor, wallPosition: list): #indeksi od 1 u pozivu funkcije!!!
        if not (1<=wallPosition[0]<=(self.height-1)):
            print("nevalidan potez")
            return
        if not (1<=wallPosition[1]<=(self.width-1)):
            print("nevalidan potez")
            return 
        if wallColor=="blue":
            self.board[wallPosition[0]-1][wallPosition[1]-1].append("down")  
            self.board[wallPosition[0]-1][wallPosition[1]].append("down") 
            self.board[wallPosition[0]][wallPosition[1]-1].append("up")  
            self.board[wallPosition[0]][wallPosition[1]].append("up")
            if self.currentPlayer=="O":
                self.blueWallNumO-=1
            else:
                self.blueWallNumX-=1

        if wallColor=="green":
            self.board[wallPosition[0]-1][wallPosition[1]-1].append("right")  
            self.board[wallPosition[0]-1][wallPosition[1]].append("left") 
            self.board[wallPosition[0]][wallPosition[1]-1].append("right")  
            self.board[wallPosition[0]][wallPosition[1]].append("left") 
            if self.currentPlayer=="O":
                self.greenWallNumO-=1
            else:
                self.greenWallNumX-=1

    def playMove(self, player, pawnNum, move: list, wallColor, wallPosition): #indeksi od 1 u pozivu funkcije!!!
        if  self.isLegal( player, pawnNum, move, wallColor, wallPosition)==False:
            print("nevalidan potez")
            
        
        if player=="X":
            #self.currentPlayer='O'
            self.wallMove(wallColor,wallPosition)  
            if wallColor=="green":       #wallMove smanjuje broj zidiva sto ove nije pogodno s obzirom da se ova f-ja koristi i kod pravljenja liste leganih poteza.
                self.greenWallNumX+=1    #zato se broj zidova vraca u prvobitno stanje
            else:
                self.blueWallNumX+=1
            if pawnNum==1:
                self.pawnPosX1=move
            else:
                self.pawnPosX2=move
           
            #self.currentPlayer='O'

        if player=="O":
            #self.currentPlayer='X'
            self.wallMove(wallColor,wallPosition)
            if wallColor=="green":
                self.greenWallNumO+=1
            else:
                self.blueWallNumO+=1
            if pawnNum==1:
                self.pawnPosO1=move
            else:
                self.pawnPosO2=move
        
    def newState(self, player, pawnNum, move: list, wallColor, wallPosition):

        newTabla=copy.deepcopy(self)
        newTabla.playMove( player, pawnNum, move, wallColor, wallPosition)
        return newTabla 

    def possitionList(self):
        colors=["green", "blue"]
        SquareNum=self.width*self.height
        legalWallList=[]
        legalPawnList=[]
        finalList=[]

        if(self.currentPlayer=="O"):
            o1=self.possiblePawnMoves(self.pawnPosO1)
            o2=self.possiblePawnMoves(self.pawnPosO2)           
            for i in range(12):
                if self.isPawnLegalComplete(self.currentPlayer, 1 , o1[i]):
                    legalPawnList.append([self.currentPlayer, 1 , o1[i]])
                if self.isPawnLegalComplete(self.currentPlayer, 2 , o2[i]):
                    legalPawnList.append([self.currentPlayer, 2 , o2[i]])

            if(self.blueWallNumO>0 and self.greenWallNumO>0):
                for j in range(2):
                    for i in range (self.width+1, self.width+SquareNum):
                        if self.isWallLegalComplete([i//(self.width) , i%(self.width)],colors[j]):
                            legalWallList.append([colors[j], [i//(self.width), i%(self.width)]])
            elif(self.blueWallNumO>0):
                j=1
                for i in range (self.width+1, self.width+SquareNum):
                    if self.isWallLegalComplete([i//(self.width) , i%(self.width)],colors[j]):
                        legalWallList.append([colors[j], [i//(self.width), i%(self.width)]])
            elif(self.greenWallNumO>0):
                j=0
                for i in range (self.width+1, self.width+SquareNum):
                    if self.isWallLegalComplete([i//(self.width) , i%(self.width)],colors[j]):
                        legalWallList.append([colors[j], [i//(self.width), i%(self.width)]])

        if(self.currentPlayer=="X"): 
            x1=self.possiblePawnMoves(self.pawnPosX1)
            x2=self.possiblePawnMoves(self.pawnPosX2)           
            for i in range(12):
                if self.isPawnLegalComplete(self.currentPlayer, 1 , x1[i]):
                    legalPawnList.append([self.currentPlayer, 1 , x1[i]])
                if self.isPawnLegalComplete(self.currentPlayer, 2 , x2[i]):
                    legalPawnList.append([self.currentPlayer, 2 , x2[i]])

            if(self.blueWallNumX>0 and self.greenWallNumX>0):
                for j in range(2):
                    for i in range (self.width+1, self.width+SquareNum):
                        if self.isWallLegalComplete([i//(self.width) , i%(self.width)],colors[j]):
                            legalWallList.append([colors[j], [i//(self.width), i%(self.width)]])
            elif(self.blueWallNumX>0):
                j=1
                for i in range (self.width+1, self.width+SquareNum):
                    if self.isWallLegalComplete([i//(self.width) , i%(self.width)],colors[j]):
                        legalWallList.append([colors[j], [i//(self.width), i%(self.width)]])
            elif(self.greenWallNumX>0):
                j=0
                for i in range (self.width+1, self.width+SquareNum):
                    if self.isWallLegalComplete([i//(self.width) , i%(self.width)],colors[j]):
                        legalWallList.append([colors[j], [i//(self.width), i%(self.width)]])

        for i in range(len(legalPawnList)):
            for j in range(len(legalWallList)):
                finalList.append(self.newState(legalPawnList[i][0],legalPawnList[i][1],legalPawnList[i][2], legalWallList[j][0], legalWallList[j][1]))
        return finalList

    def isNextTo(self,firstSquare:list, secondSquare:list):
        x=firstSquare[0]-1
        y=firstSquare[1]-1
        if(firstSquare[1]==secondSquare[1]): 
            if (firstSquare[0]==(secondSquare[0]+1) and ("up" not in self.board[x][y])) or (firstSquare[0]==(secondSquare[0]-1) and ("down" not in self.board[x][y])):
                return True
        if(firstSquare[0]==secondSquare[0]): 
            if (firstSquare[1]==(secondSquare[1]+1) and ("left" not in self.board[x][y])) or (firstSquare[1]==(secondSquare[1]-1) and ("right" not in self.board[x][y])):
                return True
        return False

    def doesWallConnect(self,wallPosition: list, wallColor):

        counterList=[0,0,0]
        if (self.pawnPosO1[0]<self.height+1) and (self.pawnPosO1[1]<self.width+1):
            if(wallColor=="green"):
                if "up" in (self.board[wallPosition[0]-1][wallPosition[1]-1]) or ("up" in self.board[wallPosition[0]-1][wallPosition[1]]):
                    counterList[0]=1
                if (wallPosition[0]-2>=0) and ("right" in self.board[wallPosition[0]-2][wallPosition[1]-1]):
                    counterList[0]=1
                if "down" in (self.board[wallPosition[0]-1][wallPosition[1]-1]) or ("down" in self.board[wallPosition[0]-1][wallPosition[1]]):
                    counterList[1]=1
                if "down" in (self.board[wallPosition[0]][wallPosition[1]-1]) or ("down" in self.board[wallPosition[0]][wallPosition[1]]): 
                    counterList[2]=1
                if  (wallPosition[0]+1<self.height) and ("right" in self.board[wallPosition[0]+1][wallPosition[1]-1]):
                    counterList[2]=1
            if(wallColor=="blue"):
                if "left" in (self.board[wallPosition[0]-1][wallPosition[1]-1]) or ("left" in self.board[wallPosition[0]][wallPosition[1]-1]):
                    counterList[0]=1
                if (wallPosition[1]-2>=0) and ("down" in self.board[wallPosition[0]-1][wallPosition[1]-2]):
                    counterList[0]=1
                if "right" in (self.board[wallPosition[0]-1][wallPosition[1]-1]) or ("right" in self.board[wallPosition[0]][wallPosition[1]-1]):
                    counterList[1]=1
                if "right" in (self.board[wallPosition[0]-1][wallPosition[1]]) or ("right" in self.board[wallPosition[0]][wallPosition[1]]): 
                    counterList[2]=1
                if  (wallPosition[1]+1<self.width) and ("down" in self.board[wallPosition[0]-1][wallPosition[1]+1]):
                    counterList[2]=1
        if counterList.count(1)==2:
            return True
        else:
            return False

    def isWallLegalComplete(self, wallPosition: list, wallColor):

        if not (1<=wallPosition[0]<=(self.height-1)):
            return False
        if not (1<=wallPosition[1]<=(self.width-1)):
            return False
        if wallColor=="blue":
            
            if "down" in self.board[wallPosition[0]-1][wallPosition[1]-1]:
                return False
            if "down" in self.board[wallPosition[0]-1][wallPosition[1]]:
                return False
            if "up" in self.board[wallPosition[0]][wallPosition[1]-1]:  
                return False
            if "up" in self.board[wallPosition[0]][wallPosition[1]]:
                return False
            if ("right" in self.board[wallPosition[0]-1][wallPosition[1]-1]) and ("right" in self.board[wallPosition[0]][wallPosition[1]-1]):
                return False

        if wallColor=="green":
            if "right" in self.board[wallPosition[0]-1][wallPosition[1]-1]:
                return False
            if "left" in self.board[wallPosition[0]-1][wallPosition[1]]:
                return False
            if "right" in self.board[wallPosition[0]][wallPosition[1]-1]:  
                return False
            if "left" in self.board[wallPosition[0]][wallPosition[1]]:
                return False
            if ("down" in self.board[wallPosition[0]-1][wallPosition[1]-1]) and ("down" in self.board[wallPosition[0]-1][wallPosition[1]]):
                return False
        if self.doesWallConnect(wallPosition, wallColor):
            return isLegalWall(self, wallPosition, wallColor)
        else: 
            return True

    def isPawnLegalComplete(self, player, pawnNum, move: list):

        #provera da li je odgovarajuca distanca izmedju izvora i odtedista pesaka (2, -2 ili sqrt(2) i -sqrt(2) za dijagonalni potez) 
        if pawnNum not in [1,2]:
            return False
        if player not in ["X", "O"]:
            return False
        if player=="X":
            if pawnNum==1:
                playerPos=[self.pawnPosX1[0], self.pawnPosX1[1]]
                if np.sqrt((move[0]-self.pawnPosX1[0])**2+(move[1]-self.pawnPosX1[1])**2) not in [np.sqrt(2),2,1]:
                    return False 
                
                                       #distanca = sqrt((X2-X1)^2+(Y2-Y1)^2)     (X2,Y2) - koordinate odredista     (X1,Y1) - koordinate izvora

            if pawnNum==2:
                playerPos=[self.pawnPosX2[0], self.pawnPosX2[1]]
                if np.sqrt((move[0]-self.pawnPosX2[0])**2+(move[1]-self.pawnPosX2[1])**2) not in [np.sqrt(2),2,1]:           
                    return False


        if player=="O":
            if pawnNum==1:
                playerPos=[self.pawnPosO1[0], self.pawnPosO1[1]]
                if np.sqrt((move[0]-self.pawnPosO1[0])**2+(move[1]-self.pawnPosO1[1])**2) not in [np.sqrt(2),2,1]:                   
                    return False

            if pawnNum==2:
                playerPos=[self.pawnPosO2[0], self.pawnPosO2[1]]
                if np.sqrt((move[0]-self.pawnPosO2[0])**2+(move[1]-self.pawnPosO2[1])**2) not in [np.sqrt(2),2,1]:
                    return False
        

        if self.possibleDirection(playerPos, move)==False:
            return False
        return True
        
def isLegalWall(board:Board, wallMove: list, wallColor, stack=deque(), visitedList=[]):
           
    newTabla=copy.deepcopy(board)
    newTabla.wallMove(wallColor,wallMove)
    Tabla=copy.deepcopy(board)
    Tabla.wallMove(wallColor,wallMove)
    visitedList.append(Tabla.pawnPosO1)
    if (Tabla.pawnPosO1[0]<Tabla.height+1) and (Tabla.pawnPosO1[1]<Tabla.width+1):

        if(Tabla.possibleDirection2([Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]],[Tabla.pawnPosO1[0]+2,Tabla.pawnPosO1[1]])):
            newTabla.pawnPosO1=[(Tabla.pawnPosO1[0]+2),(Tabla.pawnPosO1[1])]
            stack.append(copy.deepcopy(newTabla))      
        if(Tabla.possibleDirection2([Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]],[Tabla.pawnPosO1[0]-2,Tabla.pawnPosO1[1]])):
            newTabla.pawnPosO1=[Tabla.pawnPosO1[0]-2,Tabla.pawnPosO1[1]]
            stack.append(copy.deepcopy(newTabla))
        if(Tabla.possibleDirection2([Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]],[Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]-2])):
            newTabla.pawnPosO1=[Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]-2]
            stack.append(copy.deepcopy(newTabla))
        if(Tabla.possibleDirection2([Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]],[Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]+2])):
            newTabla.pawnPosO1=[Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]+2]
            stack.append(copy.deepcopy(newTabla))

        #dijagonalno
        if(Tabla.possibleDirection2([Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]],[Tabla.pawnPosO1[0]+1,Tabla.pawnPosO1[1]+1])):
            newTabla.pawnPosO1=[Tabla.pawnPosO1[0]+1,Tabla.pawnPosO1[1]+1]
            stack.append(copy.deepcopy(newTabla))
        if(Tabla.possibleDirection2([Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]],[Tabla.pawnPosO1[0]-1,Tabla.pawnPosO1[1]-1])):
            newTabla.pawnPosO1=[Tabla.pawnPosO1[0]-1,Tabla.pawnPosO1[1]-1]
            stack.append(copy.deepcopy(newTabla))
        if(Tabla.possibleDirection2([Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]],[Tabla.pawnPosO1[0]-1,Tabla.pawnPosO1[1]+1])):
            newTabla.pawnPosO1=[Tabla.pawnPosO1[0]-1,Tabla.pawnPosO1[1]+1]
            stack.append(copy.deepcopy(newTabla))
        if(Tabla.possibleDirection2([Tabla.pawnPosO1[0],Tabla.pawnPosO1[1]],[Tabla.pawnPosO1[0]+1,Tabla.pawnPosO1[1]-1])):
            newTabla.pawnPosO1=[Tabla.pawnPosO1[0]+1,Tabla.pawnPosO1[1]-1]
            stack.append(copy.deepcopy(newTabla))
    while stack:
        popedEl=stack.pop()
        if popedEl.pawnPosO1 not in visitedList:
            return isLegalWall(popedEl,wallMove, wallColor, stack, visitedList)
    pomList=[0,0,0,0,0,0,0]
    for i in range(len(visitedList)):
        if visitedList[i]==Tabla.startPosO1 or Tabla.isNextTo(visitedList[i], Tabla.startPosO1):
            pomList[0]=1
        if visitedList[i]==Tabla.startPosO2 or Tabla.isNextTo(visitedList[i], Tabla.startPosO2):
            pomList[1]=1
        if visitedList[i]==Tabla.startPosX1 or Tabla.isNextTo(visitedList[i], Tabla.startPosX1):
            pomList[2]=1
        if visitedList[i]==Tabla.startPosX2 or Tabla.isNextTo(visitedList[i], Tabla.startPosX2):
            pomList[3]=1
        if visitedList[i]==Tabla.pawnPosO2 or Tabla.isNextTo(visitedList[i], Tabla.pawnPosO2):
            pomList[4]=1
        if visitedList[i]==Tabla.pawnPosX1 or Tabla.isNextTo(visitedList[i], Tabla.pawnPosX1):
            pomList[5]=1
        if visitedList[i]==Tabla.pawnPosX2 or Tabla.isNextTo(visitedList[i], Tabla.pawnPosX2):
            pomList[6]=1
    visitedList.clear()
    stack.clear()
    if pomList.count(1)==7:
        return True
    else:
        return False

def drawBoard(board:Board): 

    root = Tk()
    root.geometry('1100x1100')
    canvas = Canvas(root, width=950, height=950)
    canvas.pack() 
    width = 930//board.width
    o=6 #offset
    for i in range(board.height):
        y = i * width+o
        for j in range(board.width):
            x = j * width+o
            canvas.create_rectangle(x, y, x+width, y+width)
    
    for i in range(board.height):
        for j in range(board.width):
            if "up" in board.board[i][j]:
                canvas.create_line(j*width+o, i*width+o, (j+1)*width+o, i*width+o, fill="blue", width=7)
            if "down" in board.board[i][j]:
                canvas.create_line(j*width+o, (i+1)*width+o, (j+1)*width+o, (i+1)*width+o, fill="blue", width=7)
            if "left" in board.board[i][j]:
                canvas.create_line(j*width+o, (i)*width+o, (j)*width+o, (i+1)*width+o, fill="green", width=7)
            if "right" in board.board[i][j]:
                canvas.create_line((j+1)*width+o, (i)*width+o, (j+1)*width+o, (i+1)*width+o, fill="green", width=7)

    board.X1Id = canvas.create_oval((board.pawnPosX1[1]-1)*width+o+o, (board.pawnPosX1[0]-1)*width+o+o, board.pawnPosX1[1]*width, board.pawnPosX1[0]*width, fill="red", tags=('X1'))
    board.X2Id = canvas.create_oval((board.pawnPosX2[1]-1)*width+o+o, (board.pawnPosX2[0]-1)*width+o+o, board.pawnPosX2[1]*width, board.pawnPosX2[0]*width, fill="red", tags=('X2'))
    board.O1Id = canvas.create_oval((board.pawnPosO1[1]-1)*width+o+o, (board.pawnPosO1[0]-1)*width+o+o, board.pawnPosO1[1]*width, board.pawnPosO1[0]*width, fill="yellow", tags=('O1'))
    board.O2Id = canvas.create_oval((board.pawnPosO2[1]-1)*width+o+o, (board.pawnPosO2[0]-1)*width+o+o, board.pawnPosO2[1]*width, board.pawnPosO2[0]*width, fill="yellow", tags=('O2'))

    canvas.create_line((board.startPosX1[1]-1)*width+o, (board.startPosX1[0]-1)*width+o, board.startPosX1[1]*width+o, board.startPosX1[0]*width+o, fill="red", width=4)
    canvas.create_line((board.startPosX2[1]-1)*width+o, (board.startPosX2[0]-1)*width+o, board.startPosX2[1]*width+o, board.startPosX2[0]*width+o, fill="red", width=4)
    canvas.create_line((board.startPosO1[1]-1)*width+o, (board.startPosO1[0]-1)*width+o, board.startPosO1[1]*width+o, board.startPosO1[0]*width+o, fill="yellow", width=4)
    canvas.create_line((board.startPosO2[1]-1)*width+o, (board.startPosO2[0]-1)*width+o, board.startPosO2[1]*width+o, board.startPosO2[0]*width+o, fill="yellow", width=4)

    root.mainloop()

def refreshBoard(board:Board, canvas, width, o):

    for i in range(board.height):
        y = i * width+o
        for j in range(board.width):
            x = j * width+o
            canvas.create_rectangle(x, y, x+width, y+width)
    
    for i in range(board.height):
        for j in range(board.width):
            if "up" in board.board[i][j]:
                canvas.create_line(j*width+o, i*width+o, (j+1)*width+o, i*width+o, fill="blue", width=7)
            if "down" in board.board[i][j]:
                canvas.create_line(j*width+o, (i+1)*width+o, (j+1)*width+o, (i+1)*width+o, fill="blue", width=7)
            if "left" in board.board[i][j]:
                canvas.create_line(j*width+o, (i)*width+o, (j)*width+o, (i+1)*width+o, fill="green", width=7)
            if "right" in board.board[i][j]:
                canvas.create_line((j+1)*width+o, (i)*width+o, (j+1)*width+o, (i+1)*width+o, fill="green", width=7)

    board.X1Id = canvas.create_oval((board.pawnPosX1[1]-1)*width+o+o, (board.pawnPosX1[0]-1)*width+o+o, board.pawnPosX1[1]*width, board.pawnPosX1[0]*width, fill="red",activefill="darkred", tags='X1')
    board.X2Id = canvas.create_oval((board.pawnPosX2[1]-1)*width+o+o, (board.pawnPosX2[0]-1)*width+o+o, board.pawnPosX2[1]*width, board.pawnPosX2[0]*width, fill="red",activefill="darkred", tags='X2')
    board.O1Id = canvas.create_oval((board.pawnPosO1[1]-1)*width+o+o, (board.pawnPosO1[0]-1)*width+o+o, board.pawnPosO1[1]*width, board.pawnPosO1[0]*width, fill="yellow",activefill="orange", tags='O1')
    board.O2Id = canvas.create_oval((board.pawnPosO2[1]-1)*width+o+o, (board.pawnPosO2[0]-1)*width+o+o, board.pawnPosO2[1]*width, board.pawnPosO2[0]*width, fill="yellow",activefill="orange", tags='O2')

    canvas.create_line((board.startPosX1[1]-1)*width+o, (board.startPosX1[0]-1)*width+o, board.startPosX1[1]*width+o, board.startPosX1[0]*width+o, fill="red", width=4)
    canvas.create_line((board.startPosX2[1]-1)*width+o, (board.startPosX2[0]-1)*width+o, board.startPosX2[1]*width+o, board.startPosX2[0]*width+o, fill="red", width=4)
    canvas.create_line((board.startPosO1[1]-1)*width+o, (board.startPosO1[0]-1)*width+o, board.startPosO1[1]*width+o, board.startPosO1[0]*width+o, fill="yellow", width=4)
    canvas.create_line((board.startPosO2[1]-1)*width+o, (board.startPosO2[0]-1)*width+o, board.startPosO2[1]*width+o, board.startPosO2[0]*width+o, fill="yellow", width=4)

def createBoard( height, width,  wallNumber, pawnPositionX1, pawnPositionX2, pawnPositionO1, pawnPositionO2):
    A=np.zeros( (height, width), dtype=list)
    Tabla=Board(A,height, width, wallNumber, pawnPositionX1, pawnPositionX2, pawnPositionO1, pawnPositionO2)
    for i in range (height):
        for j in range(width):
            Tabla.board[i][j]=[]
    for i in range(width):
        Tabla.board[0][i].append("up")
        Tabla.board[height-1][i].append("down")

    for i in range(height):
        Tabla.board[i][0].append("left")
        Tabla.board[i][width-1].append("right")

    return Tabla

def defaultBoard(): 
    return createBoard(11, 14, 9, [4,4], [8,4], [4,11],[8,11])

def onFirstClick(event, canvas, board, width, o):

    y=(event.x-o)//width+1
    x=(event.y-o)//width+1
    y1=y
    x1=x

    if(board.currentPlayer=="O" and board.greenWallNumO==0 and board.blueWallNumO==0):
        if ([x,y]==board.pawnPosO1 and board.currentPlayer=="O") or ([x,y]==board.pawnPosO2 and board.currentPlayer=="O") or ([x,y]==board.pawnPosX1 and board.currentPlayer=="X") or ([x,y]==board.pawnPosX2 and board.currentPlayer=="X"):
            canvas.bind('<Button-1>',functools.partial(onSecondClick, canvas=canvas, board=board, x1=x,y1=y, width=width, o=o))
            return

        else: 
            print("You've ran out of walls or you've tried to play with the wrong pawn, please play a valid pawn move ")
            return

    elif(board.currentPlayer=="X" and board.greenWallNumX==0 and board.blueWallNumX==0):   
        if ([x,y]==board.pawnPosO1 and board.currentPlayer=="O") or ([x,y]==board.pawnPosO2 and board.currentPlayer=="O") or ([x,y]==board.pawnPosX1 and board.currentPlayer=="X") or ([x,y]==board.pawnPosX2 and board.currentPlayer=="X"):
            canvas.bind('<Button-1>',functools.partial(onSecondClick, canvas=canvas, board=board, x1=x,y1=y, width=width, o=o))
            return

        else: 
            print("You've ran out of walls or you've tried to play with the wrong pawn, please play a valid pawn move ")
            return

    if -0.1<(round((event.x-o)/width+1)-((event.x-o)/width+1))<0.1 or -0.1<(round((event.y-o)/width+1)-((event.y-o)/width+1))<0.1:
        if board.wallPlayed==False:
            if -0.1<(round((event.y-o)/width+1)-((event.y-o)/width+1))<0.1:
                wallColor="blue"
                if (round((event.y-o)/width+1)-((event.y-o)/width+1))<=0:
                    x1-=1
                if (board.currentPlayer=="O" and board.blueWallNumO==0) or (board.currentPlayer=="X" and board.blueWallNumX==0):
                    print("You've ran out of blue walls, please place a green wall")
                    return

            else:
                wallColor="green"   
                if (round((event.x-o)/width+1)-((event.x-o)/width+1))<=0:
                    y1-=1 
                if (board.currentPlayer=="O" and board.greenWallNumO==0) or (board.currentPlayer=="X" and board.greenWallNumX==0):
                    print("You've ran out of green walls, please place a blue wall")
                    return

            if board.isWallLegalComplete([x1,y1],wallColor):
                board.wallMove(wallColor, [x1,y1])
                gameWindowUpdate(board)
                board.wallPlayed=True
                refreshBoard(board,canvas, width, o)
                canvas.unbind("<Motion>")
                canvas.delete("temporary")
                return
            else:
                print("Invalid wall")
                return
        else:
            print("You can't play two walls in a row")
            return
            

    if board.wallPlayed:
        if ([x,y]==board.pawnPosO1 and board.currentPlayer=="O") or ([x,y]==board.pawnPosO2 and board.currentPlayer=="O") or ([x,y]==board.pawnPosX1 and board.currentPlayer=="X") or ([x,y]==board.pawnPosX2 and board.currentPlayer=="X"):
            canvas.bind('<Button-1>',functools.partial(onSecondClick, canvas=canvas, board=board, x1=x,y1=y, width=width, o=o))
        else: 
            print("Invalid click or not your move")
            return
    else:
        print("You need to place a wall first!")
    
def onSecondClick(event, canvas, board, x1, y1, width, o):

    y=(event.x-o)//width+1
    x=(event.y-o)//width+1

    if(board.pawnPosO1==[x1,y1] and board.isPawnLegalComplete('O',1,[x,y])):
        board.pawnPosO1=[x,y]
        board.currentPlayer='X'
        board.wallPlayed=False
        canvas.delete("O1")
        refreshBoard(board,canvas,width, o)
        gameWindowUpdate(board)
        canvas.bind('<Button-1>',functools.partial(onFirstClick, canvas=canvas, board=board, width=width, o=o))
        canvas.bind("<Motion>", functools.partial(moved, canvas=canvas, width=width, o=o))
        if(board.isEnd()!=False):
            print("Pobedio je igrac " + board.isEnd())
        return
    
    if(board.pawnPosO2==[x1,y1] and board.isPawnLegalComplete('O',2,[x,y])):
        board.pawnPosO2=[x,y]
        board.currentPlayer='X'
        board.wallPlayed=False
        canvas.delete("O2")
        refreshBoard(board,canvas,width, o)
        gameWindowUpdate(board)
        canvas.bind('<Button-1>',functools.partial(onFirstClick, canvas=canvas, board=board, width=width, o=o))
        canvas.bind("<Motion>", functools.partial(moved, canvas=canvas,  width=width, o=o))
        if(board.isEnd()!=False):
            print("Pobedio je igrac " + board.isEnd())
        return

    if(board.pawnPosX1==[x1,y1] and board.isPawnLegalComplete('X',1,[x,y])):
        board.pawnPosX1=[x,y]
        board.currentPlayer='O'
        board.wallPlayed=False
        canvas.delete("X1")
        refreshBoard(board,canvas,width, o)
        gameWindowUpdate(board)
        canvas.bind('<Button-1>',functools.partial(onFirstClick, canvas=canvas, board=board, width=width, o=o))
        canvas.bind("<Motion>", functools.partial(moved, canvas=canvas, width=width, o=o))
        if(board.isEnd()!=False):
            print("Pobedio je igrac " + board.isEnd())
        return

    if(board.pawnPosX2==[x1,y1] and board.isPawnLegalComplete('X',2,[x,y])):
        board.pawnPosX2=[x,y]
        board.currentPlayer='O'
        board.wallPlayed=False
        canvas.delete("X2")
        refreshBoard(board,canvas,width, o)
        gameWindowUpdate(board)
        canvas.bind('<Button-1>',functools.partial(onFirstClick, canvas=canvas, board=board, width=width, o=o))
        canvas.bind("<Motion>", functools.partial(moved, canvas=canvas, width=width, o=o))
        if(board.isEnd()!=False):
            print("Pobedio je igrac " + board.isEnd())
        return

    print ("Invalid move, click another square")

def moved(event, canvas, width, o):

    y=(event.x-o)//width+1
    x=(event.y-o)//width+1

    canvas.delete("temporary")

    if  -0.1<((round((event.y-o)/width+1))-((event.y-o)/width+1))<0:
        canvas.create_line((y-1)*width+o, (x-1)*width+o, (y+1)*width+o, (x-1)*width+o, fill="grey", width=7, tag="temporary")
    
    if  -0.1<((round((event.x-o)/width+1))-((event.x-o)/width+1))<0:
        canvas.create_line((y-1)*width+o, (x+1)*width+o, (y-1)*width+o, (x-1)*width+o, fill="grey", width=7, tag="temporary")
    
    if  0<(round((event.y-o)/width+1)-((event.y-o)/width+1))<0.1:
        canvas.create_line((y-1)*width+o, (x)*width+o, (y+1)*width+o, (x)*width+o, fill="grey", width=7, tag="temporary")

    if  0<(round((event.x-o)/width+1)-((event.x-o)/width+1))<0.1:
        canvas.create_line((y)*width+o, (x+1)*width+o, (y)*width+o, (x-1)*width+o, fill="grey", width=7, tag="temporary")
    
    return    

def startGame(height, width, wallNumber, pawnsOnEdges):
    if pawnsOnEdges:
        pawnPositionX1=[1,1]
        pawnPositionX2=[height, 1]
        pawnPositionO1=[1,width]
        pawnPositionO2=[height, width]
    else:
        pawnPositionX1=[4,4]
        pawnPositionX2=[height-3, 4]
        pawnPositionO1=[4,width-3]
        pawnPositionO2=[height-3, width-3]
    tabla = createBoard(height, width,  wallNumber, pawnPositionX1, pawnPositionX2, pawnPositionO1, pawnPositionO2)
    openGameWindow(tabla)
        
def gameWindowUpdate(board):

    global frameRed
    global greenXLeft
    global blueXLeft
    global frameYellow
    global greenOLeft
    global blueOLeft

    if board.isEnd()!=False:
        greenXLeft.configure(text="Pobedio je igrač "+ board.isEnd())
        greenOLeft.configure(text="Pobedio je igrač "+ board.isEnd())
        blueXLeft.configure(text="Pobedio je igrač "+ board.isEnd())
        blueOLeft.configure(text="Pobedio je igrač "+ board.isEnd())
    else:
        greenXLeft.configure(text="Green walls left:"+ str(board.greenWallNumX))
        greenOLeft.configure(text="Green walls left:"+ str(board.greenWallNumO))
        blueXLeft.configure(text="Blue walls left:"+ str(board.blueWallNumX))
        blueOLeft.configure(text="Blue walls left:"+ str(board.blueWallNumO))
    if board.currentPlayer=="X":
        frameRed["bd"]= 10
        frameYellow["bd"]=2
    if board.currentPlayer=="O":
        frameRed["bd"]= 2
        frameYellow["bd"]=10
    
def startingScreen():
    root = Tk()
    #root.geometry("600x400")
    labela1 = Label(root, text="Broj kolona:")
    labela2 = Label(root, text="Broj vrsta:")
    labela3 = Label(root, text="Broj zidova:")
    labela4 = Label(root, text="Prvi igra:")
    
    skalaBrKolona=Scale(root, from_=6, to=28, orient=HORIZONTAL)
    skalaBrVrsta=Scale(root, from_=6, to=24,  orient=HORIZONTAL)
    skalaBrZidova=Scale(root, from_=1, to=20,  orient=HORIZONTAL)
    submit=Button(root, text="Star game", command=lambda: startGame(skalaBrVrsta.get(), skalaBrKolona.get(), skalaBrZidova.get(), cb.get()))

    v=IntVar()
    v.set(1)
    cb=IntVar()

    radiobutton_Human = Radiobutton(root, text="Covek", variable=v, value=1)
    radiobutton_Computer = Radiobutton(root, text="Kompjuter", variable=v, value=2)

    checkbox_StartingPos = Checkbutton(root, text="Pesaci na ivicama(preporuceno za table manje od 9x9)", variable=cb, onvalue=1, offvalue=0)

    radiobutton_Human.select()
    skalaBrKolona.set(14)
    skalaBrVrsta.set(11)
    skalaBrZidova.set(9)

    labela1.pack()
    skalaBrKolona.pack()
    labela2.pack()
    skalaBrVrsta.pack()
    labela3.pack()
    skalaBrZidova.pack()
    labela4.pack()
    radiobutton_Human.pack()
    radiobutton_Computer.pack()
    checkbox_StartingPos.pack()
    submit.pack(pady=20)

    root.mainloop()

def openGameWindow(board:Board):

    global frameRed
    global greenXLeft
    global blueXLeft
    global frameYellow
    global greenOLeft
    global blueOLeft

    root = Tk()
    o=6
    if board.width>board.height:
        width=850//board.width
    else:
        width=850//board.height
    canvas = Canvas(root, width=width*board.width+o+2, height=width*board.height+o+2)
    canvas.pack(side=BOTTOM, pady=10) 

    frameRed=LabelFrame(root, fg="red", font=14, text="Red player")
    greenXLeft=Label(frameRed, text="Green walls left:" + str(board.greenWallNumX), font= ("Arial",18))
    blueXLeft=Label(frameRed, text="Blue walls left:"+ str(board.blueWallNumX), font=("Arial", 18))

    frameYellow=LabelFrame(root,fg="orange", font=14, text="Yellow player")   
    greenOLeft=Label(frameYellow, text="Green walls left:"+ str(board.blueWallNumO), font=("Arial", 18))
    blueOLeft=Label(frameYellow, text="Blue walls left:"+ str(board.blueWallNumO), font=("Arial", 18))

    gameWindowUpdate(board)

    frameRed.pack(padx=170, pady=2, side=LEFT)
    frameYellow.pack(padx=170, pady=2, side=RIGHT)
    greenXLeft.pack()
    blueXLeft.pack()
    greenOLeft.pack()
    blueOLeft.pack()    

    canvas.bind("<Motion>", functools.partial(moved, canvas=canvas, width=width, o=o))
    canvas.bind('<Button-1>',functools.partial(onFirstClick, canvas=canvas, board=board, width=width, o=o))
    refreshBoard(board, canvas, width, o)

    root.mainloop()
