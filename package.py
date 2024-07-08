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
        self.status = 'Not Delivered'
        self.loadedOnTruck = False
        self.enrouteTime = None
        self.deliveredTime = None
    def __str__(self):
        return (f"Package ID: {self.id}\n"
                f"Address: {self.address}\n"
                f"City: {self.city}\n"
                f"State: {self.state}\n"
                f"Zip: {self.zip}\n"
                f"Time Requirements: {self.timeRequirements}\n"
                f"Weight: {self.weight} lbs\n"
                f"Special Instructions: {self.specialInstructions}\n"
                f"Status: {self.status}")