"""
@author: CHUNYI WANG
@file: test_get_requests.py
@time: 2025/3/25 15:21
@desc: This code automatically discovers and tests all URLs that use the GET method
@usage: python manage.py test home.tests.test_get_requests
"""

from django.test import TestCase
from django.urls import get_resolver, reverse, NoReverseMatch
from django.shortcuts import resolve_url
from home.tests.setup_test_logger import setup_test_logger


class GetUrlAutoDiscoverTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Instantiate logger
        cls.logger = setup_test_logger('auto_discover_test_GET.log')

        # Add test start information
        cls.logger.info("Starting URL auto-discovery tests")
        cls.logger.info("HTTP method: GET")
        cls.logger.info("=" * 50)


    def _url_requires_args(self, url_name: str):
        """
        Check if any argument is required for <url_name>
        """
        try:
            reverse(url_name)
            return False
        except NoReverseMatch:
            return True

    def test_get_requests(self):
        resolver = get_resolver()

        # Get all url names
        url_names = self._get_all_url_names(resolver)
        # for u in url_names:
        #     print(u)

        # Excluded url list
        exclude_urls = ['admin']
        test_urls = [
            name for name in url_names
            if not any(name.startswith(ex_url) for ex_url in exclude_urls)
        ]

        self.logger.info(f"Found {len(test_urls)} URLs to test")

        # test result statistics
        test_results = {
            'total': len(test_urls),
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
        }

        for url_name in test_urls:
            with self.subTest(url_name=url_name):
                try:
                    if self._url_requires_args(url_name):
                        self.logger.warning(f"SKIP: {url_name} - Arguments required")
                        test_results['skipped'] += 1
                        continue

                    # url = reversed(url_name)
                    response = self.client.get(resolve_url(url_name))

                    if response.status_code in [200, 302]:
                        self.logger.info(f"PASS: {url_name} - Status {response.status_code}")
                        test_results['passed'] += 1
                    else:
                        self.logger.warning(
                            f"FAIL: {url_name} - Unexpected status {response.status_code}"
                        )
                        test_results['failed'] += 1

                except Exception as e:
                    self.logger.error(
                        f"ERROR: {url_name} - {str(e)}",
                        exc_info=True
                    )
                    test_results['errors'] += 1

        # Output test summary
        self._output_test_summary(test_results)

    def _get_all_url_names(self, resolver, namespace=None):
        """
        Recursive retrieval of all URL names
        """
        url_names = []
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                new_namespace = namespace
                if pattern.namespace:
                    new_namespace = f"{namespace}:{pattern.namespace}" if namespace else pattern.namespace
                url_names.extend(self._get_all_url_names(pattern, new_namespace))
            elif hasattr(pattern, 'name') and pattern.name:
                full_name = f"{namespace}:{pattern.name}" if namespace else pattern.name
                # print(full_name)
                url_names.append(full_name)
        return url_names

    def _output_test_summary(self, results):
        """
        Output test summary to log file
        """
        self.logger.info("=" * 50)
        self.logger.info("TEST SUMMARY")
        self.logger.info("=" * 50)
        self.logger.info(f"Total URLs tested: {results['total']}")
        self.logger.info(f"Passed: {results['passed']} ({(results['passed'] / results['total']) * 100:.1f}%)")
        self.logger.info(f"Failed: {results['failed']} ({(results['failed'] / results['total']) * 100:.1f}%)")
        self.logger.info(f"Errors: {results['errors']} ({(results['errors'] / results['total']) * 100:.1f}%)")
        self.logger.info(f"Skipped: {results['skipped']} ({(results['skipped'] / results['total']) * 100:.1f}%)")
        self.logger.info("=" * 50)
