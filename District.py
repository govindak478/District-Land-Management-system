import mysql.connector 
import datetime
import sys
import re
import pandas as pd
# Database Connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pswd"
)

# Create database if it doesn't exist
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS talathi_management")
print("Database created successfully.")

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pswd",
    database="talathi_management"
)

# Create land records table if it doesn't exist
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS land_records (landowner_id INT AUTO_INCREMENT PRIMARY KEY, landowner_name VARCHAR(255), landowner_contact int(10) unique, survey_number VARCHAR(255) unique not null, area VARCHAR(255), land_type varchar(100) CHECK (land_type IN ('Agricultural', 'Non-Agricultural')) , purchase_date DATE)")
print("Land records table created successfully.")

# Create documents table if it doesn't exist
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS documents (document_id INT AUTO_INCREMENT PRIMARY KEY, landowner_id INT, document_type VARCHAR(255), issuance_date DATE, validity_period INT, status VARCHAR(255), FOREIGN KEY (landowner_id) REFERENCES land_records(landowner_id) ON DELETE CASCADE)")
print("Documents table created successfully.")


# Function to manage land records
def manage_land_records():
    print("1. Add Land Record")
    print("2. View Land Records")
    print("3. Update Land Record")
    print("4. Delete Land Record")
    print("5. Person's Land Record")
    choice = input("Enter your choice: ")

    if choice == "1":
        # Add Land Record
        landowner_name = input("Enter landowner name: ")
        landowner_contact = input("Enter landowner contact details: ")
        try:

            if len(landowner_contact)<10 or len(landowner_contact)>10:
                raise ValueError("invalid mobile number")
        except Exception as e:
                print("Enter valid mobile number eg.1234567890",e)
                sys.exit()

        survey_number = input("Enter survey number eg.123/2A/12: ")
        
        # Validate the survey number format using regular expressions
        if not re.match(r'^\d+\/\w+\/\d+$', survey_number):
            print("Invalid survey number format. Please enter in the format '123/1A/2'.")
            sys.exit()
        area = input("Enter area of land: ")
        land_type = input("Enter type of land eg.Agricultural,Non-Agricultural: ")
        try:
            purchase_date = input("Enter date of purchase eg.(yyyy-mm-day): ")
            purchase_date = datetime.datetime.strptime(purchase_date, '%Y-%m-%d').date()
            
            
        except ValueError as e:
            print("Invalid date string: ", str(e))
        
        cursor = mydb.cursor()
        sql = "INSERT INTO land_records (landowner_name, landowner_contact, survey_number, area, land_type, purchase_date) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (landowner_name, landowner_contact, survey_number, area, land_type, purchase_date)
        cursor.execute(sql, values)

        mydb.commit()
        print("Land Record added successfully.")

    elif choice == "2":
        # View Land Records
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM land_records")
        records = cursor.fetchall()
        for record in records:
            print(record)
        """ columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(records, columns=columns)
        print(df) """

    elif choice == "3":
        # Update Land Record
        landowner_id = int(input("Enter landowner ID: "))
        cursor = mydb.cursor()
        cursor.execute("SELECT landowner_id FROM land_records")
        records = cursor.fetchall()
        
        for i in range(len(records)):
            if records[i][0]==landowner_id:
                landowner_name = input("Enter landowner name: ")
                landowner_contact = input("Enter landowner contact details: ")
                survey_number = input("Enter survey number eg.123/2A/12: ")
                if not re.match(r'^\d+\/\w+\/\d+$', survey_number):
                    print("Invalid survey number format. Please enter in the format '123/1A/2'.")
                    sys.exit()
                
                area = input("Enter area of land: ")
                land_type = input("Enter type of land eg.Agricultural,Non-Agricultural: ")
                
                try:
                    purchase_date = input("Enter date of purchase eg.(yy-mm-day): ")
                    purchase_date = datetime.datetime.strptime(purchase_date, '%Y-%m-%d').date()
                    
                    
                except ValueError as e:
                    print("Invalid date string: ", str(e))

                cursor = mydb.cursor()
                sql = "UPDATE land_records SET landowner_name = %s, landowner_contact = %s, survey_number = %s, area = %s, land_type = %s, purchase_date = %s WHERE landowner_id = %s"
                values = (landowner_name, landowner_contact, survey_number, area, land_type, purchase_date, landowner_id)
                cursor.execute(sql, values)
                mydb.commit()
                print("Land Record updated successfully.")
        else:
                print("Sorry owner does not have any record")


    elif choice == "4":
        # Delete Land Record
        landowner_id = input("Enter landowner ID: ")

        cursor = mydb.cursor()
        sql = "DELETE FROM land_records WHERE landowner_id = %s"
        value = (landowner_id,)
        try:
            affected_rows = cursor.execute(sql, value)
            
            if affected_rows == None:
                raise ValueError("landowner_id does not exist")
        except Exception as e:
            print("Invalid landowner_id:", str(e))
            sys.exit()

        mydb.commit()
        print("Land Record deleted successfully.")

    elif choice=="5":
        #perticular person record
        landowner_id = input("Enter landowner ID: ")
        cursor = mydb.cursor()
        sql = "select * FROM land_records WHERE landowner_id = %s"
        value = (landowner_id,)
        cursor.execute(sql, value)
        records = cursor.fetchall()
        try:
            cursor.execute(sql, value)
            records = cursor.fetchall()
            if len(records)==0:
                raise Exception
            for record in records:
                print(record)
        
        except Exception as e:
            print("Invalid landowner_id")
        
