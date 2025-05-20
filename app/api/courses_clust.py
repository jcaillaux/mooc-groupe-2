from pymongo import MongoClient

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb://localhost:27017/')
filter={}
project={
    'content.course_id': 1, 
    'content.title': 1, 
    'content.body': 1
}
maxTimeMS=60000

result = client['mooc']['sample'].find(
  filter=filter,
  projection=project,
  max_time_ms=maxTimeMS
)

result = list(result)

print(result)
