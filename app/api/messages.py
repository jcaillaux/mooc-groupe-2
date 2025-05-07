from pymongo import MongoClient
from collections import defaultdict


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

        # Si aucune projection n'est fournie, on réccupère tous les champs par défaut
        if project_ is not None:
            projection = {field: 1 for field in project_}
        else:
            projection = ""

        client = MongoClient('mongodb://localhost:27017/')
        filter=filter_
        
        limit= limit_
        # requette MongoDB avec les paramètres fournis
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

        return list(result)
    



    
    def groupement_par_fil_de_discussion(self, messages_):
        """
        Attribue un 'thread_id' à chaque message basé sur (course_id, courseware_title).
        :param messages_: Curseur MongoDB ou liste de messages.
        :return: Liste des messages, chacun avec un champ 'thread_id'.
        """

        # S'assurer qu'on peut parcourir plusieurs fois
        if not isinstance(messages_, list):
            messages_ = list(messages_)

        grouped = defaultdict(list)

        # Grouper par (course_id, courseware_title)
        for msg in messages_:
            content = msg.get('content', {})
            key = (
                content.get('course_id'),
                content.get('courseware_title')
            )
            grouped[key].append(msg)

        # Assigner un thread_id unique
        for thread_id, group in enumerate(grouped.values()):
            for msg in group:
                msg['thread_id'] = thread_id

        return messages_  # Chaque message contient maintenant un champ 'thread_id'
    







    
    



