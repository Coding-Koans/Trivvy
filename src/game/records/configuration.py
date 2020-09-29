from src.messages import Log as report
import configparser

class Trivia_Game_Configuration:

    def __init__(self, config_file, log = print):
        self.log = log
        self.log(report.trivia_config_loading)

        # sensible defaults
        self.trivia_hinttime_1 = 45
        self.trivia_hinttime_2 = 90
        self.trivia_skiptime = 135
        self.trivia_questiondelay = 5

        try:
            config = configparser.ConfigParser()
            config.read(config_file)

            self.trivia_hinttime_1 = int(config['Trivia Settings']['trivia_hinttime_1'])
            self.trivia_hinttime_2 = int(config['Trivia Settings']['trivia_hinttime_2'])
            self.trivia_skiptime = int(config['Trivia Settings']['trivia_skiptime'])
            self.trivia_questiondelay = int(config['Trivia Settings']['trivia_questiondelay'])

            self.log(report.trivia_config_success)
        except:
            self.log(report.trivia_config_failure)

    def get_trivia_constants(self):
        return {
            'times_up': self.trivia_skiptime,
            'hint_1_up': self.trivia_hinttime_1,
            'hint_2_up': self.trivia_hinttime_2,
            'wait': self.trivia_questiondelay,
        }
