# -- coding: utf-8 --
"""
Created on Thu Nov 13 01:20:47 2025

@author: Shankh
"""

import pymysql
import tabulate
import os

db = pymysql.connect(host='localhost', user='root',
                     password='bnps1', database='AIRPORT')
cur = db.cursor()
if db.open:
    print("Connection Successful !")
else:
    print("Connection Failed !")

def insert(time, destination, flight_no, gate, remarks):      
    sql = """
                INSERT INTO FLIGHTS (TIME, DESTINATION, FLIGHTNo, GATENO, REMARKS)
                VALUES (%s, %s, %s, %s, %s)
            """
    values = (time, destination, flight_no, gate, remarks)
    cur.execute(sql, values)
    fare = float(input("Enter Fare: "))
    date_of_flight = input("Enter Date of Flight (YYYY-MM-DD): ")
    available_seats = int(input("Enter Available Seats: "))
    s = "INSERT INTO SEATS (FARE, DATE_OF_FLIGHT, AVAILABLE_SEATS, FLIGHTNo) VALUES (%s, %s, %s, %s)"
    cur.execute(s, (fare, date_of_flight, available_seats, flight_no))

    db.commit()
    print("Seat record inserted successfully !") 
    db.commit()

def disp():
    sq = "Select * from FLIGHTS"
    cur.execute(sq)
    rec = cur.fetchall()
    print(tabulate.tabulate(rec, headers=[
          "TIME", "DESTINATION", "FLIGHTNo", "GATE", "REMARKS"], tablefmt="fancy_grid"))

def update():
    fno = input("Enter Flight Number: ").strip().upper()

    cur.execute("SELECT * FROM FLIGHTS WHERE FLIGHTNo=%s", (fno,))
    rec = cur.fetchone()

    if rec is None:
        print("Flight number not found.")
        return

    print("\n--- Enter New Details (leave blank to keep existing) ---")
    new_time = input("Enter New Flight Time (HH:MM): ")
    new_dest = input("Enter New Destination: ")
    new_remark = input("Enter New Remark: ")
    new_gate = input("Enter New Gate Number: ")

    cur.execute("UPDATE FLIGHTS SET TIME = IF(%s='', TIME, %s), DESTINATION = IF(%s='', DESTINATION, %s), REMARKS = IF(%s='', REMARKS, %s), GATENO = IF(%s='', GATENO, %s) WHERE FLIGHTNo=%s",
                (new_time, new_time, new_dest, new_dest, new_remark, new_remark, new_gate, new_gate, fno))
    db.commit()

    cur.execute("SELECT * FROM SEATS WHERE FLIGHTNo=%s", (fno,))
    seat_rec = cur.fetchone()

    if seat_rec:
        new_date = input("Enter New Date of Flight (YYYY-MM-DD): ")
        new_total = input("Enter New Total Seats: ")
        cur.execute("UPDATE SEATS SET DATE_OF_FLIGHT = IF(%s='', DATE_OF_FLIGHT, %s), AVAILABLE_SEATS = IF(%s='', AVAILABLE_SEATS, %s) WHERE FLIGHTNo=%s",
                    (new_date, new_date, new_total, new_total, fno))
        db.commit()

    print("Record Updated Successfully.")

def deletefxn():    
    f = input("Enter Flight No To Be Deleted: ").strip().upper()   
    cur.execute("SELECT * FROM FLIGHTS WHERE FLIGHTNo = %s", (f,))
    rec=cur.fetchone()
    if rec is None:    
        print("No flight found with that number.")
        return
    else:
        cur.execute("DELETE FROM SEATS WHERE FLIGHTNo = %s", (f,))
        cur.execute("DELETE FROM FLIGHTS WHERE FLIGHTNo = %s", (f,))
        db.commit()
        print("Flight and related seats deleted successfully!")
    

def display():
    q = "Select * from SEATS"
    cur.execute(q)
    rec = cur.fetchall()
    print(tabulate.tabulate(rec, headers=[
          "FARE", "DATE OF FLIGHT", "AVAILABLE SEATS", "FLIGHTNo"], tablefmt="fancy_grid"))
    
