from flask_table import Table, Col
class usersTable(Table):
    classes = ['table', 'table-bordered', 'table-striped', 'table-hover', 'clickable-row']
    id = Col('Id', show=False)
    name = Col('Name')
    email = Col('Email')
