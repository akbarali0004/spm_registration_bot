# from sqlalchemy import Column, Integer, String, ForeignKey, JSON
# from sqlalchemy.orm import relationship
# from database import Base

# class Vacancy(Base):
#     __tablename__ = "vacancies"
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     questions = relationship("VacancyQuestion", back_populates="vacancy")


# class VacancyQuestion(Base):
#     __tablename__ = "vacancy_questions"
#     id = Column(Integer, primary_key=True)
#     vacancy_id = Column(Integer, ForeignKey("vacancies.id"))
#     question_text = Column(String)
#     answer_type = Column(String)    # text / date / phone / buttons
#     options = Column(JSON)          # ["Erkak", "Ayol"] agar type = buttons bo‘lsa

#     vacancy = relationship("Vacancy", back_populates="questions")


# class UserAnswer(Base):
#     __tablename__ = "user_answers"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer)
#     vacancy_id = Column(Integer)
#     question_id = Column(Integer)
#     answer = Column(String)
