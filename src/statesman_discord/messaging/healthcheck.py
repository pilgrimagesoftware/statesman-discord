__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Messaging
"""

import logging, os, time
import pika, pika.exceptions
from threading import Thread
from statesman_discord import constants
from statesman_discord.messaging import params

last_health_status = {
    "ping": {"status": "Unknown", "sent": None, "received": None},
    "rabbitmq": {
        "host": os.environ[constants.RABBITMQ_HOST],
        "port": os.environ[constants.RABBITMQ_PORT],
        "vhost": os.environ[constants.RABBITMQ_VHOST],
        "user": os.environ[constants.RABBITMQ_USER],
        "exchange": os.environ[constants.RABBITMQ_EXCHANGE],
        "queue": os.environ[constants.RABBITMQ_QUEUE],
    },
}


def health_check() -> dict:
    logging.info("Checking health of RabbitMQ...")

    last_health_status["ping"]["sent"] = str(time.time())

    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    # channel.confirm_delivery()
    try:
        ping = "ping"
        channel.basic_publish(
            exchange=os.environ[constants.RABBITMQ_EXCHANGE],
            routing_key=os.environ[constants.RABBITMQ_QUEUE],
            body=ping,
            properties=pika.BasicProperties(content_type="text/plain", delivery_mode=pika.DeliveryMode.Transient),
            mandatory=False,
        )
    except pika.exceptions.UnroutableError as e:
        logging.exception("Health check message was returned:", e)
        last_health_status["ping"]["status"] = "returned"
    except Exception as e:
        logging.exception("Exception while attempting to publish health check message:", e)
    finally:
        channel.close()

    return last_health_status


class HealthCheckConsumer(Thread):
    """_summary_

    Args:
        Thread (_type_): _description_
    """

    def message_callback(self, ch, method, properties, body):
        """_summary_

        Args:
            ch (_type_): _description_
            method (_type_): _description_
            properties (_type_): _description_
            body (_type_): _description_
        """
        logging.info("ch: %s, method: %s, properties: %s, body: %s", ch, method, properties, body)

        if body == "ping":
            logging.info("Got 'ping' check.")
            last_health_status["ping"]["received"] = str(time.time())
            last_health_status["ping"]["status"] = "healthy"
        else:
            logging.warning("Got unknown message; ignoring.")
            ch.un

    def run(self):
        logging.info("RabbitMQ health check thread started.")
        while True:
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            try:
                channel.basic_consume(queue=os.environ[constants.RABBITMQ_QUEUE], on_message_callback=self.message_callback, auto_ack=True)
                channel.start_consuming()
            except Exception as e:
                logging.exception("Exception while attempting to consume health check message:", e)
            finally:
                channel.close()


health_check_thread = HealthCheckConsumer()
health_check_thread.setDaemon(True)
health_check_thread.start()
