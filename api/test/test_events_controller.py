# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from api.models.event import Event  # noqa: E501
from api.test import BaseTestCase


class TestEventsController(BaseTestCase):
    """EventsController integration test stubs"""

    def test_get_events(self):
        """Test case for get_events

        Get events
        """
        query_string = [('offset', 56),
                        ('limit', 56)]
        response = self.client.open(
            '/events',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
