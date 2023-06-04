from sqlalchemy import JSON, Boolean, Column, Integer, LargeBinary, String, ForeignKey, Text, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    is_authorized = Column(Boolean, default=False)

    files = relationship("File", back_populates="user", cascade="all, delete-orphan")


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    filetype = Column(String, nullable=False)
    uploaded_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    file_data = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="files")

    file_content = relationship("FileContent", back_populates="file", cascade="all, delete-orphan")


class FileContent(Base):
    __tablename__ = "file_contents"

    id = Column(Integer, primary_key=True)
    contents = Column(String, nullable=False)
    data = Column(JSON, nullable=False)

    file_id = Column(Integer, ForeignKey("files.id"))
    file = relationship("File", back_populates="file_contents", cascade="all, delete-orphan")
    
