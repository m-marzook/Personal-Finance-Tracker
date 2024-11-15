import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime

#Creating a function to verify if a value inputted is of the data type 'float'
def float_input(msg, error_msg = "\nInvalid input. Please enter a numerical value.\n"):
    while True:
        try:
            num = float(input(msg))
        except ValueError:
            print(error_msg)
        else:
            #Changing the format of the number to ensure it has 2 decimal points
            return "{:.2f}".format(num)


#Creating a function to verify if a value inputted is of the data type 'int'
def int_input(msg, error_msg = "\nInvalid input. Please enter an integer value.\n"):
    while True:
        try:
            num = int(input(msg))
        except ValueError:
            print(error_msg)
        else:
            return num


#Creating a function to get input from user for the transaction type and verify if the allowed values have been inputted
def get_transaction_type(msg):
    while True:
        #Getting user input and converting it to uppercase for verification purposes
        #(as the following if-statement only takes 2 specific uppercase values and valid inputs)
        transaction_type = input(msg).upper()
        
        #Verifying if the transaction is an income/expense or if it is an invalid input
        if transaction_type == "CR":
            transaction_type = "Income"
            break
        elif transaction_type == "DR":
            transaction_type = "Expense"
            break
        else:
            print("\nInvalid Transaction type entered. Please type CR or DR\n")
    return transaction_type


#Creating a function to get input from user for their choice (yes or no) and verify if the allowed values have been inputted
def get_choice(msg):
    while True:
        #Getting user input and converting it to uppercase for verification purposes
        #(as the following if-statement only takes 2 specific uppercase values and valid inputs)
        choice = input(msg).upper()
        
        #Verifying if the user in put is "Y" or "N" or if it is an invalid input
        if choice == "Y":
            break
        elif choice == "N":
            break
        else:
            print("\nInvalid letter entered. Please type Y or N\n")
    return choice 


#Creating a function to get the date a transaction occured from the user
def get_transaction_date():
    while True:
        #Calling a function to verify if values inputted by the user are of the data type 'int'
        day = int_input("Enter the day the transaction took place : ")
        month = int_input("Enter the month the transaction took place : ")
        year = int_input("Enter the year the transaction took place : ")

        try:
            #Converting the user inputs to a date using the datetime module
            transaction_date = datetime(year, month, day).date()
        except ValueError:
            print("\nInvalid date. Please enter the correct date!\n")
        else:
            break
    return str(transaction_date)


#Creating a function to get information regarding a transaction from the user
def create_new_transaction(msg1, msg2, msg3):
    
    #Creating a sub dictionary to maintain the new transaction record
    sub_dict = {}
    
    #Calling float_input function to verify if amount inputted by the user is of the data type 'float'
    amount = float_input(msg1)
    purpose = input(msg2).capitalize()

    #Calling a function to get the type of transaction being made my the user
    type_ = get_transaction_type(msg3)

    #Calling a function to get the date from the user    
    date_ = get_transaction_date()

    #Adding the amount, type and date of a transaction to the sub dictionary
    sub_dict["amount"] = amount
    sub_dict["type"] = type_
    sub_dict["date"] = date_

    #Returning a list consisting of the purpose and sub dictionary
    return[purpose, sub_dict]


#Creating a function to load data from JSON file
def load_json(filename):
    try: 
        #Loading information in the JSON file to a data variable (with an initial value of None)
        loaded_data = None
        with open(filename, "r") as file:
            loaded_data = json.load(file)
    except json.JSONDecodeError as error_msg:
        print(f"Error decoding JSON: {error_msg}")
    except FileNotFoundError:
        print("Transaction records cannot be found.")
    return loaded_data


#Creating a function to bulk read information stored in the JSON file
def read_bulk_transactions_from_file(filename):
    #Creating an empty dictionary to store all transactions 
    transactions = {}

    #Calling a function to load  data from a JSON File
    bulk_data = load_json(filename)

    if bulk_data != None:    
        #Iterating through the key-value pairs of loaded data
        for expense, exp_transactions in bulk_data.items():

            #Iterating through the value (which consists of a transaction list) of each key
            for info in exp_transactions:

                #Creating a new list for all transactions related to the key (expenses/income category) if the key does not exist in the main transactions dictionary
                if expense not in transactions:
                    transactions[expense] = []

                #Using a temporary variable to append the expense(transaction) to the transactions list related to it's key (category)
                temp = transactions[expense]
                temp.append(info)
                transactions[expense] = temp

        return transactions

    else:
        return bulk_data


