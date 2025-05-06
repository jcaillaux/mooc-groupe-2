from modules.mongo_messages import MongoMessages

project = ['content.title', 'content.body', 'content.votes']
mongo = MongoMessages()
messages = mongo.get_messages_data(project_=project)