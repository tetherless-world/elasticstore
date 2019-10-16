"""
SPARQL implementation for RDFLib

.. versionadded:: 4.0
"""


SPARQL_LOAD_GRAPHS = True
"""
If True, using FROM <uri> and FROM NAMED <uri>
will load/parse more data
"""


SPARQL_DEFAULT_GRAPH_UNION = True
"""
If True - the default graph in the RDF Dataset is the union of all
named graphs (like RDFLib's ConjunctiveGraph)
"""


CUSTOM_EVALS = {}
"""
Custom evaluation functions

These must be functions taking (ctx, part) and raise
NotImplementedError if they cannot handle a certain part
"""


PLUGIN_ENTRY_POINT = 'rdf.plugins.sparqleval'

from . import parser
from . import operators
from . import parserutils

from .processor import prepareQuery, processUpdate

assert parser
assert operators
assert parserutils

try:
    from pkg_resources import iter_entry_points
except ImportError:
    pass  # TODO: log a message
else:
    for ep in iter_entry_points(PLUGIN_ENTRY_POINT):
        CUSTOM_EVALS[ep.name] = ep.load()


def registerplugins():
    """
    Register plugins.
    If setuptools is used to install rdflib-elasticstore, all the provided
    plugins are registered through entry_points. This is strongly recommended.
    However, if only distutils is available, then the plugins must be
    registed manually.
    This method will register the rdflib-elasticstore Store plugin.
    Adapted from rdflib-sqlalchemy on github:
    https://github.com/RDFLib/rdflib-sqlalchemy/blob/develop/rdflib_sqlalchemy/__init__.py
    """
    from rdflib.store import Store
    from rdflib import plugin
    
    try:
        plugin.get("Elasticsearch", Store)
    except plugin.PluginException:
        pass
    
    # Register the plugins ...
    plugin.register(
        "Elasticsearch",
        Store,
        "rdflib_elasticstore.elasticstore",
        "ElasticSearchStore",
    )