#Creating a function to add the values in the main transactions dictionary to a JSON file
def add_to_json(transactions, filename):
    with open(filename, "w") as file:
        file.write("{\n")
        #Iterating through the key-value pairs of the main transactions dictionary 
        for expense, exp_transactions in transactions.items():
            file.write(f'  "{expense}": [\n    ')

            #Iterating through the value (which consists of a transaction list) of each key in order to ensure every transaction gets serealized line-by-line
            # "info" represents each individual transaction under a certain key (which is an expense/income)
            for info in exp_transactions:
                json.dump(info, file)
                if info != exp_transactions[-1]:
                    file.write(",\n    ")
                else:
                    file.write("\n  ")

            #Adding the transaction keys to a list and changing how "]" is written to the JSON file based on if the final element in the keys list has been reached
            if expense == list(transactions.keys())[-1]:
                file.write("]\n")
            else:
                file.write("],\n")
                    
        file.write("}")
    return


#Creating a function to add a new transaction to the Finance Tracker
def add_transaction(transactions, filename):
    #Calling a function to create a list to store information about the transaction
    new_transaction = create_new_transaction("Enter the amount paid/receieved during the transaction : ", "Enter the purpose of the transaction : ", "Enter the type of transaction being made (Type 'CR' for Income or 'DR' for Expenses) : ")
    purpose = new_transaction[0]
    sub_dict = new_transaction[1]
    
    #Creating a new list for all transactions related to a key(purpose) if the key does not exist in the main transactions dictionary
    if purpose not in transactions:
        transactions[purpose] = []

    #Using a temporary variable to append the sub dictionary to the transactions list related to it's key   
    temp = transactions[purpose]
    temp.append(sub_dict)
    transactions[purpose] = temp

    #Calling a function to add all information from the main transactions dictionary to the JSON file
    add_to_json(transactions, filename)
    print("\nThe transaction has been successfully added.\n")
    return


#Creating a function to view all transactions recorded in the JSON file
def view_transactions(transactions):
    #Checking if the JSON file contains an empty dictionary. If the dictionary is empty, there are no financial records.
    if transactions != {}:
        #Displaying information about each transaction to the user by iterating through the key-value pairs of the main transactions dictionary
        for expense,exp_transactions in transactions.items():
            for info in exp_transactions:
                print(f"Transaction amount : {info["amount"]}\nTransaction purpose : {expense}\nTransaction type : {info["type"]}\nTransaction date : {info["date"]}\n\n")
    else:
        #Displaying a message if no transactions have been recorded
        print("There are no financial records.\n")
    return


