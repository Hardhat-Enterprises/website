#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: CHUNYI WANG
@file: get_post_urls.py
@time: 2025/4/3 10:11
@desc: A script to filter urls that support post method
@usage: python manage.py get_post_urls
@filter: jq '[.[] | select(.supports_post == true)]' url_support_method.json >> new_file_name.json
"""

import subprocess
import json
from django.urls import get_resolver, reverse, NoReverseMatch
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Test POST support for all URLs using CURL"

    def handle(self, *args, **options):
        resolver = get_resolver()
        url_names = self._get_all_urls(resolver)
        
        results = []
        for url_name in url_names:
            result = self._test_post_support(url_name)
            results.append(result)
            
            status = "POST OK" if result.get('supports_post', False) else "GET-only"
            full_url = result.get('full_url', 'Failed to resolve URL')
            self.stdout.write(f"{status}: {full_url} (Name: {url_name})")

        with open('home/tests/logs/url_support_method.json', 'w') as f:
            json.dump(results, f, indent=2)

    def _get_all_urls(self, resolver, namespace=None):
        """
        Recursive retrieval of all URL names
        """
        url_names = []
        for pattern in resolver.url_patterns:
            if str(pattern.pattern).startswith('admin/'):
                continue
                
            if hasattr(pattern, 'url_patterns'):
                new_namespace = namespace
                if pattern.namespace:
                    new_namespace = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                url_names.extend(self._get_all_urls(pattern, new_namespace))
            elif hasattr(pattern, 'name') and pattern.name:
                full_name = f"{namespace}:{pattern.name}" if namespace else pattern.name
                url_names.append(full_name)
        return url_names

    def _test_post_support(self, url_name):
        """
        Test if the URL support POST method
        """
        result = {
            'url_name': url_name,
            'full_url': None,
            'supports_post': False,
            'error': None
        }
        
        try:
            try:
                url_path = reverse(url_name)
                if not url_path.startswith('/'):
                    url_path = '/' + url_path
                result['full_url'] = f"http://localhost:8000{url_path}"
            except NoReverseMatch as e:
                result['error'] = f"Reverse parsing failed: {str(e)}"
                return result

            # send OPTIONS request
            cmd = ['curl', '-X', 'OPTIONS', '-I', '-s', result['full_url']]
            try:
                output = subprocess.check_output(cmd).decode()
                allow_header = next(
                    (line.split(':', 1)[1].strip() 
                     for line in output.splitlines() 
                     if line.startswith('Allow:')),
                    ""
                )
                result['supports_post'] = 'POST' in allow_header.upper()
                result['allowed_methods'] = allow_header
            except subprocess.CalledProcessError as e:
                result['error'] = f"Request failed: {str(e)}"

        except Exception as e:
            result['error'] = f"Unknown error: {str(e)}"

        return result