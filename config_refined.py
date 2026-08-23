# -*- coding: utf-8 -*-
"""Strict data contract for validated ORDER-HUB packets."""

from typing import List

from pydantic import BaseModel, Field, field_validator


class RefinedOrderPacket(BaseModel):
    client_id: str = Field(..., description="Unique client partition identifier")
    sku_list: List[str] = Field(..., min_length=1, description="Validated SKU identifiers")
    total_weight: float = Field(..., description="Consolidated cargo weight in kilograms")
    dispatch_priority: int = Field(default=3, ge=1, le=5, description="Routing priority [1-5]")

    @field_validator("client_id")
    @classmethod
    def validate_client_id(cls, value: str) -> str:
        prefixes = ("XC_", "SH_", "BJ_")
        if not value.startswith(prefixes):
            raise ValueError(f"client_id must start with one of: {', '.join(prefixes)}")
        return value

    @field_validator("total_weight")
    @classmethod
    def validate_weight(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("total_weight must be positive")
        return value
