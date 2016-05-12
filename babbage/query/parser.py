import os
import json

import grako
import six
import dateutil.parser
from grako.exceptions import GrakoException

from babbage.exc import QueryException, BindingException
from babbage.util import SCHEMA_PATH


with open(os.path.join(SCHEMA_PATH, 'parser.ebnf'), 'rb') as fh:
    grammar = fh.read().decode('utf8')
    model = grako.genmodel("all", grammar)


class Parser(object):
    """ Type casting for the basic primitives of the parser, e.g. strings,
    ints and dates. """

    def __init__(self, cube):
        self.results = []
        self.cube = cube
        self.tables = []

    def string_value(self, ast):
        text = ast[0]
        if text.startswith('"') and text.endswith('"'):
            return json.loads(text)
        return text

    def string_set(self, ast):
        return map(self.string_value, ast)

    def int_value(self, ast):
        return int(ast)

    def int_set(self, ast):
        return map(self.int_value, ast)

    def date_value(self, ast):
        return dateutil.parser.parse(ast).date()

    def date_set(self, ast):
        return map(self.date_value, ast)

    def parse(self, text):
        if isinstance(text, six.string_types):
            try:
                model.parse(text, start=self.start, semantics=self)
                return self.results
            except GrakoException as ge:
                raise QueryException(ge.message)
        elif text is None:
            text = []
        return text

    def ensure_table(self, q, table):
        if table not in q.froms:
            q = q.select_from(table)
        return q

    def ensure_table2(self, q, ref_table, ref):
        self.tables.append((ref_table, ref))
        return q

    def bind_tables(self, q):
        if len(self.tables) == 1:
            return q.select_from(self.tables[0][0])
        else:
            q = q.select_from(self.cube.fact_table)
        for (ref_table, ref) in self.tables:
            print("table=%r ref=%r" % (ref_table, ref))
            if ref_table not in q.froms:
                concept = self.cube.model[ref]
                print("contept=%r" % concept)
                dimension = concept.dimension  # assume it's an attribute
                print("dimension=%r key_attribute=%r" % (dimension, dimension.key_attribute))
                dimension_table, key_column = dimension.key_attribute.bind(self.cube)
                if ref_table != dimension_table:
                    raise BindingException('Attributes must be of same table as '
                                           'as their dimension key')
                join_column = self.cube.fact_table.columns[dimension.join_column_name]
                j = self.cube.fact_table.join(dimension_table,
                                              join_column == key_column,
                                              isouter=True),
                q = q.select_from(j)
        return q

    @staticmethod
    def allrefs(*args):
        return [ref for concept_list in args for concept in concept_list for ref in concept.refs]
