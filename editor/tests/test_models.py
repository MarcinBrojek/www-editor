import datetime

from django.test import TestCase
from ..models import User, Directory, File, FileSection, StatusData

# helper


def user(name, login, password, timestamp, validity_flag):
    return User(name=name, login=login, password=password,
                timestamp=timestamp, validity_flag=validity_flag)


def directory(name, description, creation_date, owner, availability_flag,
              parent_directory, timestamp, validity_flag):
    return Directory(name=name, description=description, creation_date=creation_date,
                     owner=owner, availability_flag=availability_flag, parent_directory=parent_directory,
                     timestamp=timestamp, validity_flag=validity_flag)


def file(name, description, content, line_number, end_line_number,
         creation_date, owner, availability_flag, parent_directory,
         result, timestamp, validity_flag):
    return File(name=name, description=description, content=content, line_number=line_number,
                end_line_number=end_line_number, creation_date=creation_date, owner=owner,
                availability_flag=availability_flag, parent_directory=parent_directory,
                result=result, timestamp=timestamp, validity_flag=validity_flag)


def status_data(data, owner, timestamp, validity_flag):
    return StatusData(data=data, user=owner, timestamp=timestamp, validity_flag=validity_flag)


def file_section(name, description, content, line_number, end_line_number,
                 creation_date, availability_flag, category, status,
                 status_data, parent_file, parent_section, timestamp, validity_flag):
    return FileSection(name=name, description=description, content=content, line_number=line_number,
                       end_line_number=end_line_number, creation_date=creation_date,
                       availability_flag=availability_flag, category=category, status=status,
                       status_data=status_data, parent_file=parent_file, parent_section=parent_section,
                       timestamp=timestamp, validity_flag=validity_flag)

# testing


class UserTestCase(TestCase):
    def test_user_name(self):
        self.assertNotEqual(User.validate_name(''), (True, ""))
        self.assertNotEqual(User.validate_name('aaa'), (True, ""))
        self.assertEqual(User.validate_name('aaaa'), (True, ""))
        self.assertEqual(User.validate_name('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'), (True, ""))
        self.assertNotEqual(User.validate_name('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'), (True, ""))

    def test_user_login(self):
        self.assertNotEqual(User.validate_login(''), (True, ""))
        self.assertNotEqual(User.validate_login('aaa'), (True, ""))
        self.assertEqual(User.validate_login('aaaa'), (True, ""))
        self.assertEqual(User.validate_login('aaaaaaaaaaaaaaaa'), (True, ""))
        self.assertNotEqual(User.validate_login('aaaaaaaaaaaaaaaaa'), (True, ""))

    def test_user_password(self):
        self.assertNotEqual(User.validate_passwords('', ''), (True, ""))
        self.assertNotEqual(User.validate_passwords('A1aaaaa', 'A1aaaaa'), (True, ""))
        self.assertEqual(User.validate_passwords('A1aaaaaa', 'A1aaaaaa'), (True, ""))
        self.assertEqual(User.validate_passwords('A1aaaaaaaaaaaaaa', 'A1aaaaaaaaaaaaaa'), (True, ""))
        self.assertNotEqual(User.validate_passwords('A1aaaaaaaaaaaaaaa', 'A1aaaaaaaaaaaaaaa'), (True, ""))
        self.assertNotEqual(User.validate_passwords('aaaaaaaa', 'aaaaaaaa'), (True, ""))
        self.assertNotEqual(User.validate_passwords('Aaaaaaaa', 'Aaaaaaaa'), (True, ""))
        self.assertNotEqual(User.validate_passwords('A1aaaaaa', 'A2aaaaaa'), (True, ""))

    def test_user_json(self):
        timestamp = datetime.datetime.now
        self.assertEqual(user('user', 'login', 'P4swords', timestamp, True).json(), {
            'type': 'User',
            'id': None,
            'timestamp': str(timestamp),
            'validity_flag': True,
            'name': 'user',
            'login': 'login',
            'password': 'P4swords'
        })
        self.assertEqual(user('aaaa', 'aaaaaaaa', 'A1aaaaaa', timestamp, False).json(), {
            'type': 'User',
            'id': None,
            'timestamp': str(timestamp),
            'validity_flag': False,
            'name': 'aaaa',
            'login': 'aaaaaaaa',
            'password': 'A1aaaaaa'
        })


