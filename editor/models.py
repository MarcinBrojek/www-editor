from django.db import models
from django.db.models import CharField, TextField, DateField, ForeignKey, BooleanField, DateTimeField, IntegerField


class TimestampValidityModel(models.Model):
    timestamp = DateTimeField(null=False)
    validity_flag = BooleanField(null=False)

    class Meta:
        abstract = True


class User(TimestampValidityModel):
    name = CharField(max_length=30, null=False)
    login = CharField(max_length=16, null=False)
    password = CharField(max_length=16, null=False)

    def json(self):
        return {
            'type': 'User',
            'id': self.id,
            'timestamp': str(self.timestamp),
            'validity_flag': self.validity_flag,
            'name': self.name,
            'login': self.login,
            'password': self.password
        }

    # validate returns ok, error_info
    @staticmethod
    def validate_name(name):
        if not (4 <= len(name) <= 30):
            return False, "Expected length of name is from 4 to 30."
        return True, ""

    @staticmethod
    def validate_login(login):
        if ' ' in login:
            return False, "Login can't contain white space."
        if not (4 <= len(login) <= 16):
            return False, "Expected length of login is from 4 to 16."

        query = User.objects.filter(login=login).all()
        if query.first() is not None:
            return False, "Given login exists in database."
        return True, ""

    @staticmethod
    def validate_passwords(pwd1, pwd2):
        if pwd1 != pwd2:
            return False, "Passwords are not the same."
        if not any(c.isdigit() for c in pwd1):
            return False, "Password must contain at least one digit."
        if not any(c.islower() for c in pwd1):
            return False, "Password must contain at least one lower letter."
        if not any(c.isupper() for c in pwd1):
            return False, "Password must contain at least one upper letter."
        if not (8 <= len(pwd1) <= 16):
            return False, "Expected length of password is from 8 to 16."
        return True, ""

    @staticmethod
    def get_user(login, password):
        query = User.objects.filter(login=login, password=password)
        return query.first() if query else None


class Directory(TimestampValidityModel):
    name = CharField(max_length=30, null=False)
    description = TextField(null=True, blank=True)
    creation_date = DateField(null=False)
    owner = ForeignKey(User, on_delete=models.DO_NOTHING)
    availability_flag = BooleanField(null=False, default=True)
    parent_directory = ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)

    def json(self):
        return {
            'type': 'Directory',
            'id': self.id,
            'timestamp': str(self.timestamp),
            'validity_flag': self.validity_flag,
            'name': self.name,
            'description': self.description or "",
            'creation_date': str(self.creation_date),
            'owner': self.owner.json(),
            'availability_flag': self.availability_flag,
            'parent_directory': self.parent_directory.json() if self.parent_directory is not None else ""
        }


class File(TimestampValidityModel):
    name = CharField(max_length=30, null=False)
    description = TextField(null=True, blank=True)
    content = TextField(null=True, blank=True)
    creation_date = DateField(null=False)
    owner = ForeignKey(User, on_delete=models.DO_NOTHING)
    line_number = IntegerField(null=False, default=0)
    end_line_number = IntegerField(null=False, default=0)
    availability_flag = BooleanField(null=False, default=True)
    parent_directory = ForeignKey(Directory, null=True, blank=True, on_delete=models.DO_NOTHING)
    result = TextField(null=True, blank=True)

    def json(self):
        return {
            'type': 'File',
            'id': self.id,
            'timestamp': str(self.timestamp),
            'validity_flag': self.validity_flag,
            'name': self.name,
            'description': self.description or "",
            'content': self.content or "",
            'line_number': self.line_number,
            'end_line_number': self.end_line_number,
            'creation_date': str(self.creation_date),
            'owner': self.owner.json(),
            'availability_flag': self.availability_flag,
            'parent_directory': self.parent_directory.json() if self.parent_directory is not None else "",
            'result': self.result or ""
        }


class StatusData(TimestampValidityModel):
    data = TextField(null=False)
    user = ForeignKey(User, null=False, on_delete=models.DO_NOTHING)

    def json(self):
        return {
            'type': 'StatusData',
            'id': self.id,
            'timestamp': str(self.timestamp),
            'validity_flag': self.validity_flag,
            'data': self.data,
            'user': self.user.json()
        }


class FileSection(TimestampValidityModel):
    name = CharField(max_length=30, null=True, blank=True)
    description = TextField(null=True, blank=True)
    content = TextField(null=True, blank=True)
    line_number = IntegerField(null=False, default=0)
    end_line_number = IntegerField(null=False, default=0)
    creation_date = DateField(null=False)
    availability_flag = BooleanField(null=False, default=True)
    category = CharField(max_length=30, null=False)
    status = CharField(max_length=30, null=False)
    status_data = models.OneToOneField(StatusData, null=False, blank=False, on_delete=models.DO_NOTHING)
    # exactly one of those two must be not null
    parent_file = ForeignKey(File, null=True, blank=True, on_delete=models.DO_NOTHING)
    parent_section = ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)

    def json(self):
        return {
            'type': 'FileSection',
            'id': self.id,
            'timestamp': str(self.timestamp),
            'validity_flag': self.validity_flag,
            'name': self.name or "",
            'description': self.description or "",
            'content': self.content or "",
            'line_number': self.line_number,
            'end_line_number': self.end_line_number,
            'creation_date': str(self.creation_date),
            'availability_flag': self.availability_flag,
            'category': self.category,
            'status': self.status,
            'status_data': self.status_data.json(),
            'parent_file': self.parent_file.json() if self.parent_file is not None else "",
            'parent_section': self.parent_section.json() if self.parent_section is not None else ""
        }
