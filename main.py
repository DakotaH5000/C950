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
        packagesCSV = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in packagesCSV:
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

#Create an array of addresses that haven't been visited. Used with getShortest to create manual truck loads. 
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

#Checks current address input as coord and gets the next address. Used in manual generation of truck loads, does not automatically load truck objects. 
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
#Scrub time objects to ensure they won't cause runtime issues.
def isValidTimeFormat(time, timeFormat = '%I:%M%p'):
    try:
        datetime.strptime(time,timeFormat)
        return True
    except:
        return False

# Create truck objects with packageID's assigned to trucks and departure times. \Truck 1 driver will end up driving truck 3.
Truck1 = Truck(1, '8:00AM', [12,13,14,15,16,20,21,22,24,34])
Truck2 = Truck(2, '8:00AM', [1,3,4,5,7,9,11,17,18,23,29,33,36,37,38,40])
Truck3 = Truck(3, '9:05AM', [2,6,8,10,19,22,25,26,27,28,30,31,32,33,35,39])
#Function contains data to output any data requested for a truck or packet object at a given time. 
def deliverPackages(truck, time=None, targetPackageID = None, packageTracking = False, truckFunction = False, packageFunction = False):
    #Reset Truck info each iteration
    truck.distanceTraveled = 0
    truck.truckAtDepot = False
    for p in packages:
        p.status = 'At Depot'
    if truck.TruckID == 1:
        truck.packagesOnBoard = [12,13,14,15,16,20,21,22,24,34]
    if truck.TruckID == 2:
        truck.packagesOnBoard = [1,3,4,5,7,9,11,17,18,23,29,33,36,37,38,40]
    if truck.TruckID == 3:
        truck.packagesOnBoard = [2,6,8,10,19,22,25,26,27,28,30,31,32,33,35,39]
    

    #Create array of package objects
    packagesOnTruck = []
    #Create list of addresses to visit which can be distanced out using GetDistance Function
    addressesToVisit = []
    if time == None:
        print("Departure Time: " + str(truck.truckDepartureTime))
    currentTime = datetime.strptime(truck.truckDepartureTime, '%I:%M%p')
    

    #Load packages from ID placed in array to object 
    for packageID in truck.packagesOnTruck:
        package = packages.search(packageID)
        packagesOnTruck.append(package)

#For all unique addresses of packages on truck, populate array with them 
    for p in packagesOnTruck:
        if p.address not in addressesToVisit:
            addressesToVisit.append(p.address)

        if datetime.strptime(truck.truckDepartureTime, '%I:%M%p') >= currentTime:
            for pac in packagesOnTruck:
                pac.status = 'En Route'
#START OF WHILE LOOP
#START OF WHILE LOOP
#START OF WHILE LOOP, function will execute while a package remains on truck. 
    while addressesToVisit != []:

#Change package 9 delivery address when error is discoved
        if currentTime > datetime.strptime("10:20AM", '%I:%M%p'):
            packages.search(9).address = '410 S State St'

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
#Find trucks location at a given time
        if time != None and truckFunction:
            if datetime.strptime(time, '%I:%M%p') < datetime.strptime(truck.truckDepartureTime, '%I:%M%p') and currentTime > datetime.strptime(time, '%I:%M%p'):
                print("Truck " + str(truck.TruckID) + " was awaiting loading and departure at the depot at " + time)
                break
            if (time == currentTime) and truckFunction:
                print("Truck " + truck.id + " was at " + truck.currentAddress  + " at " + truck.currentAddress)
                break
            if (datetime.strptime(time, '%I:%M%p') <= currentTime) and truckFunction:
                print("Truck " + str(truck.TruckID) + " was on the road at " + time + " headed to " + truck.currentAddress + " with the following packages on board:")
                for pac in packagesOnTruck:
                    print (pac.id)
                
                break
            if truck.truckAtDepot:
                print("Truck " + str(truck.TruckID) + " returned to depot at "  + str(truck.depotTime) + '.')
                break


#O(N) loop over array to remove packages from truck object. 
        to_remove = []
        for pack in packagesOnTruck:
            if truck.currentAddress == pack.address:
                #Set package object status to delivered
                packageStatus = packages.search(pack.id)
                packageStatus.status = "Delivered at " + str(currentTime.time())
                if targetPackageID == int(packageStatus.id) and not packageFunction:
                    print(packageStatus)
                #Queue to be removed
                to_remove.append(pack)

