import unittest

try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

import six

from rdflib import (
    ConjunctiveGraph,
    Literal,
    URIRef,
    plugin
)
from rdflib.store import Store

import requests

from rdflib_elasticstore import registerplugins


michel = URIRef(u"michel")
likes = URIRef(u"likes")
pizza = URIRef(u"pizza")
ctx_id = URIRef('http://example.org/context')


class mock_cursor():
    def execute(x):
        raise Exception("Forced exception")


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.store = plugin.get("Elasticsearch", Store)()
        self.graph = ConjunctiveGraph(self.store)

    def tearDown(self):
        self.graph.close()

    def test_success(self):
        with patch.object(requests.Session,'get') as p:
            self.graph.open('http://localhost:9200/collection', create=True)
            p.assert_called_with('http://localhost:9200/collection')


class ElasticTestCase(unittest.TestCase):
    identifier = URIRef("rdflib_test")
    dburi = Literal("http://localhost:9200/collection")

    def setUp(self):
        self.store = plugin.get(
            "Elasticsearch", Store)(identifier=self.identifier, configuration=self.dburi)
        self.graph = ConjunctiveGraph(self.store, identifier=self.identifier)
        self.graph.open(self.dburi, create=True)

    def tearDown(self):
        self.graph.destroy(self.dburi)
        self.graph.close()

    def test_registerplugins(self):
        # I doubt this is quite right for a fresh pip installation,
        # this test is mainly here to fill a coverage gap.
        registerplugins()
        self.assertIsNotNone(plugin.get("Elasticsearch", Store))
        p = plugin._plugins
        self.assertIn(("Elasticsearch", Store), p)
        del p[("Elasticsearch", Store)]
        plugin._plugins = p
        registerplugins()
        self.assertIn(("Elasticsearch", Store), p)

    def test_namespaces(self):
        self.assertNotEqual(list(self.graph.namespaces()), [])

    def test_contexts_without_triple(self):
        self.assertEqual(list(self.graph.contexts()), [])

    def test_contexts_result(self):
        g = self.graph.get_context(ctx_id)
        g.add((michel, likes, pizza))
        actual = list(self.store.contexts())
        self.assertEqual(actual[0], ctx_id)

    def test_contexts_with_triple(self):
        statemnt = (michel, likes, pizza)
        self.assertEqual(list(self.graph.contexts(triple=statemnt)), [])

    def test__len(self):
        self.assertEqual(self.store.__len__(), 0)

    def test_triples_choices(self):
        # Set this so we're not including selects for both asserted and literal tables for
        # a choice
        self.store.STRONGLY_TYPED_TERMS = True
        # Set the grouping of terms
        self.store.max_terms_per_where = 2

        results = [((michel, likes, pizza), ctx_id)]
        
        # force execution of the generator
        for x in self.store.triples_choices((None, likes, [michel, pizza, likes])):
            print("x="+str(x))
            print("results="+str(results))
            assert x in results

            
if __name__ == "__main__":
    unittest.main()
