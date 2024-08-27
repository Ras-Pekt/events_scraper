# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from cloud_security.engine.db_storage import DBStorage
from cloud_security.engine.models import WebCastItem, SummitAndSeriesItem
from cloud_security.items import WebCastItem as WCItem
from cloud_security.items import SummitAndSeriesItem as SSItem
from datetime import datetime
from itemadapter import ItemAdapter


class DateConversionPipeline:
    """
    A Scrapy pipeline to convert date strings to datetime objects.

    Attributes:
        None

    Methods:
        process_item: Convert date strings to datetime objects
        convert_to_datetime: Convert a date string to a datetime object
    """

    def process_item(self, item, spider):
        """
        Convert date strings to datetime objects.

        Args:
            item (dict): The item to process
            spider (Spider): The Scrapy spider

        Returns:
            dict: The processed item
        """

        adapter = ItemAdapter(item)

        webcast_keys = [
            "scheduled",
            "entryTime",
            "closeTime",
            "created",
            "lastUpdated",
        ]
        summit_and_series_keys = ["scheduledStartDate", "scheduledEndDate"]

        if isinstance(item, WCItem):
            for key in webcast_keys:
                date_str = adapter.get(key)
                adapter[key] = self.convert_to_datetime(date_str, spider)
        elif isinstance(item, SSItem):
            for key in summit_and_series_keys:
                date_str = adapter.get(key)
                adapter[key] = self.convert_to_datetime(date_str, spider)
        else:
            spider.logger.error(
                f"vannaDATECONVERSION -> UNKNOWN ITEM TYPE: {type(item)}"
            )

        return item

    def convert_to_datetime(self, date_str, spider):
        """
        Convert a date string to a datetime object.

        Args:
            date_str (str): The date string to convert
            spider (Spider): The Scrapy spider

        Returns:
            datetime: The datetime object
        """

        if date_str:
            try:
                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                spider.logger.error(f"Failed to parse date: {date_str}")
        return None


class DBStoragePipeline:
    """
    A Scrapy pipeline to store items in a database.

    Attributes:
        storage (DBStorage): An instance of DBStorage

    Methods:
        process_item: Store items in a database
        close_spider: Close the database connection
    """

    def __init__(self):
        """
        Initialize the DBStoragePipeline.

        Args:
            None
        """

        self.storage = DBStorage()

    def process_item(self, item, spider):
        """
        Store items in a database.

        Args:
            item (dict): The item to store
            spider (Spider): The Scrapy spider

        Returns:
            dict: The stored item
        """

        if isinstance(item, WCItem):
            webcast_item = WebCastItem(
                event_id=item.get("event_id"),
                eventType=item.get("eventType"),
                title=item.get("title"),
                description=item.get("description"),
                presenter=item.get("presenter"),
                status=item.get("status"),
                scheduled=item.get("scheduled"),
                entryTime=item.get("entryTime"),
                closeTime=item.get("closeTime"),
                created=item.get("created"),
                lastUpdated=item.get("lastUpdated"),
                calender_url=item.get("calender_url"),
                url=item.get("url"),
            )
            self.storage.add_item(webcast_item)
        elif isinstance(item, SSItem):
            summit_and_series_item = SummitAndSeriesItem(
                event_id=item.get("event_id"),
                eventType=item.get("eventType"),
                title=item.get("title"),
                description=item.get("description"),
                scheduledStartDate=item.get("scheduledStartDate"),
                scheduledEndDate=item.get("scheduledEndDate"),
                url=item.get("url"),
            )
            self.storage.add_item(summit_and_series_item)
        else:
            spider.logger.error(f"UNKNOWN ITEM TYPE: {type(item)}")

        return item

    def close_spider(self, spider):
        """
        Close the database connection.

        Args:
            spider (Spider): The Scrapy spider
        """

        self.storage.close()
