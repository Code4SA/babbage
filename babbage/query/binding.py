class Binding(object):
    def __init__(self, table, column, fact_table, fact_table_column):
        self.table = table
        self.column = column
        self.fact_table = fact_table
        self.fact_table_column = fact_table_column
