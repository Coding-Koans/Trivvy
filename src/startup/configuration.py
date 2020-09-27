from src.messages import Log as report
import configparser

class Configuration:

    def abruptly_end_the_app():
        exit()

    def __init__(self, config_file, log = print):
        self.log = log
        self.log(report.config_loading)
        try:
            config = configparser.ConfigParser()
            config.read(config_file)

            # We don't use these, but we check for their existence here
            # Finding out later that a command will error out is less-than ideal
            # The code duplication is indicating an opportunity to refactor
            # But I'd prefer to decouple the game from the bot so they can be reusable
            # Please update or delete these with whatever the config file is supposed to have
            self.trivia_filename = config['Trivia Settings']['trivia_filename']
            self.trivia_filetype = config['Trivia Settings']['trivia_filetype']
            self.trivia_questions = int(config['Trivia Settings']['trivia_questions'])
            self.trivia_hinttime_1 = int(config['Trivia Settings']['trivia_hinttime_1'])
            self.trivia_hinttime_2 = int(config['Trivia Settings']['trivia_hinttime_2'])
            self.trivia_skiptime = int(config['Trivia Settings']['trivia_skiptime'])
            self.trivia_questiondelay = int(config['Trivia Settings']['trivia_questiondelay'])
            self.trivia_bonusvalue = int(config['Trivia Settings']['trivia_bonusvalue'])
            # End Check for Unused Values

            admin1 = config['Admin Settings']['admins']
            self.admins = admin1.split(',')

            self.HOST = str(config['Bot Settings']['HOST'])
            self.PORT = int(config['Bot Settings']['PORT'])
            self.NICK = config['Bot Settings']['NICK']
            self.PASS = config['Bot Settings']['PASS']
            self.CHAN = config['Bot Settings']['CHAN']
            self.log(report.config_success)
        except:
            self.log(report.config_failure)
            Configuration.abruptly_end_the_app()

    def set_admins(config):
        separator = ','
        admin_list = config['Admin Settings']['admins'].split(separator)
        return [admin.strip() for admin in admin_list]

    def get_admins(self):
        return self.admins

    def get_connection_constants(self):
        return {
            'irc_url': self.HOST,
            'irc_port': self.PORT,
            'bot_name': self.NICK,
            'oauth_token': self.PASS,
            'channel': self.CHAN
        }
