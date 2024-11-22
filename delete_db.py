import os


fd = []
os.remove('db.sqlite3')
try:
    with open('db.sqlite3', 'x') as file:
        pass
except FileExistsError:
    pass

os.chdir('project/migrations')
for i in os.listdir():
    if i[0] == '0':
        os.remove(i)

os.chdir('..')
os.chdir('..')
os.chdir('user/migrations')
for i in os.listdir():
    if i[0] == '0':
        os.remove(i)

os.chdir('..')
os.chdir('..')
os.chdir('task/migrations')
for i in os.listdir():
    if i[0] == '0':
        os.remove(i)


os.chdir('..')
os.chdir('..')
os.chdir('comment/migrations')
for i in os.listdir():
    if i[0] == '0':
        os.remove(i)
