from modules.mongo_messages import MongoMessages
from modules.clusturings import MessagesClusterings


project = ['content.title', 'content.body', 'content.votes', 'content.course_id', 'content.courseware_title']
mongo = MongoMessages()
messages = mongo.get_messages_data(project_=project, limit_=1000, print_=False)
print(messages)
cluster = MessagesClusterings()
messages_clusterise = cluster.cluster_par_fil_de_discussion(messages_ = messages)
print(messages_clusterise)