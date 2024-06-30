from django.test import TestCase

from ..models import User, Directory, File
from ..views import log_in, register, files_list, add, remove, rerun, result
import datetime
import json

# helper


def one_user_base():
    timestamp = datetime.date.today()
    User.objects.create(name='user', login='login', password='P4swords',
                        timestamp=timestamp, validity_flag=True)


def one_dir_user_base():
    creation_date = datetime.date.today()
    user = User.objects.create(name='user', login='login', password='P4swords',
                               timestamp=creation_date, validity_flag=True)
    Directory.objects.create(name='name', description='description', creation_date=creation_date,
                             owner=user, availability_flag=True, parent_directory=None,
                             timestamp=creation_date, validity_flag=True)


def one_file_user_base():
    creation_date = datetime.date.today()
    user = User.objects.create(name='user', login='login', password='P4swords',
                               timestamp=creation_date, validity_flag=True)
    File.objects.create(name='name', description='description',
                        content='/*@ requires  y/2. <= x <= 2.*y;' \
                                '  @ ensures  \\result == x-y;' \
                                '  @*/' \
                                '' \
                                'float Sterbenz(float x, float y) {' \
                                '  return x-y;' \
                                '}',
                        line_number=0, end_line_number=8,  creation_date=creation_date,
                        owner=user, availability_flag=True, parent_directory=None,
                        result= '[kernel] Parsing tmp.c (with preprocessing)' \
                                '[wp] Running WP plugin...' \
                                '[wp] Warning: Missing RTE guards' \
                                '[wp] 1 goal scheduled' \
                                '[wp] [Alt-Ergo 2.2.0] Goal typed_Sterbenz_ensures : Timeout (Qed:3ms) (10s)' \
                                '[wp] Proved goals:    0 / 1' '' \
                                '  Alt-Ergo 2.2.0:    0  (interrupted: 1)' \
                                '[wp:pedantic-assigns] tmp.c:5: Warning:' \
                                '  No assigns specification for function Sterbenz.' \
                                '  Callers assumptions might be imprecise.',
                        timestamp=creation_date, validity_flag=True)


def response_string(response):
    return response.content.decode('utf-8')


def response_dict(response):
    return json.loads(response_string(response))

# tests


class LoginTestCase(TestCase):
    def setUp(self):
        one_user_base()

    # user not exists
    def test_login_bad_user(self):
        res = log_in(None, {'login': 'login', 'password': 'passwords'})
        self.assertEqual(response_string(res), '{"user": ""}')

    # user exists
    def test_login_ok_user(self):
        res = log_in(None, {'login': 'login', 'password': 'P4swords'})
        self.assertNotEqual(response_string(res), '{"user": ""}')


class RegisterTestCase(TestCase):
    def setUp(self):
        one_user_base()

    # bad name in register action
    def test_register_bad_name(self):
        res = register(None, {'name': 'a', 'login': 'login', 'password': 'P4swords', 'repeated_password': 'P4swords'})
        self.assertEqual(response_string(res), '{"err": "Expected length of name is from 4 to 30.", "user": ""}')

    # bad login in register action
    def test_register_bad_login(self):
        res = register(None, {'name': 'user', 'login': 'log', 'password': 'P4swords', 'repeated_password': 'P4swords'})
        self.assertEqual(response_string(res), '{"err": "Expected length of login is from 4 to 16.", "user": ""}')

    # bad passwords in register action
    def test_register_bad_passwords(self):
        res = register(None, {'name': 'user', 'login': 'new_login', 'password': 'Pas1', 'repeated_password': 'Pas1'})
        self.assertEqual(response_string(res), '{"err": "Expected length of password is from 8 to 16.", "user": ""}')

    # user with the same login exist
    def test_register_bad_user(self):
        res = register(None, {'name': 'user', 'login': 'login', 'password': 'Password4',
                              'repeated_password': 'Password4'})
        self.assertEqual(response_string(res), '{"err": "Given login exists in database.", "user": ""}')

    # register action when data is valid
    def test_register_ok_data(self):
        res = register(None, {'name': 'new_user', 'login': 'new_login', 'password': 'new_Password4',
                              'repeated_password': 'new_Password4'})
        dic = response_dict(res)
        self.assertEqual(dic['err'], "")
        self.assertNotEqual(dic['user'], "")
        query = User.objects.filter(name='new_user', login='new_login', password='new_Password4').all()
        self.assertNotEqual(query, None)


class FileListTestCase(TestCase):
    def setUp(self):
        one_dir_user_base()

    # file not exists - main directory
    def test_filelist_main_dir(self):
        res = files_list(None, {'parent_type': 'Directory', 'parent_id': ""})
        dic = response_dict(res)
        self.assertEqual(dic['list'][0]['type'], 'Directory')
        self.assertEqual(dic['list'][0]['name'], 'name')
        self.assertEqual(dic['list'][0]['description'], 'description')

    # file exists - son of main
    def test_filelist_ok_file(self):
        res = files_list(None, {'parent_type': 'Directory', 'parent_id': '1'})
        dic = response_dict(res)
        self.assertEqual(dic['list'], [])


