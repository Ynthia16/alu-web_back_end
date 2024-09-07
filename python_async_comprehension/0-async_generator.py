#!/usr/bin/env python3
"""generate a list of random numbers using an async generator"""


import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:  # type: ignore
    """generate random list of numbers"""
    for i in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
