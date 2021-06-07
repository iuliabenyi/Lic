from flask_table import Table, Col
class messagesTable(Table):
    id = Col('Id', show=False)
    nameSender = Col('Therapist Name')
    message = Col('Message')
