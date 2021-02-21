#%%
import tkinter as tk
from tkinter import ttk
from tkinter import *
import re
import pandas as pd
from utils.classifier import NaiveBayes
from utils.db import Sample, Word

root = tk.Tk()
root.geometry("1000x600")
root.pack_propagate(False)



currentItem = None

tabControl = ttk.Notebook(root)
tabControl.pack(expan = 1, fill = BOTH)

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text = "Samples")

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text = "Classifier")

tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text = "Plot")

#region Tab 1

OptionList = [
"Aries",
"Taurus",
"Gemini",
"Cancer"
] 

variable = tk.StringVar(root)
variable.set("None")

opt = tk.OptionMenu(root, variable, *OptionList)
opt.config(width=100, heigh = 1)
opt.pack(fill  = BOTH)


listbox = Listbox(tab1, width = 150, height = 20)
listbox.pack(anchor = SW, fill = NONE, padx = 10) 

deleteButton = Button(tab1,text = "Delete", width = 10)
def delete(id):
    Sample.objects.get(id=id).delete()
    listbox.delete(0,END)
    insertItems()

deleteButton.config(command = lambda: delete(currentItem))
deleteButton.pack(side = RIGHT, padx = 10)

text = Text(tab1, width = 75, height = 10)
text.pack(side = LEFT)

textStatus = Text(tab1, width = 10, height = 2)
textStatus.pack(side = LEFT, padx = 10)


def updateProbs(text, status):
    for word in text.split():
        try:
            words = Word.objects.filter(word = word.lower())

            if(len(words) != 0):
                wordObj = words[0]
                if(status.lower() == "ham"):
                    spamProb = (wordObj.spams)/(wordObj.occurrences + 1)
                    hamProb = (wordObj.hams + 1)/(wordObj.occurrences + 1)

                    spamProbNormalized = ((wordObj.occurrences + 1) * spamProb + 0.5) / ((wordObj.occurrences + 1) + 1)
                    hamProbNormalized = ((wordObj.occurrences + 1) * hamProb + 0.5) / ((wordObj.occurrences + 1) + 1)

                    Word.objects(id = str(wordObj.pk)).update_one(
                        inc__occurrences = 1,
                        inc__hams = 1,
                        spamProb = spamProb,
                        hamProb = hamProb,
                        spamProbNormalized = spamProbNormalized,
                        hamProbNormalized = hamProbNormalized,
                    )
                if(status.lower() == "spam"):
                    spamProb = (wordObj.spams + 1)/(wordObj.occurrences + 1)
                    hamProb = (wordObj.hams)/(wordObj.occurrences + 1)

                    spamProbNormalized = ((wordObj.occurrences + 1) * spamProb + 0.5) / ((wordObj.occurrences + 1) + 1)
                    hamProbNormalized = ((wordObj.occurrences + 1) * hamProb + 0.5) / ((wordObj.occurrences + 1) + 1)

                    Word.objects(id = str(wordObj.pk)).update_one(
                        inc__occurrences = 1,
                        inc__spams = 1,
                        spamProb = spamProb,
                        hamProb = hamProb,
                        spamProbNormalized = spamProbNormalized,
                        hamProbNormalized = hamProbNormalized,
                    )
                

                wordObj.reload()
            else:
                if(status.lower() == "ham"):
                    Word(
                        word = word,
                        occurrences = 1,
                        hams = 1,
                        spams = 0,
                        spamProb = 0.0,
                        hamProb = 1.0,
                        spamProbNormalized = 0.25,
                        hamProbNormalized = 0.75
                    ).save()
                if(status.lower() == "spam"):
                    Word(
                        word = word,
                        occurrences = 1,
                        hams = 0,
                        spams = 1,
                        spamProb = 1.0,
                        hamProb = 0.0,
                        spamProbNormalized = 0.75,
                        hamProbNormalized = 0.25
                    ).save()

        except Exception as e:
            print(e)

saveButton = Button(tab1,text = "Save", width = 10)
def save(text, status):
    Sample(message = text, status = status).save()
    listbox.delete(0,END)
    insertItems()
    updateProbs(text, status)

saveButton.config(command = lambda: save(re.sub("^\s+|\n|\r|\s+$", '', text.get("1.0",END)), re.sub("^\s+|\n|\r|\s+$", '', textStatus.get("1.0",END))))
saveButton.pack(expand = 1)

def insertItems():
    for sample in Sample.objects:
            listbox.insert(END, sample.message[:15] + "... , " + sample.status.upper() + ", _id: " + str(sample.pk) )

insertItems()

def CurSelect(evt):
    value=str((listbox.get(listbox.curselection())))
    global currentItem
    try:
        currentItem = value.split(", _id: ")[1]
    except Exception:
        print("Item doesn't fit")

listbox.bind('<<ListboxSelect>>',CurSelect)

#endregion

#region Tab 2

textToClassify = Text(tab2, width = 75, height = 10)
textToClassify.pack(side = LEFT, anchor = NE)

classifyButton = Button(tab2,text = "Classify", width = 10)
def classify():
    pass

classifyButton.config(command = lambda: classify())
classifyButton.pack( padx = 10, )

addButton = Button(tab2,text = "Right", width = 10, bg = "green2")
def add():
    pass

addButton.config(command = lambda: add())
addButton.pack(side = RIGHT, padx = 10, expand = 1)  

#endregion

root.mainloop()