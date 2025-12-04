import sys
import threading
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QLineEdit, QPushButton, QStackedWidget, QStackedLayout, QMessageBox, QFormLayout, QInputDialog, QDialog, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QPixmap, QPalette, QBrush, QIcon
from PySide6.QtWidgets import QScrollArea, QGridLayout
# =========================
# Global Storage
# =========================

dict_rooms = {
    '1': [],
    '2': [],
    '3': [],
    '4': [],
}

rooms = {}
current_user = None  # Add this line
# =========================
# Model Classes
# =========================

class ArtifactModel:
    def __init__(self, title, description, location, image):
        self.title = title
        self.description = description
        self.location = location
        self.image = image

class RoomModel:
    def __init__(self, name, description, image, artifacts=None):
        self.name = name
        self.description = description
        self.image = image
        self.artifacts = artifacts if artifacts else []

# Initialize rooms with sample data
rooms['1'] = RoomModel(
    name="Ancient Egypt Room",
    description="Explore the wonders of ancient Egyptian civilization.",
    image="./images/1.jpg",
    artifacts=[]
)

rooms['2'] = RoomModel(
    name="Pharaohs Hall",
    description="Discover the lives of the great pharaohs.",
    image="./images/2.jpg",
    artifacts=[]
)

rooms['3'] = RoomModel(
    name="Artifacts Gallery",
    description="A collection of ancient artifacts from Egypt.",
    image="./images/3.jpg",
    artifacts=[]
)

rooms['4'] = RoomModel(
    name="Mummies Exhibit",
    description="Learn about mummification and the afterlife.",
    image="./images/4.jpg",
    artifacts=[]
)

# Initialize sample artifacts
rooms['1'].artifacts.append(ArtifactModel(
    title="Statue of Pharaoh",
    description="A stone statue of an ancient Egyptian pharaoh.",
    location='1',
    image='./images/1.jpg'
))

rooms['2'].artifacts.append(ArtifactModel(
    title="Ancient Mummy",
    description="Preserved mummy from the New Kingdom period.",
    location='2',
    image='./images/2.jpg'
))

rooms['3'].artifacts.append(ArtifactModel(
    title="Hieroglyphic Tablet",
    description="Stone tablet with inscribed hieroglyphics.",
    location='3',
    image='./images/3.jpg'
))

rooms['4'].artifacts.append(ArtifactModel(
    title="Golden Jewelry",
    description="Ancient Egyptian gold jewelry and ornaments.",
    location='4',
    image='./images/4.jpg'
))

class UserModel:
    def __init__(self, gmail, password, name, from_where, phone_number):
        self.gmail = gmail
        self.password = password
        self.name = name
        self.from_where = from_where
        self.phone_number = phone_number


# =========================
# System Class
# =========================

class system:

    dict_available = {
        '1': 10,
        '2': 8,
        '3': 12,
        '4': 6,
    }

    dict_namebooking = {
        '1': [],
        '2': [],
        '3': [],
        '4': [],
    }

    def __init__(self):
        pass


# =========================
# Artifact Logic
# =========================

class artifact:
    

    def add(self, location, description, title, image):
        new_artifact = ArtifactModel(title, description, location, image)
        dict_rooms[location].append(new_artifact)
        if location in rooms:
            rooms[location].artifacts.append(new_artifact)
        print("Done")

    def display(self):
        for room, artifacts in dict_rooms.items():
            print(f"Artifacts in {room}:")
            for a in artifacts:
                print(f"  Title: {a.title}")
                print(f"  Image: {a.image}")  # GUI
                print(f"  Description: {a.description}")

    def search(self, title, room):
        for a in dict_rooms.get(room, []):
            if a.title == title:
                return a
        print ("artifact not found")
        return False

    def delete(self, title, room):

        a=self.search(title, room)
        if a:
            dict_rooms[room].remove(a)
            print ("artifact deleted")


    def update(self, title, room, new_description, new_image,new_room):
        a=self.search(title, room)

        if a:
            a.description = new_description
            a.image = new_image
            if room != new_room:
                dict_rooms[room].remove(a)
                a.location = new_room
                dict_rooms[new_room].append(a)
            print( "artifact updated")




# =========================
# User Logic
# =========================

