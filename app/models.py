from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)

    files = relationship("File", back_populates="user", cascade="all, delete-orphan")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    filetype = Column(String, nullable=False)
    uploaded_at = Column(TIMESTAMP(timezone=True), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="files")

    file_content = relationship("FileContent", back_populates="file", cascade="all, delete-orphan")


class FileContent(Base):
    __tablename__ = "file_contents"

    id = Column(Integer, primary_key=True)
    content_table = Column(String, nullable=False)

    file_id = Column(Integer, ForeignKey("files.id"))
    file = relationship("File", back_populates="file_contents", cascade="all, delete-orphan")
    
