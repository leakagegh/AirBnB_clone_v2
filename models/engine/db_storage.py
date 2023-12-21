#!/usr/bin/python3
"""
New engine DBStorage
"""
import os
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBStorage:
    """Database storage engine for hbnb models"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the database engine and session"""
        # Retrieve database credentials from environment variables
        db_user = os.getenv('HBNB_MYSQL_USER')
        db_pwd = os.getenv('HBNB_MYSQL_PWD')
        db_host = os.getenv('HBNB_MYSQL_HOST')
        db_name = os.getenv('HBNB_MYSQL_DB')

        # Create the database engine
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(db_user, db_pwd, db_host, db_name),
            pool_pre_ping=True
        )

        # Drop all tables if HBNB_ENV is set to 'test'
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

        # Create all tables if they don't exist
        Base.metadata.create_all(self.__engine)

        # Create the database session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
        self.__session = SessionLocal()

    def all(self, cls=None):
        """Returns a dictionary of all objects of the specified class or all classes"""
        if cls:
            objects = self.__session.query(cls).all()
        else:
            # Query all types of objects if cls is None
            objects = []
            for model_class in Base.__subclasses__():
                objects.extend(self.__session.query(model_class).all())

        dictionary = {}
        for obj in objects:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            dictionary[key] = obj

        return dictionary

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes the object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads all models from the database"""
        Base.metadata.create_all(self.__engine)

        # Create a new session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
        self.__session = SessionLocal()
