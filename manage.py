# coding:utf-8

import os 

from app import create_app, db
from app.models import Role, User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
# from livereload import Server

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,Role=Role,User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# 1. shell: make_shell_context()
# make_shell_context() 函数注册了程序、数据库实例以及模型，因此这些对象能直接导入 shell:
#  $ python hello.py shell
# >>> app
# <Flask 'app'>
# >>> db
# <SQLAlchemy engine='sqlite:////home/flask/flasky/data.sqlite'> >>> User
# <class 'app.User'>

# 2. 使用Flask-Migrate实现数据库迁移
# from flask.ext.migrate import Migrate, MigrateCommand # ...
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)
# 为了导出数据库迁移命令，Flask-Migrate 提供了一个 MigrateCommand 类，可附加到 Flask- Script 的 manager 对象上。在这个例子中，MigrateCommand 类使用 db 命令附加。
#
# 2.1 创建迁移仓库
# 在维护数据库迁移之前，要使用 init 子命令创建迁移仓库:
# (venv) $ python hello.py db init
# Creating directory /home/flask/flasky/migrations...done
# Creating directory /home/flask/flasky/migrations/versions...done Generating /home/flask/flasky/migrations/alembic.ini...done Generating /home/flask/flasky/migrations/env.py...done Generating /home/flask/flasky/migrations/env.pyc...done Generating /home/flask/flasky/migrations/README...done Generating /home/flask/flasky/migrations/script.py.mako...done Please edit configuration/connection/logging settings in '/home/flask/flasky/migrations/alembic.ini' before proceeding.
# 这个命令会创建 migrations 文件夹，所有迁移脚本都存放其中。
#
# 2.2 创建迁移脚本
# migrate 子命令用来自动创建迁移脚本:
#      (venv) $ python hello.py db migrate -m "initial migration"
#      INFO  [alembic.migration] Context impl SQLiteImpl.
#      INFO  [alembic.migration] Will assume non-transactional DDL.
#      INFO  [alembic.autogenerate] Detected added table 'roles'
#      INFO  [alembic.autogenerate] Detected added table 'users'
#      INFO  [alembic.autogenerate.compare] Detected added index
#      'ix_users_username' on '['username']'
# Generating /home/flask/flasky/migrations/versions/1bc 594146bb5_initial_migration.py...done
#
# 2.3 更新数据库
# 检查并修正好迁移脚本之后，我们可以使用 db upgrade 命令把迁移应用到数据库中:
#      (venv) $ python hello.py db upgrade
#      INFO  [alembic.migration] Context impl SQLiteImpl.
#      INFO  [alembic.migration] Will assume non-transactional DDL.
#      INFO  [alembic.migration] Running upgrade None -> 1bc594146bb5, initial migration
# 对第一个迁移来说，其作用和调用 db.create_all() 方法一样。但在后续的迁移中， upgrade 命令能把改动应用到数据库中，且不影响其中保存的数据。

@manager.command
def deploy():
    from flask_migrate import upgrade
    upgrade()

    # db.create_all()

    from app.models import Role
    Role.init_roles()

# @manager.command
# def dev():
#     live_server = Server(app.wsgi_app)
#     live_server.watch('**/*.*')
#     live_server.serve(host='127.0.0.1',port='5000',liveport='5000',open_url_delay=1)

if __name__ == '__main__':
    manager.run()