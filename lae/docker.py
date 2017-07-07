# -*- coding: utf8 -*-
import json
import os
import shutil
from .utils import find_app_root
from .utils.config import load_app_config
from .utils.log import logger
from mako.template import Template

COMMAND_NAME = "docker"
COMMAND_DESCRIPTION = "run project with docker."


def populate_argument_parser(parser):
    parser.add_argument('-r', '--refresh', action='append',
                        default=False, help='Build LEA app image')


def main(args):
    root_path = find_app_root()
    appcfg = load_app_config(root_path)
    appname = appcfg['application']

    # 处理 app.yaml 里的 handler 部分
    deal_handlers(appcfg=appcfg)

    # 处理 app.yaml 里的 crons 部分
    deal_crons(appcfg=appcfg)

    # build 相应的 docker
    pwd = os.getcwd()
    os.system("docker build -t %s %s" % (appname, pwd))

    # 删除临时文件
    shutil.rmtree(pwd + "/tmp")
    os.remove(pwd + '/Dockerfile')
    os.remove(pwd + '/cron_runner.py')
    logger.info('Docker image [%s] build complete. Run command "docker run -ti -p your_port:470 %s " to up it!' % (appname, appname))


def deal_handlers(appcfg):
    appname = appcfg['application']
    nginx_urls = []
    supervisord_program = []
    for handler in appcfg['handlers']:
        url = handler['url']
        url = url[:url.rfind('/')]
        # 处理各种类型的 url handler
        if 'static_dir' in handler:
            static_dir = handler.get('static_dir', 'static')
            static_dir = static_dir[:str(static_dir).rfind('/')]
            nginx_url_conf = render_template("nginx_static_url", context=dict(path=url, appname=appname, static_dir=static_dir))
            nginx_urls.append(nginx_url_conf)

        elif 'wsgi_app' in handler:
            app = handler['wsgi_app'].split(":")[1]
            module = handler['wsgi_app'].split(":")[0]
            context = dict(appname=appname, module=module, app=app, path=url)
            uwsgi_ini = render_template('uwsgi.ini', context=context)
            nginx_url_conf = render_template('nginx_url', context=context)
            supervisord = render_template('supervisord_program', context=context)
            save_file('%s_uwsgi.ini' % app, uwsgi_ini)
            nginx_urls.append(nginx_url_conf)
            supervisord_program.append(supervisord)

    dockerfile = render_template('Dockerfile', context=dict(appname=appname))
    save_file('Dockerfile', dockerfile, tmp_dir=False)
    supervisord_conf = render_template('supervisord.conf', context=dict(programs='\n'.join(supervisord_program)))
    save_file('supervisord.conf', supervisord_conf)
    nginx_conf = render_template('nginx.conf', context=dict(urls='\n\t'.join(nginx_urls)))
    save_file(appname + '_nginx.conf', nginx_conf)


def deal_crons(appcfg):
    appname = appcfg['application']

    maintainers = dict()
    for cron in appcfg['crons']:
        name = cron['name']
        maintainers[name] = cron['maintainers'].split(',')
    cron_runner_py = render_template("cron_runner.py", context=dict(maintainers=json.dumps(maintainers)))
    save_file("cron_runner.py", cron_runner_py, tmp_dir=False)
    crons = []
    for cron in appcfg['crons']:
        name = cron['name']
        schedule = cron['schedule']
        handler = name + ":" + cron["handler"]
        _ = render_template('cron_task', context=dict(appname=appname, schedule=schedule, handler=handler))
        crons.append(_)

    crons_file = '\n'.join(crons) + "\n"
    save_file('crontabfile', crons_file)


def save_file(filename, content, tmp_dir=True):
    pwd = os.getcwd()
    if not os.path.exists(pwd + "/tmp"):
        os.mkdir(pwd + "/tmp")
    if tmp_dir:
        filename = pwd + "/tmp/" + filename
    else:
        filename = pwd + "/" + filename
    fh = file(filename, mode='w')
    fh.write(content)
    fh.close()


def render_template(tmpl_name, context):
    basedir = os.path.abspath(os.path.dirname(__file__))
    template = Template(open(basedir + "/template/" + tmpl_name + ".tmpl").read())
    return template.render(**context)
