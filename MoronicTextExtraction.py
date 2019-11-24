import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import csv

smsText = "Purchase of AED 6.19 with Debit Card ending 2932 at W MART SUPERMARKET MARI, DUBAI. Avl Balance is AED 1,244.68."

filename = "C:\\pyy\\ENBDMessages.txt"

class Transactions:
    def __init__(self, amount, location, timestamp, balance, transactionType):
        self.amount = amount
        self.location = location
        self.timestamp = timestamp
        self.balance = balance
        self.transactionType = transactionType
    
def tokenIt(text):
    #tokens = nltk.word_tokenize(text)
    tokens = text.split()
    return tokens

def prepareTransactionIdentifiers():
    ListOfWords = []
    #PSDCwRC
    ListOfWordsForPurchase = ["Purchase", "Avl", "Balance", "AED", "Debit", "Card"]
    ListOfWordsForSalary = ["Salary", "credited", "account"]
    ListOfWordsForDebit = ["has", "been", "debited", "account" ]
    ListOfWordsForWithdrawal = ["Cash", "Withdrawal", "Debit", "Card"]
    ListOfWordsForRefund = ["Purchase", "Debit", "Card", "refunded"]
    ListOfWordsForCredit = ["credited", "Current", "balance"]

    ListOfWords.append(ListOfWordsForPurchase)
    ListOfWords.append(ListOfWordsForSalary)
    ListOfWords.append(ListOfWordsForDebit)
    ListOfWords.append(ListOfWordsForWithdrawal)
    ListOfWords.append(ListOfWordsForRefund)
    ListOfWords.append(ListOfWordsForCredit)

    return ListOfWords


def isTransaction(tokens):
    ListOfWords = prepareTransactionIdentifiers()    
    listIndex = 0
    for SubList in ListOfWords:        
        result = all(elem in tokens for elem in SubList)
        #x = listIndex if result else (listIndex += 1)
        if result: 
            return listIndex
        else: 
            listIndex += 1
    return -1


def extractofy(tokens, listIndex):
    #if purchase extract words
    #if salary extract 
    #PSDCwRC
    features = [[["at", "Avl"], 6, -4, -3, "Purchase"], ["ADCB", 6, -4, -3, "Salary"], ["ENBD", 4, -4, -3, "Debit"], ["Withdraw", 7, -4, -3, "Withraw"], [["at", "on"], 7, -4, -3, "Refund"], ["Deposit", 4, 15, -3, "Credit"]]
    featuresOf = features[listIndex]
    location = getValue(tokens, featuresOf[0] )
    amount = getValue(tokens, featuresOf[1])
    balance = getValue(tokens, featuresOf[2])
    #balance = balance.replace(".,", "")
    timestamp = getValue(tokens, featuresOf[3])
    #timestamp = timestamp.replace(",", "")
    #TODO: Write get type function
    transactionType = featuresOf[4]
    #transactionType = "DUMMY VALUE"
    transaction = Transactions(amount, location, timestamp, balance, transactionType)
    return transaction

def getValue(tokens, features):
    if isinstance(features, list):
        start = tokens.index(features[0]) + 1
        end = tokens.index(features[1])
        loc = tokens[start:end]
        return " ".join(loc)
    elif isinstance(features, str):
        return features
    val = tokens[features]
    val = val.replace(".,", "")
    val = val.replace(",", "")
    return val 


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

def writeToCSV2(rows):
    csvFile = "outputTransactions.csv"
    with open(csvFile,'w') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        transactions = []
        for row in rows:
            t = "Amount: " + row.amount + " | Location: " + row.location + " | Timestamp: " + row.timestamp + " | Balance: " + row.balance + " | Type: " + row.transactionType
            transactions.append(t)
        wr.writerow(transactions)

#Main flow
f = open(filename, "r", encoding="utf8")
transactionCount = 0
Locations = []
TransactionList = []
for row in f:
  #print(x)
  tokens = tokenIt(row)
  listIndex = isTransaction(tokens)
  if listIndex > -1:
      TransactionList.append(extractofy(tokens, listIndex))
      #transactionCount = transactionCount + 1
      #Locations.append(getLocation(tokens))
      #print (transactionCount)
writeToCSV2(TransactionList)   



  
