import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QDialog,QMainWindow, QPushButton, QLabel
from PyQt5.uic import loadUi
from datetime import datetime
import pyrebase
import csv

#Connects to google firebase project
firebaseConfig={ 'apiKey': "AIzaSyA0Jp7OlBdc2iR_pL5D_rz2ygwjkV826rs",
    'authDomain': "tseproject-51623.firebaseapp.com",
    'databaseURL': "https://tseproject-51623.firebaseapp.com",
    'projectId': "tseproject-51623",
    'storageBucket': "tseproject-51623.appspot.com",
    'messagingSenderId': "474097261685",
    'appId': "1:474097261685:web:0893ac7c9142e81b04ac3c",
    'measurementId': "G-JY9M8E7N90"}
firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

#Creates a global order list to store the user's order 
orderList = []

#Specifies a login class to create the login interface
class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("MainWindow.ui",self) # Loads the GUI design created in QT Designer
        self.loginButton.clicked.connect(self.loginFunction) # If the login button has been clicked go to login function
        self.enterPassword.setEchoMode(QtWidgets.QLineEdit.Password)# Format the user entered data to hide their password
        self.createAccountButton.clicked.connect(self.gotoCreateAccount)# If the create account button has been clicked goto create account
        self.invalidEmailOrPassword.setVisible(False)# Hide the error message

    #Functionality for allowing the user to login to the service
    def loginFunction(self):
        global email
        email=self.enterEmail.text() # Assign an email variable to the text entered in the text box
  
        password=self.enterPassword.text()# Assign a password variable to the text entered in the text box

        # Attempt to sign the user into the firebase project if failed then display an error message otherwise go to the next interface
        try: 
            auth.sign_in_with_email_and_password(email,password)
            self.gotoOrderOrTrackDrone()

        except:
            self.invalidEmailOrPassword.setVisible(True)
            
    #Creates the createAccount interface allowing the user to create a new firebase account
    def gotoCreateAccount(self):
        createAccount=CreateAccount()
        #Sets the createAccount widget as the current widget making it visible
        widget.addWidget(createAccount)
        widget.setCurrentIndex(widget.currentIndex()+1)

    #Creates the order or track drone interface after the user has logged in
    def gotoOrderOrTrackDrone(self):
        orderOrTrackDrone=OrderOrTrackDrone()
        #Sets the orderOrTrackDrone widget as the current widget making it visible
        widget.addWidget(orderOrTrackDrone)
        widget.setCurrentIndex(widget.currentIndex()+1)

#Specifies the functionality for creating an account
class CreateAccount(QMainWindow):
    def __init__(self):
        super(CreateAccount,self).__init__()
        loadUi("SignUp.ui",self)# Loads the GUI design created in QT Designer
        self.invalidEmailOrPassword.setVisible(False) #Dont display the error message 
        self.passwordsDontMatch.setVisible(False)#Dont display the passwords dont match error message
        self.signupButton.clicked.connect(self.createAccountFunction)# If the signup button has been pressed then go to the create account function
        self.enterPassword.setEchoMode(QtWidgets.QLineEdit.Password)# Format the user entered data to hide their password
        self.enterConfirmPassword.setEchoMode(QtWidgets.QLineEdit.Password)# Format the user entered data to hide their confirmed password
     



    #Creates the firebase account using the data entered by the user
    def createAccountFunction(self):
     
        
     
        #Assign an email variable to the text entered by the user
        email = self.enterEmail.text()
    
        #If the password equals the confirm password
        if self.enterPassword.text() == self.enterConfirmPassword.text():
            password=self.enterPassword.text() #Assign the password to a variable

          #Attemps to create the user with the entered email and password if it cant then it displays an error message
            try:
                auth.create_user_with_email_and_password(email,password)
                #Moves back to the login screen to allow the user to login
                login=Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex()+1)
            except:
                self.invalidEmailOrPassword.setVisible(True)
        #If the passwords dont match then display an error message however dont display the other error message if that exists
        else:
            self.passwordsDontMatch.setVisible(True)
            self.invalidEmailOrPassword.setVisible(False)