def change():
    f = input("Enter Flight Number: ").strip().upper()
    q = """SELECT FLIGHTS.TIME,FLIGHTS.DESTINATION,FLIGHTS.FLIGHTNo,FLIGHTS.GATENO,
                 FLIGHTS.REMARKS,SEATS.FARE,SEATS.DATE_OF_FLIGHT,SEATS.AVAILABLE_SEATS
          FROM FLIGHTS 
          INNER JOIN SEATS ON FLIGHTS.FLIGHTNo=SEATS.FLIGHTNo 
          WHERE FLIGHTS.FLIGHTNo=%s"""
    cur.execute(q, f)
    result = cur.fetchone()
    if result:
        print("\n--- FLIGHT DETAILS ---")
        print(f"Time: {result[0]}")
        print(f"Destination: {result[1]}")
        print(f"Flight No: {result[2]}")
        print(f"Terminal: {result[3]}")
        print(f"Remarks: {result[4]}")
        print("\n--- SEAT DETAILS ---")
        print(f"Fare: ₹{result[5]}")
        print(f"Date: {result[6]}")
        print(f"Available Seats: {result[7]}")
    else:
        print("No Details Found With That Flight Number!")

def verify_passports():
    cur.execute("SELECT * FROM PASSENGER WHERE LOWER(PASSPORT_STATUS)='pending'")
    f = cur.fetchall()

    if not f:
        print("\nNo pending passport verifications at the moment!")
        return

    print("\n===== PENDING PASSPORT VERIFICATIONS =====")
    print(tabulate.tabulate(
        f,
        headers=["Passenger Name", "Phone Number", "Destination", "Passport Status", "FlightNo"],
        tablefmt="fancy_grid"
    ))

    try:
        pno = input("\nEnter the Phone Number of the passenger to verify (or 0 to exit): ")
        if pno == '0':
            print("Returning to Admin Menu...")
            return

        status = input("Enter passport status (Valid/Invalid): ").capitalize()

        if status not in ["Valid", "Invalid"]:
            print("Invalid status! Please enter either 'Valid' or 'Invalid'.")
            return

        cur.execute("UPDATE PASSENGER SET PASSPORT_STATUS=%s WHERE PHONE_NUMBER=%s", (status, pno))
        db.commit()
        print(f"Passport status for passenger PHONE_NUMBER {pno} updated to '{status}' successfully!")

    except ValueError:
        print("Invalid input! Please enter a valid number for Phone Number.")


def admin():
    while True:
        print("Welcome To Flight Program!")
        print("1. Display Flights Schedule")
        print("2. Insert Flight & Seat Record")
        print("3. Update Current Flight Record")
        print("4. Delete A Flight Record")
        print("5. Display Seat Record")
        print("6. Display Flight And Seat Details With Flight No")
        print("7. Display Passengers Record")
        print("8. Verification of Passport")
        print("9. Exit the program")
        
        ch = int(input("Enter Your Choice: "))
        if ch == 1:
            disp()
        elif ch == 2:
            t = input("Enter Flight Time (HH:MM): ")
            dest = input("Enter Destination: ")
            fno = input("Enter Flight Number: ").strip().upper()
            gate = input("Enter Gate Number: ")
            remark = input("Enter Remarks: ")
            insert(t, dest, fno, gate, remark)
        elif ch == 3:
            update()
        elif ch == 4:
            deletefxn()
        elif ch == 5:
            display()
        elif ch == 6:
            change()
        elif ch == 7:
            q = "SELECT * FROM PASSENGER"
            cur.execute(q)
            rec = cur.fetchall()
            print(tabulate.tabulate(
                rec,
                headers=["SNo", "Passenger Name", "Phone Number", "Destination", "Passport Status", "FLIGHTNo"],
                tablefmt="fancy_grid"
            ))
        elif ch == 8:
            verify_passports()
        elif ch == 9:
            print("Program Exited")
            break
        else:
            print("Invalid choice, please try again.")

def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    if username == "admin" and password == "IGI":
        print("\n Login successful! Redirecting to Admin Menu...\n")
        admin()
    else:
        print("\n Invalid credentials. Access denied.\n")            

from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import webbrowser
import urllib.parse

