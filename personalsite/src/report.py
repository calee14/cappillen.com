from .earnings import *
from .income import *
from .models import *
from .util import *
# from util.snapshot import store_report, get_report
import time
import csv
import pandas as pd

def build_report(ticker) -> CompanyReport:
    '''
    Run scraper functions to build report and store
    it into json file.
    '''
    # income financial report
    report_date, revq, rev_growth, epsq, eps_growth = company_income(ticker)
    fcfq, fcf_growth = company_fcf(ticker)
    pegq, psq = company_ratios(ticker)
    revy, epsy = prior_annual_stats(ticker)

    # earnings financial report
    eps_est, rev_est, eps_report = earnings_est(ticker)
    price_delta = price_change(ticker)

    
    income_report = IncomeReport()
    income_report.load_data(revq, rev_growth, 
                            epsq, eps_growth, fcfq, fcf_growth, pegq, psq)

    # build earnings report, calc forecast percentage change
    # by using getting last fiscal year's eps and rev
    earnings_report = EarningsReport()
    earnings_report.load_data(eps_est, [epsq[-1], epsy],
                              rev_est, [revq[1], revy],
                              eps_report, price_delta)
    
    report = CompanyReport(ticker, report_date, income_report, earnings_report)
    
    # store report after scraping
    store_report(report)

    return report

def report_xlsx(reports: list[CompanyReport]):

    income_df = pd.DataFrame(columns=['Revenue', 'Rev. Growth', 'Earnings', 'EPS Growth', 'FCF', 'FCF Growth', 'Price/Earnings/Growth', 'Price/Sales'])
    
    income_data = {
        'Ticker': [],
        'Revenue': [], 
        'Rev. Growth (%)': [], 
        'Earnings': [], 
        'EPS Growth (%)': [], 
        'FCF': [], 
        'FCF Growth (%)': [], 
        'Price/Earnings/Growth': [], 
        'Price/Sales': []
    }

    earnings_data = {
        'Ticker': [],
        'EPS Estimate': [],
        'EPS Actual': [],
        'EPS Surprise (%)': [],
        'EPS Growth Quarter and Year Forecast (%)': [],
        'Revenue Growth Quarter and Year Forecast (%)': [],
        'Price Delta': []
    }

    # build the income and earning reports for all companies
    for report in reports:
        # build the income report
        income_report = report.income_report
        income_data['Ticker'].append(report.ticker)
        income_data['Revenue'].append(income_report.revq)
        income_data['Rev. Growth (%)'].append(income_report.rev_growth)
        income_data['Earnings'].append(income_report.epsq)
        income_data['EPS Growth (%)'].append(income_report.eps_growth)
        income_data['FCF'].append(income_report.fcfq)
        income_data['FCF Growth (%)'].append(income_report.fcf_growth)
        income_data['Price/Earnings/Growth'].append(income_report.pegq)
        income_data['Price/Sales'].append(income_report.psq)
        
        # build the earnings report
        earnings_report = report.earnings_report
        earnings_data['Ticker'].append(report.ticker)
        earnings_data['EPS Estimate'].append(earnings_report.eps_est)
        earnings_data['EPS Actual'].append(earnings_report.eps_act)
        earnings_data['EPS Surprise (%)'].append(earnings_report.eps_surprise)
        earnings_data['EPS Growth Quarter and Year Forecast (%)'].append(earnings_report.eps_growth_quarter_year_forecast)
        earnings_data['Revenue Growth Quarter and Year Forecast (%)'].append(earnings_report.rev_growth_quarter_year_forecast)
        earnings_data['Price Delta'].append(earnings_report.price_delta)
    
    # make dataframe of data
    income_df = pd.DataFrame(income_data)
    earnings_df = pd.DataFrame(earnings_data)

    # make the pandas excel writer
    writer = pd.ExcelWriter('report.xlsx', engine='xlsxwriter')

    # write dataframes to xcel sheets in the xlsx file
    income_df.to_excel(writer, 
                       sheet_name='IncomeReport',
                       index=False)
    earnings_df.to_excel(writer,
                         sheet_name='EarningsReport',
                         index=False)
    
    # change each col size to squish them a little
    for col in income_df:
        col_len = max(income_df[col].astype(str).map(len).max() / 2, len(col))
        col_idx = income_df.columns.get_loc(col)
        writer.sheets['IncomeReport'].set_column(col_idx, col_idx, col_len)
    for col in earnings_df:
        col_len = max(earnings_df[col].astype(str).map(len).max() / 2, len(col))
        col_idx = earnings_df.columns.get_loc(col)
        writer.sheets['EarningsReport'].set_column(col_idx, col_idx, col_len)

    # Access the workbook and worksheet objects
    workbook = writer.book
    income_worksheet = writer.sheets['IncomeReport']
    earnings_worksheet = writer.sheets['EarningsReport']
    
    # Change row heights for sheets
    # Change the row height
    income_worksheet.set_default_row(30)  # Set the default row height to 20 (in pixels)
    income_worksheet.set_row(0, 20) 
    earnings_worksheet.set_default_row(30)  # Set the default row height to 20 (in pixels)
    earnings_worksheet.set_row(0, 20) 

    # Write the DataFrame to the worksheet with header formatting
    header_format = workbook.add_format({'bold': False})
    for col_num, value in enumerate(income_df.columns):
        income_worksheet.write(0, col_num, value, header_format)
    for col_num, value in enumerate(earnings_df.columns):
        earnings_worksheet.write(0, col_num, value, header_format)

    # Define cell formats for alternating row colors
    even_format = workbook.add_format({'bg_color': '#F4F9F8', 'align':'left', 'valign': 'vcenter', 'border': 1, 'border_color': '#929292', 'text_wrap': True})
    odd_format = workbook.add_format({'bg_color': '#FFFFFF', 'align': 'left', 'valign': 'vcenter', 'border': 1, 'border_color': '#929292', 'text_wrap': True})

    # Apply alternating row colors by iterating through rows
    for i, row in income_df.iterrows():
        row_format = even_format if i % 2 == 0 else odd_format
        for j, value in enumerate(row):
            income_worksheet.write(i+1, j, value, row_format)
    for i, row in earnings_df.iterrows():
        row_format = even_format if i % 2 == 0 else odd_format
        for j, value in enumerate(row):
            earnings_worksheet.write(i+1, j, value, row_format)

    workbook.close()
    

