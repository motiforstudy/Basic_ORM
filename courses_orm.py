from typing import Optional
from sqlmodel import SQLModel, Field

class Course(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str
    hours : int
    is_active : bool = True



from sqlmodel import create_engine

engine = create_engine("sqlite:///courses.db", echo=True)



def create_db_and_tables()-> None:
    SQLModel.metadata.create_all(engine)



from sqlmodel import Session, select

def add_course(name: str, hours: int, is_active: bool = True) -> None:
    course = Course(name = name, hours = hours, is_active = is_active)
    with Session(engine) as session:
        session.add(course)
        session.commit()
        session.refresh(course)
        print(f"Added course with id = {course.id}")


def get_active_courses() -> list[Course]:
    with Session(engine) as session:
        statement = select(Course).where(Course.is_active == True)
        result = session.exec(statement)
        courses = result.all()
        return courses



if __name__ == "__main__":

    create_db_and_tables()

    add_course("SQL Basics", 20, True)
    add_course("Python intro", 30, True)
    add_course("Legacy System", 10, False)

    active = get_active_courses()
    print("Active courses: ")
    for c in  active:
        print(f"{c.id}: {c.name}({c.hours} hours) active = {c.is_active}")