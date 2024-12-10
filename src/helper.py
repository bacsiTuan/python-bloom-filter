#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math


def get_size(n, p):
    """
    Return the size of bit array(m) to used using
    following formula
    m = -(n * lg(p)) / (lg(2)^2)
    n : int
        number of items expected to be stored in filter
    p : float
        False Positive probability in decimal
    """
    m = -(n * math.log(p)) / (math.log(2) ** 2)
    return int(m)


def get_hash_count(m, n):
    """
    Return the hash function(k) to be used with following formula
    k = (m/n) * lg(2)

    m : int
        size of bit array
    n : int
        number of items expected to be stored in filter
    """
    k = (m / n) * math.log(2)
    return int(k)
