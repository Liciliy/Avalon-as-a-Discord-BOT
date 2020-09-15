import logging

class ChatHandler:
    _game                = None
    _messages_blocks     = None
    _chat_without_header = None

    MAX_CHAT_LENGHT     = 2000
    USER_MAX_NICK_LEN   = 33
    CHAT_HEADER_CONTENT = '📨 **CHAT** '

    header_size      = len(CHAT_HEADER_CONTENT)
    content_max_size = MAX_CHAT_LENGHT - (header_size + USER_MAX_NICK_LEN)

    def _get_header(self, nickname):
        return self.CHAT_HEADER_CONTENT + nickname

    def __init__(self, game):
        self._game                = game
        self._messages_blocks     = list()
        self._chat_without_header = ''

    def get_chat_str(self, player_name):
        result = self._get_header(player_name) + self._chat_without_header

        return result

    async def handle_new_player_message(self, msg):

        
        if len(self._messages_blocks) == 0:
            self._messages_blocks.append(MessageBlock(msg))
        else:
            last_msg_block = self._messages_blocks[-1]

            new_msg_block = MessageBlock(msg)
            if last_msg_block.is_same_author(msg):
                last_msg_block.append(msg)
            else: 
                self._messages_blocks.append(new_msg_block)
            
            free_space = self.content_max_size - self.msg_blocks_size
          
           
            logging.debug('Free space before shrink: ' + str( free_space))
            
            if free_space < 0:
                space_to_release = (-1) * free_space
                
                pos = 0
                for pos in range(0, len(self._messages_blocks)):
                    logging.debug('pos is: ' + str(pos))
                    block = self._messages_blocks[pos]

                    if block.shrink(space_to_release): 
                        logging.debug('Successful shrink.')                       
                        break
                    else:
                        logging.debug('Removing whole block.') 
                        pos += 1
                        space_to_release -= block.size
                        if space_to_release <= 0:
                            break


                logging.debug('Cutting msges from ' + str(pos) + ' to end')

                self._messages_blocks = self._messages_blocks[pos:] 
        self._chat_without_header = ''

        for block in self._messages_blocks:
            self._chat_without_header += str(block)

        logging.debug('Free space after shrink: ' + str( self.content_max_size - self.msg_blocks_size))


        logging.debug('Chat size: ' + str(self.msg_blocks_size + self.header_size + self.USER_MAX_NICK_LEN))
       
        await msg.delete()
 
    @property
    def msg_blocks_size(self):
        result = 0

        for block in self._messages_blocks:
            result += block.size

        return result 
  

class MessageBlock:
    _author_nick   = None
    _messages_list = None 
    _author_id     = None

    # TODO add message lenght limit, mb in higher execution layers
    def __init__(self, msg):
        self._author_nick   = '\n**`' + msg.author.name + '`**'
        self._author_id     = msg.author.id
        self._messages_list = ['\n' + str(msg.content)]

    def shrink(self, needed_size):
        """Tries to decrease message size by provided amount of characters.

        Arguments:
            needed_size {[int]} -- number of characters needed to becone free.

        Returns:
            True if shrik was successful; False if its impossible to shrink 
            without removal of all messages.
        """
        result = False

        if self.messages_size <= needed_size: return result

        released_characters = 0     
        number_of_messages = len(self._messages_list)  

        for pos in range(0, number_of_messages):

            released_characters += len(self._messages_list[pos])

            if released_characters >= needed_size and pos != number_of_messages-1:
                result = True
                self._messages_list =\
                     self._messages_list[pos + 1 :]
                break

        return result

    # TODO add message lenght limit, mb in higher execution layers
    def append(self, new_msg):
        result = 0
        if self._author_id == new_msg.author.id:
            
            content = '\n' + new_msg.content    
            self._messages_list.append(content)
            result = len (content)
        else:
            logging.error('Cant extend a chat message with discord' +
                          ' message having different author ID.')
        return result
    
    def __str__(self):
        result = ''
        result += self._author_nick
        result += ''.join(self._messages_list)

        return result

    def is_same_author(self, new_msg):
        return new_msg.author.id == self._author_id

    @property
    def messages_size(self):
        result = 0
        for msg in self._messages_list:
            result += len(msg)

        return result

    @property
    def size(self):
        result = self.messages_size
        result += len(self._author_nick)

        return result