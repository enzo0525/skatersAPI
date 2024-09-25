import requests
import json
import string
from bs4 import BeautifulSoup
from database import add_skater_database

LETTERS = list(string.ascii_lowercase)
MAIN_DIV_CLASS = 'css-42igy1'
INNER_DIV_CLASS = 'css-0'
LINKS_CLASS = 'chakra-link css-spn4bz'
SCRIPT_ID = '__NEXT_DATA__'

def get_full_prize(tournament_list):
    total_prize = 0

    for tournament in tournament_list:
        if tournament['PrizeMoney'] != '':
            total_prize += int(float(tournament['PrizeMoney'])) #Can't transform base 10 to int, first need to transform to float, then int.

    return total_prize

def get_info():
    for letter in LETTERS:
        letter_response = requests.get(f'https://theboardr.com/skateboarders_list/{letter}')
        letter_soup = BeautifulSoup(letter_response.text, 'html.parser')

        main_div = letter_soup.find('div', class_=MAIN_DIV_CLASS)
        inner_divs = main_div.find_all('div', class_=INNER_DIV_CLASS)

        for div in inner_divs:
            skater_page = div.find('a', class_=LINKS_CLASS).get('href')

            skater_response = requests.get(f'https://theboardr.com{skater_page}')
            skater_soup = BeautifulSoup(skater_response.text, 'html.parser')

            script_tag = skater_soup.find('script', id=SCRIPT_ID)
            json_data = script_tag.string

            try:
                skater_details = json.loads(json_data).get('props', {}).get('pageProps', {}).get('skaterDetails', [])

                if skater_details:
                    data = skater_details[0]
                    skater_earnings = get_full_prize(data['ContestHistory'])

                    if skater_earnings > 0:
                        skater = {
                            'fName': data['FirstName'],
                            'lName': data['LastName'],
                            'age': data['Age'],
                            'dateOfBirth': data['DateOfBirth'],
                            'gender': data['Gender'],
                            'from': f"{data['City']}, {data['State']}, {data['CountryName']}",
                            'sponsors': data['Sponsors'].split(', '),
                            'stance': data['Stance'],
                            'globalRanking': data['GlobalRanking'],
                            'earnings': skater_earnings
                        }
                        add_skater_database(skater)
                else:
                    print(f'no skater found for {skater_page}')
            except Exception as e:
                print(f'error trying to get {skater_page}, {e}')

if __name__ == '__main__':
    get_info()
    print('finish')