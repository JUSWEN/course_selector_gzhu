import os

studentNumber_path = './student_number.txt'
password_path = './password.txt'


def access():
    '''获取学号与密码'''
    studentNumber_txt = os.path.exists(studentNumber_path)
    password_txt = os.path.exists(password_path)

    # 如果没有student_number.txt或者password.txt就要求用户输入学号与密码
    if not studentNumber_txt or not password_txt:
        student_number = input('请输入学号:')
        password = input('请输入密码:')
    # 如果student_number.txt与password.txt都存在,就读取这两个文件中储存的学号密码
    else:
        with open(studentNumber_path, 'r') as file:
            student_number = file.read()

        with open(password_path, 'r') as file:
            password = file.read()

    return student_number, password


def save(student_number, password):
    '''保存学号密码'''
    with open(studentNumber_path, 'w') as file:
        file.write(student_number)

    with open(password_path, 'w') as file:
        file.write(password)
