# Importing the Necessary Libraries
from playwright.sync_api import sync_playwright
import re
from pathlib import Path


#Call User Input
webPage = input("Please Enter The URL Of Desired Site: ")
date = input("Please enter the date of the records: ")


status = False
filePath = Path("./AthleticRecords.csv")
if filePath.is_file():
    status = True
print(status)

if (webPage == "https://oh.milesplit.com/meets/576849-ohio-capital-conference-central-2023/results/979142/formatted/?type=formatted&event="):
   
    # The Function Scrapes The MileSplit Website
    def scrapeMilesOH(site):


        # Initializes PlayWright
        with sync_playwright() as play:


            # Helps Launch The Browser Without The Need Of A GUI (Graphical User Interface)
            browser = play.chromium.launch(headless = True)


            # Initializes A New Page TO Help With The Following Interactions
            page = browser.new_page()


            # Accesses The Desired URL
            page.goto(site)


            # Wait for the table to load
            page.wait_for_selector("table")
           
            #Setting The Headers
            finalHeaders = ["Athlete", "School", "Time"]


            # Extract table content
            rows = page.query_selector_all("table tr")


            # Remove The First Element Of Rows In Order To Help Separate The Two Tables Later On
            rows.pop(0)


            data = []


            # Run A For Loop Through The Table Content (Row By Row)
            for row in rows:
               
                # This Allows To Extract Each Cell In The Table With The Attribute of <td>
                cells = row.query_selector_all("td")
               
                # This Is The Unformatted Record For All Entries In Table
                original = [cell.text_content().strip() for cell in cells]


                formattedRecords = []


                # This Method Runs Through The Unformatted List & Formats Each Record As Well As Add N/A For The Empty Records
                for item in original:
                    if (item == ""):
                       item = "N/A"
                    formattedRecords.append(item)


                # Ensures Only The First Table Of The Webpage Is Extracted
                if (len(formattedRecords) == 0):
                    break    
               
                # Add All Final Formatted Records To Final List
                data.append([formattedRecords[2], formattedRecords[4], str(date) + ": " + formattedRecords[5]])


            finalData = [finalHeaders] + data


            # Ends Browser Session
            browser.close()


            return finalData


    # Extracts Only Coffman Records From The Entire List Of Entries
    def coffmanExtracter():


        # Utilizes Previously Built Function
        entries = scrapeMilesOH(webPage)
        coffmanEntries = []
        coffmanEntries.clear()
        coffmanEntries = [entries[0]]


        # Runs Through All Entries & Selects The Entries Containing Dublin Coffman Students
        for entry in entries:
            if any("Dub. Coffman" in cell for cell in entry) or any("Dublin Coffman" in cell for cell in entry):
                coffmanEntries.append(entry)
       
        if status == True:
            print("Successfully opened existing file.")


            list = []
            finalList = []
            with open("AthleticRecords.csv", 'r') as file:
              for row in file:
                finalList.append(row)
                list.append(row.strip())
            indeces = []


            for record in list:
                string = record
                for item in coffmanEntries:
                    if (item[0] in string and "Time" not in string):
                        string = string + ", " + item[len(item) - 1] + "\n"
                        coffmanEntries.remove(item)
                if (string != record):
                    indeces.append(list.index(record))
                    list[len(indeces) - 1] = string


            for x in range(len(finalList)):
                for y in indeces:
                    if (x == y):
                        finalList[x] = list[y]


            if len(coffmanEntries) != 0:
                for record in coffmanEntries:
                    String = str(record[0])
                    for item in record:
                        if (item == record[len(record) - 1]):
                            String = String + ", " + str(item) + "\n"
                        else:
                            String = String + ", " + item
                    finalList.append(String)


            return finalList, True
           
        else:
            return coffmanEntries, False
       


    #All Data Concerning Coffman Atheletes
    exportingData = coffmanExtracter()


    # Transmits The Data To A CSV File
    def exportToCSV(data, fileName, status):
        if (status == False):
            # Organizing The Table Content
            headers = data[0]
            records = data[1:]
           
            fileN = fileName
            with open(fileN, "w") as file:
                stringHe = headers[0]
                for i in range(1, len(headers)):
                    if (i == len(headers) - 1):
                        stringHe = stringHe + ", " + headers[i] + "\n"
                    else:
                        stringHe = stringHe + ", " + headers[i]
                file.write(stringHe)


                for record in records:
                    string = str(record[0])
                    for i in range(1, len(record)):
                        if (i == len(record) - 1):
                            string = string + ", " + record[i] + "\n"
                        else:
                            string = string + ", " + record[i]
                    file.write(string)
           
            # Provides Confirmation To User of Success
            print("Data has been saved to " + fileName)


        if (status == True):
            headers = data[0]
            records = data[1:]


            with open("AthleticRecords.csv", "w") as file:
                pass
            with open("AthleticRecords.csv", "w") as file:
                file.write(headers)
                for item in records:
                    file.write(item)


            print("Data has been updated to AthleticRecords.csv")


    exportToCSV(exportingData[0], "AthleticRecords.csv", exportingData[1])


