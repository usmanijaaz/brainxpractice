import re
import spacy
from spacy.tokens import Span
from spacy import displacy
import os
import pathlib
import nltk
from nltk.corpus import stopwords
# import RegexpTokenizer() method from nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer


termIds = {}
termCount={}

def Stemming(tokens):
  output=[]
  st = PorterStemmer()
  for line in tokens:
    output.append(" ".join([st.stem(i) for i in line.split()]))
  return output


stopwords = open('stoplist.txt','r')
stops = stopwords.readlines()
stoplist = []
for word in stops:
    stoplist.append(word.strip())


def getFiles(path):
    Files = []
    for path1 in pathlib.Path(path).iterdir():
        if path1.is_file():
          Files.append(path1)
    return Files

def removeWords(list, obj):
    tex = obj.__str__()
    for token in obj:
        if token.text in list:
            tex = tex.replace(token.text,'')
    return tex

def ExtractDatafromFiles(Files, output):
    docCounter = 0
    termIdCounter = 0

    for file in Files:
        with open(output,'a', encoding='utf-8', errors='ignore') as f1:
            f1.write(docCounter.__str__() + "\t" + file)
            docCounter = docCounter + 1
            f1.write("\n")
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
            #print(data)
            #removing header of file
            text = re.sub("<head>.*?</head>", "", data, flags=re.DOTALL)
            #removing all the HTMl tags from file
            CleanTags = re.compile('<.*?>')
            text = re.sub(CleanTags,'', text)
            #converting to lower case
            text = text.lower()
            #removing stop words
            nlp = spacy.load('en_core_web_sm')
            obj = nlp(text)
            text = removeWords(stoplist, obj)
            #tokenization
            # Create a reference variable for Class RegexpTokenizer
            tk = RegexpTokenizer('\s+', gaps=True)
            # Use tokenize method
            tokens = tk.tokenize(text)
            #Stemming
            StemmedList = Stemming(tokens)
            #creating files
            for word in StemmedList:
                if word not in termIds:
                    if word not in termIds.values():
                        termIds[termIdCounter] = word
                        termCount[termIdCounter] = 1
                        termIdCounter = termIdCounter + 1
                    else:
                        key_list = list(termIds.keys())
                        val_list = list(termIds.values())
                        position = val_list.index(word)
                        termCount[position] += 1




def writeFiles(terms, docindex):
    f = open('terms.txt', 'a')
    f1 = open('docindex.txt', 'a')
    for i in range(len(termIds)):
        f.write(i.__str__() + "\t" + termIds[i])
        f.write('\n')
        f1.write("1" + "\t" + termIds[i] + "\t" + termCount[i].__str__())
        f1.write('\n')









if __name__ == '__main__':
    dir = input('enter directory name: ')
    out = input('enter output path dir')
    docid = out + "docids.txt"
    termids = out + "terms.txt"
    docindex = out + "docindex.txt"

    ExtractDatafromFiles(dir,docid)
    writeFiles(termids,docindex)





