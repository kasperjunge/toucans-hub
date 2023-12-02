import logging
from typing import Optional, Tuple, Type

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, SQLModel, select

# Configure logger (configure it according to your logging setup)
logger = logging.getLogger(__name__)


def get_or_create(
    session: Session,
    model: Type[SQLModel],
    **kwargs,
) -> Tuple[SQLModel, bool]:
    """
    Retrieves an existing record or creates a new one based on the provided criteria.

    Args:
        session (Session): The database session.
        model (Type[SQLModel]): The model class for the record.
        **kwargs: Field-value pairs for record identification or creation.

    Returns:
        Tuple[SQLModel, bool]: A tuple containing the record and a boolean flag
                               indicating if the record was created (True) or retrieved (False).

    Raises:
        ValueError: If kwargs contains invalid fields.
        SQLAlchemyError: If a database operation fails.
    """

    # Validate input fields
    for k in kwargs.keys():
        if not hasattr(model, k):
            logger.error(f"Invalid field '{k}' for model {model.__name__}")
            raise ValueError(f"Invalid field '{k}' for model {model.__name__}")

    try:
        # Search for the record
        query = select(model).where(
            *(getattr(model, k) == v for k, v in kwargs.items())
        )
        record = session.exec(query).first()

        if record:
            return record, False

        # Create a new record if not found
        record = model(**kwargs)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record, True

    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        session.rollback()
        raise


def update(
    session: Session, model: Type[SQLModel], identifier: dict, updates: dict
) -> bool:
    """
    Updates specified fields in an existing record.

    Args:
        session (Session): The database session.
        model (Type[SQLModel]): The model class of the record to update.
        identifier (dict): Field-value pairs to identify the record.
        updates (dict): Field-value pairs to update in the record.

    Returns:
        bool: True if the record was updated, False if not found or in case of an error.

    Raises:
        ValueError: If identifier or updates contain invalid fields.
    """

    # Validate input fields
    for key in {*identifier.keys(), *updates.keys()}:
        if not hasattr(model, key):
            logger.error(f"Invalid field '{key}' for model {model.__name__}")
            raise ValueError(f"Invalid field '{key}' for model {model.__name__}")

    try:
        # Retrieve the record
        query = select(model).where(
            *(getattr(model, k) == v for k, v in identifier.items())
        )
        record = session.exec(query).first()

        # Check if the record exists and update it
        if record:
            updated = False
            for key, value in updates.items():
                if getattr(record, key) != value:
                    setattr(record, key, value)
                    updated = True

            if updated:
                session.commit()
                return True
            else:
                return False
        else:
            return False

    except SQLAlchemyError as e:
        logger.error(f"Error during database operation: {e}")
        session.rollback()
        return False


def get(session: Session, model: Type[SQLModel], **kwargs) -> Optional[SQLModel]:
    """
    Retrieves an existing record based on the provided criteria.

    Args:
        session (Session): The database session.
        model (Type[SQLModel]): The model class for the record.
        **kwargs: Field-value pairs for record identification.

    Returns:
        Optional[SQLModel]: The retrieved record, or None if not found or in case of an error.
    """

    # Validate input fields
    for k in kwargs.keys():
        if not hasattr(model, k):
            logger.error(f"Invalid field '{k}' for model {model.__name__}")
            return None

    try:
        # Build query with dynamic field-value pairs
        query = select(model).where(
            *(getattr(model, k) == v for k, v in kwargs.items())
        )
        logger.debug(
            f"Executing query for model {model.__name__} with criteria {kwargs}"
        )

        # Execute query and fetch the first result
        record = session.exec(query).first()
        return record

    except SQLAlchemyError as e:
        # Handle database errors gracefully
        logger.error(f"Database error occurred: {e}")
        return None


def create(session: Session, model: Type[SQLModel], **kwargs) -> SQLModel:
    """
    Creates a new record with the given data.

    Args:
        session (Session): The database session.
        model (Type[SQLModel]): The model class for the record.
        **kwargs: Field-value pairs for creating the new record.

    Returns:
        SQLModel: The newly created record.

    Raises:
        ValueError: If kwargs contains invalid fields.
        SQLAlchemyError: If a database operation fails.
    """

    # Validate input fields
    for k in kwargs.keys():
        if not hasattr(model, k):
            logger.error(f"Invalid field '{k}' for model {model.__name__}")
            raise ValueError(f"Invalid field '{k}' for model {model.__name__}")

    try:
        # Create a new record and commit changes
        new_record = model(**kwargs)
        session.add(new_record)
        session.commit()

    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        session.rollback()
        raise

    # Refresh the instance after successful commit
    session.refresh(new_record)

    return new_record
