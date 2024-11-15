import tkinter as tk
from tkinter import ttk, messagebox
import json

#Creating a class definition for the GUI the Finance Tracker to Search and Sort Transactions
class FinanceTrackerGUI:
    
    #Creating a function to act as the constructor of an object
    def __init__(self, root, filename):
        self.root = root
        
        #Changing the title of the root window
        self.root.title("Personal Finance Tracker")
        
        #Calling a function to create widgets for the GUI
        self.create_widgets()
        
        #Calling a function to load the transactions from the JSON File
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
            #Displaying a message box consisting of an error message for the user 
            messagebox.showerror("Error", "Transaction records cannot be found.\nPlease ensure all neccessary files are loacted in the same root folder")
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

search_and_sort_transactions("transactions.json")



