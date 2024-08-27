from cloud_security.engine import Base
from sqlalchemy import Column, String, Integer, Text, DateTime


class WebCastItem(Base):
    """
    A SQLAlchemy model to store webcast data.

    Attributes:
        id (int): The primary key
        eventType (str): The type of the event
        title (str): The title of the webcast
        description (str): The description of the webcast
        presenter (str): The presenter of the webcast
        status (str): The status of the webcast
        scheduled (datetime): The scheduled date and time of the webcast
        entryTime (datetime): The entry time of the webcast
        closeTime (datetime): The close time of the webcast
        created (datetime): The creation date and time of the webcast
        lastUpdated (datetime): The last update date and time of the webcast
        calender_url (str): The URL to the webcast calendar
        url (str): The URL to the webcast

    Methods:
        None
    """

    __tablename__ = "webcasts"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    eventType = Column(String(256))
    title = Column(String(256))
    description = Column(Text)
    presenter = Column(String(256))
    status = Column(String(256))
    scheduled = Column(DateTime)
    entryTime = Column(DateTime)
    closeTime = Column(DateTime)
    created = Column(DateTime)
    lastUpdated = Column(DateTime)
    calender_url = Column(String(256))
    url = Column(String(256))


class SummitAndSeriesItem(Base):
    """
    A SQLAlchemy model to store summit and series data.

    Attributes:
        id (int): The primary key
        eventType (str): The type of  the event
        title (str): The title of the summit or series
        description (str): The description of the summit or series
        scheduledStartDate (datetime): The scheduled start date and time of the summit or series
        scheduledEndDate (datetime): The scheduled end date and time of the summit or series
        url (str): The URL to the summit or series

    Methods:
        None
    """

    __tablename__ = "summits_and_series"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    eventType = Column(String(256))
    title = Column(String(256))
    description = Column(Text)
    scheduledStartDate = Column(DateTime)
    scheduledEndDate = Column(DateTime)
    url = Column(String(256))
