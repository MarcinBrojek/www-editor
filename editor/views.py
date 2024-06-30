import datetime
from django.http import JsonResponse
from django.shortcuts import render
from .models import User, Directory, File, FileSection, StatusData
import subprocess


# https://stackoverflow.com/questions/70419441/attributeerror-wsgirequest-object-has-no-attribute-is-ajax
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# Helper functions


def file_end_line_number(content):
    if content == "":
        return 0
    n = 1
    for c in content:
        if c == '\n':
            n += 1
    return n


def set_result(file, lst):
    content = file.content or ""
    f = open("tmp.c", "w")
    f.write(content)
    f.close()
    file.result = subprocess.check_output(lst).decode("utf-8")
    file.save()


def set_sections(owner, file, lst):
    content = file.content or ""
    f = open("tmp.c", "w")
    f.write(content)
    f.close()
    output = subprocess.check_output(lst).decode("utf-8")

    pos = 0
    list_names = []
    list_types = []
    list_status = []
    list_content = []

    while 1:
        ind = output.find('Goal typed', pos)
        if ind == -1:
            break
        pos = ind + 11
        lname = ""
        while output[pos] != ' ' and pos < len(output):
            lname += output[pos]
            pos += 1
        list_names.append(lname)

    pos = 0
    while 1:
        ind = output.find('------------------------------------------------------------\n\nGoal', pos)
        if ind == -1:
            break
        pos = ind + 67
        ltype = ""
        while output[pos] != ' ' and pos < len(output):
            ltype += output[pos]
            pos += 1
        list_types.append(ltype)

    pos = 0
    while 1:
        pos = output.find('returns', pos)
        if pos == -1:
            break
        pos += 8
        status = ""
        while output[pos] != ' ':
            status += output[pos]
            pos += 1
        list_status.append(status)

    pos = 0
    while 1:
        pos = output.find('------------------------------------------------------------\n\nGoal', pos)
        if pos == -1:
            break
        pos += 62
        endpos = output.find('\n\n', pos)
        cont = ""
        while pos < endpos:
            cont += output[pos]
            pos += 1
        list_content.append(cont)

    i = 0
    while i < len(list_names):
        validity_flag = True
        timestamp = datetime.datetime.now()
        creation_date = datetime.date.today()
        availability_flag = True
        category = list_types[i]
        status = list_status[i]
        status_data = StatusData(validity_flag=validity_flag, timestamp=timestamp, data="example data", user=owner)
        status_data.save()

        FileSection(timestamp=timestamp, validity_flag=validity_flag, name=list_names[i], description="",
                    creation_date=creation_date, availability_flag=availability_flag, category=category,
                    status=status, status_data_id=status_data.id, parent_file=file, content=list_content[i],
                    line_number=0, end_line_number=file_end_line_number(list_content[i]), parent_section=None).save()
        i += 1


def do_json_for_list(lst):
    lst = [e.json() for e in lst]
    return lst


def only_available(lst):
    res = []
    for e in lst:
        if e.availability_flag:
            res.append(e)
    return res


def get_parents(parent_id, parent_type):
    if parent_id == "":
        return {'Directory': "", 'File': "", 'FileSection': ""}
    parent_directory = Directory.objects.filter(id=parent_id, availability_flag=True).all()[0] if parent_type == 'Directory' else ""
    parent_file = File.objects.filter(id=parent_id, availability_flag=True).all()[0] if parent_type == 'File' else ""
    parent_section = FileSection.objects.filter(id=parent_id, availability_flag=True).all()[0] if parent_type == 'FileSection' else ""
    return {'Directory': parent_directory, 'File': parent_file, 'FileSection': parent_section}


def get_sons_list_objects(parent):
    list_of_sons = []
    if parent == "":
        list_of_sons += Directory.objects.filter(parent_directory=None).all()
        list_of_sons += File.objects.filter(parent_directory=None).all()
    else:
        if isinstance(parent, Directory):
            list_of_sons += Directory.objects.filter(parent_directory=parent).all()
            list_of_sons += File.objects.filter(parent_directory=parent).all()
        if isinstance(parent, File):
            list_of_sons += FileSection.objects.filter(parent_file=parent).all()
        if isinstance(parent, FileSection):
            list_of_sons += FileSection.objects.filter(parent_section=parent).all()
    return only_available(list_of_sons)