class DirectoryTestCase(TestCase):
    def test_directory_json(self):
        date = datetime.date.today()
        timestamp = datetime.datetime.now
        self.assertEqual(directory('directory', 'description', date,
                                   user('name', 'login', 'P4swords', timestamp, True),
                                   True, None, timestamp, True).json(), {
            'type': 'Directory',
            'id': None,
            'timestamp': str(timestamp),
            'validity_flag': True,
            'name': 'directory',
            'description': 'description',
            'creation_date': str(date),
            'owner': {
                'type': 'User',
                'id': None,
                'timestamp': str(timestamp),
                'validity_flag': True,
                'name': 'name',
                'login': 'login',
                'password': 'P4swords'
            },
            'availability_flag': True,
            'parent_directory': ""
        })


class FileTestCase(TestCase):
    def test_file_json(self):
        date = datetime.date.today()
        timestamp = datetime.datetime.now
        self.assertEqual(file('file', 'description', 'content', 0, 1, date,
                              user('name', 'login', 'P4swords', timestamp, True),
                              True, None, 'result', timestamp, True).json(), {
            'type': 'File',
            'id': None,
            'timestamp': str(timestamp),
            'validity_flag': True,
            'name': 'file',
            'description': 'description',
            'content': 'content',
            'line_number': 0,
            'end_line_number': 1,
            'creation_date': str(date),
            'owner': {
                'type': 'User',
                'id': None,
                'timestamp': str(timestamp),
                'validity_flag': True,
                'name': 'name',
                'login': 'login',
                'password': 'P4swords'
            },
            'availability_flag': True,
            'parent_directory': "",
            'result': 'result'
        })


class StatusDataTestCase(TestCase):
    def status_data_json(self):
        timestamp = datetime.datetime.now
        self.assertEqual(status_data('data', user('name', 'login', 'P4swords', timestamp, True),
                                     timestamp, True).json(), {
            'type': 'StatusData',
            'id': None,
            'timestamp': str(timestamp),
            'validity_flag': True,
            'data': 'data',
            'user': {
                'type': 'User',
                'id': None,
                'timestamp': str(timestamp),
                'validity_flag': True,
                'name': 'name',
                'login': 'login',
                'password': 'P4swords'
            }
        })


class FileSectionTestCase(TestCase):
    def test_file_section_json(self):
        date = datetime.date.today()
        timestamp = datetime.datetime.now
        self.assertEqual(file_section('section', 'description', 'content', 0, 1,
                                      date, True, 'Lemma', 'Unchecked',
                                      status_data('data', user('name', 'login', 'P4swords', timestamp, True),
                                                  timestamp, True),
                                      file('file', 'description', 'content', 0, 1, date,
                                           user('name', 'login', 'P4swords', timestamp, True),
                                           True, None, 'result', timestamp, True),
                                      None, timestamp, True).json(), {
            'type': 'FileSection',
            'id': None,
            'timestamp': str(timestamp),
            'validity_flag': True,
            'name': 'section',
            'description': 'description',
            'content': 'content',
            'line_number': 0,
            'end_line_number': 1,
            'creation_date': str(date),
            'availability_flag': True,
            'category': 'Lemma',
            'status': 'Unchecked',
            'status_data': {
                'type': 'StatusData',
                'id': None,
                'timestamp': str(timestamp),
                'validity_flag': True,
                'data': 'data',
                'user': {
                    'type': 'User',
                    'id': None,
                    'timestamp': str(timestamp),
                    'validity_flag': True,
                    'name': 'name',
                    'login': 'login',
                    'password': 'P4swords'
                }
            },
            'parent_file': {
                'type': 'File',
                'id': None,
                'timestamp': str(timestamp),
                'validity_flag': True,
                'name': 'file',
                'description': 'description',
                'content': 'content',
                'line_number': 0,
                'end_line_number': 1,
                'creation_date': str(date),
                'owner': {
                    'type': 'User',
                    'id': None,
                    'timestamp': str(timestamp),
                    'validity_flag': True,
                    'name': 'name',
                    'login': 'login',
                    'password': 'P4swords'
                },
                'availability_flag': True,
                'parent_directory': "",
                'result': 'result'
            },
            'parent_section': ""
        })
