# Personal-Finance-Tracker
An application developed to track and filter financial records using Python and Tkinter as a GUI framework.

Functionalities include:
1. Adding, removing and updating transaction information by providing all relvant transaction details.
2. Retrieving previously entered information into the system from the main transactions JSON source file, as well as updating the file automatically with new records before program termination.
3. Displaying the financial history and all the relevant information about each transaction (as stored in the JSON file).
4. Providing a clear numbered list for each transaction type in the transaction history, as well as the Total Income, Total Expenses and Usable Balance based on the transactions 
recorded.
5. Displaying a GUI, built using Tkinter framework and Object-Oriented Programming principles, to filter finiacial records. The GUI consists of a Treeview with columns including data from the finance tracker, a searchbar and buttons to choose a search criteria. Several functions may be performed using this, including sorting the data in ascending/descending order based on the column heading clicked and choosing a search criteria and typing a value to filter out in among the records of the Finance Tracker.


The provided Python and JSON files allow a user to create and manage their own personal finance tracker. The set-up information is as follows:
1. Ensure Python is installed, download all files provided and save them in a root folder.
2. All files (Python file(s) and JSON file(s)) should be available in the same folder or location to ensure the Python program will be able to access data stored in the JSON file. If not a message shall be displayed to the user stating that the transactions could not be found.
3. The ‘sample_transactions.json’ file exists for demonstration purposes and was used to test the program’s functionality. If you wish to access/manipulate data in this file, the file should be renamed to ‘transactions.json’ or the value of the ‘filename’ variable in the “main_menu” function of the code (line number 630) should be changed to ‘sample_transactions.json’ first.
4. The ‘transactions.json’ file provided contains an empty dictionary with no records. Initially, if any functions besides “Add a Transaction” or “Exit Finance Tracker” are performed, a message explaining that there are no financial records will be displayed to the user. Additionally the GUI will consist of empty rows due to the lack of records.
5. The “Personal Finance Tracker GUI.py” file consists solely of the Graphical User Interface used for searching and sorting transaction records. Additionally, the code in this file has been integrated into the “Personal Finance Tracker.py” file.
