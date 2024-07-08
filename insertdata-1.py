from pymysql import*
from csv import reader

def insertdata():
    try:
        # Establish database connection
        con = connect(host="localhost",user="root",password="harisudhan",db="railway",port=3306)
        c = con.cursor()

        # Open the CSV file (using a raw string for the path)
        with open(r"F:\Python project\Train_details.csv", "r") as f:
            cr = reader(f)
            
            # Skip the header row if it exists
            next(cr, None)
            
            # Insert each row into the database
            for row in cr:
                # Ensure the data types and formats match the database schema
                query = "INSERT INTO train_info (Train_no, Station_code, Station_name, Arrival_time, Deapature_time, Distance, Source_station_code, Source_station_name, Destination_station_code, Destination_station_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                c.execute(query, row)

        # Commit the transaction
        con.commit()

    except Error as err:
        print(f"Error: {err}")
        con.rollback()
    
    except FileNotFoundError as e:
        print(e)
    
    finally:
        # Close the cursor and connection
        c.close()
        con.close()
        print("Database connection closed.")

# Call the function to insert data
insertdata()
