import mysql.connector

def save_job_to_db(title, company, location, salary, description):
    connection = None
    try:
        # Establish the connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='jai28deep',  # Update this with your actual password
            database='jobscraper'
        )

        # Check if connection was successful
        if connection.is_connected():
            cursor = connection.cursor()

            # Insert job details into the table
            sql = """INSERT INTO jobs (title, company, location, salary, description) 
                     VALUES (%s, %s, %s, %s, %s)"""
            values = (title, company, location, salary, description)
            cursor.execute(sql, values)
            
            # Commit the transaction
            connection.commit()
            print("Job saved successfully")
            cursor.close()
    
    except mysql.connector.Error as e:
        print(f"Failed to insert record: {e}")
    
    finally:
        # Ensure that connection is closed if it was established
        if connection and connection.is_connected():
            connection.close()

# Test the function
save_job_to_db("Software Engineer", "Tech Corp", "Chennai", "10-12 Lacs PA", "Great opportunity")
