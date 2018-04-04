class House(object):
    """description of class"""
    def __init__(self):
        self.AgentName = "NA"
        self.CompanyName = "NA"
        self.PropertyAddress = "NA"
        self.City = "NA"
        self.State = "NA"
        self.PhoneNumber = "NA"
        self.Url = "NA"
        self.MLSNumber = "NA"
        self.Price= "NA"
        self.Date = "NA"
        self.AgentProfile = "NA"

    def getHouseString(self):
        house =  self.AgentName+', '+ self.AgentProfile+', '+self.CompanyName+', '+self.PropertyAddress+', '+  self.State+', '+self.City+', '+  self.PhoneNumber+', '+  self.MLSNumber+', '+self.Price+', '+self.Date+', '+self.Url+',\n'
        return house
        


