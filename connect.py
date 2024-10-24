import mysql.connector

def connection():
    con = mysql.connector.connect(
        host='localhost',
        user='root',  
        password='sql@2004',
        database='jobs_listing'
    )
    return con

con = connection()
cur = con.cursor()


drop_query = '''
DROP TABLE IF EXISTS jobs_listing
'''

cur.execute(drop_query)
con.commit()

create_query = '''
CREATE TABLE jobs_listing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    position VARCHAR(255),
    company VARCHAR(255),
    details_time VARCHAR(255),
    details_level VARCHAR(255),
    details_place VARCHAR(255),
    location VARCHAR(255),
    time_posted VARCHAR(255))
'''
cur.execute(create_query)
con.commit()


data_to_insert = '''
        INSERT INTO jobs_listing (position, company, details_time, details_level, details_place, location, time_posted) VALUES
    ('UX Researcher', 'WebFlow', 'Fulltime', 'Senior level', 'Remote', 'California, CA', '1 hour ago'),
    ('Quality Assurance', 'Notion', 'Fulltime', 'Senior level', 'Remote', 'Idaho, ID', '2 hours ago'),
    ('Senior Dev', 'Zappler', 'Fulltime', 'Senior level', 'Remote', 'Oklahoma, OK', '6 hours ago'),
    ('Product Designer', 'MailChimp', 'Fulltime', 'Senior level', 'Remote', 'New York, NY', '3 hours ago'),
    ('Sales', 'Outreach', 'Fulltime', 'Senior level', 'Remote', 'Dallas, TX', '10 hours ago'),
    ('Project Manager', 'SquareSpace', 'Fulltime', 'Senior level', 'Remote', 'Florida, FL', '1 day ago'),
    ('UX Researcher', 'WebFlow', 'Fulltime', 'Senior level', 'Remote', 'California, CA', '1 hour ago'),
    ('Quality Assurance', 'Notion', 'Fulltime', 'Senior level', 'Remote', 'Idaho, ID', '2 hours ago'),
    ('Senior Dev', 'Zappler', 'Fulltime', 'Senior level', 'Remote', 'Oklahoma, OK', '6 hours ago'),
    ('Product Designer', 'MailChimp', 'Fulltime', 'Senior level', 'Remote', 'New York, NY', '3 hours ago'),
    ('Sales', 'Outreach', 'Fulltime', 'Senior level', 'Remote', 'Dallas, TX', '10 hours ago'),
    ('Project Manager', 'SquareSpace', 'Fulltime', 'Senior level', 'Remote', 'Florida, FL', '1 day ago')
        '''


cur.execute(data_to_insert)
con.commit()

select_query = "SELECT * FROM job_postings"
cur.execute(select_query)

records = cur.fetchall()

# print(f"ID\tTitle\t\t\tCompany\t\t\tLocation\t\tEmployment Type\t\tDescription")
# print("="*150)  

# for record in records:
#     print(f"{record[0]}\t{record[1]}\t\t{record[2]}\t{record[3]}\t\t{record[4]}")

cur.close()
con.close()

# print("Server connected successfully")
