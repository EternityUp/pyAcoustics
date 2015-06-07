'''
Created on Oct 11, 2012

@author: timmahrt
'''

import os
from os.path import join

import functools
import itertools
import shutil
import codecs

def _getMatchFunc(pattern):
    '''
    An unsophisticated pattern matching function
    '''
    
    # '#' Marks word boundaries, so if there is more than one we need to do
    #    something special to make sure we're not mis-representings them
    assert(pattern.count('#') < 2)

    def startsWith(subStr, fullStr):
        return fullStr[:len(subStr)] == subStr
            
    def endsWith(subStr, fullStr):
        return fullStr[-1*len(subStr):] == subStr
    
    def inStr(subStr, fullStr):
        return subStr in fullStr

    # Selection of the correct function
    if pattern[0] == '#':
        pattern = pattern[1:]
        cmpFunc = startsWith
        
    elif pattern[-1] == '#':
        pattern = pattern[:-1]
        cmpFunc = endsWith
        
    else:
        cmpFunc = inStr
    
    return functools.partial(cmpFunc, pattern)


def findFiles(path, filterPaths=False, filterExt=None, filterPattern=None,
              skipIfNameInList=None, stripExt=False):
    
    fnList = os.listdir(path)
    
    
    if filterPaths == True:
        fnList = [folderName for folderName in fnList if os.path.isdir(os.path.join(path, folderName))]    


    if filterExt != None:
        splitFNList = [[fn,] + list(os.path.splitext(fn)) for fn in fnList]
        fnList = [fn for fn, name, ext in splitFNList if ext == filterExt]
        
        
    if filterPattern != None:
        splitFNList = [[fn,] + list(os.path.splitext(fn)) for fn in fnList]
        matchFunc = _getMatchFunc(filterPattern)
        fnList = [fn for fn, name, ext in splitFNList if matchFunc(name)]
    
    if skipIfNameInList != None:
        targetNameList = [os.path.splitext(fn)[0] for fn in skipIfNameInList]
        fnList = [fn for fn in fnList if os.path.splitext(fn)[0] not in targetNameList]
    
    if stripExt == True:
        fnList = [os.path.splitext(fn)[0] for fn in fnList]
    
    fnList.sort()
    return fnList
    

def openCSV(path, fn, valueIndex=None, encoding="ascii"):
    '''
    Load a feature
    
    In many cases we only want a single value from the feature (mainly because
    the feature only contains one value).  In these situations, the user
    can indicate that rather than receiving a list of lists, they can receive
    a lists of values, where each value represents the item in the row indiciated
    by valueIndex.
    '''
    
    # Load CSV file
    with codecs.open(join(path, fn), "rU", encoding=encoding) as fd:
        featureList = fd.read().splitlines()
    featureList = [row.split(",") for row in featureList]
    
    if valueIndex != None:
        featureList = [row[valueIndex] for row in featureList]
    
    return featureList


def changeFileType(path, fromExt, toExt):
    
    if fromExt[0] != ".":
        fromExt = "." + fromExt
    if toExt[0] != ".":
        toExt = "." + toExt
        
    for fn in os.listdir(path):
        name, ext = os.path.splitext(fn)
        if ext == fromExt:
            shutil.move(join(path, fn), join(path, name + toExt))


def makeDir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def extractLines(path, matchStr, outputDir = "output"):
    
    outputPath = join(path, outputDir)
    makeDir(outputPath)
    
    for fn in findFiles(path, filterExt=".csv"):
        data = open(join(path, fn), "rU").read()
        dataList = data.split("\n")
        
        dataList = [line for line in dataList if matchStr in line]
        
        open(join(outputPath, fn), "w").write("\n".join(dataList))


def cat(fn1, fn2, outputFN):
    txt1 = open(fn1, 'r').read()
    txt2 = open(fn2, 'r').read()
    
    open(outputFN, 'w').write(txt1 + txt2)
    
    
def catAll(path, ext, ensureNewline=False):
    outputPath = join(path, "cat_output")
    makeDir(outputPath)
    
    outputList = []
    for fn in findFiles(path, filterExt=ext):
        data = open(join(path, fn), "rU").read()
        
        if ensureNewline and data[-1] != "\n":
            data += "\n"
        
        outputList.append(data)
    
    outputTxt = "".join(outputList)
    open(join(outputPath, "catFiles" + ext), "w").write(outputTxt)
    
    
def whatever(path):
    outputList = []
    for fn in findFiles(path, filterExt=".txt"):
        outputList.extend([fn,]*30)
        
    for fn in outputList:
        print fn


def divide(numerator, denominator, zeroValue):
    if denominator == 0:
        retValue = zeroValue
    else:
        retValue = numerator / float(denominator)
        
    return retValue


def safeZip(listOfLists, enforceLength):
    
    if enforceLength == True:
        length = len(listOfLists[0])
        assert(all([length == len(subList) for subList in listOfLists]))
    
    return itertools.izip_longest(*listOfLists)


if __name__ == "__main__":
#     catAll("/Users/tmahrt/Desktop/experiments/Mother_Prosody_RAship/features/manual_speech_rate_dictionary", ".txt", True)
#     catAll("/Users/tmahrt/Desktop/experiments/Mother_Prosody_RAship/features/praat_f0_measures", ".txt", True)
    
    whatever("/Users/tmahrt/Desktop/experiments/Mother_Prosody_RAship/features/praat_f0_measures")
    
#     path = "/Users/timmahrt/Sites/tests/prelim_stimuli/audio"
#     path = "/Users/timmahrt/Desktop/blah99/cleaned"
#     x = findFiles(path, filterExt=".ogg")
#     
#     txt = "\n".join(x)
#     open(join(path, "names.txt"), "w").write(txt)
    
#    # getMatchFunc() unit tests
#    x = getMatchFunc('#s')
#    print x('satatonic')
#    print x('bird')
#    
#    y = getMatchFunc('#cat')
#    print y('catatonic')
#    
#    z = getMatchFunc('d#')
#    print z('birdz')
#    print z('bird')
#    
#    a = getMatchFunc('bird#')
#    print a('I love big bird')
#    print a('Do you see the birds')
#    
#    b = getMatchFunc('tall')
#    print b('taller than you')
#    print b('Smaller than you')
    
    

