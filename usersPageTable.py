from flask_table import Table, Col
class usersPageTable(Table):
    id = Col('Id', show=False)
    userId = Col('UserName')
    userTags = Col('UserTags')
    mainTag = Col('Main Tag')
