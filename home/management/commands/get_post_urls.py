#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: CHUNYI WANG
@file: get_post_urls.py
@time: 2025/4/3 10:11
@desc: A script to filter urls that support post method
@usage: python manage.py get_post_urls
@filter: jq '[.[] | select(.supports_post == true)]' url_support_method.json > new_file_name.json
"""

import subprocess
import json
from django.urls import get_resolver, reverse, NoReverseMatch
from django.core.management.base import BaseCommand
from django.test import override_settings
from django.conf import settings

class Command(BaseCommand):
    help = "Test POST support for all URLs using CURL"

    # 关键修改1：添加装饰器临时覆盖设置
    @override_settings(
        CSRF_COOKIE_SECURE=False,
        CSRF_COOKIE_HTTPONLY=False,
        CSRF_USE_SESSIONS=False,
        MIDDLEWARE=[m for m in settings.MIDDLEWARE 
                   if m != 'django.middleware.csrf.CsrfViewMiddleware']
    )
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
        """保持不变"""
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

    # 关键修改2：在请求中添加CSRF豁免头
    def _test_post_support(self, url_name):
        result = {
            'url_name': url_name,
            'full_url': None,
            'supports_post': False,
            'error': None
        }
        
        try:
            url_path = reverse(url_name)
            result['full_url'] = f"http://localhost:8000{url_path}"
            
            # 尝试发送真实POST请求（带豁免头）
            cmd = [
                'curl', '-X', 'POST',
                '-H', 'X-CSRFToken: exempt',
                '-H', 'Content-Type: application/json',
                '-d', '{}',  # 空JSON数据
                '-s', '-o', '/dev/null', '-w', '%{http_code}',
                result['full_url']
            ]
            
            try:
                # 获取HTTP状态码
                status_code = int(subprocess.check_output(cmd).decode())
                # 2xx/3xx状态码视为支持POST
                result['supports_post'] = 200 <= status_code < 400
                result['status_code'] = status_code
            except subprocess.CalledProcessError as e:
                result['error'] = f"POST failed: {str(e)}"
        
        except Exception as e:
            result['error'] = str(e)
        
        return result