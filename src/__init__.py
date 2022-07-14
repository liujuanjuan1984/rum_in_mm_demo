import datetime
import logging

now = datetime.datetime.now()

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(
    format="%(name)s %(asctime)s %(levelname)s %(message)s",
    filename=f"rss_{datetime.date.today()}_{now.hour}_{now.minute}.log",
    level=logging.INFO,
)
