import asyncio
import logging
import sys
from pathlib import Path

from temporalio.client import Client
from temporalio.worker import Worker

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import TEMPORAL_HOST, DOCKER_MONITOR_TASK_QUEUE

# Import workflow
from docker_monitor.docker_temporal_agent import DockerMonitorWorkflow

# Import activities
from docker_monitor.docker_temporal_agent import ai_orchestrator_activity

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


async def main():

    logger.info("Connecting to Temporal server...")

    client = await Client.connect(TEMPORAL_HOST)

    logger.info("Connected to Temporal")

    worker = Worker(
        client,
        task_queue=DOCKER_MONITOR_TASK_QUEUE,
        workflows=[DockerMonitorWorkflow],
        activities=[ai_orchestrator_activity],  
    )

    logger.info("Docker monitor worker started...")

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
