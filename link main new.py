from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector
import time

# Function to connect to MySQL and insert job data
def save_job_to_db(title, company, location, salary, description, link, uploaded_time):
    connection = None
    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='jai28deep',  # Replace with your MySQL password
            database='scraped_jobs'  # New database name
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # SQL query to insert job data
            sql = """INSERT INTO jobs (title, company, location, salary, description, link, uploaded_time) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (title, company, location, salary, description, link, uploaded_time)
            cursor.execute(sql, values)
            connection.commit()
            print(f"Job '{title}' saved successfully")
            cursor.close()
    except mysql.connector.Error as e:
        print(f"Failed to insert record: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()

# Function to scrape jobs from Naukri.com
def get_jobs(keyword, location, experience):
    url = f"https://www.naukri.com/k-jobs-in-l?k={keyword}&l={location}&experience={experience}"
    
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)  # Delay to let the page load

    try:
        job_listings = driver.find_elements(By.CLASS_NAME, 'srp-jobtuple-wrapper')
        
        if not job_listings:
            print("\nNo jobs found. Please refine your search criteria.")
            return

        print(f"\nFound {len(job_listings)} jobs for '{keyword}' in '{location}' with '{experience}' years of experience:\n")

        for job in job_listings:
            # Extract job title
            try:
                title_element = job.find_element(By.CSS_SELECTOR, 'a.title')
                title = title_element.text
                link = title_element.get_attribute('href')  # Extract the link
            except:
                title = "Title not found"
                link = "Link not found"
            
            # Extract company name
            try:
                company = job.find_element(By.CSS_SELECTOR, 'a.comp-name').text
            except:
                company = "Company not found"
            
            # Extract job location
            try:
                job_location = job.find_element(By.XPATH, ".//span[contains(@class, 'loc')]").text
            except:
                job_location = "Location not found"

            # Extract salary
            try:
                salary = job.find_element(By.CSS_SELECTOR, 'span.sal-wrap').text
            except:
                salary = "Salary not found"

            # Extract job description
            try:
                description = job.find_element(By.CSS_SELECTOR, 'span.job-desc').text
            except:
                description = "Description not found"
            
            # Extract uploaded time
            try:
                uploaded_time = job.find_element(By.CSS_SELECTOR, 'span.job-post-day').text
            except:
                uploaded_time = "Uploaded time not found"

            print(f"Title: {title}\nCompany: {company}\nLocation: {job_location}\nSalary: {salary}\nDescription: {description}\nLink: {link}\nUploaded Time: {uploaded_time}\n")

            # Save job to the database
            save_job_to_db(title, company, job_location, salary, description, link, uploaded_time)
    
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

# Prompt the user for inputs and scrape jobs
if __name__ == "__main__":
    print("Welcome to the Naukri Job Scraper!")
    keyword = input("Enter job keyword (e.g., software engineer): ").strip()
    location = input("Enter location (e.g., Chennai): ").strip()
    experience = input("Enter years of experience (e.g., 0): ").strip()

    get_jobs(keyword, location, experience)
