from dataclasses import asdict
from typing import Any

import orjson

from domain.common.events.event import Event


def convert_event_to_broker_message(event: Event, **kwargs) -> bytes:
    if kwargs: 
        for k, v in kwargs.items():
            event.__setattr__(k, v)
    return orjson.dumps(event, default=str)


def convert_event_to_json(event: Event) -> dict[str, Any]:
    return asdict(event)
