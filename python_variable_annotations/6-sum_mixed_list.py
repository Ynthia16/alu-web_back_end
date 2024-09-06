#!/usr/bin/env python3
"""
Write a type-annotated function sum_mixed_list
"""
from typing import Union, List


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Takes a list of integers and floats and returns their sum."""
    return sum(mxd_lst)
