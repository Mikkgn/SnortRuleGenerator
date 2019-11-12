# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from api.test import BaseTestCase


class TestAnalyzerController(BaseTestCase):
    """AnalyzerController integration test stubs"""

    def test_start_traffic_analyzer(self):
        """Test case for start_traffic_analyzer

        Start traffic analyzer
        """
        response = self.client.open(
            '/analyzer/start',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start_traffic_analyzer_0(self):
        """Test case for start_traffic_analyzer_0

        Start traffic analyzer
        """
        response = self.client.open(
            '/analyzer/stop',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
