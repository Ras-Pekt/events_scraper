from cloud_security.items import WebCastItem, SummitAndSeriesItem
from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider


class EventscraperSpider(Spider):
    """
    A Scrapy spider to scrape webcasts, summits, and series from the BrightTALK API.

    Attributes:
        name (str): The name of the spider
        allowed_domains (list): A list of domains allowed to be scraped
        webcast_start (int): The starting index for webcasts
        ss_start (int): The starting index for summits and series
        scraped_webcasts (bool): A flag to track if webcasts have been scraped
        scraped_summits_and_series (bool): A flag to track if summits and series have been scraped

    Methods:
        start_requests: Generate URLs dynamically for webcasts, summits, and series
        parse: Parse the JSON response from the BrightTALK API
        parse_webcasts: Parse the webcasts from the JSON response
        parse_summits_or_series: Parse the summits or series from the JSON response
    """

    name = "eventscraper"
    allowed_domains = ["www.brighttalk.com"]

    def __init__(self, *args, **kwargs):
        """
        Initialize the spider with a start value and flags to track scraping progress.
        The start values are used to paginate through the BrightTALK API.
        The flags are used to stop the spider when there's no more data to scrape.

        args:
            None
        returns:
            None
        """

        super().__init__(*args, **kwargs)
        self.webcast_start = 0
        self.ss_start = 0
        self.scraped_webcasts = False
        self.scraped_summits_and_series = False

    def start_requests(self):
        """
        Generate URLs dynamically for webcasts, summits, and series.
        The URLs are paginated using the start value.

        args:
            None
        yields:
            Request: A Scrapy Request object to scrape the BrightTALK API
        """

        while True:
            webcast_start = self.webcast_start * 8
            ss_start = self.ss_start * 6

            urls = [
                (
                    f"https://www.brighttalk.com/api/webcasts?start={webcast_start}&size=8&rank=-webcast_relevance&bq=%28and+type%3A%27webcast%27+status%3A%27recorded%27+%27Cloud+Security%27%29&rankClosest=&paidSearch=true&returnFields=&q=",
                    "webcast",
                ),
                (
                    f"https://www.brighttalk.com/api/webcasts?start={webcast_start}&size=8&rank=webcast_relevance&bq=%28and+type%3A%27webcast%27+status%3A%27upcoming%27+%27Cloud+Security%27%29&rankClosest=&paidSearch=true&returnFields=&q=",
                    "webcast",
                ),
                (
                    f"https://www.brighttalk.com/api/summits?start={ss_start}&size=6&rank=-custom_relevance%2Cdatetime&bq=%28and+type%3A%27summit%27+%27Cloud+Security%27%29&rankClosest=",
                    "summit",
                ),
                (
                    f"https://www.brighttalk.com/api/series?start={ss_start}&size=6&rank=-custom_relevance%2Cdatetime&bq=%28and+type%3A%27series%27+%27Cloud+Security%27%29&rankClosest=",
                    "series",
                ),
            ]

            for url, event_type in urls:
                yield Request(url, self.parse, cb_kwargs={"event_type": event_type})

            self.webcast_start += 1
            self.ss_start += 1

    def parse(self, response, **cb_kwargs):
        """
        Parse the JSON response from the BrightTALK API.
        The response contains webcasts, summits, or series.

        args:
            response: The JSON response from the BrightTALK API
            event_type: The type of event (webcast, summit, or series)
        yields:
            dict: A dictionary containing event details
        """

        data = response.json()

        event_type = cb_kwargs.get('event_type')

        if event_type == "webcast":
            webcasts = data.get("communications", [])
            webcasts_found = data.get("found")
            if webcasts_found != 0:
                yield from self.parse_webcasts(webcasts, event_type)
            else:
                self.scraped_webcasts = True

        elif event_type in ["summit", "series"]:
            summits_or_series = data.get("summits", [])
            summits_found = data.get("found")
            if summits_found != 0:
                yield from self.parse_summits_or_series(summits_or_series, event_type)
            else:
                self.scraped_summits_and_series = True

        if self.scraped_webcasts and self.scraped_summits_and_series:
            raise CloseSpider("No more events to scrape")

    def parse_webcasts(self, webcasts, event_type):
        """
        Parse the webcasts from the JSON response.
        The webcasts contain details like title, status, and URL.

        args:
            webcasts: A list of webcasts from the JSON response
            event_type: The type of event (webcast, summit, or series)
        yields:
            WebCastItem: A Scrapy Item object containing webcast details
        """

        webcast_item = WebCastItem()
        for event in webcasts:
            webcast_item["event_id"] = event.get("id")
            webcast_item["eventType"] = event_type
            webcast_item["title"] = event.get("title")
            webcast_item["description"] = event.get("description")
            webcast_item["presenter"] = event.get("presenter")
            webcast_item["status"] = event.get("status")

            if event.get("status") == "upcoming":
                webcast_item["calender_url"] = event.get("links")[2].get("href")
            else:
                webcast_item["calender_url"] = "Recorded Event"

            webcast_item["scheduled"] = event.get("scheduled")
            webcast_item["entryTime"] = event.get("entryTime")
            webcast_item["closeTime"] = event.get("closeTime")
            webcast_item["created"] = event.get("created")
            webcast_item["lastUpdated"] = event.get("lastUpdated")
            webcast_item["url"] = event.get("url")

            yield webcast_item

    def parse_summits_or_series(self, summits_or_series, event_type):
        """
        Parse the summits or series from the JSON response.
        The summits or series contain details like title and URL.

        args:
            summits_or_series: A list of summits or series from the JSON response
            event_type: The type of event (webcast, summit, or series)
        yields:
            SummitAndSeriesItem: A Scrapy Item object containing summit or series details
        """

        summits_or_series_item = SummitAndSeriesItem()

        for event in summits_or_series:
            summits_or_series_item["event_id"] = event.get("id")
            summits_or_series_item["eventType"] = event_type
            summits_or_series_item["title"] = event.get("title")
            summits_or_series_item["description"] = event.get("description")
            summits_or_series_item["scheduledStartDate"] = event.get(
                "scheduledStartDate"
            )
            summits_or_series_item["scheduledEndDate"] = event.get("scheduledEndDate")
            summits_or_series_item["url"] = event.get("wordPressLink")

            yield summits_or_series_item
