from src.messages import Log as report
import configparser

class Configuration:

    def __init__(self, config_file, log = print):
        self.log = log
        self.log(report.config_loading)
        try:
            config = configparser.ConfigParser()
            config.read(config_file)

            self.trivia_filename = config['Trivia Settings']['trivia_filename']
            self.trivia_filetype = config['Trivia Settings']['trivia_filetype']
            self.trivia_questions = int(config['Trivia Settings']['trivia_questions'])
            self.trivia_hinttime_1 = int(config['Trivia Settings']['trivia_hinttime_1'])
            self.trivia_hinttime_2 = int(config['Trivia Settings']['trivia_hinttime_2'])
            self.trivia_skiptime = int(config['Trivia Settings']['trivia_skiptime'])
            self.trivia_questiondelay = int(config['Trivia Settings']['trivia_questiondelay'])
            self.trivia_bonusvalue = int(config['Trivia Settings']['trivia_bonusvalue'])

            self.log(report.trivia_config_success)
        except:
            self.log(report.trivia_config_failure)

    def get_trivia_constants(self):
        return {
            self.trivia_filename,
            self.trivia_filetype,
            self.trivia_questions,
            self.trivia_hinttime_1,
            self.trivia_hinttime_2,
            self.trivia_skiptime,
            self.trivia_questiondelay,
            self.trivia_bonusvalue,
        }
