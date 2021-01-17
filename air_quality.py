import csv
import copy


def print_menu():
    print("Choose one of the options:")
    print("0 - Exit")
    print("1 - Print statistics")
    print("2 - Print the verbal air quality table.")


def NumbersIntoWords(maksimilista):
    listOfWords = []
    
    for i in maksimilista:
        if i == -1:
            listOfWords.append("-")
        elif i < 51:
            listOfWords.append("Good")
        elif 51 <= i <= 75:
            listOfWords.append("Satisfactory")
        elif 76 <= i <= 100:
            listOfWords.append("Fair")
        elif 101 <= i <= 150:
            listOfWords.append("Poor")
        elif i > 150:
            listOfWords.append("Very poor")
            
    return listOfWords


def PrintStats(paikat, UudetMaksimit, UusiPyoristetty, sanat):
    
    print("Printing the maximum and average air quality index by measurement site.")
    print("{:<15s} {:<7s} {:<7s} {:<15s}".format("Location", "Maximum", "Average", "Average Air Quality"))
    for i in range(len(paikat)):
        print("{:<15s} {:<7d} {:<7d} {:<15s}".format(paikat[i], UudetMaksimit[i], UusiPyoristetty[i], sanat[i]))
        
    print("")
    
    
def PrintVerbalTable(PlacesAndTimestamps, newList, allWords):
    
    print("The air quality as a verbal table")
    print("---------------------------------")
    for i in PlacesAndTimestamps:
        print('{:<16s}'.format(i), end=' ')
    print("")
    for i in range(len(allWords[0])):
        for lista in newList:
            print('{:<16s}'.format(lista[i]), end=' ')
        print()
    print("")


def FindIncorrectLinesAndValues(temp1, temp2):
    incorrectLines = []
    for i in range(0, len(temp1)):
            if (len(temp2[i]) == len(temp2[0])):
                for numero in temp2[i]:
                    if numero == '-1':
                        print("An incorrect value in line:",''.join(temp1[i]))
            elif (len(temp2[i]) != len(temp2[0])):
                print("Incorrect line:",''.join(temp1[i]))
                incorrectLines.append(temp2[i])
                
    return incorrectLines


def cleanData():
    try:
        filename = input("Enter the name of the file to be read:\n")
        x = 1
        temp1 = []
        temp2 = []
        temp3 = []
        with open(filename, 'r') as f:
            for row in f:
                row = row.strip()
                splitRow = row.split(",")
                temp1.append(row)
                temp2.append(splitRow)
                temp3.append(splitRow)
        
        for lista in temp3:
            lista.pop(0)
        temp3.pop(0)
        
        #Changes every datapoint where there is no data to '-1'            
        for i, x in enumerate(temp3):
            for j, a in enumerate(x):
                if 'NoData' in a:
                    temp3[i][j] = a.replace('NoData', '-1')
                                
        EmptyList = []
        for i in range(len(temp2[0])):
            EmptyList.append(-1)
        
        listOfData = []
        for lst in temp3:
            if (len(lst) != len(temp2[0])):
                listOfData.append(EmptyList)
            else:
                listOfData.append(lst)
        
        return temp1, temp2, listOfData, filename
                
    except OSError:
        print("Error in reading the file '{}'.".format(filename))
        print("Program ends.")
        exit()
        
        
def readData(listOfData, filename):
    print("The file has been read.")
    with open(filename, 'r') as csv_file:
        csv_array = []
        csv_reader = csv.reader(csv_file)  
        for row in csv_reader:
            csv_array.append(row)
            
        locationsAndTimes = []
        for i in csv_array[0]:
            locationsAndTimes.append(i)
            
        times = []
        for i in csv_array:
            times.append(i[0])
        times.pop(0)
            
        locations = csv_array[0]
        allDataPoints = [[] for i in range(len(locations))]
        csv_array.pop(0)
            
        for rivi in listOfData:
            for i in range(len(locations)):
                allDataPoints[i - 1].append(rivi[i - 1])
        locations.pop(0)
            
        allDataPoints = allDataPoints[:-1]         
        for i in allDataPoints:
            for j in range(0, len(allDataPoints[0])):
                i[j] = int(i[j])
                   
        ViimeinenLista = copy.deepcopy(allDataPoints)
            
        for list in allDataPoints:
            for j in list:
                try:
                    list.remove(-1)
                except ValueError:
                    pass
                    
        listOfAverages = []
        for i in allDataPoints:
            average = sum(i) / len(i)
            listOfAverages.append(average)
                
        roundedAverages = [round(x) for x in listOfAverages]
        airQualitiesAsWords = NumbersIntoWords(roundedAverages)
        maximums = [max(s) for s in allDataPoints]
                
        temp = []
        allWords = []
        for i in range(len(locations)):
            newNumbers = [int(h) for h in ViimeinenLista[i]]
            temp = NumbersIntoWords(newNumbers)
            allWords.append(temp)
                
        arrayOfRawData = []
        arrayOfRawData.append(times)
        for i in allWords:
            arrayOfRawData.append(i)
                
    return locations, maximums, roundedAverages, airQualitiesAsWords, locationsAndTimes, arrayOfRawData, allWords
                
    
def main():
    print("The program calculates and visualises air quality.")
    temp1, temp2, listOfData, filename = cleanData()
    incorrectLines = FindIncorrectLinesAndValues(temp1, temp2)
    temp1.pop(0)
        
    if len(incorrectLines) == len(temp1):
        print("The file has been read.")
        print("Not enough data for statistics.")
        print("Program ends.")
    else:
        locations, maximums, roundedAverages, airQualitiesAsWords, locationsAndTimes, arrayOfRawData, allWords = readData(listOfData, filename)
        
        while True:
            try:
                print_menu()
                choiceOfAction = int(input(""))
                if choiceOfAction == 0:
                    print("Program ends.")
                    break
                elif choiceOfAction == 1:
                    PrintStats(locations, maximums, roundedAverages, airQualitiesAsWords)
                elif choiceOfAction == 2:
                    PrintVerbalTable(locationsAndTimes, arrayOfRawData, allWords) 
            except ValueError:
                print("The choice must be an integer.")
            
main()
