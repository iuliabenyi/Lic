from flask_table import Table, Col
class usersTable(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    email = Col('Email')
    mainTag = Col('Main Tag')
