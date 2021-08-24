import subprocess
def run_command(command):
    command=command.rstrip()#去掉空格
    try:
        child = subprocess.run(command,shell=True)
    except:
        child = 'Can not execute the command.\r\n'
    return child
execute="dir d:"#遍历D盘文件
output = run_command(execute)