class User:
    users = []   # ALL users stored here

    def __init__(self, system_obj):
        self.system = system_obj
        self.gmail = None

    def created_account(self, gmail, password, name, from_where, phone_number):
        for u in User.users:
            if u.gmail == gmail:
                print("account already exists")
                return

        new_user = UserModel(gmail, password, name, from_where, phone_number)
        User.users.append(new_user)

        self.gmail = gmail
        print("account created successfully")

    def login(self, gmail, password):
        for u in User.users:
            if u.gmail == gmail and u.password == password:
                self.gmail = gmail
                # Store user info in this instance
                self.name = u.name
                self.from_where = u.from_where
                self.phone_number = u.phone_number
                print(f"Hi {u.name}")
                return True
        print("Error: email or password is incorrect")
        return False

    def payment(self, gui_mode=False, parent_widget=None):
        if gui_mode and parent_widget:
            # GUI mode - show a dialog instead of console input
            reply = QMessageBox.question(
                parent_widget,
                "Payment",
                "Do you want to pay now?",
                QMessageBox.Yes | QMessageBox.No
            )
            return reply == QMessageBox.Yes
        else:
            # CLI mode
            input_payment = input("do you want to pay now? yes/no: ")
            return input_payment.lower() == "yes"

    def book(self, room, num_people=1, gui_mode=False, parent_widget=None):
        # Check if room exists in the system
        if room not in self.system.dict_available:
            if gui_mode and parent_widget:
                QMessageBox.warning(parent_widget, "Error", f"Room {room} does not exist")
            else:
                print(f"Room {room} does not exist")
            return False
            
        # Check if there are enough available spots
        if self.system.dict_available[room] >= num_people:
            # Make payment
            if self.payment(gui_mode, parent_widget):
                # Update available spots
                self.system.dict_available[room] -= num_people
                
                # Add booking to the system
                for _ in range(num_people):
                    if self.gmail not in self.system.dict_namebooking[room]:
                        self.system.dict_namebooking[room].append(self.gmail)
                
                if gui_mode and parent_widget:
                    QMessageBox.information(parent_widget, "Success", f"Successfully booked {num_people} ticket(s) for room {room}")
                else:
                    print(f"Successfully booked {num_people} ticket(s) for room {room}")
                return True
            else:
                if gui_mode and parent_widget:
                    QMessageBox.warning(parent_widget, "Payment Failed", "Booking cancelled")
                else:
                    print("Payment failed")
                return False
        else:
            if gui_mode and parent_widget:
                QMessageBox.warning(parent_widget, "Not Available", f"Not enough available spots in room {room}. Available: {self.system.dict_available[room]}")
            else:
                print(f"Not enough available spots in room {room}. Available: {self.system.dict_available[room]}")
            return False
# =========================
# Admin Logic
# =========================

class admin:

    dict_price = {
        '1': 100,
        '2': 150,
        '3': 200,
        '4': 250,
    }

    def __init__(self):
        self.system = system()
        self.artifact = artifact()
        self.user_obj = User(self.system)

    def login_admin(self, admin_name, admin_password):
        if admin_name == "taho" and admin_password == "ad123":
            print("welcome admin")
            return True
        print("error admin name or password is incorrect")
        return False

    def all_booking(self, room): # done[1]
        return self.system.dict_namebooking[room]
    
    def display_price(self):
        print(self.dict_price) #all_booking,display_price,update_price,display_available_rooms,add_room,remove_room,view_customers,determine_room_capacity

    def update_price(self, new_price, room):
        self.dict_price[room] = new_price
        print( "price updated")

    def display_available_rooms(self):
        for room, available in self.system.dict_available.items():
            print(f"{room}: {available} available")

    def add_room(self, new_room, new_price, number_of_available, description, image):
        global rooms
        dict_rooms[new_room] = []
        self.dict_price[new_room] = new_price
        self.system.dict_available[new_room] = number_of_available
        self.system.dict_namebooking[new_room] = []
        rooms[new_room] = RoomModel(name=new_room, description=description, image=image, artifacts=[])

    def remove_room(self, room):
        if room in dict_rooms:
            del dict_rooms[room]
        if room in self.dict_price:
            del self.dict_price[room]
        if room in self.system.dict_available:
            del self.system.dict_available[room]
        if room in self.system.dict_namebooking:
            del self.system.dict_namebooking[room]

    def view_customers(self):
        for u in User.users:
            print(f"Name: {u.name}, Gmail: {u.gmail}, From: {u.from_where}, Phone: {u.phone_number}")

    def determine_room_capacity(self, room):
        self.system.dict_available[room]=int(input(f"Enter number of available in {room}: "))
        print("Done")

    def update_room_info(self, room_name, new_description, new_image):
        global rooms
        if room_name in rooms:
            rooms[room_name].description = new_description
            rooms[room_name].image = new_image
            print("Room info updated")
        else:
            print("Room not found")