class AddTestCase(TestCase):
    def setUp(self):
        one_dir_user_base()

    # user is not logged
    def test_add_bad_user(self):
        args_bad_user = {
            'login': 'login',
            'password': 'password'
        }
        dic = response_dict(add(None, args_bad_user))
        self.assertEqual(dic['info'], 'bad user')

    # adding sth that is forbidden: like directory in file
    def test_add_bad_hierarchy(self):
        args_bad_hierarchy = {
            'login': 'login',
            'password': 'P4swords',
            'type_name': 'Directory',
            'name': 'new_name',
            'description': 'description',
            'parent_type': 'File',
            'parent_id': ''
        }
        dic = response_dict(add(None, args_bad_hierarchy))
        self.assertEqual(dic['info'], 'bad hierarchy')

    # not unique name
    def test_add_unique_name(self):
        args_not_unique_name = {
            'login': 'login',
            'password': 'P4swords',
            'type_name': 'Directory',
            'name': 'name',
            'description': 'description',
            'parent_type': 'Directory',
            'parent_id': '',
        }
        dic = response_dict(add(None, args_not_unique_name))
        self.assertEqual(dic['info'], 'not unique name')

    # example of adding dir
    def test_add_ok_dir(self):
        args_ok_dir = {
            'login': 'login',
            'password': 'P4swords',
            'type_name': 'Directory',
            'name': 'new_directory',
            'description': 'description',
            'parent_type': 'Directory',
            'parent_id': '1',
        }
        dic = response_dict(add(None, args_ok_dir))
        self.assertEqual(dic['info'], 'ok')

    # example of adding file
    def test_add_ok_file(self):
        content = '/*@ requires  y/2. <= x <= 2.*y;' \
                  '  @ ensures  \\result == x-y;' \
                  '  @*/' \
                  '' \
                  'float Sterbenz(float x, float y) {' \
                  '  return x-y;' \
                  '}'
        args_ok_file = {
            'login': 'login',
            'password': 'P4swords',
            'type_name': 'File',
            'name': 'new_file',
            'description': 'description',
            'parent_type': 'Directory',
            'parent_id': '1',
            'category_name': 'Procedure',
            'status_name': 'Unchecked',
            'content': content,
            'line_number': '0'
        }
        dic = response_dict(add(None, args_ok_file))
        self.assertEqual(dic['info'], 'ok')


class RemoveTestCase(TestCase):
    def setUp(self):
        one_dir_user_base()

    # user is not logged
    def test_remove_bad_user(self):
        args_bad_user = {
            'login': 'login',
            'password': 'password'
        }
        dic = response_dict(remove(None, args_bad_user))
        self.assertEqual(dic['info'], 'bad user')

    # file not exists
    def test_remove_bad_file(self):
        args_bad_file = {
            'login': 'login',
            'password': 'P4swords',
            'name': 'no ',
            'type_name': 'Directory',
            'parent_type': 'Directory',
            'parent_id': ''
        }
        dic = response_dict(remove(None, args_bad_file))
        self.assertEqual(dic['info'], 'file not exists')

    # example of removing file
    def test_remove_ok_file(self):
        args_ok_file = {
            'login': 'login',
            'password': 'P4swords',
            'name': 'name',
            'type_name': 'Directory',
            'parent_type': 'Directory',
            'parent_id': ''
        }
        dic = response_dict(remove(None, args_ok_file))
        self.assertEqual(dic['info'], 'ok')


class RerunTestCase(TestCase):
    def setUp(self):
        one_file_user_base()

    # user is not logged
    def test_rerun_bad_user(self):
        args_bad_user = {
            'login': 'login',
            'password': 'password'
        }
        dic = response_dict(rerun(None, args_bad_user))
        self.assertEqual(dic['ok'], False)

    # file not exists
    def test_rerun_bad_file(self):
        args_bad_file = {
            'login': 'login',
            'password': 'P4swords',
            'file_id': 2,
            'prover': 'alt-ergo',
            'rte': True
        }
        dic = response_dict(rerun(None, args_bad_file))
        self.assertEqual(dic['ok'], False)

    # example of rerun file
    def test_rerun_ok_file(self):
        args_ok_file = {
            'login': 'login',
            'password': 'P4swords',
            'file_id': 1,
            'prover': 'alt-ergo',
            'rte': True
        }
        dic = response_dict(rerun(None, args_ok_file))
        self.assertEqual(dic['ok'], True)


class ResultTestCase(TestCase):
    def setUp(self):
        one_file_user_base()

    # user is not logged
    def test_result_bad_user(self):
        args_bad_user = {
            'login': 'login',
            'password': 'password'
        }
        dic = response_dict(result(None, args_bad_user))
        self.assertEqual(dic['result'], "")

    # file not exists
    def test_result_bad_file(self):
        args_bad_file = {
            'login': 'login',
            'password': 'P4swords',
            'file_id': 2
        }
        dic = response_dict(result(None, args_bad_file))
        self.assertEqual(dic['result'], "")

    # example of result action
    def test_result_ok_file(self):
        args_ok_file = {
            'login': 'login',
            'password': 'P4swords',
            'file_id': 1
        }
        dic = response_dict(result(None, args_ok_file))
        self.assertNotEqual(dic['result'], "")
