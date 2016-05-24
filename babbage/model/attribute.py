from babbage.model.concept import Concept


class Attribute(Concept):
    """ An attribute describes some concrete value stored in the data model.
    This value can either be stored directly on the facts table as a column,
    or introduced via a join. """

    def __init__(self, dimension, name, spec):
        super(Attribute, self).__init__(dimension.model, name, spec, '%s.%s' % (dimension.hierarchy, name))
        self.dimension = dimension

    @property
    def ref(self):
        return '%s.%s' % (self.dimension.name, self.name)

    @property
    def datatype(self):
        return self.spec.get('type')

    @property
    def column_name(self):
        #        import pdb; pdb.set_trace()
        if self.dimension.join_column_name and self == self.dimension.key_attribute:
            return self.dimension.join_column_name
        else:
            return self._column_name

    @column_name.setter
    def column_name(self, val):
        self._column_name = val

    def __repr__(self):
        return "<Attribute(%s)>" % self.ref

    def to_dict(self):
        data = self.spec.copy()
        data['ref'] = self.ref
        return data
