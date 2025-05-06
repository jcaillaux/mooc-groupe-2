from pymongo import MongoClient

class MongoMessages:
    def __init__(self):
        pass
    def get_messages_data(self, project_=None, filter_={}, limit_=1000, database_='mooc', collection_='sample', print_=True):
        """
        Cette fonction permet de récupérer les messages d'une collection MongoDB.
        :param project_: Liste des champs à récupérer. Si None, des champs par défault sont récupérés.
        :param filter_: Filtre à appliquer sur les messages. Par défaut, tous les messages sont récupérés.
        :param limit_: Limite du nombre de messages à récupérer. Par défaut, 1000 messages sont récupérés.
        :param database_: Nom de la base de données. Par défaut, 'mooc'.
        :param collection_: Nom de la collection. Par défaut, 'sample'.
        :param print_: Si True, les messages sont affichés dans la console. Par défaut, True.
        :return: Liste des messages récupérés.
        """

        
        if project_ is not None:
            projection = {field: 1 for field in project_}
        else:
            projection = ""

        client = MongoClient('mongodb://localhost:27017/')
        filter=filter_
        
        limit= limit_

        result = client[database_][collection_].find(
        filter=filter,
        projection=projection,
        limit=limit
        )

        if print_:
            for message in result:
                print("")
                print(message)
                print("_______________________________________________________________________________________")

        return result


# project = ['content.title', 'content.body', 'content.votes']
# mongo = MongoMessages()
# messages = mongo.get_messages_data(project_=project)
