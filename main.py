#Student ID: 011690051
import csv
from datetime import datetime, timedelta
from package import Package
from HashTable import HashTable
from truck import Truck

#Create Hashtable object
packages = HashTable()

#Read in package Info and populate packages hashtable with
with open('packageData.csv', newline='', encoding='utf-8-sig') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvReader:
            package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            packages.insert(package.id, package)

#Read in file with location distance matrix as csvDistance
with open('distance.csv', newline='', encoding='utf-8-sig') as csvfile:
    csvDistance = csv.reader(csvfile, delimiter=',')
    csvDistance = list(csvDistance)

#Read in file with location names as csvDistanceNames
with open('distance_names.csv', newline='', encoding='utf-8-sig') as csvfile:
    csvDistanceNames = csv.reader(csvfile, delimiter=',')
    csvDistanceNames = list(csvDistanceNames)

#Create an array of addresses that haven't been visited and a total number of addresses
addresses = []
for row in range(len(csvDistance)):
     addresses.append(row)

#Checks the distance.csv file for a distance between two given points
def getDistance(x_coord, y_coord):
    distance = csvDistance[x_coord][y_coord]
    #distances are mirroed across the table, if (1,2) is blank (2,1) should hold desired value. 
    if distance == '':
        distance = csvDistance[y_coord][x_coord]
    return distance

#Checks current address input as coord and gets the next address. 
def getShortest(coord):
    #Place holder value of 999, if program was traveling 1000+ miles, value would need to be adjusted.
    distance = 999.0
    id = (0,0)
    addressId = 0
    for num in range(len(csvDistance[coord])):
        if (float(getDistance(coord, num)) != 0 and float(getDistance(coord, num)) < float(distance)) and num in addresses:
            distance = getDistance(coord, num)
            id = (coord,num)
            addressId = csvDistanceNames[num]
    if id[0] in addresses:
        addresses.remove(id[0])
    if id[1] in addresses:
        addresses.remove(id[1])
    return distance, id
#converts a street adress to the coordinate on distance.csv via the distance_names.csv file. 
def nameToCoord(name):
    for row in csvDistanceNames:
        if name in row:
            return row[0]
#Same as above function, but returns a different value
def coordToAddress(target):
    for row in csvDistanceNames:
        if str(target) == row[0]:
            return row[2]


# Create truck objects with packageID's assigned to trucks and departure times. Truck 1 driver will drive Truck 3 when returned. 
Truck1 = Truck(1, '8:00AM', [12,13,14,15,16,20,21,24,34])
Truck2 = Truck(2, '8:00AM', [1,2,3,4,5,7,11,17,18,22,23,29,31,33,36,37,38,40])
Truck3 = Truck(3, '8:34AM', [6,8,9,10,19,22,25,26,27,28,30,32,35,39])


def deliverPackages(truck):
    #Create array of package objects
    packagesOnTruck = []
    #Create list of addresses to visit which can be distanced out using GetDistance Function
    addressesToVisit = []
    print("Depart Time:")
    currentTime = datetime.strptime(truck.truckDepartureTime, '%I:%M%p')
    print(currentTime)

    #Load packages from ID placed in array to object 
    for packageID in truck.packagesOnTruck:
        package = packages.search(packageID)
        packagesOnTruck.append(package)

    #For all unique addresses of packages on truck, populate array with them 
    for p in packagesOnTruck:
        if p.address not in addressesToVisit:
            addressesToVisit.append(p.address)
    #Deliver packages
    while addressesToVisit != []:
        #Distance once again a placeholder value, if 1000+ would need to be changed. 
        nextStop = 999

        #O(N) loop over array
        for p  in addressesToVisit:
            dist = float(getDistance( int(nameToCoord(truck.currentAddress)), int(nameToCoord(p)) ))
            #Distance of 0 is self and would always be best option. 
            if dist < nextStop and dist != 0:
                nextStop = dist
                truck.currentAddress= p
        
        truck.distanceTraveled += nextStop
        #Next stop is a distance, speed/distance = time Traveled which will be a decimal 0-99, must be converted to seconds
        travelTime =  round(truck.speed/nextStop, 2)
        #Convert decimal to time and add time to dime elapsed
        currentTime += timedelta(minutes=travelTime)
        currentTime = currentTime.replace(microsecond=0)
        print("Packages delivered at:" + str(currentTime.time()))

        #O(N) loop over array
        to_remove = []
        for pack in packagesOnTruck:
            if truck.currentAddress == pack.address:
                #Set package object status to delivered
                print(pack.id)
                packageStatus = packages.search(pack.id)
                packageStatus.status = "Delivered at " + str(currentTime.time())
                #Queue to be removed
                to_remove.append(pack)
        
        #O(N) operationi where N= to_remove length, should however occur for every item in initial packagesOnTruck  
        #Remove From Truck
        for pack in to_remove:
            packagesOnTruck.remove(pack)
        #Mark address as visited
        addressesToVisit.remove(truck.currentAddress)

    #Return to depot time/distance of truck
    truck.distanceTraveled += float(getDistance(int(nameToCoord(truck.currentAddress)), 0))
    travelTime = getDistance(int(nameToCoord(truck.currentAddress)), 0)
    currentTime += timedelta(minutes=float(travelTime))
    currentTime = currentTime.replace(microsecond=0)

    print("Depot Time: " + str(currentTime.time()))
    print("Total distance: " + str(truck.distanceTraveled))

print("Truck 1")
deliverPackages(Truck1)
print("Truck 2")
deliverPackages(Truck2)
print("Truck 3")
deliverPackages(Truck3)
