from fabric.api import task, run, env, sudo, cd


env.sudo_user = 'fstat'


@task
def update_code():
    with cd('/fstat/code'):
        sudo('git pull --rebase origin master')


@task
def do_migrations():
    with prefix('source /fstat/env/bin/activate'):
        with cd('/fstat/code'):
            sudo('FLASK_APP="/fstat/code/fstat/__init__.py" flask db upgrade')


@task
def restart_fstat():
    run('systemctl restart fstat')