def is_unique_name_in_location(parent_type, parent_id, name):
    parent = None
    if parent_id == "":
        return not Directory.objects.filter(parent_directory=None, name=name) \
               and not File.objects.filter(parent_directory=None, name=name)

    if parent_type == 'Directory':
        parent = Directory.objects.filter(id=parent_id).all()[0]
    if parent_type == 'File':
        parent = File.objects.filter(id=parent_id).all()[0]
    if parent_type == 'FileSection':
        parent = FileSection.objects.filter(id=parent_id).all()[0]

    sons = get_sons_list_objects(parent=parent)
    names = [e.name for e in sons]
    return names.count(name) == 0


def is_possible_hierarchy(parent_type, son_type):
    return not ((parent_type == 'Directory' and son_type == 'FileSection') or
                (parent_type == 'File' and son_type == 'File') or
                (parent_type == 'File' and son_type == 'Directory') or
                (parent_type == 'FileSection' and son_type == 'File') or
                (parent_type == 'FileSection' and son_type == 'Directory'))


def find_el(el_type, el_name, par_type, par_id):
    if par_type == "":
        par_type = 'Directory'
    parent = get_parents(parent_id=par_id, parent_type=par_type)[par_type]
    sons = get_sons_list_objects(parent=parent)
    for son in sons:
        if son.name == el_name:
            return son
    return None


def get_content(content, beg_line_number, end_line_number):
    return "\n".join(content.split('\n')[beg_line_number:end_line_number])


def request_get(request, args, field, default=""):
    if request is not None:
        return request.GET.get(field, default)
    if field not in args:
        return ""
    return args[field]

# Create your views here.


def index(request):
    return render(request, 'editor/index.html')


def log_in(request, args=None):
    assert(args is not None or (is_ajax(request=request) or request.method == 'GET'))
    login = request_get(request, args, 'login')
    password = request_get(request, args, 'password')
    user = User.get_user(login=login, password=password)
    if user is None:
        return JsonResponse({'user': ""})
    else:
        return JsonResponse({'user': user.json()})


def register(request, args=None):
    assert (args is not None or (is_ajax(request=request) or request.method == 'GET'))
    name = request_get(request, args, 'name')
    login = request_get(request, args, 'login')
    password = request_get(request, args, 'password')
    repeated_password = request_get(request, args, 'repeated_password')

    ok, err = User.validate_name(name=name)
    if not ok:
        return JsonResponse({'err': err, 'user': ""})
    ok, err = User.validate_login(login=login)
    if not ok:
        return JsonResponse({'err': err, 'user': ""})
    ok, err = User.validate_passwords(pwd1=password, pwd2=repeated_password)
    if not ok:
        return JsonResponse({'err': err, 'user': ""})

    user = User(timestamp=datetime.datetime.now(), validity_flag=True, name=name, password=password, login=login)
    user.save()
    return JsonResponse({'err': "", 'user': user.json()})


def files_list(request, args=None):
    assert (args is not None or (is_ajax(request=request) or request.method == 'GET'))
    parent_type = request_get(request, args, 'parent_type')
    parent_id = request_get(request, args, 'parent_id')
    if parent_id == "":
        parent = ""
    else:
        parent = get_parents(parent_id=parent_id, parent_type=parent_type)[parent_type]
    return JsonResponse({'list': do_json_for_list(get_sons_list_objects(parent))})


