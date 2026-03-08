import asyncio
import logging
import sys
from pathlib import Path

from temporalio.client import Client
from temporalio.worker import Worker

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import TEMPORAL_HOST, DOCKER_MONITOR_TASK_QUEUE

from docker_monitor.docker_temporal_agent import (
    DockerMonitorWorkflow,
    ai_orchestrator_activity,
    get_container_status_activity,
    get_container_logs_activity,
    restart_container_activity,
    start_container_activity,
    stop_container_activity,
    list_containers_activity,
    container_stats_activity,
    inspect_container_activity,
)

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
        activities=[
            ai_orchestrator_activity,

            # container info
            list_containers_activity,
            get_container_status_activity,
            inspect_container_activity,

            # logs
            get_container_logs_activity,

            # lifecycle control
            restart_container_activity,
            start_container_activity,
            stop_container_activity,

            # monitoring
            container_stats_activity,
        ],
    )

    logger.info("Docker AI monitor worker started...")

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