#Specifies the functionality for ordering or tracking a drone
class OrderOrTrackDrone(QMainWindow):
    def __init__(self):
        super(OrderOrTrackDrone,self).__init__()
        loadUi("OrderOrTrackDrone.ui",self)# Loads the GUI design created in QT Designer
        self.orderANewDroneButton.clicked.connect(self.gotoSelectDate) # If the user selects the orderANewDrone button then goto select date
        self.trackAnExistingDroneButton.clicked.connect(self.gotoSelectOrder)# If the user selects the track an existing drone button then goto select order

    #Allows the user to go to the next interface selectDate
    def gotoSelectDate(self):
        selectDate = SelectDate()
        widget.addWidget(selectDate)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    #Allows the user to go to the next interface selectOrder
    def gotoSelectOrder(self):
        selectOrder = SelectOrder()
        widget.addWidget(selectOrder)
        widget.setCurrentIndex(widget.currentIndex()+1)






#Specifies the functionality to allow the user to select a date
class SelectDate(QMainWindow):
    def __init__(self):
        super(SelectDate,self).__init__()
        loadUi("SelectDate.ui",self) #Loads the GUI design created in QT Designer
       
        self.proceedButton.clicked.connect(self.gotoGetAddressesAndTime) #If the proceed button is pressed then goto the next interface get addresses and time

    #Allows the user to go to the addresses and time interface
    def gotoGetAddressesAndTime(self):

        #Gets the data selected from the calander widget and stores it in a variable
        self.orderDate = self.calendarWidget.selectedDate()
       

        #Creates the getAddressesAndTime object and sets it visible to the user
        getAddressesAndTime = GetAddressesAndTime(self.orderDate)
        widget.addWidget(getAddressesAndTime)
        widget.setCurrentIndex(widget.currentIndex()+1)




#Specifies the functionality for allowing the user to select the addresses and time for the drone delivery
class GetAddressesAndTime(QMainWindow):
    def __init__(self,orderDate):
        super(GetAddressesAndTime,self).__init__()
        loadUi("GetAddressesAndTime.ui",self)#Loads the GUI design created in QT Designer

        #Adds available time slots to the drop down box
        self.selectTimeFrame.addItem("7:00 - 7:30")
        self.selectTimeFrame.addItem("8:00 - 8:30")
        self.selectTimeFrame.addItem("9:00 - 9:30")
        self.selectTimeFrame.addItem("10:00 - 10:30")
        self.selectTimeFrame.addItem("10:30 - 10:45")
        self.selectTimeFrame.addItem("11:15 - 11:30")
        self.selectTimeFrame.addItem("12:00 - 12:15")
        self.selectTimeFrame.addItem("14:00 - 14:20")
        self.selectTimeFrame.addItem("14:20 - 14:50")
        self.selectTimeFrame.addItem("15:15 - 15:30")
        self.selectTimeFrame.addItem("16:20 - 16:40")
        self.selectTimeFrame.addItem("17:15 - 17:30")
        self.confirmButton.clicked.connect(self.addDataToList) #if the confirm button has been selected then go to addDataToList
        self.orderDate = str(orderDate)
        
    def gotoOrderOrTrackDrone(self):
        orderOrTrackDrone=OrderOrTrackDrone()
        widget.addWidget(orderOrTrackDrone)
        widget.setCurrentIndex(widget.currentIndex()+1)

    #Adds the user data to a list for it to be written to a CSV file
    def addDataToList(self):

        #Assigns an address variable to the data entered by the user and appends it to a list
        self.yourAddress = self.enterYourAddress.text()

        #Appends the existing email variable to the list
        orderList.append(str(email))
       
        orderList.append(str(self.yourAddress))
        
        
        #Gets the text entered into the destination address text box and assign it to a viable which is appended to the orderList
        self.destinationAddress = self.enterDestinationAddress.text()
        
        orderList.append(str(self.destinationAddress))
       
        
        #The orderDate which was previously entered is added to the orderList
        orderList.append(str(self.orderDate))

        #Creates a variable an assigns it to the time selected by the user which is then appeneded to the orderList
        self.timeFrame = self.selectTimeFrame.currentText()
        orderList.append(str(self.timeFrame))
        
        #Get the current date and time
        now = datetime.now()

        #Assign the current data and time to a variable with a specific format
        self.currentDateAndTime = now.strftime("%d/%m/%Y %H:%M:%S")

        #Appand this to the orderList
        orderList.append(str(self.currentDateAndTime))

        #Save the users data
        self.saveOrderData()

    def saveOrderData(self):
        saveData = SaveData() #Creates an instance of the saveData class

        #Go back to order or track drone
        self.gotoOrderOrTrackDrone()
       