def add(request, args=None):
    assert (args is not None or (is_ajax(request=request) or request.method == 'GET'))
    login = request_get(request, args, 'login')
    password = request_get(request, args, 'password')
    type_name = request_get(request, args, 'type_name')
    name = request_get(request, args, 'name')
    description = request_get(request, args, 'description')
    parent_type = request_get(request, args, 'parent_type')
    parent_id = request_get(request, args, 'parent_id')
    category_name = request_get(request, args, 'category_name', 'Procedure')
    status_name = request_get(request, args, 'status', 'Unchecked')
    content = request_get(request, args, 'content')
    line_number = int(request_get(request, args, 'line_number', "0") or "0")

    owner = User.get_user(login=login, password=password)
    if owner is None:
        return JsonResponse({'info': 'bad user'})

    if not is_possible_hierarchy(parent_type=parent_type, son_type=type_name):
        return JsonResponse({'info': 'bad hierarchy'})

    if not is_unique_name_in_location(parent_type=parent_type, parent_id=parent_id, name=name):
        return JsonResponse({'info': 'not unique name'})

    parents = get_parents(parent_id=parent_id, parent_type=parent_type)
    parent_directory, parent_file, parent_section = parents['Directory'], parents['File'], parents['FileSection']
    if parent_id == "":
        parent_directory = None

    validity_flag = True
    timestamp = datetime.datetime.now()  # any
    creation_date = datetime.date.today()  # any
    availability_flag = True
    category = category_name
    status = status_name
    status_data = StatusData(validity_flag=validity_flag, timestamp=timestamp, data="example data", user=owner)
    status_data.save()

    if parent_directory == "":
        parent_directory = None
    if parent_file == "":
        parent_file = None
    if parent_section == "":
        parent_section = None

    if type_name == 'Directory':
        Directory(timestamp=timestamp, validity_flag=validity_flag, name=name, description=description,
                  creation_date=creation_date, owner=owner, availability_flag=availability_flag,
                  parent_directory=parent_directory).save()

    if type_name == 'File':
        end_line_number = file_end_line_number(content=content)

        el = File(timestamp=timestamp, validity_flag=validity_flag, name=name, description=description,
                  creation_date=creation_date, owner=owner, availability_flag=availability_flag,
                  parent_directory=parent_directory, line_number=0, end_line_number=end_line_number,
                  content=content, result="")
        el.save()
        set_result(el, ['frama-c', '-wp', '-wp-log=r:result.txt', 'tmp.c'])
        set_sections(owner, el, ['frama-c', '-wp', '-wp-print', 'tmp.c'])

    if type_name == 'FileSection':
        parent = parent_file if parent_file is not None else parent_section
        if line_number > parent.end_line_number:
            return JsonResponse({})

        content = get_content(parent.content, parent.line_number, line_number)
        end_line_number = file_end_line_number(content=content)
        parent.line_number = line_number
        parent.save()

        FileSection(timestamp=timestamp, validity_flag=validity_flag, name=name, description=description,
                    creation_date=creation_date, availability_flag=availability_flag, category=category,
                    status=status, status_data_id=status_data.id, parent_file=parent_file, content=content,
                    line_number=line_number, end_line_number=end_line_number, parent_section=parent_section).save()
    return JsonResponse({'info': 'ok'})


def remove(request, args=None):
    assert (args is not None or (is_ajax(request=request) or request.method == 'GET'))
    login = request_get(request, args, 'login')
    password = request_get(request, args, 'password')
    type_name = request_get(request, args, 'type_name')
    name = request_get(request, args, 'name')
    parent_type = request_get(request, args, 'parent_type')
    parent_id = request_get(request, args, 'parent_id')

    if User.get_user(login=login, password=password) is None:
        return JsonResponse({'info': 'bad user'})

    if not is_possible_hierarchy(parent_type=parent_type, son_type=type_name):
        return JsonResponse({'info': 'file not exists'})

    removed_object = find_el(el_type=type_name, el_name=name, par_type=parent_type, par_id=parent_id)
    if removed_object is not None:
        removed_object.availability_flag = False
        removed_object.save()
        return JsonResponse({'info': 'ok'})

    return JsonResponse({'info': 'file not exists'})


def rerun(request, args=None):
    assert (args is not None or (is_ajax(request=request) or request.method == 'GET'))
    login = request_get(request, args, 'login')
    password = request_get(request, args, 'password')
    file_id = request_get(request, args, 'file_id')
    prover = request_get(request, args, 'prover')
    rte = request_get(request, args, 'rte')
    prop = request_get(request, args, 'prop_content')

    user = User.get_user(login=login, password=password)
    if user is None:
        return JsonResponse({"ok": False})

    el = File.objects.filter(id=file_id)
    if not el:
        return JsonResponse({"ok": False})
    el = el.first()

    sections = get_sons_list_objects(el)
    for section in sections:
        section.availability_flag = False
        section.save()

    par_list = ['frama-c', '-wp', '-wp-prover', prover]
    if prop != "":
        par_list.append('-wp-prop="' + prop + '"')
    if rte != "":
        par_list.append('-wp-rte')

    par_list.append('-wp-log=r:result.txt')
    par_list.append('tmp.c')
    set_result(el, par_list)

    par_list[len(par_list) - 2] = '-wp-print'
    set_sections(user, el, par_list)
    return JsonResponse({"ok": True})


def result(request, args=None):
    assert (args is not None or (is_ajax(request=request) or request.method == 'GET'))
    login = request_get(request, args, 'login')
    password = request_get(request, args, 'password')
    file_id = request_get(request, args, 'file_id')

    user = User.get_user(login=login, password=password)
    if user is None:
        return JsonResponse({"result": ""})

    el = File.objects.filter(id=file_id)
    if not el:
        return JsonResponse({"result": ""})
    el = el.first()

    return JsonResponse({"result": el.result})