#Handle looking up package by time Package can be At depot prior to start of day, on truck, delayed on plane, en route or delivered.
        if time != None and packageTracking == True and packageFunction: 
            if datetime.strptime(str(time), '%I:%M%p') >= currentTime:
                packageStatus = packages.search(targetPackageID).status
                if 'Delivered' in packageStatus and packageFunction:
                    print("Package " + str(truck.TruckID) + " already delivered at " + time + ", package was " + packageStatus.lower())
                    break
            elif  datetime.strptime(str(truck.truckDepartureTime), '%I:%M%p') > datetime.strptime(str(time), '%I:%M%p'):
                if int(packages.search(targetPackageID).id) in [6,25,28,32,]:
                    print('Package ' + str(packages.search(targetPackageID).id) + ' delayed at airport, awaiting arrival at depot.')
                    break
                else:
                    print("Package at depot, awaiting truck departure at " + truck.truckDepartureTime + ".")
                    break
            elif datetime.strptime(str(time), '%I:%M%p') < currentTime:
                print("Package " + str(packages.search(targetPackageID).id) + ' enroute at ' + time)
                break
            else:
                packageStatus = packages.search(targetPackageID).status
                print("Package " + str(targetPackageID) + " was " + packageStatus + " at " + time)
                break

        #O(N) operation where N= to_remove length, should however occur for every item in initial packagesOnTruck  
        #Remove From Truck
        for pack in to_remove:
            packagesOnTruck.remove(pack)
        #Mark address as visited
        addressesToVisit.remove(truck.currentAddress)
    if time == None:
        print("All packages delivered by " + str(currentTime.time()))
    if truckFunction and datetime.strptime(time, '%I:%M%p') > currentTime:
        print("Truck "+str(truck.TruckID) + " had returned to depot by " + time)
    #Return to depot time/distance of truck
    truck.distanceTraveled += float(getDistance(int(nameToCoord(truck.currentAddress)), 0))
    travelTime = getDistance(int(nameToCoord(truck.currentAddress)), 0)
    currentTime += timedelta(minutes=float(travelTime))
    currentTime = currentTime.replace(microsecond=0)
    truck.truckAtDepot = True

    
    if time == None:
        print("Depot Time: " + str(currentTime.time()))
        print("Total distance: " + str(truck.distanceTraveled) + " miles")
    #Reset distance