# Specifies the select order functionality
class SelectOrder(QMainWindow):
    def __init__(self):
        super(SelectOrder,self).__init__()
        loadUi("SelectOrder.ui",self)#Loads the GUI design created in QT Designer
        orderList.clear()#Clears any data in the orderList 
        self.readOrderData() #Reads the data in from the CSV file
        self.displayOrder()# Displays the order

    def readOrderData(self):
        readData = ReadData()# Creates an instance of ReadData

    #Displays the order read in through the CSV file
    def displayOrder(self):

        #Creates a new button for each row of the CSV File 
        self.buttons = []
        itemnum = 0
        location = 320
        for i in orderList:
            itemnum += 1
      
            self.button = QPushButton("Order " + str(itemnum),self)

            self.buttons.append(self.button)

            self.button.setGeometry(200,150,280,40)
       
            self.button.move(60,location)
            location += 60


           

       # for i in self.buttons:
        
           # i.clicked.connect(self.gotoSeeOrder(itemnum))


    #Using the item number goto the order selected by the user
    def gotoSeeOrder(self,itemnum):
        print(itemnum)
        seeOrder = SeeOrder(itemnum)
       
        widget.addWidget(seeOrder)
        widget.setCurrentIndex(widget.currentIndex()+1)
       
class SeeOrder(QMainWindow):
    def __init__(self,itemnum):
        super(SeeOrder,self).__init__()
  
        loadUi("SeeOrder.ui",self) # Load the GUI
      
        self.displayOrder = QLabel(orderList[itemnum],self) # Display as a label
    
        
#Specifies the functionality for saving data
class SaveData:
    def __init__(self):

        #Appends to the CSV file then closes the CSV file
        self.appendToCSVFile()
        self.closeCSVFile()

    #Writes the orderlist which contains the user entered data to a CSV file called Orders
    def appendToCSVFile(self):
        self.file = open('Orders.csv', 'a',newline = '\n')
        with self.file:
           
            write = csv.writer(self.file)
            
            write.writerow(orderList)
        
    #Closes the file
    def closeCSVFile(self):
        self.file.close()
        
        
#Specifies the functionality for reading a CSV file
class ReadData:
    def __init__(self):
        self.openAndReadFile()
        self.closeCSVFile()

    #Opens and reads the file appending the data into the Orderlist
    def openAndReadFile(self):
        with open('Orders.csv') as self.file:
            reader = csv.reader(self.file,delimiter= ',')
            for i in reader:
                
                orderList.append(str(i))
            
    #Closes the CSV file
    def closeCSVFile(self):
        self.file.close()
        
#Creates the window and sets the login screen to be the inital interface
app=QApplication(sys.argv)
mainWindow =Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)

#Sets fixed width and height
widget.setFixedWidth(400)
widget.setFixedHeight(680)

#Displays widgets
widget.show()

app.exec_()


