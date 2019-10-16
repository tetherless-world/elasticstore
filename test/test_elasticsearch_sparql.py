import logging
import os
import unittest

from rdflib import Literal

from . import context_case
from . import graph_case

from nose import SkipTest

_logger = logging.getLogger(__name__)

elasticsearch_url = Literal(os.environ.get("DBURI", "http://localhost:9200/collection"))


class ElasticstoreGraphTestCase(graph_case.GraphTestCase):
    storetest = True
    storename = "Elasticsearch"
    uri = elasticsearch_url

    def setUp(self):
        super(ElasticstoreGraphTestCase, self).setUp(
            uri=self.uri, storename=self.storename)

    def tearDown(self):
        super(ElasticstoreGraphTestCase, self).tearDown(uri=self.uri)


class ElasticstoreContextTestCase(context_case.ContextTestCase):
    storetest = True
    storename = "Elasticsearch"
    uri = elasticsearch_url

    def setUp(self):
        super(ElasticstoreContextTestCase, self).setUp(
            uri=self.uri, storename=self.storename)

    def tearDown(self):
        super(ElasticstoreContextTestCase, self).tearDown(uri=self.uri)

    def testLenInMultipleContexts(self):
        raise SkipTest("Known issue.")


if __name__ == "__main__":
    unittest.main()