#Creating a function to update a transaction from the Finance Tracker
def update_transaction(transactions, filename):
    #Allowing user to input transaction information to be updated if there are previous transaction records in the main transactions dictionary
    if transactions != {}:
        
        #Calling a function to create a new list for comparison purposes
        upd_transaction_info = create_new_transaction("Enter the amount of money from the transaction to be updated : ", "Enter the purpose of the transaction which should to be updated : ", "Enter the type of transaction which should be updated (Type 'CR' for Income or 'DR' for Expenses): ")
        purpose = upd_transaction_info[0]
        sub_dict = upd_transaction_info[1]
        
        #Comparing the the list information consisting of user inputs with existing transaction information to verify if the transaction exists
        try:
            for expense, exp_transactions in transactions.items():
                #Checking if the value of "purpose" is among the keys of the main dictionary
                if purpose == expense:
                    #Iterating through the values (which exist as lists consisting of dictionaries for each transaction) of the main transactions dictionary
                    for info in exp_transactions:
                        if sub_dict == info:
                            while True:
                                #Getting the field to be updated and it's updated value from the user
                                field = input("\nWhich field do you wish to update? (Please type Amount/Purpose/Type/Date) : ").lower()
                                if field == "amount":
                                    info["amount"] = float_input("Enter updated amount paid/recieved : ")
                                    
                                elif field == "purpose":
                                    new_expense = input("Enter updated purpose : ").capitalize()

                                    #Creating a new list for all transactions related to "new_expense" if the a key of the same value does not exist in the main transactions dictionary
                                    if new_expense not in transactions:
                                        transactions[new_expense] = []
                                        
                                    #Using a temporary variable to append the transaction information(the dictionary "info") to the transactions list related to it's key
                                    temp = transactions[new_expense]
                                    temp.append(info)
                                    transactions[new_expense] = temp

                                    #Deleting the old transaction "info" as the same transaction exists with a new key value(new_purpose)
                                    del transactions[expense][exp_transactions.index(info)]
         
                                elif field == "type":
                                    info["type"] = get_transaction_type("Enter updated transaction type (Type 'CR' for Income or 'DR' for Expenses) : ")
                                elif field == "date":
                                    info["date"] = get_transaction_date()
                                else:
                                    print("\nInvalid field. Please try again.\n")
                                    continue
                                
                                #Giving user the option to make more changes to the transaction
                                #.upper() is used for the user input for comparison purposes with the if-statement.
                                choice = get_choice("\nDo you wish to make more updates to this transaction? (Y/N) : ")
                                if choice == "Y":
                                    continue
                                else:
                                    print("\nAll changes to the transaction have been made.\n")
                                    break
                        
                            #Calling a function to add all information from the main transactions dictionary to the JSON file
                            add_to_json(transactions, filename)
                            return

                        #Displaying a message to the user if the final iteration of the list of transactions related to each key of the main transactions dictionary has been reached                 
                        elif info == exp_transactions[-1]:
                            print("\nThis transaction could not be found.\n")

                            #Giving user the option to try again if the transaction details entered does not match any transactions stored in the main transactions dictionary
                            choice = get_choice("Do you wish to try again? (Y/N) : ")
                            if choice == "Y":
                                print("\n")
                                update_transaction(transactions,filename)
                            else:
                                break

                #Giving user the option to try again if the entered "purpose" does not match any key of the main transactions dictionary
                elif purpose not in list(transactions.keys()):
                    print("\nThis transaction could not be found.\n")
                    
                    choice2 = get_choice("Do you wish to try again? (Y/N) : ")
                    if choice2 == "Y":
                        print("\n")
                        update_transaction(transactions, filename)
                    else:
                        break

        #Returning to the main program if a Runtime error is experienced due after changes made to the main transactions dictionary            
        except RuntimeError:
            return
                        
    else:
        #Displaying message if no transactions have been recorded
        print("No transactions to be updated are available.\n")
        return


#Creating a function to delete a transaction from the Finance Tracker
def delete_transaction(transactions, filename):

    #Allowing user to input transaction information to be deleted if there are previous transaction records
    if transactions != {}:
        
        #Calling a function to create a new list for comparison purposes
        del_transaction_info = create_new_transaction("Enter the amount of money from the transaction to be deleted : ", "Enter the purpose of the transaction which should to be deleted : ", "Enter the type of transaction which should be deleted (Type 'CR' for Income or 'DR' for Expenses): ")
        purpose = del_transaction_info[0]
        sub_dict = del_transaction_info[1]
        
        #Comparing the the list information consisting of user inputs with existing transaction information to verify if the transaction exists
        try:
            for expense, exp_transactions in transactions.items():
                #Checking if the value of "purpose" is among the keys of the main transactions dictionary
                if purpose == expense:
                    #Iterating through the values (which exist as lists consisting of dictionaries for each transaction) of the main transactions dictionary
                    for info in exp_transactions:
                        
                        if sub_dict == info:
                            #Removing transaction to be deleted from main transactions dictionary and displaying "successfully removed" message to the user
                            del transactions[expense][exp_transactions.index(info)]
                            print("\nThe transaction has been successfully removed.\n")

                            #Calling a function to add all information from the main transactions dictionary to the JSON file
                            add_to_json(transactions, filename)
                            return

                        #Displaying a message to the user if the final iteration of the list of transactions related to each key of the main transactions dictionary has been reached
                        elif info == exp_transactions[-1]:
                            print("\nThis transaction could not be found.\n")

                            #Giving user the option to try again if the transaction details entered does not match any transactions stored in the main transactions dictionary
                            choice = get_choice("Do you wish to try again? (Y/N) : ")
                            if choice == "Y":
                                print("\n")
                                delete_transaction(transactions, filename)
                            else:
                                break
                
                #Giving user the option to try again if the entered "purpose" does not match any key of the main transactions dictionary
                elif purpose not in list(transactions.keys()):
                    print("\nThis transaction could not be found.\n")
                    
                    choice2 = get_choice("Do you wish to try again? (Y/N) : ")
                    if choice2 == "Y":
                        print("\n")
                        delete_transaction(transactions, filename)
                    else:
                        break

        #Returning to the main program if a Runtime error is experienced due after changes made to the main transactions dictionary            
        except RuntimeError:
            return

    else:
        #Displaying message if no transactions have been recorded
        print("No transactions to be deleted are available.\n")
        return
    

