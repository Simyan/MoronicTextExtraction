import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import csv

smsText = "Purchase of AED 6.19 with Debit Card ending 2932 at W MART SUPERMARKET MARI, DUBAI. Avl Balance is AED 1,244.68."

filename = "ENBDMessages.txt"

def tokenIt(text):
    #tokenz = nltk.word_tokenize(text)
    tokenz = text.split()
    return tokenz


def isTransaction(tokenz):
    ListOfWords = ["Purchase", "Avl", "Balance", "AED", "Debit", "Card"]
    result = all(elem in tokenz for elem in ListOfWords)
    return result

def getLocation(tokens):
    isItOverYet = True
    loc = []
    location = ""
    i = 13
    while isItOverYet:
        if tokens[i] == "Avl":
            location = " ".join(loc)
            print("loc: " + location)
            break
        loc.append(tokens[i])
        #loc = loc + " " + tokens[i] 
        i = i + 1
    return location   

def writeToCSV(locations):
    csvFile = "output.csv"
    with open(csvFile, "w") as f:
        writer = csv.writer(f)
        for loc in locations:
            writer.writerows(loc)

def writeToCSV2(locations):
    csvFile = "output.csv"
    with open(csvFile,'w') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerow(locations)


f = open(filename, "r", encoding="utf8")
transactionCount = 0
Locations = []
for x in f:
  #print(x)
  tokenz = tokenIt(x)
  if isTransaction(tokenz):
      transactionCount = transactionCount + 1
      Locations.append(getLocation(tokenz))
      
      print (transactionCount)
writeToCSV2(Locations)   



  
