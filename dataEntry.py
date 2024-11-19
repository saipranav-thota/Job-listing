from connect import connection

con = connection()
cur = con.cursor()

data_to_insert = '''INSERT INTO jobs_listing (position, company, employment_type, max_experience, min_experience, work_mode, location, date_posted) VALUES
                        ('Software Engineer', 'TechCorp', 'Fulltime', 5, 0, 'Remote', 'Mumbai', 'Last 24 hours'),
                        ('Data Analyst', 'DataWorks', 'Fulltime', 10, 2, 'Hybrid', 'Pune', 'Last 3 Days'),
                        ('Project Manager', 'Innovate', 'Contract', 15, 5, 'Remote', 'Hyderabad', 'Last 7 Days'),
                        ('Backend Developer', 'DevSolutions', 'Internship', 2, 0, 'Hybrid', 'Bangalore', 'Last 14 Days'),
                        ('DevOps Engineer', 'CloudOps', 'Fulltime', 20, 5, 'Remote', 'Mumbai', 'Last 3 Days'),
                        ('Frontend Developer', 'Webify', 'Contract', 8, 2, 'Hybrid', 'Pune', 'Last 7 Days'),
                        ('UI/UX Designer', 'CreativeMinds', 'Internship', 1, 0, 'Remote', 'Hyderabad', 'Last 24 hours'),
                        ('Product Manager', 'Visionary', 'Fulltime', 10, 3, 'Hybrid', 'Bangalore', 'Last 14 Days'),
                        ('QA Engineer', 'QualityTech', 'Fulltime', 5, 1, 'Remote', 'Mumbai', 'Last 24 hours'),
                        ('Marketing Analyst', 'Brandify', 'Contract', 7, 1, 'Hybrid', 'Pune', 'Last 7 Days'),
                        ('Machine Learning Engineer', 'AI Innovators', 'Fulltime', 30, 10, 'Remote', 'Hyderabad', 'Last 3 Days'),
                        ('Software Tester', 'BugFixers', 'Internship', 3, 0, 'Hybrid', 'Bangalore', 'Last 14 Days'),
                        ('HR Manager', 'PeopleFirst', 'Fulltime', 10, 5, 'Remote', 'Mumbai', 'Last 7 Days'),
                        ('Cybersecurity Specialist', 'SecureNet', 'Contract', 25, 8, 'Hybrid', 'Pune', 'Last 24 hours'),
                        ('Sales Executive', 'Sellify', 'Internship', 1, 0, 'Remote', 'Hyderabad', 'Last 3 Days');
'''
cur.execute(data_to_insert)
con.commit()

cur.close()
con.close()