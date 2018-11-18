import logging, datetime

class Logger:

    def __init__(self, name, level = logging.INFO, stream = ['file', 'console']):
        self.name = name
        self.level = level
        self.stream = stream
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.__handler_attached__ = False
        self.__setup_file_handler__()
    
    def __setup_file_handler__(self, stream = None):
        stream = self.stream if stream == None else stream
        if 'file' in stream:
            if self.__handler_attached__ == False:
                handler = logging.FileHandler(self.name + '-' + datetime.datetime.today().strftime('%Y-%m-%d') + '.log')
                handler.setLevel(self.level)
                handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
                self.logger.addHandler(handler)
                self.__handler_attached__ = True
            return True
        else:
            return False

    def write(self, message, level = None, stream = None):
        stream = self.stream if stream == None else stream
        level = self.level if level == None else level

        if self.__setup_file_handler__(stream):
            if level == logging.INFO:
                self.logger.info(message)
            elif level == logging.ERROR:
                self.logger.error(message)
            elif level == logging.WARNING:
                self.logger.warning(message)
        
        if 'console' in stream:
            if level == logging.INFO:
                symbol = '~'
            elif level == logging.ERROR:
                symbol = '-'
            elif level == logging.WARNING:
                symbol = '!'
            print(f'[{symbol}] {message}')

    def info(self, message, stream = None):
        self.write(message, logging.INFO, stream)
        
    def error(self, message, stream = None):
        self.write(message, logging.ERROR, stream)

    def warn(self, message, stream = None):
        self.write(message, logging.WARNING, stream)