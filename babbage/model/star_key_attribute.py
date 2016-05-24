from babbage.model.attribute import Attribute


class StarKeyAttr(Attribute):
    def __init__(self, attr):
        self.attr = attr

    def bind_star_column(self, cube):
        """
        Normally when binding a key attribute of a dimension with a dedicated
        dimension table you want the join_column in the fact table
        to be used as it might avoid unnecessarily joining to the dimension
        table. When you know you really want to bind the dimension table,
        this bind function can be used instead.
        """
        table, column = self.attr._physical_column(cube, self.attr._column_name)
        column = column.label(self.attr.matched_ref)
        column.quote = True
        return table, column
