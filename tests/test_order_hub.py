import pytest
from pydantic import ValidationError

from config_refined import RefinedOrderPacket
from main import ThreadPoolScheduler


def test_valid_packet_commits_and_can_be_read_back():
    scheduler = ThreadPoolScheduler()
    packet = RefinedOrderPacket(
        client_id="XC_TEST_CLIENT",
        sku_list=["SKU-001", "SKU-002"],
        total_weight=10.5,
        dispatch_priority=2,
    )

    tx_id = scheduler.execute_ingest(packet)
    saved = scheduler.get_transaction(tx_id)

    assert tx_id.startswith("TX_SECURE_")
    assert saved is not None
    assert saved["client_id"] == "XC_TEST_CLIENT"
    assert saved["total_weight"] == 10.5


def test_invalid_client_prefix_is_rejected():
    with pytest.raises(ValidationError):
        RefinedOrderPacket(
            client_id="INVALID_CLIENT",
            sku_list=["SKU-001"],
            total_weight=1.0,
        )


def test_non_positive_weight_is_rejected():
    with pytest.raises(ValidationError):
        RefinedOrderPacket(
            client_id="XC_TEST_CLIENT",
            sku_list=["SKU-001"],
            total_weight=0,
        )


def test_empty_sku_list_is_rejected():
    with pytest.raises(ValidationError):
        RefinedOrderPacket(
            client_id="XC_TEST_CLIENT",
            sku_list=[],
            total_weight=1.0,
        )
