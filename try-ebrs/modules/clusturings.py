from collections import defaultdict

class MessagesClusterings:
    def __init__(self):
        pass

    def cluster_par_fil_de_discussion(self, messages_):
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