#Defines user interface function and displays options
#(truck, time=None, targetPackageID = None, packageTracking = False, truckFunction = False, packageFunction = False)
def userInterface():
    while True:
        userChoice = input("Enter a number:\n Get Truck Information: 1\n Get Package Info?: 2 \n Quit: 3\n")
        while userChoice not in ['1','2','3']:
            userChoice = input("INVALID INPUT: Enter a number:\n Get Truck Information: 1\n Get Package Info?: 2 \n Quit: 3\n")
        userChoice = int(userChoice)
        if userChoice == 1:
                while True:
                    truckInput = (input("\nWhich Truck would you like information on?\n Truck 1: 1\n Truck 2: 2\n Truck 3: 3\n All Trucks Distance: 4\n Know a trucks position at a given time?: 5 \n"))
                    while truckInput not in ['0','1','2','3','4','5']:
                        truckInput = (input("\nINVALID INPUT Which Truck would you like information on?\n Truck 1: 1\n Truck 2: 2\n Truck 3: 3\n All Trucks Distance: 4\n Know a trucks position at a given time?: 5 \n"))
                    truckInput = int(truckInput)
                    if truckInput == 0:
                        break
                    if truckInput == 1:
                        deliverPackages(Truck1)
                    if truckInput == 2:
                        deliverPackages(Truck2)
                    if truckInput == 3:
                        deliverPackages(Truck3)
                    if truckInput == 4:
                        deliverPackages(Truck1, '11:59PM', None, None, False, True)
                        deliverPackages(Truck2, '11:59PM', None, None, False, True)
                        deliverPackages(Truck3, '11:59PM', None, None, False, True)
                        print("Truck 1 traveled: " + str(Truck1.distanceTraveled) + "\nTruck 2 traveled: " + str(Truck2.distanceTraveled) + "\nTruck 3 traveled: " + str(Truck3.distanceTraveled))
                        print("Trucks traveled " + str(int(Truck1.distanceTraveled) + int(Truck1.distanceTraveled) + int(Truck1.distanceTraveled)) + " miles in total")
                    if truckInput == 5:
                        truckID =  input("Which Truck?\n")
                        if truckID == '0':
                            break
                        while (truckID) not in ['1','2','3']:
                            truckID =  (input("Which Truck? (Enter 1/2/3)\n"))
                        truckID = int(truckID)
                        #Convert this to a time object either here or in function.
                        truckTime = input("Which time (HH:MM(AM/PM) Format)\n")
                        while "AM" not in truckTime and "PM" not in truckTime or not isValidTimeFormat(truckTime):
                            truckTime = input("Please correctly format time (HH:MM(AM/PM) Format)\n")
                        if truckID == 1:
                            deliverPackages(Truck1, truckTime, truckFunction=True)
                        if truckID == 2:
                            deliverPackages(Truck2, truckTime, truckFunction=True)
                        if truckID == 3:
                            deliverPackages(Truck3, truckTime, truckFunction=True)
        elif userChoice == 2:
            while True:
                packageInput = (input("Which package would you like to track? (1-40) Enter 0 to return\n"))
                while packageInput not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40']:
                    packageInput = (input("Invalid input Which package would you like to track? Enter 0 to return\n"))
                if packageInput == 0:
                    break
                if  1 <= int(packageInput) <= 40:
                    packageInput = int(packageInput)
                    packageInfoTypeInput = (input("Package Information: 1\nStatus at a given time: 2\n"))
                    if packageInfoTypeInput not in ['1' , '2']:
                        packageInfoTypeInput = (input("Invalid Input: Package Information: 1\nStatus at a given time: 2\n"))
                    packageInfoTypeInput = int(packageInfoTypeInput)
                    if packageInfoTypeInput == 1:
                        deliverPackages(Truck1, '11:59PM', packageInput, None, False, False)
                        deliverPackages(Truck2, '11:59PM', packageInput, None, False, False)
                        deliverPackages(Truck3, '11:59PM', packageInput, None, False, False)
                    if packageInfoTypeInput == 2:
                        timeInput = input("Which time (HH:MM(AM/PM) Format)\n")
                        while ("AM" not in timeInput and "PM" not in timeInput) or not isValidTimeFormat(timeInput):
                            timeInput = input("Please correctly format time (HH:MM(AM/PM) Format)\n")
                        if int(packageInput) in [12,13,14,15,16,20,21,22,24,34]:
                            deliverPackages(Truck1, timeInput, packageInput, True, False, True)
                        if int(packageInput) in [1,3,4,5,7,9,11,17,18,23,29,33,36,37,38,40]:
                            deliverPackages(Truck2, timeInput, packageInput, True, False, True)
                        if int(packageInput) in [2,6,8,10,19,25,26,27,28,30,31,32,33,35,39]:
                            deliverPackages(Truck3, timeInput, packageInput, True, False, True)

        elif userChoice == 3:
            print("Goodbye!")
            break
                
userInterface()

#Section F
'''
F1. The algorithm used in this code has the strength of a near optimal solution. While a greedy algorith will not give a perfect answer everytime, the ability of making the best current decision every time leads to a near optimal solution. 
The second strength is the time/space complexity, Since we do not have nested loops s we would with dijkstra's algorith and we use a linear comparision,
 we know this algorithm scales linerally with the amount of elements put into it. 
F2. All packages delivered, all packages required to be dlivered prior to 9AM delivered prior, same with 10AM and package 9 not delivered until after 1020AM. 
F3. We could use Dijkstra or Bellman ford's shortest path. 
F3A. Both of these algorithms are different from my greedy algorithm as they look deeper into the further iterations of the problem. Using recursion and dynamic programming, they find the shortest path throughout the graph accounting for all paths. With a
O((V + E ) log V) and O(V*E) respectively they grow at a faster rate than this implmentation. 
'''
#Section G
'''
Creating the user input lead to much code bloat. Lines of code where made obselete and most likely not deleted, confusing conditionals were added with the deliverPackages function which started with one input of a truck object 
collecting many more parameters inorder to correctly output the desired output. I would condense my function calls and conditionals down to minimize the redundant code. 
'''
#Section H
'''
H. Data strucutre used in solution meets requirements. 
H1. An list or dictionary could be used instead of hashtable. 
    H1A. An list is very similar to the hash table, as the hashtable is commonly an list under the hood. The only differrence is the accessing of them. Package one could be stored inside of a list as [[1, rest of values]] and could be indexed as 
    myList[0][0] to interact with the rest of the values being some other attribute. This would lead to not requiring the search, insert and delete function which we required for the hash table. 
    The dictionary would store the objects as myDict = { IDnumber = package(ID, other values)}. This would once again allow for direct indexing and access to the data, depricating the search insert and delete function allowing easy alteration
    of the package objects.  
'''