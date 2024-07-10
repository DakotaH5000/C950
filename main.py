#Student ID: 011690051
import csv
from datetime import datetime, timedelta
from package import Package
from HashTable import HashTable
from truck import Truck

#Create Hashtable object
packages = HashTable()

#Read in package Info and populate packages hashtable with
with open('C950/packageData.csv', newline='', encoding='utf-8-sig') as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvReader:
            package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            if package.id == "9":
                package.delay = datetime.strptime("10:20AM", '%I:%M%p')
            packages.insert(package.id, package)

#Read in file with location distance matrix as csvDistance
with open('C950/distance.csv', newline='', encoding='utf-8-sig') as csvfile:
    csvDistance = csv.reader(csvfile, delimiter=',')
    csvDistance = list(csvDistance)

#Read in file with location names as csvDistanceNames
with open('C950/distance_names.csv', newline='', encoding='utf-8-sig') as csvfile:
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


def deliverPackages(truck, time=None):
    Truck1 = Truck(1, '8:00AM', [12,13,14,15,16,20,21,22,24,34])
    Truck2 = Truck(2, '8:00AM', [1,3,4,5,7,9,11,17,18,23,29,33,36,37,38,40])
    Truck3 = Truck(3, '9:05AM', [2,6,8,10,19,22,25,26,27,28,30,31,32,33,35,39])
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
        if currentTime < datetime.strptime("10:20AM", '%I:%M%p'):
            packages.search(9).address == '410 S State St'
        #Distance once again a placeholder value, if 1000+ would need to be changed. 
        nextStop = 999

        #O(N) loop over array
        for p  in addressesToVisit:
            if any(pa.address == p and pa.delay and currentTime < pa.delay for pa in packagesOnTruck):
                continue
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
        #print("Packages delivered at:" + str(currentTime.time()))

        #O(N) loop over array
        to_remove = []
        for pack in packagesOnTruck:
            if truck.currentAddress == pack.address:
                #Set package object status to delivered
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

    #print("Depot Time: " + str(currentTime.time()))
    #print("Total distance: " + str(truck.distanceTraveled))

def userInterface():
    print('========')
    print('Welcome!')
    print('========')
    userChoice = int(input("Would you like to :\n Get Truck Information: 1\n Get Package Info?: 2 \n"))
    if userChoice == 1:
        truckInput = int(input("Which Truck would you like information on?:\nTruck 1: 1\nTruck 2: 2\nTruck 3: 3\n All Trucks: 4\n Know a trucks position at a given time?: 5 "))
        if truckInput == 1:
            deliverPackages(1)
        if truckInput == 2:
            deliverPackages(2)
        if truckInput == 3:
            deliverPackages(3)
        if truckInput == 4:
            deliverPackages(1)
            deliverPackages(2)
            deliverPackages(3)
        if truckInput == 5:
            truckID = int(input("Which Truck?\n"))
            #Convert this to a time object either here or in function.
            truckTime = input("Which time (HH:MM(AM/PM) Format)\n")
    if userChoice == 2:
        print('2')
        


'''
DeliverBy10 = [1,6,13,14,15,16,20,25,29,30,31,34,37,40]
print("Truck 1")
deliverPackages(Truck1)
print("Truck 2")
deliverPackages(Truck2)
print("Truck 3")
deliverPackages(Truck3)

for p in DeliverBy10:
    package = packages.search(p)
    print(package.id + " " + package.status)
'''

userInterface()