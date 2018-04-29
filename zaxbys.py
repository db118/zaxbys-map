from bs4 import BeautifulSoup
import requests
import os


"""
   Writes to a specified csv file
"""
def write_to_file(filename, state_informations):
    with open(filename, 'a') as fopen:
        for key in state_informations:
            fopen.write(state_informations[key]['address'] + ' + ' + state_informations[key]['city'] + "\n")

def get_state_names(location_url):
    # Get all state_names location data from zaxbys homepage
    page = requests.get(location_url)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    options = soup.find(id='state-selector').find_all('option')[1:]
    return [option['value'] for option in options]

def get_location_list(location_url, state_name):
    # Get desired location data from zaxbys
    state_url = location_url + '/' + state_name + '/'
    page = requests.get(state_url)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    locations = soup.find(class_='location-ctn').find_all(class_="location-address-ctn")
    state_information = dict()
    for index, location in enumerate(locations):
        state_information[index] = dict()
        location_address = location.find(class_="location-address").find_all('p')
        state_information[index]['address'] = location_address[0].contents[0]
        state_information[index]['city'] = location_address[1].contents[0]
    return state_information

"""
   Scrapes state data for the amount of zaxbys in the state
"""
def main():
    filename = "test_data.txt"
    with open(filename, 'w') as fopen: 
        fopen.write('')
    location_url = 'https://www.zaxbys.com/locations/'

    state_names = get_state_names(location_url)

    for state_name in state_names:
        state_information = get_location_list(location_url, state_name)
        print(str(state_name) + " " + str(len(state_information)))
        write_to_file(filename, state_information)





                
if __name__ == "__main__":
    main()