#Creating a function to display a summary of all transactions recorded by the Finance Tracker
def transactions_summary(transactions):
    total_expenses = 0
    total_income = 0
    total_usable = 0

    #Displaying information about all transactions recorded by iterating through the key-value pairs of the main transactions dictionary
    for expense, exp_transactions in transactions.items():

        #Setting a counter to number each transaction related to a specific key
        count = 1

        #Iterating through the values (which exist as lists consisting of dictionaries for each transaction) of the main transactions dictionary and displaying the information
        print(f"{expense} :\n")
        for info in exp_transactions:
            print(f"{count}. Transaction amount : {info["amount"]}\n   Transaction type : {info["type"]}\n   Transaction date : {info["date"]}\n\n")
            count += 1

            #Calculating the total income and expenses incurred by the user
            if info["type"] == "Expense":
                total_expenses += float(info["amount"])
            else:
                total_income += float(info["amount"])

        #Calculating the usable amount of money based on the transactions recorded in the Finance Tracker
        total_usable = total_income - total_expenses
        if total_usable < 0:
            total_usable = 0
            
    #Displaying the total expenses, income and usable balance to the users
    print(f"Total Expenses are : {"{:.2f}".format(total_expenses)} \nTotal Income is : {"{:.2f}".format(total_income)} \nUsable Balance : {"{:.2f}".format(total_usable)}")
    return                       



