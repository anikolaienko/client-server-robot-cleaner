from typing import Callable, Awaitable

from aiokafka import AIOKafkaConsumer
import asyncio

from server.models import ExecutionResult, ExecutionStatus

RECONNECT_INTERVAL = 5  # seconds
KAFKA_URL = "localhost:9094"
KAFKA_TOPICS = ["commands"]


async def try_connect() -> AIOKafkaConsumer:
    while True:
        try:
            consumer = AIOKafkaConsumer(
                *KAFKA_TOPICS,
                bootstrap_servers=KAFKA_URL
            )
            
            return consumer.start()
        except Exception as ex:
            print(f"Failed to connect to Kafka. Trying again in {RECONNECT_INTERVAL} seconds.")
            await asyncio.sleep(RECONNECT_INTERVAL)


async def start_receiving(execute_command: Callable[[str, dict[str, str]], Awaitable[ExecutionResult]]):
    while True:
        try:
            consumer = AIOKafkaConsumer(
                *KAFKA_TOPICS,
                bootstrap_servers=KAFKA_URL
            )
            await consumer.start()

            # Consume messages
            print("connected to Kafka successfully. Listening to queue...")
            async for msg in consumer:
                print(f"received: {msg.value}")

                msg_body_bytes: bytes = msg.value
                msg_body = msg_body_bytes.decode()

                args = msg_body.split()
                if not args:
                    continue

                command = args[0]
                data = {k: v for k, v in zip(args[1::2], args[2::2])}

                print(f"sending command `{command}` with data: `{data}`")

                result = await execute_command(command, data)  # send message to robot
                if result.status == ExecutionStatus.SUCCESS:
                    print(f"successfully sent command `{command}` with data `{data}`")
                else:
                    print(f"failed command `{command}` with data `{data}`\nError: {result.error}")
        except Exception as ex:
            print(f"Failed to connect to Kafka.\nError:\n{ex}\nTrying again in {RECONNECT_INTERVAL} seconds.")
            await asyncio.sleep(RECONNECT_INTERVAL)


async def send_error() -> None:
    ...
    # TODO: Implement post to Kafka error_log topic
