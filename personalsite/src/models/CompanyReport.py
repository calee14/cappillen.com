from . import *
class CompanyReport(object):
    def __init__(self, ticker, date ,income_report, earnings_report):
        self.ticker = ticker
        self.date = date
        self.income_report = income_report
        self.earnings_report = earnings_report

    def __str__(self):
        return str(self.__dict__)
    
    def as_dict(self):
        dic = self.__dict__.copy()
        dic['income_report'] = dic['income_report'].__dict__
        dic['earnings_report'] = dic['earnings_report'].__dict__
        return dic