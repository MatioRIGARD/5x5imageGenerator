#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 12:56:34 2021

@author: matio
"""



from skimage import data, io, filters


class imgGen:
    def __init__(self, filePath, gridSizeX, gridSizeY):
        
        self.img = io.imread(filePath)
        
        self.xSize = self.img.shape[0]
        self.ySize = self.img.shape[1]
        
        self.xSectionSize = int(self.xSize/gridSizeX)
        self.ySectionSize = int(self.ySize/gridSizeY)
        
        self.colors = [   
            0x000000,
            0xFF0000,
            0x0000FF,
            0xFFFF00,
            0x800080,
            0xFFA500,
            0x00FF00,
            0x808000,
            0x00FFFF,
            0xFFFFFF,
            0xFF6347,
            0x00FFFF,
            0x808080,
            0xFFC0CB,
            0xD2B48C,
            0x40E0D0,
            0xEE82EE,
            0xFFD700,
            0xC0C0C0,
            0xA52A2A,
            0xFFFAFA]
   
        
    def getColorFromSquareAsHexStr(self, x, y):  # x et y de 0 à 4
        rPxSum = 0;
        gPxSum = 0;
        bPxSum = 0;
        rPxMoy = 0;
        gPxMoy = 0;
        bPxMoy = 0;
        pxQty = 0;
        for pxX in range(x*self.xSectionSize, x*self.xSectionSize+self.xSectionSize):
            for pxY in range(y*self.ySectionSize, y*self.ySectionSize+self.ySectionSize):
                pxQty = pxQty+1;
                rPxSum = rPxSum+self.img[pxX][pxY][0];
                gPxSum = gPxSum+self.img[pxX][pxY][1];
                bPxSum = bPxSum+self.img[pxX][pxY][2];
        
        rPxMoy = int(rPxSum/pxQty);
        gPxMoy = int(gPxSum/pxQty);
        bPxMoy = int(bPxSum/pxQty);
        
        hexVal = rPxMoy*65536+gPxMoy*256+bPxMoy
        
        return hexVal
    
    
    def getSquareForBsStream(self):
        square = []
        for x in range(0, 5):
            for y in range(0,5):
                square.append(self.getColorFromSquareAsHexStr(x, y))
                
        return square
        
    
    def getStrForBsStream(self):
        strCmd = ""
        square = self.getSquareForBsStream()
        for elem in range(0, len(square)):
            strCmd += "!"+str(elem)+"|"+str(hex(square[elem]))+" "
        
        return strCmd
    
    def getClosestColorDefined(self):
        square = self.getSquareForBsStream()
        colorsChosen = []
        
        for elem in range(0, len(square)):
            closeRatio = 65536
            currentColor = None
            colorStr = ""
            for colorNum in range(0, len(self.colors)):
                rMark = -1
                gMark = -1
                bMark = -1
                mark = -1
                rElem = (square[elem]&0xFF0000)>>16
                gElem = (square[elem]&0x00FF00)>>8
                bElem = square[elem]&0x0000FF
                
                rColor = (self.colors[colorNum]&0xFF0000)>>16
                gColor = (self.colors[colorNum]&0x00FF00)>>8
                bColor = self.colors[colorNum]&0x0000FF
                
                if rElem > rColor:
                    rMark = rElem-rColor
                else:
                    rMark = rColor-rElem
                    
                if gElem > gColor:
                    gMark = gElem-gColor
                else:
                    gMark = gColor-gElem
                    
                if bElem > bColor:
                    bMark = bElem-bColor
                else:
                    bMark = bColor-bElem
                    
                if rMark != -1 and gMark != -1 and bMark != -1:
                    mark = rMark+gMark+bMark/3
                
                if mark < closeRatio:
                    closeRatio = mark
                    currentColor = colorNum
                    
            colorsChosen.append(currentColor)
        
        for num in range(0, len(colorsChosen)):
            colorStr = colorStr+"!"+str(num)+"|"+str(colorsChosen[num])+" "
            
        return colorStr
            


gen = imgGen("degrade4.jpg", 5, 5)
print("hex:")
print(gen.getStrForBsStream())
print("\n")
print("values:")
print(gen.getClosestColorDefined())







# tutos:
# https://python-prepa.github.io/ateliers/image_tuto.html
# https://scikit-image.org/


"""
AliceBlue =0xF0F8FF, Amethyst =0x9966CC, AntiqueWhite =0xFAEBD7, Aqua =0x00FFFF,
Aquamarine =0x7FFFD4, Azure =0xF0FFFF, Beige =0xF5F5DC, Bisque =0xFFE4C4,
Black =0x000000, BlanchedAlmond =0xFFEBCD, Blue =0x0000FF, BlueViolet =0x8A2BE2,
Brown =0xA52A2A, BurlyWood =0xDEB887, CadetBlue =0x5F9EA0, Chartreuse =0x7FFF00,
Chocolate =0xD2691E, Coral =0xFF7F50, CornflowerBlue =0x6495ED, Cornsilk =0xFFF8DC,
Crimson =0xDC143C, Cyan =0x00FFFF, DarkBlue =0x00008B, DarkCyan =0x008B8B,
DarkGoldenrod =0xB8860B, DarkGray =0xA9A9A9, DarkGrey =0xA9A9A9, DarkGreen =0x006400,
DarkKhaki =0xBDB76B, DarkMagenta =0x8B008B, DarkOliveGreen =0x556B2F, DarkOrange =0xFF8C00,
DarkOrchid =0x9932CC, DarkRed =0x8B0000, DarkSalmon =0xE9967A, DarkSeaGreen =0x8FBC8F,
DarkSlateBlue =0x483D8B, DarkSlateGray =0x2F4F4F, DarkSlateGrey =0x2F4F4F, DarkTurquoise =0x00CED1,
DarkViolet =0x9400D3, DeepPink =0xFF1493, DeepSkyBlue =0x00BFFF, DimGray =0x696969,
DimGrey =0x696969, DodgerBlue =0x1E90FF, FireBrick =0xB22222, FloralWhite =0xFFFAF0,
ForestGreen =0x228B22, Fuchsia =0xFF00FF, Gainsboro =0xDCDCDC, GhostWhite =0xF8F8FF,
Gold =0xFFD700, Goldenrod =0xDAA520, Gray =0x808080, Grey =0x808080,
Green =0x008000, GreenYellow =0xADFF2F, Honeydew =0xF0FFF0, HotPink =0xFF69B4,
IndianRed =0xCD5C5C, Indigo =0x4B0082, Ivory =0xFFFFF0, Khaki =0xF0E68C,
Lavender =0xE6E6FA, LavenderBlush =0xFFF0F5, LawnGreen =0x7CFC00, LemonChiffon =0xFFFACD,
LightBlue =0xADD8E6, LightCoral =0xF08080, LightCyan =0xE0FFFF, LightGoldenrodYellow =0xFAFAD2,
LightGreen =0x90EE90, LightGrey =0xD3D3D3, LightPink =0xFFB6C1, LightSalmon =0xFFA07A,
LightSeaGreen =0x20B2AA, LightSkyBlue =0x87CEFA, LightSlateGray =0x778899, LightSlateGrey =0x778899,
LightSteelBlue =0xB0C4DE, LightYellow =0xFFFFE0, Lime =0x00FF00, LimeGreen =0x32CD32,
Linen =0xFAF0E6, Magenta =0xFF00FF, Maroon =0x800000, MediumAquamarine =0x66CDAA,
MediumBlue =0x0000CD, MediumOrchid =0xBA55D3, MediumPurple =0x9370DB, MediumSeaGreen =0x3CB371,
MediumSlateBlue =0x7B68EE, MediumSpringGreen =0x00FA9A, MediumTurquoise =0x48D1CC, MediumVioletRed =0xC71585,
MidnightBlue =0x191970, MintCream =0xF5FFFA, MistyRose =0xFFE4E1, Moccasin =0xFFE4B5,
NavajoWhite =0xFFDEAD, Navy =0x000080, OldLace =0xFDF5E6, Olive =0x808000,
OliveDrab =0x6B8E23, Orange =0xFFA500, OrangeRed =0xFF4500, Orchid =0xDA70D6,
PaleGoldenrod =0xEEE8AA, PaleGreen =0x98FB98, PaleTurquoise =0xAFEEEE, PaleVioletRed =0xDB7093,
PapayaWhip =0xFFEFD5, PeachPuff =0xFFDAB9, Peru =0xCD853F, Pink =0xFFC0CB,
Plaid =0xCC5533, Plum =0xDDA0DD, PowderBlue =0xB0E0E6, Purple =0x800080,
Red =0xFF0000, RosyBrown =0xBC8F8F, RoyalBlue =0x4169E1, SaddleBrown =0x8B4513,
Salmon =0xFA8072, SandyBrown =0xF4A460, SeaGreen =0x2E8B57, Seashell =0xFFF5EE,
Sienna =0xA0522D, Silver =0xC0C0C0, SkyBlue =0x87CEEB, SlateBlue =0x6A5ACD,
SlateGray =0x708090, SlateGrey =0x708090, Snow =0xFFFAFA, SpringGreen =0x00FF7F,
SteelBlue =0x4682B4, Tan =0xD2B48C, Teal =0x008080, Thistle =0xD8BFD8,
Tomato =0xFF6347, Turquoise =0x40E0D0, Violet =0xEE82EE, Wheat =0xF5DEB3,
White =0xFFFFFF, WhiteSmoke =0xF5F5F5, Yellow =0xFFFF00, YellowGreen =0x9ACD32,
FairyLight =0xFFE42D, FairyLightNCC =0xFF9D2A
"""

"""
CRGB::Black, 0x000000
CRGB::Red, 0xFF0000
CRGB::Blue, 0x0000FF
CRGB::Yellow, 0xFFFF00
CRGB::Purple, 0x800080
CRGB::Orange, 0xFFA500
CRGB::Lime, 0x00FF00
CRGB::Olive, 0x808000
CRGB::Cyan,0x00FFFF
CRGB::White, 0xFFFFFF
CRGB::Tomato,0xFF6347
CRGB::Aqua, 0x00FFFF
CRGB::Gray,0x808080
CRGB::Pink, 0xFFC0CB
CRGB::Tan, 0xD2B48C
CRGB::Turquoise, 0x40E0D0
CRGB::Violet, 0xEE82EE
CRGB::Gold, 0xFFD700
CRGB::Silver,0xC0C0C0
CRGB::Brown,0xA52A2A
CRGB::Snow,0xFFFAFA
"""