from app.database import db, Base
from sqlalchemy import Column, Integer, String, Date


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    level = Column(String(50))
    gender = Column(String(10))
    department = Column(String(100))
    position = Column(String(100))
    entry_date = Column(Date)
    status = Column(String(20))

    @classmethod
    def get_total_count(cls, session):
        return session.query(cls).count()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level,
            'gender': self.gender,
            'department': self.department,
            'position': self.position,
            'entry_date': self.entry_date.strftime('%Y-%m-%d') if self.entry_date else None,
            'status': self.status
        }


def get_users_with_birthday():
    def operation(session):
        return session.query(User).filter(User.birthday.isnot(None)).all()

    return db.execute_with_retry(operation)
