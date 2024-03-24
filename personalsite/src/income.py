from bs4 import BeautifulSoup
from .util import *
# from util.get_site import get_site
# from util.process import rev_to_int, strip_parentheses, eps_to_float
import requests
import csv

# Set the headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
}


def custom_fin_table(tag):
    return tag.name == 'table' and 'Financials - data table' in tag.attrs.get('aria-label', '')

def custom_fcf_table(tag):
    return tag.name == 'table' and 'Financials - Financing Activities data table' in tag.attrs.get('aria-label', '')

def company_income(ticker):
    '''
    Returns tuple of 5 elements: (string, list, int, list, int)
    Revenue history, Revenue growth, EPS history, EPS growth
    '''

    url = f"https://www.marketwatch.com/investing/stock/{ticker}/financials/income/quarter"
    # Send a GET request to the website with headers
    response = get_site(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # find table with custom attributes
    fin_table = soup.find_all(custom_fin_table)[0]
    tbl_rows = fin_table.find_all('tr')

    # get header row from table
    header = tbl_rows[0].find_all('th')
    report_date = header[-2].get_text()
    
    # get revenue data from table
    # quarters oldest to newest
    rev = tbl_rows[1].find_all('td')
    revq = [r.get_text() for r in rev][1:-1]
    # print(revq)

    # calculate the rev growth yoy
    newq = rev_to_int(revq[4])
    oldq = rev_to_int(revq[0])
    rev_growth = round((newq - oldq) / oldq * 100)
    # print(rev_growth)

    # get eps data from table
    # quarters oldest to newest
    eps = tbl_rows[52].find_all('td')
    epsq = [strip_parentheses(r.get_text()) for r in eps][1:-1]
    # print(epsq)

    # calculate eps growth yoy
    new_eps = eps_to_float(epsq[4])
    old_eps = eps_to_float(epsq[0])
    eps_growth = round((new_eps - old_eps) * 100 / abs(old_eps))
    # print(eps_growth)
    
    return report_date, revq, rev_growth, epsq, eps_growth
    
def company_fcf(ticker):
    '''
    Returns tuple of 2 elements
    FCF history, FCF growth
    '''
    
    url = f"https://www.marketwatch.com/investing/stock/{ticker}/financials/cash-flow/quarter"

    # Send a GET request to the website with headers
    response = get_site(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # find table with custom attributes
    fin_table = soup.find_all(custom_fcf_table)[0]
    tbl_rows = fin_table.find_all('tr')

    # fcf quarters oldest to newest
    fcf = tbl_rows[23].find_all('td')
    fcfq = [r.get_text() for r in fcf][1:-1]

    # calc fcf growth yoy
    new_fcf = rev_to_int(fcfq[4])
    old_fcf = rev_to_int(fcfq[0])
    fcf_growth = round((new_fcf - old_fcf) / abs(old_fcf)*100)
    
    return fcfq, fcf_growth

def company_ratios(ticker):
    '''
    Returns tuple of 2 lists
    Past four quarters PEG and PS ratios for _ticker 
    '''
    url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}"

    # Send a GET request to the website with headers
    response = get_site(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # get the valuation table and its rows
    fin_table = soup.find_all('table')[0]
    tbl_rows = fin_table.find_all('tr')

    # get price/earnings/growth ratio newest to oldest
    # number getting smaller and below 1 is better
    peg = tbl_rows[5].find_all('td')
    pegq = [r.get_text() for r in peg][2:]

    # get price/sales ratio newest to oldest
    ps = tbl_rows[6].find_all('td')
    psq = [r.get_text() for r in ps][2:]

    return pegq, psq

def prior_annual_stats(ticker):
    '''
    Returns string
    Previous fiscal annual revenue for _ticker 
    '''
    url = f"https://www.marketwatch.com/investing/stock/{ticker}/financials/income"

    # Send a GET request to the website with headers
    response = get_site(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # find table with custom attributes
    fin_table = soup.find_all(custom_fin_table)[0]
    tbl_rows = fin_table.find_all('tr')

    # get revenue of last fiscal year from table
    rev = tbl_rows[1].find_all('td')
    revy = [r.get_text() for r in rev][-2]

    # get eps data from table
    # quarters oldest to newest
    eps = tbl_rows[52].find_all('td')
    epsy = strip_parentheses([r.get_text() for r in eps][-2])

    return revy, epsy


# company_income('CRWD')
# company_fcf('CRWD')
# company_ratios('CRWD')
# prior_annual_stats('CRWD')