from ..util.process import eps_to_float

class IncomeReport(object):
    def __init__(self):
        pass

    def load_data(self, revq, rev_growth, epsq, eps_growth, fcfq, fcf_growth, pegq, psgq, psq):
        self.revq = ' -> '.join(revq)
        self.rev_growth = rev_growth
        epsq = [str(eps_to_float(eps)) for eps in epsq]
        self.epsq = ' -> '.join(epsq)
        self.eps_growth = eps_growth
        self.fcfq = ' -> '.join(fcfq)
        self.fcf_growth = fcf_growth
        self.pegq = ' <- '.join(pegq)
        self.psq = ' <- '.join(psq)

    @classmethod
    def load_json(cls, j):
        new_class = cls()
        new_class.revq = j['revq']
        new_class.rev_growth = j['rev_growth']
        new_class.epsq = j['epsq']
        new_class.eps_growth = j['eps_growth']
        new_class.fcfq = j['fcfq']
        new_class.fcf_growth = j['fcf_growth']
        new_class.pegq = j['pegq']
        new_class.psgq = j.get('pqgq', 'Missing values')
        new_class.psq = j['psq']

        return new_class
    
    def __str__(self):
        return str(self.__dict__)