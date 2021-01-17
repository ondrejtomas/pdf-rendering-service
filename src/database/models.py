# Third Party
from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.ext.declarative import declarative_base

# initialize automapping
Base = declarative_base()


class Document(Base):
    __tablename__ = 'document'

    id = Column(String, primary_key=True)
    name = Column(String)
    pages_number = Column(Integer)
    status = Column(String)


class Page(Base):
    __tablename__ = 'page'

    # to be able to quickly fetch Nth page or given document
    # we make document id as a part of primary key, that should
    # allows us to access /documents/{document_id}/pages/{N}
    # by just looking into this table instead using join
    id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("document.id"), primary_key=True)
    data = Column(LargeBinary)
