import motor.motor_asyncio
import os

# database logging
import logging
import pymongo

logger = logging.getLogger(__name__)


class _MongoLogger(pymongo.monitoring.ServerListener):
    def opened(self, event):
        logger.info(
            "Server {0.server_address} added to topology "
            "{0.topology_id}".format(event)
        )

    def description_changed(self, event):
        previous_server_type = event.previous_description.server_type
        new_server_type = event.new_description.server_type
        if new_server_type != previous_server_type:
            # server_type_name was added in PyMongo 3.4
            logger.info(
                "Server {0.server_address} changed type from "
                "{0.previous_description.server_type_name} to "
                "{0.new_description.server_type_name}".format(event)
            )

    def closed(self, event):
        logger.warning(
            "Server {0.server_address} removed from topology "
            "{0.topology_id}".format(event)
        )


# helper function
async def unravell_cursor(cursor: motor.motor_asyncio.AsyncIOMotorCursor):
    result = []
    async for i in cursor:
        result.append(i)
    return result


# register listener
pymongo.monitoring.register(_MongoLogger())

# todo: easy configuration
client = motor.motor_asyncio.AsyncIOMotorClient(
    os.environ.get("MONGO_SRV", "mongodb://localhost:27017")
)
database = client.dev
