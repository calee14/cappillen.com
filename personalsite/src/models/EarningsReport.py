from ..util.process import rev_to_int

def calculate_percentage_change(old, new):
    small_value = 1e-3  # A small positive value to compare against zero

    if old != 0:
        percentage_change = ((new - old) / abs(old)) * 100
    else:
        percentage_change = ((new - small_value) / small_value) * 100

    return int(percentage_change)

class EarningsReport(object):
    def __init__(self):
        pass

    def load_data(self, eps_est, eps_prior, rev_est, rev_prior, eps_report, price_delta):
        self.eps_est = eps_report[0]
        self.eps_act = eps_report[1]
        self.eps_surprise = eps_report[2]
        # calc eps growth: forecast eps next quarter v. quarter yoy
        # and also forecast end of year eps v. last fiscal year eps
        eps_est = [float(eps) for eps in eps_est]
        eps_prior = [float(eps) for eps in eps_prior]
        # eps_forecast = [next quarter growth yoy, end of year growth yoy]
        self.eps_growth_quarter_year_forecast = ', '.join([str(calculate_percentage_change(eps_prior[0], eps_est[0])),
                             str(calculate_percentage_change(eps_prior[1], eps_est[1]))])
        # calc rev growth: forecast rev next quarter v. quarter yoy
        # and also forecast end of year rev v. last fiscal year rev
        rev_est = [rev_to_int(rev) for rev in rev_est]
        rev_prior = [rev_to_int(rev) for rev in rev_prior]
        # rev_forecast = [next quarter growth yoy, end of year growth yoy]
        self.rev_growth_quarter_year_forecast = ', '.join([str(calculate_percentage_change(rev_prior[0], rev_est[0])),
                             str(calculate_percentage_change(rev_prior[1], rev_est[1]))])
        # calc price change over past 6 months
        self.price_delta = price_delta

    @classmethod
    def load_json(cls, j):
        new_class = cls()
        new_class.eps_est = j['eps_est']
        new_class.eps_act = j['eps_act']
        new_class.eps_surprise = j['eps_surprise']
        new_class.eps_growth_quarter_year_forecast = j['eps_growth_quarter_year_forecast']
        new_class.rev_growth_quarter_year_forecast = j['rev_growth_quarter_year_forecast']
        new_class.price_delta = j['price_delta']
        return new_class
    
    def __str__(self):
        return str(self.__dict__)