#Creating a class definition for the GUI the Finance Tracker to Search and Sort Transactions
class FinanceTrackerGUI:
    
    #Creating a function to act as the constructor of an object
    def __init__(self, root, filename):
        self.root = root
        
        #Changing the title of the root window
        self.root.title("Personal Finance Tracker")
        
        #Calling a function to create widgets for the GUI
        self.create_widgets()
        
        #Calling a function to load the transactions from the JSON file
        self.transactions = self.load_transactions(filename)
        
        #Calling a function to display the transactions to be added to the treeview
        self.display_transactions(self.transactions)
        
        #Using the style module of the ttk module to modify the theme of the window and change the font style and background colour of the column headings
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview.Heading", font = ("Calibri", 12), background = "lightgrey")
        
        #Initializing variables for the sort function of the GUI
        self.sort_column = None
        self.sort_descending = False

    
    #Creating a function to create widgets for the GUI 
    def create_widgets(self):
        
        #Creating a frame for the table and scrollbar and setting it to expand horizontally and vertically (when the frame size is adjusted)
        frame = ttk.Frame(self.root)
        frame.pack(fill = "both", expand = True)
        
        #Treeview for displaying transactions
        #Creating a tuple with columns
        column_names =("Transaction", "Amount", "Type", "Date")
        
        #Creating a Treeview in the frame with the names of each column
        self.tree = ttk.Treeview(frame, columns = column_names, show = "headings")
        
        #Setting the headings for each column
        #When each column heading is clicked, the column name is set as the parameter for a function that is called to sort the elements of the columns
        self.tree.heading("Transaction", text = "Transaction", command = lambda: self.sort_by_column("Transaction"))
        self.tree.heading("Amount", text = "Amount", command = lambda: self.sort_by_column("Amount"))
        self.tree.heading("Type", text = "Type", command = lambda: self.sort_by_column("Type"))
        self.tree.heading("Date", text = "Date", command = lambda: self.sort_by_column("Date"))
        
        #Setting the treeview to the left side of the frame and enabling it to expand horizontally and vertically (when the frame size is adjusted)
        self.tree.pack(side = "left", fill = "both", expand = True)
        
        #Center aligning items in each column, including the column headings
        for col in ("Transaction", "Amount", "Type", "Date"):
            self.tree.heading(col, anchor = "center")
            self.tree.column(col, anchor = "center")
        
        #Scrollbar for the Treeview
        #Creating a vertical scrollbar in the y-axis (vertically) of the Treeview
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command = self.tree.yview)
        self.tree.configure(yscrollcommand = scrollbar.set)
        
        #Adding the scrollbar on the right side of the Treeview
        scrollbar.pack(side = "right", fill = "y")
        
        #Creating string variable for the search choice and setting the default value to "Transaction"
        self.search_choice = tk.StringVar()
        self.search_choice.set("Transaction")
        
        #Creating a seperate frame for search functions
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady = 5)
        
        #Creating radio buttons in the search frame for each type of value in the treeview (Transaction, Amount, Type, Date)
        #'side = "left"' is used to indicate that each radio button is aligned in the frame towards the left side of eachother consecutively.
        ttk.Radiobutton(search_frame, text = "Transaction", variable = self.search_choice, value = "Transaction").pack(side = "left")
        ttk.Radiobutton(search_frame, text = "Amount", variable = self.search_choice, value = "Amount").pack(side = "left")
        ttk.Radiobutton(search_frame, text = "Type", variable = self.search_choice, value = "Type").pack(side = "left")
        ttk.Radiobutton(search_frame, text = "Date", variable = self.search_choice, value = "Date").pack(side = "left")
        
        #Creating the searchbar for the user to enter the value they wish to filter out
        #Initializing a string variable for the value entered in the searchbar
        self.search_str = tk.StringVar()

        #Creating an entry widget/textbox for the user input
        #textvariable is set to search_str to ensure the user input can be set as an accessible variable
        searchbar = ttk.Entry(self.root, textvariable = self.search_str)
        searchbar.pack(pady = 5)
        
        #Creating a search button which, when clicked, calls a search transaction function
        search_button = ttk.Button(self.root, text = "Search", command = self.search_transactions)
        search_button.pack()

        #Creating an empty label which can be used in cases on an invalid input being entered
        self.invalid_input_label = tk.Label(self.root, text = "", fg = "red")
        self.invalid_input_label.pack()

        #Creating a reset button that calls a function to reset the elements in the treeview
        reset_button = ttk.Button(self.root, text = "Reset", command = self.reset_transactions)
        reset_button.pack(pady = 5)

    
    #Creating a function to load transactions from the JSON file to the self.transactions variable
    def load_transactions(self, filename):
        try:
            with open(filename, "r") as file:
                loaded_data = json.load(file)
            return loaded_data
        except json.JSONDecodeError as error_msg:
            print(f"Error decoding JSON: {error_msg}")
        except FileNotFoundError:
            return {}

    
    #Creating a function to display all transactions to the user in the Treeview of the GUI
    def display_transactions(self, transactions):
        #Removing any existing items in the treeview
        for info in self.tree.get_children():
            self.tree.delete(info)

        #Add all transactions to the Treeview
        #Iterating through the key-value pairs of the transactions dictionary
        for  expense, exp_transactions in transactions.items():
            #Iterating through the values (which exist as lists consisting of dictionaries for each transaction) of the transactions dictionary
            for info in exp_transactions:
                #Inserting the relevant values to a row of the under each respective column Treeview
                self.tree.insert("", "end", values = (expense, info["amount"], info["type"], info["date"]))

    
    #Creating a function to search for transactions that match the user inputted value and chosen value category
    def search_transactions(self):
        #Getting user inputted value from the search_str variable and the search choice
        user_input = self.search_str.get().capitalize()
        search_choice = self.search_choice.get()

        #Creating an empty dictionary to store all filtered transaction information
        filtered_transactions = {}

        #Iterating through the key-value pairs of the transactions dictionary
        for expense, exp_transactions in self.transactions.items():

            #Creating an empty list to store information related to a transaction
            filtered_items = []

            #Iterating through the values (which exist as lists consisting of dictionaries for each transaction) of the transactions dictionary
            #The values get added to the filtered_items list if they match the user input and search criteria
            for info in exp_transactions:
                if search_choice == "Transaction" and user_input in expense:
                    filtered_items.append(info)
                elif search_choice == "Amount" and user_input == info["amount"]:
                    filtered_items.append(info)
                elif search_choice == "Type" and user_input in info["type"].capitalize():
                    filtered_items.append(info)
                elif search_choice == "Date" and user_input in info["date"]:
                    filtered_items.append(info)

            #Adding the filtered items related to a specific type of transaction (key) as a value for the relevant transaction in the filtered_transactions dictionary
            if filtered_items:
                filtered_transactions[expense] = filtered_items

        #Adding the filtered transactions to the treeview by calling the display transactions function
        if filtered_transactions:
            self.display_transactions(filtered_transactions)
            #The label is emptied here to ensure that if a previous search had no results and the new search does, the unnecessary text in the label will be erased
            self.invalid_input_label.config(text = "")
        else:
            #Displaying a message in the label to the user if no results that match the input and search criteria have been found
            self.invalid_input_label.config(text = "No results were found to match the chosen search criteria.")

    
    #Creating a function to reset the values displayed in the Treeview
    def reset_transactions(self):
        #Calling the display transactions function and setting the invalid input label to "" (To empty the label)
        self.display_transactions(self.transactions)
        self.invalid_input_label.config(text = "")


    #Creating a function to sort the values in ascending or descending order by column
    def sort_by_column(self, column_name):
        #When the coumn is clicked, the current sort_descending value changes to its opposite value (True or False)
        if self.sort_column == column_name:
            self.sort_descending = not self.sort_descending
        else:
            self.sort_column = column_name
            self.sort_descending = False

        #Creating an empty list to store the values related to in each row of a column in tuples
        data = []

        #Iterating throught the values of each row of the Treeview
        for item in self.tree.get_children(""):
            #Getting the value of the specified column and assigning it to the value for each item
            value = self.tree.set(item, column_name)

            #Converting the value to a floating point value if it is of the type "Amount" to ensure it isn't sorted as a string value
            if column_name == "Amount":
                value = float(value)

            #Appending a tuple with the value and item to the data list
            data.append((value, item))

        #Sorting the values in the data list.
        #The reverse parameter is determined by the the sort_descending value (True/False) in the beginning of the function
        data.sort(reverse = self.sort_descending)

        #Initializing variable to specify the new position of a row (item) in the Treeview
        num = 0

        #Iterating throught the tuples in the the data list
        for val, item in data:
            #Moving the item in the Treeview to the new position based on the sorting order and num value
            self.tree.move(item, "", num)
            num += 1

