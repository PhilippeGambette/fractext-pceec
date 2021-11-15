# coding: utf8
#!/usr/sfw/bin/python

import glob, os, re, sys, time
from io import open

# store in the folder variable the address of the folder containing this program
folder = os.path.abspath(os.path.dirname(sys.argv[0]))

outputFile = open(os.path.join(folder, "output.csv"), "w", encoding='utf-8')

nbCharPerWord = 0
nbTokens = 0
nbPunctuationSigns = 0
nbCommas = 0
nbVerbs = 0
nbSubordination = 0

tokenFrequencies = {}
posFrequencies = {}

punctuation = [".",";","?","!",":",",","-"]
punctuationDict = {}

# Consider all input texts
for file in glob.glob(folder + "\\psd-cs1\\*.psd"):
   # Create corresponding output file
   #outputWordFile = open(file + ".words.csv","w", encoding="utf-8")
   #outputSentenceFile = open(file + ".sentences.csv","w", encoding="utf-8")
   nbSentences = 0
   
   # Display the address of the file being treated
   print("Currently extacting criteria from file " + file)
   
   inputFile = open(file, "r", encoding='utf-8', errors='ignore')
   currentBlock = ""
   metadata = False
   lineNb = 0
   for line in inputFile:
      lineNb += 1
      #print(lineNb)
      res = re.search("^[(] [(]CODING .*$", line)
      res2 = re.search("^[(] [(]METADATA.*$", line)
      if res or res2:
         # A new sentence starts on the next line
         nbCar = []
         nbTokens = 0
         nbPunctuation = 0
         nbCommas = 0
         nbVerbs = 0
         nbSubordination = 0
         metadata = True
         if re.search("[)][)]", line):
            metadata = False
         #print("new sentence")
      else:
         if metadata:
            if re.search("[)][)]", line):
               metadata = False
         else:
            # Analyze the line by finding the next token:
            regexp = "[(]([^ ]+) ([^()]+)[)](.*)$"
            res = re.search(regexp, line)
            while res:
               token = res.group(2) 
               posLabel = res.group(1) 
               if posLabel != "CODE" and posLabel != "ID" and token != "*" and token != "0" and token != "*T*-1":
                  # the token should be counted (neither CODE nor ID, nor empty token * or 0)
                  nbTokens += 1
                  #print(file + "new token: " + token + " ("+ posLabel + ")")
                  if (posLabel == "." or posLabel == ",") and not(token in punctuation):
                     if token in punctuationDict:
                        punctuationDict[token] += 1
                     else:
                        punctuationDict[token] = 1
                     print(token + " ("+ posLabel + ")")
                  if token in punctuation:
                     nbPunctuation += 1
                     
                     if token == ",":
                        nbCommas += 1
               # Look for the next token on the same line
               res = re.search(regexp, res.group(3))
   inputFile.close()
   #outputWordFile.close()
   #outputSentenceFile.close()

for token in punctuationDict:
   outputFile.writelines(token+"\t"+str(punctuationDict[token])+"\n")

"""
tokens = sorted(list(tokenFrequencies.keys()))
pos = sorted(list(posFrequencies.keys()))

outputTokens = open(os.path.join(folder, "tokens.csv"), "w", encoding='utf-8')
for token in tokens:
   if tokenFrequencies[token] > 0:
      outputTokens.writelines(token + "\t" + str(tokenFrequencies[token]) + "\n")
outputTokens.close()

outputPos = open(os.path.join(folder, "pos.csv"), "w", encoding='utf-8')
for po in pos:
   if posFrequencies[po] > 0:
      outputPos.writelines(po + "\t" + str(posFrequencies[po]) + "\n")
outputPos.close()

"""

outputFile.close()
