from app.postgreDB import Message, engine
from sqlmodel import Session, select

def get_list_of_courses():
    """
    Récupère la liste des cours dans la base de données PostgreSQL.
    
    Returns:

        List[str]: Liste des cours (course_id)
    """
    global engine
    with Session(engine) as session:
        query = select(Message.course_id).distinct()
        result = session.exec(query)        
    return result.all()

if __name__ == "__main__":
    courses = get_list_of_courses()
    print(type(courses))
    print(f"Nombre de cours : {len(courses)}")
    print(f"Liste des cours : {courses}")
    print(courses[0])
