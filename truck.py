class Truck:
    def __init__(self, TruckID, truckDepartureTime, packagesOnTruck):
        self.TruckID = TruckID
        self.packagesOnTruck = packagesOnTruck or []
        self.maxLoad = 16
        self.speed = 18
        self.truckDepartureTime = truckDepartureTime
        self.currentAddress = '4001 South 700 East'
        self.distanceTraveled = 0