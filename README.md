# C.R.U.D 1.0
Project Documentation: C.R.U.D 1.0

Aim:

The aim of the C.R.U.D 1.0 project is to provide a simple yet functional application for performing basic C.R.U.D (Create, Read, Update, Delete) operations on a customer database. The application allows users to interact with a SQL Server database, perform data entry, update existing records, delete records, and execute custom SQL queries.

Key Features:

User-Friendly Interface:

The graphical user interface (GUI) is designed to be intuitive and user-friendly.
Implemented using the Tkinter library in Python.
C.R.U.D Operations:

Create: Users can add new customer records to the database.
Read: The application displays the latest customer records in a table format.
Update: Users can modify existing customer records.
Delete: Users can remove customer records from the database.
SQL Query Execution:

Users have the ability to execute custom SQL queries.
The results of the queries are displayed in a table, enhancing user interaction with the database.
Preview Functionality:

Users can preview the first 50 records in the database to get a quick overview.
Error Handling:

The application includes comprehensive error handling to guide users and prevent unintended actions.
Steps Taken:

Database Connection:

Utilized the PyODBC library to establish a connection to a SQL Server database.
GUI Development:

Developed a tab-based GUI using Tkinter and ttk for the different C.R.U.D operations.
Included entry widgets for data input and buttons for actions such as create, update, delete, and execute SQL queries.
C.R.U.D Functions:

Implemented functions for creating, updating, and deleting customer records.
Incorporated functions to read and display the latest customer records in the application.
SQL Query Execution:

Enabled users to input custom SQL queries.
Executed the queries and displayed the results in a text box and updated the table with the new data.
Preview Functionality:

Included a button to preview the first 50 records in the database.
Error Handling:

Implemented error handling to ensure data integrity and provide meaningful feedback to users.
Limitations:

Limited Scalability:

The application is designed for basic C.R.U.D operations and may not be suitable for large-scale databases or complex operations.
Security Considerations:

Security measures such as user authentication and authorization are not implemented, making the application vulnerable to unauthorized access.
UI Customization:

While the GUI is functional, further customization options may be limited for users seeking a highly personalized interface.
How to Make Further Modifications:

GUI Layout:

To modify the layout, position, or appearance of GUI elements, update the corresponding Tkinter widgets and their properties.
Functionality Changes:

Adjust C.R.U.D functions or SQL query execution functions based on specific requirements.
Database Connection:

Modify the database connection details in the code to connect to a different SQL Server database.
Enhance Security:

Implement user authentication and authorization mechanisms for improved security.
UI Styling:

Utilize Tkinter styling options or consider using a different GUI framework for more advanced UI customization.
Contributing:

Contributions to the project are welcome. Fork the repository, make your modifications, and submit a pull request.