def generate_boarding_pass(passenger_name, flight_no, destination, time, fare):
    file_name = f"Boarding_Pass_{passenger_name.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_name, pagesize=A5)

    # Blue background
    c.setFillColorRGB(0.15, 0.35, 0.65)
    c.rect(0, 0, 420, 297, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(110, 250, "✈ IGI AIRLINES - BOARDING PASS ✈")

    # Passenger Info
    c.setFont("Helvetica", 12)
    c.drawString(50, 220, f"Passenger Name : {passenger_name}")
    c.drawString(50, 200, f"Flight Number  : {flight_no}")
    c.drawString(50, 180, f"Destination    : {destination}")
    c.drawString(50, 160, f"Departure Time : {time}")
    c.drawString(50, 140, f"Fare           : ₹{fare}")
    c.drawString(50, 120, f"Issue Date     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(120, 90, "Have a Safe Flight with IGI Airlines!")
    c.drawString(100, 75, "Please arrive at the airport 2 hours before departure.")

    c.save()

    abs_path = os.path.abspath(file_name)
    file_url = f"file:///{urllib.parse.quote(abs_path.replace(os.sep, '/'))}"

    print(f"\n✅ Boarding Pass generated successfully!")
    print(f"📄 Click below to open:\n{file_url}")

    try:
        webbrowser.open_new(file_url)
    except Exception as e:
        print(f"⚠ Could not auto-open PDF: {e}")

from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import random

def generate_boarding_pass(passenger_name, flight_no, destination, time, fare):
    file_name = f"Boarding_Pass_{passenger_name.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_name, pagesize=A5)

    # Background (smooth blue)
    c.setFillColorRGB(0.15, 0.35, 0.65)
    c.rect(0, 0, 420, 297, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(110, 250, "✈ IGI AIRLINES - BOARDING PASS ✈")

    # Passenger Info
    c.setFont("Helvetica", 12)
    c.drawString(50, 220, f"Passenger Name : {passenger_name}")
    c.drawString(50, 200, f"Flight Number  : {flight_no}")
    c.drawString(50, 180, f"Destination    : {destination}")
    c.drawString(50, 160, f"Departure Time : {time}")
    c.drawString(50, 140, f"Fare           : ₹{fare}")
    c.drawString(50, 120, f"Issue Date     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(130, 90, "Have a Safe Flight with IGI Airlines!")
    c.drawString(110, 75, "Please arrive at the airport 2 hours before departure.")

    c.save()

    abs_path = os.path.abspath(file_name)
    print(f"\n✅ Boarding Pass generated successfully!")

    # Make it clickable
    file_url = f"file:///{abs_path.replace(os.sep, '/')}"
    print(f"📄 Click below to open:")
    print(f"{file_url}")

    # Automatically open the PDF
    webbrowser.open_new(file_url)


def generate_flight_receipt(passenger_name, phone, flight_no, destination, fare):
    file_name = f"Flight_Receipt_{passenger_name.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_name, pagesize=A5)

    # Blue background
    c.setFillColorRGB(0.18, 0.4, 0.7)
    c.rect(0, 0, 420, 297, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 260, "💳 IGI AIRLINES - FLIGHT RECEIPT 💳")

    c.setFont("Helvetica", 11)
    c.drawString(50, 230, f"Passenger Name : {passenger_name}")
    c.drawString(50, 210, f"Phone Number   : {phone}")
    c.drawString(50, 190, f"Flight Number  : {flight_no}")
    c.drawString(50, 170, f"Destination    : {destination}")
    c.drawString(50, 150, f"Fare           : ₹{fare}")
    c.drawString(50, 130, f"Booking Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 110, f"Payment Status : PAID")

    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 80, "Thank you for booking with IGI Airlines!")
    c.drawString(50, 65, "Have a pleasant journey :)")

    c.save()

    abs_path = os.path.abspath(file_name)
    print(f"\n✅ Flight Receipt generated successfully!")
    print(f"📄 Click to open: {abs_path}")

    # Open automatically after creation
    webbrowser.open(f"file:///{abs_path.replace(os.sep, '/')}")

def book_flight():
    print("\n===== ADD PASSENGER DETAILS =====")
    pname = input("Enter Passenger Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    dest = input("Enter Desired Destination: ").strip().title()

    query = """SELECT FLIGHTS.FLIGHTNo, FLIGHTS.DESTINATION, FLIGHTS.TIME, 
                      SEATS.AVAILABLE_SEATS, SEATS.FARE
               FROM FLIGHTS 
               INNER JOIN SEATS ON FLIGHTS.FLIGHTNo = SEATS.FLIGHTNo
               WHERE FLIGHTS.DESTINATION = %s AND SEATS.AVAILABLE_SEATS > 0
               LIMIT 1"""
    cur.execute(query, (dest,))
    result = cur.fetchone()

    if not result:
        print("\nOops! No flight available for this destination at the moment.")
        return

    flight_no, destination, time, seats, fare = result
    print("\n===== FLIGHT FOUND =====")
    print(f"Destination: {destination}")
    print(f"Flight Number: {flight_no}")
    print(f"Departure Time: {time}")
    print(f"Fare: ₹{fare}")
    print(f"Seats Available: {seats}")

    confirm = input("\nDo you want to confirm this booking? (y/n): ").lower()
    if confirm != 'y':
        print("Booking cancelled by user.")
        return

    sql = """INSERT INTO PASSENGER 
             (PASSENGER_NAME, PHONE_NUMBER, DESTINATION, PASSPORT_STATUS, FLIGHTNo)
             VALUES (%s, %s, %s, %s, %s)"""
    cur.execute(sql, (pname, phone, dest, "Pending", flight_no))

    cur.execute("UPDATE SEATS SET AVAILABLE_SEATS = AVAILABLE_SEATS - 1 WHERE FLIGHTNo = %s", (flight_no,))

    db.commit()
    print("\n🎉 Booking Successful!")
    print(f"Flight Assigned: {flight_no}")
    print("Passport Status: Pending (Admin will verify soon)")
    generate_boarding_pass(pname, flight_no, dest, time, fare)
    generate_flight_receipt(pname, phone, flight_no, destination, fare)
       
    
def cancel_booking():
    print("\n===== CANCEL BOOKING =====")
    phone = input("Enter Phone Number of the Passenger: ")
    cur.execute("SELECT * FROM PASSENGER WHERE PHONE_NUMBER=%s", (phone,))
    record = cur.fetchone()
    if record:
        confirm = input("Are you sure you want to cancel this booking? (y/n): ")
        if confirm.lower() == 'y':
            cur.execute("DELETE FROM PASSENGER WHERE PHONE_NUMBER=%s", (phone,))
            db.commit()
            print("Booking Cancelled Successfully")
        else:
            print("Cancellation Aborted")
    else:
        print("No Booking Found For This Phone Number")

def check_seat():
    print("\n===== SHOW BOOKED FLIGHT DETAILS =====")
    phone = input("Enter Your Registered Phone Number: ")
    cur.execute("""
        SELECT PASSENGER_NAME, PHONE_NUMBER, DESTINATION, PASSPORT_STATUS, FlightNo
        FROM PASSENGER WHERE PHONE_NUMBER=%s
    """, (phone,))
    rows = cur.fetchall()

    if rows:
        print(tabulate.tabulate(
            rows,
            headers=["Passenger Name", "Phone Number", "Destination", "Passport Status", "Flight No"],
            tablefmt="fancy_grid"
        ))
    else:
        print("No Booking Found With This Phone Number")

def passenger():      
    while True:
        print("\n===== WELCOME TO IGI AIRPORT =====")
        print("1. Show Available Flights")
        print("2. Book A Flight")
        print("3. Cancel A Booking")
        print("4. Show Seat Details Of Booked Flight")
        print("5. Exit")
        ch = int(input("Enter Your Choice: "))      
        if ch==1:
            disp()
        elif ch==2:    
            book_flight() 
        elif ch==3:
            cancel_booking()     
        elif ch==4:
            check_seat()
        elif ch==5:
            print("You have successfuly exited the menu !")
            break
        else:
            print("You have entered invalid input !!!")
            break

def main():
    print("========== AIRPORT MANAGEMENT SYSTEM ==========")
    print("1. Login As Admin")
    print("2. Login As Passenger")
    print("3. Exit")
    ch = input("Enter your choice: ")
    if ch == '1':
        admin_login()
    elif ch == '2':
        print("\n Login successful! Redirecting to Passenger Menu...\n")
        passenger()
    elif ch=='3':
        print("Program Exited,Thank You For Using!")
    else:
        print("Invalid Choice")

main()
