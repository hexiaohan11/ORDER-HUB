# -*- coding: utf-8 -*-
"""ORDER-HUB thread-safe transaction dispatcher."""

import threading
import time
import sys
from typing import Dict

from config_refined import RefinedOrderPacket


def log_terminal(level: str, module: str, message: str) -> None:
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} [{level}] [{module}] {message}")
    sys.stdout.flush()


class ThreadPoolScheduler:
    def __init__(self) -> None:
        self._global_lock = threading.Lock()
        self._partition_locks: Dict[str, threading.Lock] = {}
        self._database_store: Dict[str, dict] = {}

    def get_partition_lock(self, client_id: str) -> threading.Lock:
        if client_id not in self._partition_locks:
            with self._global_lock:
                if client_id not in self._partition_locks:
                    self._partition_locks[client_id] = threading.Lock()
        return self._partition_locks[client_id]

    def execute_ingest(self, packet: RefinedOrderPacket) -> str:
        lock = self.get_partition_lock(packet.client_id)
        with lock:
            time.sleep(0.05)
            tx_id = f"TX_SECURE_{time.time_ns()}"
            self._database_store[tx_id] = packet.model_dump()
            log_terminal("INFO", "TX", f"Transaction committed. ID: {tx_id}")
        return tx_id

    def get_transaction(self, tx_id: str) -> dict | None:
        return self._database_store.get(tx_id)


if __name__ == "__main__":
    scheduler = ThreadPoolScheduler()
    packet = RefinedOrderPacket(
        client_id="XC_DEMO_CLIENT_2026",
        sku_list=["SKU-001"],
        total_weight=142.5,
    )
    scheduler.execute_ingest(packet)