#Function to manage documents
def manage_documents():
    print("1. Add Document")
    print("2. View Documents")
    print("3. Update Document")
    print("4. Delete Document")
    choice = input("Enter your choice: ")


    if choice == "1":
        # Add Document
        landowner_id = input("Enter landowner ID: ")
        document_type = input("Enter document type: ")
        
        try:
            issuance_date = input("Enter issuance date: eg.(yy-mm-day): ")
            issuance_date = datetime.datetime.strptime(issuance_date, '%Y-%m-%d').date()
            
            
        except ValueError as e:
            print("Invalid date string: ", str(e))
            sys.exit()
        validity_period = input("Enter validity period (in years): ")
        status = input("Enter status of document eg.approved,pending: ")

        cursor = mydb.cursor()
        sql = "INSERT INTO documents (landowner_id, document_type, issuance_date, validity_period, status) VALUES (%s, %s, %s, %s, %s)"
        values = (landowner_id, document_type, issuance_date, validity_period, status)
        try:
            cursor.execute(sql, values)
            mydb.commit()
            print("Document added successfully.")
        except Exception as e:
            print("Invalid Entries")
        

    elif choice == "2":
        # View Documents
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM documents")
        records = cursor.fetchall()
        for record in records:
            print(record)
        


    elif choice == "3":
        # Update Document
        document_id = input("Enter document ID: ")
        landowner_id = input("Enter landowner ID: ")
        document_type = input("Enter document type: ")
        issuance_date = input("Enter issuance date: ")
        validity_period = input("Enter validity period (in years): ")
        status = input("Enter status of document: ")

        cursor = mydb.cursor()
        sql = "UPDATE documents SET landowner_id = %s, document_type = %s, issuance_date = %s, validity_period = %s, status = %s WHERE document_id = %s"
        values = (landowner_id, document_type, issuance_date, validity_period, status, document_id)
        cursor.execute(sql, values)
        mydb.commit()
        print("Document updated successfully.")

    elif choice == "4":
        # Delete Document
        document_id = input("Enter document ID: ")
        cursor = mydb.cursor()
        sql = "DELETE FROM documents WHERE document_id = %s"
        value = (document_id,)
        cursor.execute(sql, value)
        mydb.commit()
        print("Document deleted successfully.")

    else:
        print("Invalid choice.")
#Main function
""" def main():
    print("1. Manage Land Records")
    print("2. Manage Documents")
    choice = input("Enter your choice: ")


    if choice == "1":
        manage_land_records()
    elif choice == "2":
        manage_documents()
    else:
        print("Invalid choice.") """

print("#############( WELCOME TO LAND AND DOCUMENT MANAGEMENT SYSTEM )#############")
while True:
    print("1. Manage Land Records")
    print("2. Manage Documents")
    choice = input("Enter your choice: ")

    if choice == "1":
        manage_land_records()
    elif choice == "2":
        manage_documents()
    else:
        print("Invalid choice.")



    
