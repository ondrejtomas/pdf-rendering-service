# Standard Library
from logging import getLogger
from typing import List

# Third Party
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

# Local
from src.common import settings
from src.common.enums import DocumentStatus
from src.common.utils import Singleton
from src.database.models import Base, Document, Page

logger = getLogger(__name__)


class DatabaseHandler(metaclass=Singleton):
    # (TODO: make this class abstract and implement specific handlers)

    def __init__(self):
        # create PostgreSQL engine to connect to the database
        self.engine = create_engine(
            f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}',
            pool_pre_ping=True)

        # create the database if does not exist
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        # connect to the database
        self.engine.connect()

        # create tables if do not exist
        Base.metadata.create_all(self.engine, checkfirst=True)

        # create a configured "Session" class
        self.Session = sessionmaker(bind=self.engine)

    def close(self):
        # TODO: close database connection
        pass

    def get_document(self, document_id: str):
        # create a Session
        session = self.Session()

        # get the document from database
        document = session.query(Document).get(document_id)

        return document

    def insert_document(self,
                        document_id: str,
                        document_name: str,
                        document_status: DocumentStatus = DocumentStatus.IN_QUEUE.value):
        # create a Session
        session = self.Session()

        # create database object
        document = Document(id=document_id, name=document_name, status=document_status)

        # add to the session and commit changes
        session.add(document)
        session.commit()

    def update_document(self,
                        document_id: str,
                        document_name: str = None,
                        document_pages_number: int = None,
                        document_status: DocumentStatus = None):
        # create a Session
        session = self.Session()

        # create patch object
        patch = {}

        if document_name:
            patch['name'] = document_name

        if document_pages_number:
            patch['pages_number'] = document_pages_number

        if document_status:
            patch['status'] = document_status.value

        # update database object and commit changes
        session.query(Document).filter(Document.id == document_id).update(patch)
        session.commit()

    def get_page(self, document_id: str, page_id: str):
        # create a Session
        session = self.Session()

        # get the document from database
        page = session.query(Page).get((page_id, document_id))

        return page

    def insert_pages(self, document_id: str, pages_data: List[str]):
        # create a Session
        session = self.Session()

        # create database objects and add them to the session
        for page_id, page_data in enumerate(pages_data):
            page = Page(id=page_id, document_id=document_id, data=page_data)
            session.add(page)

        # update number of pages in the document
        self.update_document(document_id=document_id, document_pages_number=len(pages_data))

        # commit changes
        session.commit()
