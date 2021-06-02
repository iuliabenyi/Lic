from flask_table import Table, Col
class messagesTable(Table):
    id = Col('Id', show=False)
    nameTherapist = Col('Therapist Name')
    message = Col('Message')
