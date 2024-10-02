import mysql.connector

con = mysql.connector.connect(
    host='localhost',
    user='root',  
    password='sql@2004',
    database='jobs_listing'
)

cur = con.cursor()

insert_query = '''
INSERT INTO job_postings (title, company, employment_type, position, work_type, location, employment_type, time_posted ,description)
VALUES (%s, %s, %s, %s, %s)
'''

data_to_insert = [
    ('Software Engineer', 'Tech Corp', 'New York, NY', 'Full-time', 'Software Engineer', 'Onsite', '2024-10-01', 'Develop and maintain software applications.'),
    ('Data Analyst', 'Data Solutions', 'Los Angeles, CA', 'Part-time', 'Data Analyst', 'Remote', '2024-10-01', 'Analyze data and generate reports.'),
    ('Product Manager', 'Innovate Inc.', 'Remote', 'Full-time', 'Product Manager', 'Hybrid', '2024-10-01', 'Lead product development and strategy.'),
    ('Web Developer', 'WebWorks', 'Austin, TX', 'Contract', 'Web Developer', 'Onsite', '2024-10-01', 'Build and maintain websites.')
]


cur.executemany(insert_query, data_to_insert)
con.commit()

select_query = 'SELECT * FROM job_postings'
cur.execute(select_query)

records = cur.fetchall()

print(f"ID\tTitle\t\t\tCompany\t\t\tLocation\t\tEmployment Type\t\tDescription")
print("="*150)  

for record in records:
    print(f"{record[0]}\t{record[1]}\t\t{record[2]}\t{record[3]}\t\t{record[4]}")

cur.close()
con.close()

print("Server connected successfully")
