import os

xuhao_path = './xuhao.txt'
mima_path = './mima.txt'


# 准备学号与密码
def xuehao_mima():
    xuhao_txt = os.path.exists(xuhao_path)
    mima_txt = os.path.exists(mima_path)

    # 如果没有xuhao.txt或者mima.txt就要求用户输入学号与密码
    if not xuhao_txt or not mima_txt:
        xuhao = input('请输入学号:')
        mima = input('请输入密码:')

    # 如果xuhao.txt与mima.txt都存在,就读取这两个文件中储存的学号密码
    else:
        with open(xuhao_path, 'r') as xuhao_file:
            xuhao = xuhao_file.read()
            xuhao_file.close()
        with open(mima_path, 'r') as mima_file:
            mima = mima_file.read()
            mima_file.close()

    return xuhao, mima


def save_xuhaoMima(xuhao, mima):
    with open(xuhao_path, 'w') as xuhao_file:
        xuhao_file.write(xuhao)
        xuhao_file.close()
    with open(mima_path, 'w') as mima_file:
        mima_file.write(mima)
        mima_file.close()
