import argparse
import urllib.request
import logging
import datetime


def downloadData(url):
#Downloads and decode data from a url
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")
            return data
    except Exception:
        print("Check that the url was entered correctly and try again")
        exit()


def processData(file_content):
#Parses data from CSV and store it in a dictionary
    birthdate_dict = {}
    parse_data = file_content.splitlines()
    index = 2
    header = True
    for datedata in parse_data:
        if header:
            header = False
            continue
        datesection = datedata.split(",")
        try:
            formatted_date = datetime.datetime.strptime(datesection[2], "%d/%m/%Y").date()
            birthdate_dict[int(datesection[0])] = (datesection[1], formatted_date)
        except ValueError:
            logging.error(f"Error processing line #{index} for ID #{datesection[0]}")
        index += 1

    return birthdate_dict

  
def displayPerson(id, personData):
#Prints name and birthday identified by input id
    try:
        name, date = personData[id]
        print(f"Person #{id} is {name} with a birthday of {date}")
    except:
        print("No user found with that id")


def main(url):
    print(f"Running main with URL = {url}...")
    logging.getLogger("assignment2")
    logging.basicConfig(
        filename="error.log",
        level=logging.ERROR,
        format="%(levelname)-8s %(message)s",
        filemode="w"
    )

    csvData = downloadData(url)
    personData = processData(csvData)

    user_input = True
    while user_input > 0:
        user_input = int(input("Enter ID: "))
        if user_input <= 0:
            exit()
        else:
            displayPerson(user_input, personData)

if __name__ == "__main__":
#Main entry point
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)