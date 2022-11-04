class Contact:
    def __init__(self, number, optins):
        self.number = number
        self.optins = optins
    def is_optin(self, orgid):
        return True if orgid in self.optins else False