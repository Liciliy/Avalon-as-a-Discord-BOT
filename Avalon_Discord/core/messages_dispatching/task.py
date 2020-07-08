
class ContentType:
    FILE  = 0
    EMBED = 1
    TEXT  = 2

class MsgActType:
    SEND = 0
    EDIT = 1
    DEL  = 2

class Task:
    type         = None
    content      = None
    content_type = None
    message_id   = None
    channel_id   = None

    def __init__(self, 
                type, 
                content      = None, 
                content_type = None,
                channel_id   = None,
                message_id   = None):

        self.type         = type
        self.content      = content
        self.content_type = content_type
        self.message_id   = message_id
        self.channel_id   = channel_id

    def __str__(self):
        result = 'Task as a string:'

        result += ('\nTask type is: '         + str(self.type) )
        result += ('\nTask content is: '      + str(self.content) )
        result += ('\nTask content_type is: ' + str(self.content_type) )
        result += ('\nTask message_id is: '   + str(self.message_id) )
        result += ('\nTask channel_id is: '   + str(self.channel_id) )

        return result
