"""Script to web scrape gas prices and electricity prices.

Gas prices:
    https://www.eia.gov/petroleum/gasdiesel/
Electricity prices:
    https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_06_b
"""

import requests
import bs4


def get_gas_prices(url='https://www.eia.gov/petroleum/gasdiesel/'):
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='html.parser')

    table = soup.table
    rows = table.find_all('tr')
    prices = {}
    for row in rows:
        tds = row.find_all('td')
        if len(tds) == 0:
            continue
        else:
            prices[tds[0].text] = float(tds[3].text)
    return prices


def state_to_PADD(state):
    state_to_PADD_dict = {
        'Alabama': 'PADD 3',
        'Alaska': 'PADD 5',
        'Arizona': 'PADD 5',
        'Arkansas': 'PADD 3',
        'California': 'PADD 5',
        'Colorado': 'PADD 4',
        'Connecticut': 'PADD 1A',
        'Delaware': 'PADD 1B',
        'Florida': 'PADD 1C',
        'Georgia': 'PADD 1C',
        'Hawaii': 'PADD 5',
        'Idaho': 'PADD 4',
        'Illinois': 'PADD 2',
        'Indiana': 'PADD 2',
        'Iowa': 'PADD 2',
        'Kansas': 'PADD 2',
        'Kentucky': 'PADD 2',
        'Louisiana': 'PADD 3',
        'Maine': 'PADD 1A',
        'Maryland': 'PADD 1B',
        'Massachusetts': 'PADD 1A',
        'Michigan': 'PADD 2',
        'Minnesota': 'PADD 2',
        'Mississippi': 'PADD 3',
        'Missouri': 'PADD 2',
        'Montana': 'PADD 4',
        'Nebraska': 'PADD 2',
        'Nevada': 'PADD 5',
        'New Hampshire': 'PADD 1A',
        'New Jersey': 'PADD 1B',
        'New Mexico': 'PADD 3',
        'New York': 'PADD 1B',
        'North Carolina': 'PADD 1C',
        'North Dakota': 'PADD 2',
        'Ohio': 'PADD 2',
        'Oklahoma': 'PADD 2',
        'Oregon': 'PADD 5',
        'Pennsylvania': 'PADD 1B',
        'Rhode Island': 'PADD 1A',
        'South Carolina': 'PADD 1C',
        'South Dakota': 'PADD 2',
        'Tennessee': 'PADD 2',
        'Texas': 'PADD 3',
        'Utah': 'PADD 4',
        'Vermont': 'PADD 1A',
        'Virginia': 'PADD 1',
        'Washington': 'PADD 5',
        'West Virginia': 'PADD 1',
        'Wisconsin': 'PADD 2',
        'Wyoming': 'PADD 4'
    }

    PADD_to_row_title_dict = {
        'PADD 1': 'East Coast (PADD1)',
        'PADD 1A': 'New England (PADD1A)',
        'PADD 1B': 'Central Atlantic (PADD1B)',
        'PADD 1C': 'Lower Atlantic (PADD1C)',
        'PADD 2': 'Midwest (PADD2)',
        'PADD 3': 'Gulf Coast (PADD3)',
        'PADD 4': 'Rocky Mountain (PADD4)',
        'PADD 5': 'West Coast (PADD5)',
    }
    return PADD_to_row_title_dict[state_to_PADD_dict[state]]

def get_gas_by_state(state):
    return get_gas_prices()[state_to_PADD(state)]


def get_electricity_prices(url='https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_06_b'):
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='html.parser')

    table = soup.find_all('table')[1]
    rows = table.find_all('tr')
    prices = {}
    for row in rows:
        tds = row.find_all('td')
        if len(tds) == 0:
            continue
        else:
            prices[tds[0].text] = float(tds[1].text)
    return prices

def get_electricity_by_state(state):
    return get_electricity_prices()[state]