"""User objects for handling users."""

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import Session

from Cereal.constants import Base, pwd_context


class User(Base):
    """User object for handling users.

    Currently only the admin user has specific rights,
    but other rights can be implimented.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    email = Column(String(255))
    hashed_password = Column(String(255))
    rights = Column(Enum("Admin", "User"))

    def __init__(
        self,
        username: str,
        email: str,
        hashed_password: str,
        rights: str,
    ) -> None:
        """Initialize class.

        Args:
            username (str): Username.
            email (str): Email.
            hashed_password (str): Hashed password.
            rights (str): User rights.
        """
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.rights = rights

    @classmethod
    def create_user(
        cls,
        db: Session,
        username: str,
        email: str,
        password: str,
    ) -> None:
        """Create a new user.

        Args:
            db (Session): Session.
            username (str): Username.
            email (str): Email.
            password (str): Password.
        """
        hashed_password = pwd_context.hash(password)

        db_user = cls(
            username=username,
            email=email,
            hashed_password=hashed_password,
            rights="User",
        )
        db_user.rights = "User"
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.close()

    @classmethod
    def create_admin(cls, db: Session) -> None:
        """Create the admin user.

        Args:
            db (Session): Session.
        """
        hashed_password = pwd_context.hash("admin")
        db_admin = cls(
            username="admin",
            email="admin@admin.com",
            hashed_password=hashed_password,
            rights="Admin",
        )
        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)
        db.close()
