#!/usr/bin/env python3
"""Database manager module.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session


class DatabaseHandler:
    """Handles database operations and user management.
    """

    def __init__(self) -> None:
        """Initialize the database connection and ensure the schema is set up.
        """
        self._db_engine = create_engine("sqlite:///users.db", echo=False)
        Base.metadata.drop_all(self._db_engine)
        Base.metadata.create_all(self._db_engine)
        self._session_instance = None

    @property
    def session(self) -> Session:
        """Retrieve or create a database session.
        """
        if self._session_instance is None:
            session_factory = sessionmaker(bind=self._db_engine)
            self._session_instance = session_factory()
        return self._session_instance

    def add_new_user(self, email: str, password_hash: str) -> User:
        """Add a new user to the database using email and hashed password.
        """
        try:
            new_user = User(email=email, hashed_password=password_hash)
            self.session.add(new_user)
            self.session.commit()
        except Exception:
            self.session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **filters) -> User:
        """Find a user by various attributes provided as filters.
        """
        filter_columns, filter_values = [], []
        for attribute, value in filters.items():
            if hasattr(User, attribute):
                filter_columns.append(getattr(User, attribute))
                filter_values.append(value)
            else:
                raise InvalidRequestError("Invalid field name provided.")

        query_result = self.session.query(User).filter(
            tuple_(*filter_columns).in_([tuple(filter_values)])
        ).first()

        if query_result is None:
            raise NoResultFound("No user found!")
        return query_result

    def update_user(self, user_id: int, **updates) -> None:
        """Update user information by their user ID.
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update_data = {}
        for attribute, value in updates.items():
            if hasattr(User, attribute):
                update_data[getattr(User, attribute)] = value
            else:
                raise ValueError(f"Invalid update field: {attribute}")

        self.session.query(User).filter(User.id == user_id).update(
            update_data,
            synchronize_session=False,
        )
        self.session.commit()
