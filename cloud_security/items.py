# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class WebCastItem(Item):
    """
    A Scrapy Item object containing webcast details

    Attributes:
        event_id (int): The ID of the event
        eventType (str): The type of event (webcast, summit, or series)
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

    event_id = Field()
    eventType = Field()
    title = Field()
    description = Field()
    presenter = Field()
    status = Field()
    scheduled = Field()
    entryTime = Field()
    closeTime = Field()
    created = Field()
    lastUpdated = Field()
    calender_url = Field()
    url = Field()


class SummitAndSeriesItem(Item):
    """
    A Scrapy Item object containing summit or series details

    Attributes:
        event_id (int): The ID of the event
        eventType (str): The type of event (webcast, summit, or series)
        title (str): The title of the summit or series
        description (str): The description of the summit or series
        scheduledStartDate (datetime): The scheduled start date and time of the summit or series
        scheduledEndDate (datetime): The scheduled end date and time of the summit or series
        url (str): The URL to the summit or series

    Methods:
        None
    """

    event_id = Field()
    eventType = Field()
    title = Field()
    description = Field()
    scheduledStartDate = Field()
    scheduledEndDate = Field()
    url = Field()
