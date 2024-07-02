# Online editor

This repository hosts a web application designed for writing programs in the C language. It functions as an online text editor that enables users to create programs directly within a web-based environment. The application operates as a single-page web app, ensuring a seamless user experience without the need for page refreshes.

Key features include the ability for users to create and delete their own files after setting up an account. The application leverages technologies such as Django, jQuery, Frama-C, and CodeMirror. These tools collectively enable functionalities such as code writing, syntax highlighting, and code analysis.

---

### How to start server?

1. create python environemnt and install dependencies from requirements (in main directory)

```
> python -m venv ./myenv
> source myenv/bin/activate
> pip install -r requirements.txt
```

2. install frama-c, instruction on page: https://frama-c.com/html/get-frama-c.html

3. run server (locally)

```
> python manage.py migrate
> python manage.py runserver
```

4. go to web brower to adress http://127.0.0.1:8000 and use application (as user, when logged)

For more information about database go to http://127.0.0.1:8000/admin (login: admin, password: admin)

---

### Technologies versions:

In project used:
- django (4.2.13)
- jquery (3.6.0) - already in static directory
- codemirror (5.61.1) - already in static directory
- frama-c (22.0 (Titanium))

---

### Usage tips:
- to add/remove, log into app; the structure for files is: <br>
  directory_1 / ... / directory_n / file / file section
- in reality user does not delete files, only hides them; <br>
  from admin perpective they can be removed
- when admin deletes files - they should be removed in order: <br>
  file section -> file -> directory, so dependecies will be erased in proper manner

---


**Application preview**

: Code example            :|: Night mode              :|: Account register        :  
:-------------------------:|:-------------------------:|:-------------------------:
 <img alt="1" src="https://github.com/MarcinBrojek/www_editor/assets/73189722/3315edb0-0d1f-4eb8-934b-14e4160b7fcb"> | <img alt="2" src="https://github.com/MarcinBrojek/www_editor/assets/73189722/cae3951f-5736-4e79-8625-ad037621ab2a"> | <img alt="3" src="https://github.com/MarcinBrojek/www_editor/assets/73189722/e785dd6b-710f-462c-a98c-d89f4be25ace">

---

Tutorial (of frama-c) and code examples can be found at: https://github.com/AllanBlanchard/tutoriel_wp 
