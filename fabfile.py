import os

from fabric.api import env, task, run, local, lcd, cd, sudo, put, settings

from fabtools import require
from fabtools.require.files import temporary_directory
from fabtools.python import virtualenv

from vagrant import Vagrant

import yaml

# read the config file
with open("config.yaml") as config_file:
    config = yaml.load(config_file)


@task
def vagrant(machine="default"):
    """ connect to a vagrant box
        :keyword machine, default =default
    """

    v = Vagrant(quiet_stdout=False)
    v.up(vm_name=machine)

    env.host_string = v.user_hostname_port(vm_name=machine)
    env.key_filename = v.keyfile(vm_name=machine),
    env.disable_known_hosts = True


@task
def setup():
    """do all the things """
    install_requirements()
    setup_module()
    deploy()
    setup_nginx()
    setup_uwsgi()


@task
def deploy():
    """deploy your module to host """
    with lcd(config['module']):
        local('python setup.py sdist --formats=gztar')
        dist = local('python setup.py --fullname', capture=True) + ".tar.gz"

        with temporary_directory() as tmp_dir:
            dist_path = os.path.join(tmp_dir, dist)
            put('dist/%s' % dist, os.path.join(tmp_dir, dist))
            sudo("{working_dir}/env/bin/pip install --upgrade --force-reinstall {dist}".format(
                    working_dir=config['working_dir'], dist=dist_path))

    with settings(warn_only=True):
        sudo("reload %s" % config['module'])

@task
def install_requirements():
    """install all requirements on the host"""
    sudo("apt-get install -y python-pip")
    sudo("pip install virtualenv")
    sudo("apt-get install -y nginx")
    sudo("apt-get install -y build-essential")
    sudo("apt-get install -y python-dev")
    sudo("apt-get install -y uwsgi-plugin-python")
    sudo("pip install uwsgi")


@task
def setup_module():
    """create the working directory and virtual environment"""

    sudo('mkdir -p {working_dir}'.format(**config))

    with cd(config['working_dir']):
        sudo("virtualenv env")


@task
def setup_nginx():

    require.nginx.disable('default')

    with open("templates/nginx.conf") as f:
        require.nginx.site(config['module'], template_contents=f.read().format(**config))


@task
def setup_uwsgi():
    with open("templates/uwsgi.conf") as f:
        require.file("/etc/init/{module}.conf".format(**config),
                     contents=f.read().format(**config),
                     use_sudo=True)

    with open("templates/uwsgi.ini") as f:
        require.file("{working_dir}/uwsgi.ini".format(**config),
                     contents=f.read().format(**config),
                     use_sudo=True)

    sudo("start %s" % config['module'])


@task
def host():
    """just for testing, display uname on host"""
    run('uname -a')


@task()
def test_deploy():
    v = Vagrant(quiet_stdout=False)
    v.destroy()
    v.up()
    setup()