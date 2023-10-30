from Analyzer.Analyzer import commands

def getData(data):
   data = data.replace('\r', '')
   array = data.split('\n')
   array = [elemento for elemento in array if elemento != '']
   return commands(array)