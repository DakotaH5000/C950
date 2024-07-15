class Package:
    def __init__(self, id, address, city, state, zip, timeRequirements, weight, specialInstructions):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.timeRequirements = timeRequirements
        self.weight = weight
        self.specialInstructions = specialInstructions if specialInstructions is not None else ""
        self.delay = None
        self.status = 'At Depot'
        self.loadedOnTruck = False
        self.enrouteTime = None
        self.deliveredTime = None
    #Part B requirements
    def __str__(self):
        return (f"Package ID: {self.id} "
                f"Address: {self.address} "
                f"City: {self.city} "
                f"State: {self.state} "
                f"Zip: {self.zip} "
                f"Deadline: {self.timeRequirements} "
                f"Weight: {self.weight} lbs "
                f"Status: {self.status}")