def main():
    adm = admin()                    
    user = User(adm.system)         

    while True:
        print("\n===== Museum System =====")
        print("1) Admin Login")
        print("2) Create User Account")
        print("3) User Login")
        print("4) Exit")

        choice = input("Choose: ")

        if choice == "1":
            admin_name = input("Enter admin name: ")
            admin_password = input("Enter admin password: ")

            if adm.login_admin(admin_name, admin_password):
                while True:
                    print("\n--- Admin Menu ---")
                    print("1) Add Artifact")
                    print("2) Delete Artifact")
                    print("3) Update Artifact")
                    print("4) Display Artifacts")
                    print("5) Add Room")
                    print("6) Remove Room")
                    print("7) Show Available Rooms")
                    print("8) View All Bookings")
                    print("9) View Customers")
                    print("10) Display Rooms Prices")
                    print("11) Update Room Price")
                    print("12) Determine Room Capacity")
                    print("13) Back")

                    admin_choice = input("Choose: ")

                    if admin_choice == "1":
                        title = input("Title: ")
                        desc = input("Description: ")
                        room = input("Room: ")
                        img = input("Image path: ")
                        adm.artifact.add(room, desc, title, img)

                    elif admin_choice == "2":
                        title = input("Title to delete: ")
                        room = input("Room: ")
                        print(adm.artifact.delete(title, room))

                    elif admin_choice == "3":
                        title = input("Title to search: ")
                        room = input("current Room: ")
                        desc = input("New Description: ")
                        img = input("New Image path: ")
                        new_room = input('New Room: ')
                        adm.artifact.update(title, room, desc, img,new_room)

                    elif admin_choice == "4":
                        adm.artifact.display()

                    elif admin_choice == "5":
                        room = input("New room name: ")
                        price = int(input("Room price: "))
                        available = int(input("Number of available spots: "))
                        adm.add_room(room, price, available)

                    elif admin_choice == "6":
                        room = input("Room to remove: ")
                        adm.remove_room(room)

                    elif admin_choice == "7":
                        adm.display_available_rooms()

                    elif admin_choice == "8":
                        room = input("Room: ")
                        print(adm.all_booking(room))

                    elif admin_choice == "9":
                        adm.view_customers()

                    elif admin_choice == "10":
                        adm.display_price()

                    elif admin_choice == "11":
                        room = input("Room: ")
                        price = int(input("New price: "))
                        adm.update_price(price, room)
                    
                    elif admin_choice == "12":
                        room = input("Room: ")
                        adm.determine_room_capacity(room)

                    elif admin_choice == "13":
                        break



        elif choice == "2":
            gmail = input("gmail: ")
            password = input("password: ")
            name = input("name: ")
            from_where = input("from where: ")
            phone_number = input("phone number: ")
            if len(password)>4 and gmail.count('@')==1 and len(phone_number)<17 and len(phone_number)>4 :
                user.created_account(gmail, password, name, from_where, phone_number)
            print("Invalid input data")

        elif choice == "3":
         gmail = input("gmail: ")
         password = input("password: ")

        logged_in= user.login(gmail, password)

        if logged_in:   # logged in
          while True:
            print("\n--- User Menu ---")
            print("1) Book Room")
            print("2) Logout")

            user_choice = input("Choose: ")

        if user_choice == "1":
            room = input("Room name: ")
    # Ask for number of people
            try:
                num_people = int(input("Number of people: "))
                user.book(room, num_people)  # CLI mode, no gui_mode parameter
            except ValueError:
                print("Please enter a valid number")

        elif user_choice == "2":
                user.gmail = None
                break
        elif choice == "4":
            print("Goodbye!")
            break

class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Egyptian Museum")
        self.setFixedSize(800, 600)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        # Keep track of navigation history
        self.page_history = []
        self.rooms = rooms

        #create instances of different pages
        self.mainPage = MainPage(self) #index 0
        self.loginPage = LoginPage(self) #index 1
        self.signupPage = SignupPage(self) #index 2
        self.adminLoginPage = AdminLoginPage(self) #index 3
        self.adminPage = AdminPage(self) #index 4
        self.paymentPage = PaymentPage(self) #index 5
        self.roomsPage = RoomsPage(self, rooms) #index 6
        #add pages to stacked widget
        self.stacked_widget.addWidget(self.mainPage)
        self.stacked_widget.addWidget(self.loginPage)
        self.stacked_widget.addWidget(self.signupPage)
        self.stacked_widget.addWidget(self.adminLoginPage)
        self.stacked_widget.addWidget(self.adminPage)
        self.stacked_widget.addWidget(self.paymentPage)
        self.stacked_widget.addWidget(self.roomsPage)
        #start with the main page
        self.stacked_widget.setCurrentIndex(0)

    def go_to_login(self):
        self.stacked_widget.setCurrentIndex(1)
    
    def go_to_signup(self):
        self.stacked_widget.setCurrentIndex(2)
    
    def go_to_admin_login(self):
        self.stacked_widget.setCurrentIndex(3)
    
    def go_to_admin_page(self):
        self.stacked_widget.setCurrentIndex(4)
    
    def go_to_payment(self):
        self.stacked_widget.setCurrentIndex(5)
    
    def go_to_rooms(self):
        self.stacked_widget.setCurrentIndex(6)

    def go_to_main(self):
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_page(self, page):
        if page not in [self.stacked_widget.widget(i) for i in range(self.stacked_widget.count())]:
            self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)
        self.page_history.append(page)
  
class MainPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        title = QLabel("Welcome to the Egyptian Museum")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        login_button = QPushButton("User Login")
        signup_button = QPushButton("Create Account")
        admin_login_button = QPushButton("Admin Login")

        login_button.clicked.connect(self.main_window.go_to_login)
        signup_button.clicked.connect(self.main_window.go_to_signup)
        admin_login_button.clicked.connect(self.main_window.go_to_admin_login)

        layout.addWidget(title)
        layout.addWidget(login_button)
        layout.addWidget(signup_button)
        layout.addWidget(admin_login_button)

        self.setLayout(layout)
       
class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        title = QLabel("User Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        form_layout = QFormLayout()
        self.gmail_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Gmail:", self.gmail_input)
        form_layout.addRow("Password:", self.password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        # back to main page button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.main_window.go_to_main)

        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(login_button)
        layout.addWidget(back_button)

        self.setLayout(layout)
        
    def login(self):
        global current_user  # Add this
        email = self.gmail_input.text()
        password = self.password_input.text()
        if email and password:
            user_obj = User(system())
            success = user_obj.login(email, password)
            if success:
                # Set the current user
                current_user = user_obj
                QMessageBox.information(self, "Login", f"Welcome {email}!")
                self.main_window.go_to_rooms()
            else:
                QMessageBox.warning(self, "Login", "Invalid email or password")
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields")
class SignupPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        title = QLabel("Create User Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        form_layout = QFormLayout()
        self.gmail_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.name_input = QLineEdit()
        self.from_where_input = QLineEdit()
        self.phone_number_input = QLineEdit()

        form_layout.addRow("Gmail:", self.gmail_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("From Where:", self.from_where_input)
        form_layout.addRow("Phone Number:", self.phone_number_input)

        signup_button = QPushButton("Create Account")
        signup_button.clicked.connect(self.created_account)

        #back to main page button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.main_window.go_to_main)


        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(signup_button)
        layout.addWidget(back_button)

        self.setLayout(layout)
        
    def created_account(self):
            gmail = self.gmail_input.text()
            password = self.password_input.text()
            name = self.name_input.text()
            from_where = self.from_where_input.text()
            phone_number = self.phone_number_input.text()

            if gmail and password and name and from_where and phone_number:
                user = User(system())
                user.created_account(gmail, password, name, from_where, phone_number)
                QMessageBox.information(self, "Account Created", "Your account has been created successfully!")
                self.main_window.go_to_login()
            else:
                QMessageBox.warning(self, "Error", "Please fill all fields")
class AdminLoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        title = QLabel("Admin Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        form_layout = QFormLayout()
        self.admin_name_input = QLineEdit()
        self.admin_password_input = QLineEdit()
        self.admin_password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Admin Name:", self.admin_name_input)
        form_layout.addRow("Admin Password:", self.admin_password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login_admin)
        #back to main page button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.main_window.go_to_main)


        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(login_button)
        layout.addWidget(back_button)

        self.setLayout(layout)
        
    def login_admin(self):
            admin_name = self.admin_name_input.text()
            admin_password = self.admin_password_input.text()
            if admin_name and admin_password:
                adm = admin()
                success = adm.login_admin(admin_name, admin_password)
                if success:
                    QMessageBox.information(self, "Login", f"Welcome Admin {admin_name}!")
                    self.main_window.go_to_admin_page()
                else:
                    QMessageBox.warning(self, "Login", "Invalid admin name or password")
            else:
                QMessageBox.warning(self, "Error", "Please fill all fields")
class AdminPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        title = QLabel("Admin Page")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        layout.addWidget(title)
        # Add admin functionalities here
        #all functions used
        #all_booking,display_price,update_price,display_available_rooms,add_room,remove_room,view_customers,determine_room_capacity
        self.button_1 = QPushButton("View All Bookings")
        self.button_2 = QPushButton("Display Room Prices")
        self.button_3 = QPushButton("Update Room Price")
        self.button_4 = QPushButton("Display Available Rooms")
        self.button_5 = QPushButton("Add Room")
        self.button_6 = QPushButton("Remove Room")
        self.button_7 = QPushButton("Add Artifact")
        self.button_8 = QPushButton("View Customers")
        self.button_9 = QPushButton("Determine Room Capacity")
        self.button_10 = QPushButton("Update Room Info")
        #back to main page button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.main_window.go_to_main)
        layout.addWidget(back_button)

        #add the function to every button
        self.button_1.clicked.connect(self.view_all_bookings)
        self.room_input_1 = QLineEdit()
        self.room_input_1.setPlaceholderText("Enter Room Name ...")
        self.button_2.clicked.connect(self.display_room_prices)
        self.button_3.clicked.connect(self.update_room_price)
        self.room_input_2 = QLineEdit()
        self.room_input_2.setPlaceholderText("Enter Room Name ...")
        self.button_4.clicked.connect(self.display_available_rooms)
        self.button_5.clicked.connect(self.add_room)
        self.button_6.clicked.connect(self.remove_room)
        self.button_7.clicked.connect(self.add_artifact)
        self.room_input_4 = QLineEdit()
        self.room_input_4.setPlaceholderText("Enter Room Name for Artifact ...")
        self.button_8.clicked.connect(self.view_customers)
        self.button_9.clicked.connect(self.determine_room_capacity)
        self.room_input_3 = QLineEdit()
        self.room_input_3.setPlaceholderText("Enter Room Name ...")
        self.button_10.clicked.connect(self.update_room_info)
        self.room_input_5 = QLineEdit()
        self.room_input_5.setPlaceholderText("Enter Room Name to Update ...")

        #add buttons to layout
        layout.addWidget(self.button_1)
        layout.addWidget(self.room_input_1)
        layout.addWidget(self.button_2)
        layout.addWidget(self.button_3)
        layout.addWidget(self.room_input_2)
        layout.addWidget(self.button_4)
        layout.addWidget(self.button_5)
        layout.addWidget(self.button_6)
        layout.addWidget(self.button_7)
        layout.addWidget(self.room_input_4)
        layout.addWidget(self.button_8)
        layout.addWidget(self.button_9)
        layout.addWidget(self.room_input_3)
        layout.addWidget(self.button_10)
        layout.addWidget(self.room_input_5)

        self.setLayout(layout)
        

    def view_all_bookings(self):
         adm = admin()
         room = self.room_input_1.text()
         bookings = adm.all_booking(room)
         QMessageBox.information(self, "All Bookings", f"Bookings for {room}: {bookings}")

    def display_room_prices(self):
        adm = admin()
        adm.display_price()
        QMessageBox.information(self, "Room Prices",
                        "\n".join(f"{room}: ${price}" for room, price in adm.dict_price.items()))

    def update_room_price(self):
        adm = admin()
        room = self.room_input_2.text()
        new_price, ok = QInputDialog.getInt(self, "Update Price", f"Enter new price for {room}:")
        if ok:
            adm.update_price(new_price, room)
            QMessageBox.information(self, "Success", f"Price for {room} updated to ${new_price}")

    def display_available_rooms(self):
        adm = admin()
        adm.display_available_rooms()
        available_rooms = "\n".join(f"{room}: {available} available" for room, available in adm.system.dict_available.items())
        QMessageBox.information(self, "Available Rooms", available_rooms)

    def add_room(self):
        adm = admin()
        new_room, ok1 = QInputDialog.getText(self, "Add Room", "Enter new room name:")
        new_price, ok2 = QInputDialog.getInt(self, "Add Room", f"Enter price for {new_room}:")
        number_of_available, ok3 = QInputDialog.getInt(self, "Add Room", "Enter number of available spots:")
        room_description, ok4 = QInputDialog.getText(self, "Add Room", "Enter room description:")
        room_image, ok5 = QInputDialog.getText(self, "Add Room", "Enter room image path:")

        if ok1 and ok2 and ok3 and ok4 and ok5 and new_room.strip() != '' and room_description.strip() != '' and room_image.strip() != '':
            adm.add_room(new_room, new_price, number_of_available, room_description, room_image)
            QMessageBox.information(self, "Success", f"Room {new_room} added with price ${new_price}")
            
            # Update main_window rooms to match global rooms
            self.main_window.rooms = rooms
            
            def refresh_after_add():
                try:
                    # Update rooms reference
                    self.main_window.roomsPage.rooms = self.main_window.rooms
                    # Refresh display
                    self.main_window.roomsPage.refresh_display()
                    # Switch to rooms page
                    self.main_window.stacked_widget.setCurrentWidget(self.main_window.roomsPage)
                except Exception as e:
                    print(f"Error after adding room: {e}")
                    self.main_window.stacked_widget.setCurrentWidget(self.main_window.roomsPage)
            
            QTimer.singleShot(100, refresh_after_add)
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields.")

    def remove_room(self):
        adm = admin()
        room, ok = QInputDialog.getText(self, "Remove Room", "Enter room name to remove:")
        if ok:
            adm.remove_room(room)
            QMessageBox.information(self, "Success", f"Room {room} removed")

    def view_customers(self):
        adm = admin()
        adm.view_customers()
        customers = "\n".join(f"Name: {u.name}, Gmail: {u.gmail}, From: {u.from_where}, Phone: {u.phone_number}" for u in User.users)
        QMessageBox.information(self, "Customers", customers)

    def determine_room_capacity(self):
        adm = admin()
        room = self.room_input_3.text()
        capacity, ok = QInputDialog.getInt(self, "Determine Capacity", f"Enter number of available in {room}:")
        if ok:
            adm.system.dict_available[room] = capacity
            QMessageBox.information(self, "Success", f"Capacity for {room} set to {capacity}")

    def add_artifact(self):
        adm = admin()
        room = self.room_input_4.text()
        title, ok1 = QInputDialog.getText(self, "Add Artifact", "Enter artifact title:")
        description, ok2 = QInputDialog.getText(self, "Add Artifact", "Enter artifact description:")
        image, ok3 = QInputDialog.getText(self, "Add Artifact", "Enter artifact image path:")

        if ok1 and ok2 and ok3 and room.strip() != '' and title.strip() != '' and description.strip() != '' and image.strip() != '':
            adm.artifact.add(room, description, title, image)
            QMessageBox.information(self, "Success", f"Artifact '{title}' added to room '{room}'")
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields.")

    def update_room_info(self):
        room_name = self.room_input_5.text()
        
        # Debug: Show what rooms are available
        print(f"Looking for room: '{room_name}'")
        print(f"Available rooms: {list(self.main_window.rooms.keys())}")
        
        # Check if room exists by key or by name
        room_found = False
        room_key = None
        
        # First check by key
        if room_name in self.main_window.rooms:
            room_found = True
            room_key = room_name
        else:
            # Check by room name
            for key, room_obj in self.main_window.rooms.items():
                if room_obj.name == room_name:
                    room_found = True
                    room_key = key
                    break
        
        if not room_found:
            QMessageBox.warning(self, "Error", f"Room '{room_name}' not found!")
            return
        
        new_description, ok1 = QInputDialog.getText(self, "Update Room Info", 
                                                    f"Enter new description for {room_name}:")
        new_image, ok2 = QInputDialog.getText(self, "Update Room Info", 
                                              f"Enter new image path for {room_name}:")
        
        if ok1 and ok2 and room_name.strip() != '' and new_description.strip() != '' and new_image.strip() != '':
            # Update the room object
            room_obj = self.main_window.rooms[room_key]
            room_obj.description = new_description
            room_obj.image = new_image
            
            # Also update global rooms dict
            global rooms
            if room_key in rooms:
                rooms[room_key].description = new_description
                rooms[room_key].image = new_image
            
            QMessageBox.information(self, "Success", f"Room '{room_name}' info updated")
            
            # Use QTimer to defer the UI refresh (prevents crashes)
            def refresh_after_update():
                try:
                    # Update rooms reference
                    self.main_window.roomsPage.rooms = self.main_window.rooms
                    
                    # Switch to rooms page
                    self.main_window.stacked_widget.setCurrentWidget(self.main_window.roomsPage)
                    
                    # Simple refresh - just update the current display
                    self.main_window.roomsPage.refresh_display()
                except Exception as e:
                    print(f"Error refreshing rooms: {e}")
                    # Fallback: just switch to rooms page
                    self.main_window.stacked_widget.setCurrentWidget(self.main_window.roomsPage)
            
            QTimer.singleShot(100, refresh_after_update)  # 100ms delay
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields.")

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QScrollArea
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

class RoomsPage(QWidget):
    @staticmethod
    def button_style():
        return """
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                color: #ffd700;
                background-color: #333;
                border-radius: 8px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """

    def __init__(self, main_window, rooms):
        super().__init__()
        self.main_window = main_window
        self.rooms = rooms
        self.build_ui()
    
    def build_ui(self):
        layout = QVBoxLayout(self)
        
        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedHeight(40)
        back_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                color: #ffd700;
                background-color: #333;
                border-radius: 8px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)
        
        # Title
        title = QLabel("Egyptian Museum - Rooms")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; color: #d4af37;")
        layout.addWidget(title)
        
        # Check if rooms exist
        if not self.rooms:
            no_rooms_label = QLabel("No rooms available.")
            no_rooms_label.setAlignment(Qt.AlignCenter)
            no_rooms_label.setStyleSheet("font-size: 20px; color: red;")
            layout.addWidget(no_rooms_label)
            return
        
        # Create scroll area with rooms
        self.create_rooms_scroll_area(layout)
    
    def create_rooms_scroll_area(self, parent_layout):
        """Helper method to create the scroll area with rooms"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(25)
        
        row = 0
        col = 0
        
        for room_key, room_obj in self.rooms.items():
            btn = QPushButton()
            btn.setFixedSize(240, 240)
            btn.setIconSize(QSize(230, 230))
            
            # Check if image exists
            if os.path.exists(room_obj.image):
                btn.setIcon(QIcon(room_obj.image))
            else:
                # Use default icon
                btn.setIcon(QIcon.fromTheme("folder"))
                btn.setText(f"{room_obj.name}\n(No Image)")
                btn.setStyleSheet("font-size: 14px; color: #ffd700;")
            
            btn.clicked.connect(lambda checked, key=room_key: self.open_room(key))
            
            name_label = QLabel(room_obj.name)
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("font-size: 18px; color: #ffd700; font-weight: bold;")
            
            box = QVBoxLayout()
            box.addWidget(btn)
            box.addWidget(name_label)
            
            wrap = QWidget()
            wrap.setLayout(box)
            grid.addWidget(wrap, row, col)
            
            col += 1
            if col >= 2:
                col = 0
                row += 1
        
        scroll.setWidget(container)
        parent_layout.addWidget(scroll)
    
    def refresh_display(self):
        """Refresh the rooms display without rebuilding entire layout"""
        try:
            # Find and remove the scroll area if it exists
            for i in range(self.layout().count()):
                widget = self.layout().itemAt(i).widget()
                if isinstance(widget, QScrollArea):
                    self.layout().removeWidget(widget)
                    widget.deleteLater()
                    break
            
            # Add new scroll area with updated rooms
            if self.rooms:
                self.create_rooms_scroll_area(self.layout())
        except Exception as e:
            print(f"Error in refresh_display: {e}")
    
    def open_room(self, room_key):
        room_obj = self.rooms[room_key]
        page = RoomDetailPage(self.main_window, room_key, room_obj)
        self.main_window.switch_to_page(page)
    
    def go_back(self):
        self.main_window.go_to_main()
    
    def update_rooms(self, updated_rooms):
        """Update rooms and refresh display - simpler version"""
        self.rooms = updated_rooms
        
        # Use QTimer to defer refresh
        def deferred_refresh():
            self.refresh_display()
        
        QTimer.singleShot(50, deferred_refresh)


# =========================
# Room Detail Page
# =========================
# =========================
# Room Detail Page
# =========================
# =========================
# Room Detail Page
# =========================
class RoomDetailPage(QWidget):
    def __init__(self, main_window, key, room):
        super().__init__()
        self.main_window = main_window
        self.key = key
        self.room = room
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Back button
        back_btn = QPushButton("← Back to Rooms")
        back_btn.setFixedHeight(35)
        back_btn.setStyleSheet(RoomsPage.button_style())
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)
        
        # Room Title
        title = QLabel(self.room.name)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #d4af37;")
        layout.addWidget(title)
        
        # Room description
        desc = QLabel(self.room.description)
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 18px; color: white;")
        layout.addWidget(desc)
        
        # Get room price from admin class
        adm = admin()
        room_price = adm.dict_price.get(self.key, 0)
        
        # Available spots
        system_obj = system()
        available_spots = system_obj.dict_available.get(self.key, 0)
        
        # Available spots label
        spots_label = QLabel(f"Available spots: {available_spots}")
        spots_label.setStyleSheet("font-size: 16px; color: #ffd700; font-weight: bold;")
        layout.addWidget(spots_label)
        
        # Price label
        price_label = QLabel(f"Price: ${room_price} per ticket")
        price_label.setStyleSheet("font-size: 16px; color: #ffd700; font-weight: bold;")
        layout.addWidget(price_label)
        
        # Booking button
        book_button = QPushButton(f"Book Now - ${room_price} per ticket")
        book_button.setFixedHeight(45)
        book_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                color: white;
                background-color: #27ae60;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
            }
        """)
        
        # Check if user is logged in
        global current_user
        if not current_user or not current_user.gmail:
            book_button.setEnabled(False)
            book_button.setText("Please Login to Book")
        elif available_spots <= 0:
            book_button.setEnabled(False)
            book_button.setText("Sold Out")
        
        book_button.clicked.connect(self.book_tickets)
        layout.addWidget(book_button)
        
        # Artifacts list
        if not self.room.artifacts:
            empty = QLabel("No artifacts in this room yet.")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("font-size: 16px; color: gray;")
            layout.addWidget(empty)
        else:
            artifacts_label = QLabel("Artifacts in this room:")
            artifacts_label.setStyleSheet("font-size: 20px; color: #d4af37; font-weight: bold;")
            layout.addWidget(artifacts_label)
            
            for art in self.room.artifacts:
                btn = QPushButton(art.title)
                btn.setStyleSheet(RoomsPage.button_style())
                btn.clicked.connect(lambda checked, a=art: self.open_artifact(a))
                layout.addWidget(btn)
    
    def book_tickets(self):
     global current_user
    
    # Check if user is logged in
     if not current_user or not current_user.gmail:
        QMessageBox.warning(self, "Login Required", "Please login to book tickets.")
        return
    
    # Get room price
     adm = admin()
     room_price = adm.dict_price.get(self.key, 0)
    
    # Get available spots
     system_obj = system()
     available_spots = system_obj.dict_available.get(self.key, 0)
    
     if available_spots <= 0:
        QMessageBox.warning(self, "Sold Out", "This room is sold out!")
        return
    
    # Ask for number of tickets
     num_tickets, ok = QInputDialog.getInt(
        self, 
        "Book Tickets", 
        f"Enter number of tickets (${room_price} each)\nAvailable spots: {available_spots}",
        1,      # Default value
        1,      # Minimum value
        available_spots,  # Maximum value
        1       # Step
    )
    
     if ok and num_tickets > 0:
        if num_tickets > available_spots:
            QMessageBox.warning(self, "Not Enough Spots", 
                              f"Only {available_spots} spots available.")
            return
        
        # Calculate total price
        total_price = num_tickets * room_price
        
        # Ask for confirmation
        confirm = QMessageBox.question(
            self,
            "Confirm Booking",
            f"Book {num_tickets} ticket(s) for {self.room.name}?\n"
            f"Price per ticket: ${room_price}\n"
            f"Total: ${total_price}\n\n"
            f"Proceed with payment?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Try to book - USE GUI MODE
            success = current_user.book(self.key, num_tickets, gui_mode=True, parent_widget=self)
            if success:
                QMessageBox.information(self, "Booking Successful", 
                                      f"Successfully booked {num_tickets} ticket(s)!\n"
                                      f"Total paid: ${total_price}")
                
                # Update available spots display
                system_obj = system()
                available_spots = system_obj.dict_available.get(self.key, 0)
                
                # Find and update the spots label
                for i in range(self.layout().count()):
                    widget = self.layout().itemAt(i).widget()
                    if isinstance(widget, QLabel) and "Available spots:" in widget.text():
                        widget.setText(f"Available spots: {available_spots}")
                        break
                
                # Update button if sold out
                if available_spots <= 0:
                    for i in range(self.layout().count()):
                        widget = self.layout().itemAt(i).widget()
                        if isinstance(widget, QPushButton) and "Book Now" in widget.text():
                            widget.setEnabled(False)
                            widget.setText("Sold Out")
                            break
            else:
                QMessageBox.warning(self, "Booking Failed", "Booking was not successful.")
    
    def open_artifact(self, artifact):
        self.main_window.switch_to_page(ArtifactDetailPage(self.main_window, self.key, self.room, artifact))
    
    def go_back(self):
        # Go back to rooms page
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.roomsPage)
# =========================
# Artifact Detail Page
# =========================
class ArtifactDetailPage(QWidget):
    def __init__(self, main_window, key, room, artifact):
        super().__init__()
        self.main_window = main_window
        self.key = key
        self.room = room
        self.artifact = artifact
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Back button
        back_btn = QPushButton("← Back to Room")
        back_btn.setFixedHeight(35)
        back_btn.setStyleSheet(RoomsPage.button_style())
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        # Artifact title
        title = QLabel(self.artifact.title)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #d4af37;")
        layout.addWidget(title)

        # Artifact image
        img = QLabel()
        img.setAlignment(Qt.AlignCenter)
        if os.path.exists(self.artifact.image):
            img.setPixmap(QPixmap(self.artifact.image).scaled(350, 350, Qt.KeepAspectRatio))
        else:
            img.setText("No Image Available")
            img.setStyleSheet("font-size: 16px; color: gray;")
        layout.addWidget(img)

        # Description
        desc = QLabel(self.artifact.description)
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 18px; color: white;")
        layout.addWidget(desc)

        # Origin
        loc = QLabel(f"Origin: {self.artifact.location}")
        loc.setStyleSheet("font-size: 18px; color: #d4af37;")
        layout.addWidget(loc)

    def go_back(self):
        self.main_window.switch_to_page(self.main_window.roomsPage)

class PaymentPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        title = QLabel("Payment Page")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        layout.addWidget(title)
        # Add payment functionalities here

        self.setLayout(layout)
        




if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    # Sample data initialization
    window = mainwindow()
    window.show()

    sys.exit(app.exec())