#Creating a function to open a GUI that allow user to navigate through the transactions in the Finance Tracker and search for specific transactions
def search_and_sort_transactions(filename):
    root = tk.Tk()
    app = FinanceTrackerGUI(root, filename)
    root.mainloop()


#Creating a function to display the main menu to the user
def main_menu():
    #Creating an infinite loop with functions the Finance Tracker can perform
    while True:
        filename = "transactions.json"
        transactions = read_bulk_transactions_from_file(filename)
        if transactions != None:
            print("\n-----------------------------------------------------------------------------")
            print("\n Welcome to Your Personal Finance Tracker!!\n")
            print("1. Add a Transaction")
            print("2. View All Transactions")
            print("3. Update a Transaction")
            print("4. Delete a Transaction")
            print("5. Display Transactions Summary")
            print("6. Search for Transactions")
            print("7. Exit Finance Tracker")

            #Gettng user input for the function user wants to perform
            choice = input("\nEnter your choice : ")
            print("\n")

            #Verifying if user input is valid and performing the respective function if the input is valid
            if choice == "1":
                add_transaction(transactions, filename)
            elif choice == "2":
                view_transactions(transactions)
            elif choice == "3":
                update_transaction(transactions, filename)
            elif choice == "4":
                delete_transaction(transactions, filename)
            elif choice == "5":
                transactions_summary(transactions)
            elif choice == "6":
                search_and_sort_transactions(filename)
            elif choice == "7":
                print("\nExiting Finance Tracker.\n")
                break
            else:
                print("\nInvalid choice. Please try again.\n")

        else:
            break
        
    return



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------  Main Code

#Displaying main menu to user as the program executes
if __name__ == "__main__":
    main_menu()




    







    
