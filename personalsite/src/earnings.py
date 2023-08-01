from bs4 import BeautifulSoup
from .util.get_site import get_site
from .util.process import rm_commas_parentheses, rm_commas
import datetime
import requests

# Set the headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
}

def custom_hist_table(tag):
    return tag.name == 'table' and 'historical-prices' in tag.attrs.get('data-test', '')

def percent_to_int(string):
    return round(int(string.split('.')[0]))

def earnings_est(ticker):
    '''
    Returns tuple of size 3:
    First element is a list of EPS forecast for next quarter and full year (current)
    Second element is a list of Revenue forecast for next quarter and full year (current)
    Third element is a list of EPS report for most recent quarter (estimate, actual, beat '%')
    '''

    # Set the URL of the page you want to scrape
    url = f"https://finance.yahoo.com/quote/{ticker}/analysis?p={ticker}"

    # Send a GET request to the website with headers
    response = get_site(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # print(soup.find('div', id='Main'))
    tables = soup.find_all('table')
    
    # earnings estimate table
    earnings_rows = tables[0].find_all('tr')
    eps_forecast = [e.get_text() for e in earnings_rows[2].find_all('td')]
    # get eps forecast for next quarter
    eps_nq = rm_commas_parentheses(eps_forecast[1])
    # get eps forecast for full year (current fiscal year)
    eps_end_yr = rm_commas_parentheses(eps_forecast[3])
    # print(eps_nq, eps_end_yr)

    # revenue estimate table
    revenue_rows = tables[1].find_all('tr')
    revenue_forecast = [r.get_text() for r in revenue_rows[2].find_all('td')]
    # get revenue forecast for next quarter
    rev_nq = revenue_forecast[1]
    # get revenue forecast for full year (current fiscal year)
    rev_end_yr = revenue_forecast[3]
    # print(rev_nq, rev_end_yr)

    # earnings report table
    report_rows = tables[2].find_all('tr')
    # get eps estimate for the recent quarter
    report_eps_est = report_rows[1].find_all('td')[-1].get_text()
    # get eps actual for recent quarter
    report_eps_act = report_rows[2].find_all('td')[-1].get_text()
    # get eps surprise %
    report_eps_surprise = report_rows[4].find_all('td')[-1].get_text()
    # print(report_eps_est, report_eps_act, percent_to_int(report_eps_surprise))

    return [eps_nq, eps_end_yr], [rev_nq, rev_end_yr], [report_eps_est, report_eps_act, percent_to_int(report_eps_surprise)]

    

def price_change(ticker):
    '''
    Returns price change (percentage) in the recent 6 months 
    '''

    current_time = datetime.datetime.today()
    six_months_ago = (current_time - datetime.timedelta(days=30*6))
    current_time = int(current_time.timestamp())
    six_months_ago = int(six_months_ago.timestamp())

    # Set the URL of the page you want to scrape
    url = f"https://finance.yahoo.com/quote/{ticker}/history?period1={six_months_ago}&period2={current_time}&interval=1wk&filter=history&frequency=1wk&includeAdjustedClose=true"
    print(url)
    # Send a GET request to the website with headers
    response = get_site(url, headers=headers)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    hist_table = soup.find_all(custom_hist_table)[0]

    hist_rows = hist_table.find_all('tr')
    # get price two days ago to avoid yahoo finance formatting
    hist_recent = float(rm_commas(hist_rows[2].find_all('td')[4].get_text()))
    # get price 6 months ago
    hist_6_months = float(rm_commas(hist_rows[-2].find_all('td')[4].get_text()))
    return int((hist_recent - hist_6_months)*100/hist_6_months)


# print(earnings_est('CRWD'))
# print(price_change('CRWD'))