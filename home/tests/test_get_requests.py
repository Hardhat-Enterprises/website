#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: CHUNYI WANG
@file: test_get_requests.py
@time: 2025/3/25 15:21
@desc: This code automatically discovers and tests all URLs that use the GET method
"""

import logging
from django.test import TestCase
from django.urls import get_resolver
from django.shortcuts import resolve_url
from home.tests.setup_test_logger import setup_test_logger


class GetUrlAutoDiscoverTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Instantiate logger
        cls.logger = setup_test_logger()

        # Add test start information
        cls.logger.info("Starting URL auto-discovery tests")
        cls.logger.info("=" * 50)
