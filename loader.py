# from elasticsearch import Elasticsearch
# import csv

# es = Elasticsearch(hosts= ["http://127.0.0.1:9200"])

# print(f"Connected to es `{es.info().body['cluster_name']}`")

# with open ("laptop_pricing_dataset_mod1.csv","r") as f:
#     reader = csv.reader(f)

#     for i, line in enumerate(reader):
#         document ={
#             "Manufacturer": line[1],
#             "Screen": line[3],
#         }
#         es.index(index="laptops", document=document)

from elasticsearch import Elasticsearch
import csv

# Connect to Elasticsearch
es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

# Check connection
print(f"Connected to Elasticsearch: `{es.info().body['cluster_name']}`")

# Open and read the CSV file
with open("laptop_pricing_dataset_mod1.csv", "r") as f:
    reader = csv.reader(f)

    # Skip header if there is one
    next(reader)

    # Iterate through the rows in the CSV
    for i, line in enumerate(reader):
        # Create a document from the CSV row
        document = {
            "Manufacturer": line[1],  # Adjust index based on your CSV structure
            "Screen": line[3],        # Adjust index based on your CSV structure
        }
        
        es.index(index="laptops", document=document)

        print(f"Indexed document {i + 1}: {document}")