def make_print_report(tickers: list[str]):
    reports: list[CompanyReport] = []
    for ticker in tickers:
        # start timer
        start = time.time()
        try:
            # builds report for ticker
            report: CompanyReport = build_report(ticker)
            reports.append(report) 
        except Exception as error:
            print(f'Error while scraping for {ticker}:')
            print(error)
            print('Will attempt to retrieve older reports.')
            _report = get_report(ticker)
            if _report.income_report != None:
                reports.append(_report)
                print(f'Found an older report for {ticker}')
            else:
                print(f'Failed to find a prior report for {ticker}')
        # end timer
        end = time.time()
        print(f'Scraping {ticker} took:', (end - start) * 1000, 'milliseconds')
    
    # make the report and local file
    report_xlsx(reports)

def print_report(tickers: list[str]):
    reports: list[CompanyReport] = []
    for ticker in tickers:
        _report = get_report(ticker)
        if _report.income_report != None:
            reports.append(_report)
    report_xlsx(reports)
        
def test_store():
    income_report = {'revq': '487.83M -> 535.15M -> 580.88M -> 637.37M -> 692.58M', 'rev_growth': 42, 'epsq': '-0.14 -> -0.21 -> -0.24 -> -0.2 -> 0.0', 'eps_growth': 100, 'fcfq': '159.74M -> 138.25M -> 176.41M -> 212.85M -> 230.93M', 'fcf_growth': 45, 'pegq': '1.61 <- 1.22 <- 2.19 <- 3.79 <- 4.63', 'psq': '12.49 <- 12.06 <- 20.25 <- 25.68 <- 31.10'}
    earnings_report = {'eps_est': '0.51', 'eps_act': '0.57', 'eps_surprise': 11, 'eps_growth_quarter_year_forecast': '55900, 402', 'rev_growth_quarter_year_forecast': '35, 35', 'price_delta': 47}

    report = CompanyReport('CRWD', 'today', IncomeReport.load_json(income_report), EarningsReport.load_json(earnings_report))
    # print(report)

    store_report(report)
    
    report_xlsx([report])

# print('start')
# start = time.time()
# build_report('CRWD')
# test_store()
# make_print_report(['CRWD', 'RUN'])
# end = time.time()
# print('finished')
# print('program took:',(end - start) * 1000, 'milliseconds')
