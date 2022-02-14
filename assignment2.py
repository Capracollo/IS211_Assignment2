import argparse
import urllib.request
import logging
from datetime import datetime


def downloadData(url):
    """Downloads the data"""

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return data
    except Exception as error:
        print("Uh Oh. Double check the url you entered and try again.")
        exit()


def processData(file_content):
    """Decodes and breaks CSV data up then stores it in a dictionary """

    person_data = {}
    split_list = file_content.splitlines()
    format = "%d/%m/%Y"
    index = 1

    for i in split_list:
        a = i.decode("utf-8")  # decodes each entry
        b = a.split(",")  # splits each entry into it's own list
        try:
            date_req_format = datetime.strptime(b[2], format).date()  # formats datetime obj
            person_data[b[0]] = (b[1], date_req_format)  # adds entries to dictionary
        except ValueError:
            logging.error("Error processing line #{} for ID #{}".format(index, b[0]))

        index += 1

    return person_data  # returns dictionary


def displayPerson(id, personData):
    """Gets name and bday of a user"""

    try:
        name, date = personData[str(id)]
        print("Person #{} is {} with a birthday of {}".format(id, name, date))
    except:
        print("No user found with that ID")


def main(url):
    print(f"Running main with URL = {url}...")

    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
    logging.getLogger("assignment2")
    logging.basicConfig(filename="error.log", level=logging.ERROR, format=LOG_FORMAT, filemode="w")

    csvData = downloadData(url)
    personData = processData(csvData)

    # prompts user for ID input until they give a value of <= 0
    val = True

    while val > 0:
        val = int(input("Enter a user ID: "))
        if val < 1:
            exit()
        else:
            displayPerson(val, personData)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)