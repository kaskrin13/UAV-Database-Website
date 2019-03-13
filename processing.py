# Takes a text file that contains the absolute file names of images for website v1
# Gets relevant info from file names places into list and returns the list for website
# Assumes the files have been processed to thumbnails and placed in appropriate folder for website /static/images/YYYY

# Generate the file with the following command in powershell (assumes you are in the correct directory):
# Get-ChildItem -Path *.jpg -Recurse | Select-Object -ExpandProperty FullName > filenames.txt
from datetime import datetime
import re

# Separates file names from file paths
def getFileNames(lines):
    fileNames = []
    for line in lines:
        if line.find("Bands/") > 0:
            fileNames.append(line[line.find("Bands/")+6:])
        elif line.find("RGB/") > 0:
            fileNames.append(line[line.find("RGB/")+4:])
    return fileNames

# Separates file paths from file names
# creates absolute path
def getAbsoluteFilePaths(lines):
    filePaths = []
    for line in lines:
        if line.find("Bands/") > 0:
            filePaths.append(line[:line.find("Bands/")+6])
        if line.find("RGB/") > 0:
            filePaths.append(line[:line.find("RGB/")+4])
    return filePaths

# Separates file paths from file names
# creates relative path
def getRelativeFilePaths(lines):
    filePaths = []
    for line in lines:
        if line.find("Bands/") > 0:
            filePaths.append(line[line.find("static/")+7:line.find("Bands/")+6])
        if line.find("RGB/") > 0:
            filePaths.append(line[line.find("static/")+7:line.find("RGB/")+4])
    return filePaths

# Splits the parts of the file name into separate parts to populate html template
def splt(string):
    splitted = string.split("_")
    # Remove -thumb.jpg from file name
    splitted[-1] = splitted[-1].split("-")[0]
    return splitted

def getPlatforms(filePaths):
    platforms = []
    for path in filePaths:
        platforms.append(path.split("/")[2])
    return platforms

def getFarms(filePaths):
    farms = []
    for path in filePaths:
        farms.append(path.split("/")[3])
    return farms

def getNames(fileNames):
    names = []
    for fileName in fileNames:
        names.append(fileName[0])
    return names

def getAltitudes(fileNames):
    altitudes = []
    for fileName in fileNames:
        altitudes.append(fileName[1])
    return altitudes

def getSensors(fileNames):
    sensors = []
    for fileName in fileNames:
        sensors.append(fileName[2])
    return sensors

def getDates(fileNames):
    dates = []
    for fileName in fileNames:
        # Remove parenthesis from file name
        dates.append(fileName[4].strip("()"))
    return dates

def getImageTypes(fileNames):
    imageTypes = []
    for fileName in fileNames:
        # processed RGB images are called group1
        if fileName[7] == "group1":
            imageTypes.append("RGB")
        else:
            imageTypes.append(fileName[7].capitalize())
    return imageTypes

# Converts date from m-d-yy or m-d-yyyy to yyyymmdd
# used to name generated html files
def fileNameDate(origDate):
    date = parseMultipleFormats(origDate)
    return date.strftime("%Y%m%d")

# Parses multiple date formats
def parseMultipleFormats(text):
    for fmt in ("%m-%d-%y", "%m-%d-%Y"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def getYears(lines):
    pattern = '20\d\d'

    years = set()
    for line in lines:
        r = re.search(pattern, line)
        if r:
            years.add(r.group(0))

    yearAndLines = []
    for year in years:
        lst = []
        for line in lines:
            if re.search(year, line):
                lst.append(line)
        yearAndLines.append([year, lst])

    return yearAndLines

def processYear(lines):
    fileNames = getFileNames(lines)
    filePaths = getRelativeFilePaths(lines)

    data = []

    for i in range(len(fileNames)):
        data.append(splt(fileNames[i]))

    names = getNames(data)
    altitudes = getAltitudes(data)
    sensors = getSensors(data)
    dates = getDates(data)
    imageTypes = getImageTypes(data)
    platforms = getPlatforms(filePaths)
    farms = getFarms(filePaths)

    # List containing lists of strings needed for html page
    fieldInfo = [filePaths, fileNames, names, altitudes, sensors, dates, imageTypes, farms, platforms]

    # Convert columns to rows
    fieldInfo = [list(x) for x in zip(*fieldInfo)]

    return fieldInfo

def main():
    # Location of txt file with image files to be added
    file = "static/images/filenames.txt"
    with open(file, "r", encoding="utf-16") as f:
        lines = f.readlines()

    f.close()

    # Remove trailing characters
    #for i in range(len(lines)):
    #    lines[i] = lines[i].rstrip('    \n')
    lines = [line.rstrip('    \n') for line in lines]

    # Convert from \ (used in windows) to /
    #for i in range(len(lines)):
    #    lines[i] = lines[i].replace("\\", "/")
    lines = [line.replace("\\", "/") for line in lines]

    years = getYears(lines)
    for year in years:
        year[1] = processYear(year[1])

    return years

if __name__ == "__main__":
    main()
