class EditMsgTask:
    channel_id = None
    message_id = None
    fields     = None

    def __init__(self, ch_id, msg_id, fields):
        self.channel_id = ch_id
        self.message_id = msg_id
        self.fields     = fields