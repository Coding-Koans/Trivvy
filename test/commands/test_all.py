import unittest
import inspect
from test.test_helpers.file_system import cleanup
from src.commands import All

class AllCommandsTestCase(unittest.TestCase):
    mock_opts = {
        'qa': "mock_questions_asked",
        'ps': "mock_player_scores"
    }

    def test_commands_returns_tuples_with_message_matchers(self):
        subject = All(self.mock_opts).commands()

        cleanup(self.mock_opts['qa'])
        cleanup(self.mock_opts['ps'])
        for command in subject:
            message_matcher = command[0]
            self.assertEqual(type(message_matcher), str)
            self.assertNotEqual(message_matcher, "")

    def test_commands_returns_a_tuple_with_callbacks(self):
        subject = All(self.mock_opts).commands()

        cleanup(self.mock_opts['qa'])
        cleanup(self.mock_opts['ps'])
        for command in subject:
            callback = command[1]
            self.assertTrue(callable(callback))
            params = inspect.signature(callback).parameters

            class_signature = 'self'
            if class_signature in params:
                self.assertEqual(len(params), 3)
            else:
                self.assertEqual(len(params), 2)


    def test_commands_returns_a_tuple_with_validations(self):
        valid_validations = [ "admin_only" ]

        subject = All(self.mock_opts).commands()

        cleanup(self.mock_opts['qa'])
        cleanup(self.mock_opts['ps'])
        for command in subject:
            validations = command[2]
            self.assertEqual(type(validations), list)
            for validation in validations:
                self.assertTrue(validation in valid_validations)

    def test_commands_does_not_contain_name_collisions(self):
        subject = All(self.mock_opts).commands()

        command_messages = []
        unique = []
        cleanup(self.mock_opts['qa'])
        cleanup(self.mock_opts['ps'])
        for command in subject:
            command_messages.append(command[0])
            if command[0] not in unique:
                unique.append(command[0])
        self.assertEqual(unique, command_messages)