if (webPage == "https://www.athletic.net/CrossCountry/meet/251065/results/1003101"):
    def parseTheRecord(string):
        # To determine if a given re matches the beginning of a string helping to parse the school and time
        schoolNameMatch = re.match(r"^(.*?)\s\d{1,2}:\d{2}\.\d{2}", string)
        timeMatch = re.search(r"\d{1,2}:\d{2}\.\d{2}", string)  


        # To define the school, time, and year
        schoolName = schoolNameMatch.group(1)
        time = str(date) + ": " + timeMatch.group(0)


        # Return the parsed data
        return [schoolName, time]


    def scrapeAthleticNet(site):
        # Initializes PlayWright       
        with sync_playwright() as play:


            # Helps Launch The Browser Without The Need Of A GUI (Graphical User Interface)           
            browser = play.chromium.launch(headless = True)


            # Initializes A New Page TO Help With The Following Interactions
            page = browser.new_page()


             # Accesses The Desired URL           
            page.goto(site)


            # Wait for the table to load
            page.wait_for_selector("div.has-logos.ng-star-inserted")
           
            #Locate all div tags containing each record
            rows = page.query_selector_all("div.d-grid.result-row.ng-star-inserted")


            records = []


            #Format each record
            for row in rows:
                # Split The Record Into An Array
                record = row.text_content().split("  ")


                # Remove The Initials Before The Name
                if (len(record[1]) == 2 and str(record[1]).isupper()):
                    record.remove(record[1])


                # Format the 3rd element with the unformatted string
                formatted = parseTheRecord(record[2])
                record.pop(2)


                # Replace the 3rd element with the formatted strings
                for item in formatted:
                    record.append(item)


                # Remove unneccessary place in record
                record.pop(0)


                records.append(record)
           
            # Add the headers to the list
            headers = ["Athlete", "School", "Time"]
            records.insert(0, headers)


            return records
       
    # Extracts Only Coffman Records From The Entire List Of Entries
    def coffmanExtracter():


        # Utilizes Previously Built Function
        entries = scrapeAthleticNet(webPage)
        coffmanEntries = []
        coffmanEntries.clear()
        coffmanEntries = [entries[0]]


        # Runs Through All Entries & Selects The Entries Containing Dublin Coffman Students
        for entry in entries:
            if any("Dublin Coffman" in cell for cell in entry) or any("Dub. Coffman" in cell for cell in entry):
                coffmanEntries.append(entry)
       
        if status == True:
            print("Successfully opened existing file.")


            list = []
            finalList = []
            with open("AthleticRecords.csv", 'r') as file:
              for row in file:
                finalList.append(row)
                list.append(row.strip())
            indeces = []


            for record in list:
                string = record
                for item in coffmanEntries:
                    if (item[0] in string and "Time" not in string):
                        string = string + ", " + item[len(item) - 1] + "\n"
                        coffmanEntries.remove(item)


                if (string != record):
                    indeces.append(list.index(record))
                    list[len(indeces) - 1] = string


            for x in range(len(finalList)):
                for y in indeces:
                    if (x == y):
                        finalList[x] = list[y]


            coffmanEntries.pop(0)
            if len(coffmanEntries) != 0:
                for record in coffmanEntries:
                    String = str(record[0])
                    for item in record:
                        if (item == record[len(record) - 1] and item not in String):
                            String = String + ", " + str(item) + "\n"
                        else:
                            String = String + ", " + item
                    finalList.append(String)


            return finalList, True
           
        else:
            return coffmanEntries, False
   
   # All Data Concerning Coffman Atheletes
    exportingData = coffmanExtracter()


    def exportToCSV(data, fileName, status):
        if (status == False):
            # Organizing The Table Content
            headers = data[0]
            records = data[1:]
            print(data)
            fileN = fileName
            with open(fileN, "w") as file:
                stringHe = headers[0]
                for i in range(1, len(headers)):
                    if (i == len(headers) - 1):
                        stringHe = stringHe + ", " + headers[i] + "\n"
                    else:
                        stringHe = stringHe + ", " + headers[i]
                file.write(stringHe)


                for record in records:
                    string = str(record[0])
                    for i in range(1, len(record)):
                        if (i == len(record) - 1):
                            string = string + ", " + record[i] + "\n"
                        else:
                            string = string + ", " + record[i]
                    file.write(string)
           
            # Provides Confirmation To User of Success
            print("Data has been saved to" + fileName)


        if (status == True):
            headers = data[0]
            records = data[1:]


            with open("AthleticRecords.csv", "w") as file:
                pass
            with open("AthleticRecords.csv", "w") as file:
                file.write(headers)
                for item in records:
                    file.write(item)


            print("Data has been updated to AthleticRecords.csv")


    exportToCSV(exportingData[0], "AthleticRecords.csv", exportingData[1])