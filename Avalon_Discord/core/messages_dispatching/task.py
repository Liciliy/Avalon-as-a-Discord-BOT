
class ContentType:
    FILE  = 0
    EMBED = 1
    TEXT  = 2
    REACTIONS = 4

    STR_REPR = {
        FILE      : 'FILE',
        EMBED     : 'EMBED',
        TEXT      : 'TEXT',
        REACTIONS : 'REACTIONS',
    }


class MsgActType:
    SEND = 0
    EDIT = 1
    DEL  = 2
    ADD_REACT = 3
    DEL_REACT = 4
    DEL_OWN_REACT = 5
    DEL_ALL_REACT = 6

    STR_REPR = {
        SEND          : 'SEND_MSG',
        EDIT          : 'EDIT_MSG',
        DEL           : 'DEL_MSG',
        ADD_REACT     : 'ADD_REACT',
        DEL_REACT     : 'DEL_REACT',
        DEL_OWN_REACT : 'DEL_OWN_REACT',
        DEL_ALL_REACT : 'DEL_ALL_REACT',
    }


class Task:
    type          = None
    content       = None
    content_type  = None
    message_id    = None
    channel_id    = None
    member_id     = None
    edit_in_queue = None

    def __init__(self, 
                type, 
                content       = None, 
                content_type  = None,
                channel_id    = None,
                message_id    = None,
                member_id     = None,
                edit_in_queue = False):
 
        self.type          = type
        self.content       = content
        self.content_type  = content_type
        self.message_id    = message_id
        self.channel_id    = channel_id
        self.member_id     = member_id
        self.edit_in_queue = edit_in_queue

    def __str__(self):
        result = 'Task as a string:'

        result += ('\nTask type is: '         + MsgActType.STR_REPR[self.type] )
        result += ('\nTask content is: '      + str(self.content) )
        result += ('\nTask content_type is: ' + ContentType.STR_REPR[self.content_type] )
        result += ('\nTask message_id is: '   + str(self.message_id) )
        result += ('\nTask channel_id is: '   + str(self.channel_id) )
        result += ('\nTask member_id is: '    + str(self.member_id) )
        result += ('\nTask in_queue is: '     + str(self.edit_in_queue) )

        return result
