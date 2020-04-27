import os
import sys
import json
import shutil
import traceback

from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand
from django.template.loader import render_to_string


CUR_DIR = os.path.dirname(os.path.abspath(__file__))


class FrontApp(object):
    """docstring for FrontApp"""
    def __init__(self, django_app_conf):
        super(FrontApp, self).__init__()
        self.django_app_conf = django_app_conf

    @property
    def alias(self):
        return self.django_app_conf.name

    @property
    def src_dir(self):
        return os.path.join(
            self.django_app_conf.path,
            'frontend',
            'src'
        )

    @property
    def entries(self):
        entries = []
        for filename in os.listdir(self.src_dir):
            root, ext = os.path.splitext(filename)
            if ext == '.js':
                entries.append(root)
        return entries

    
            

class Command(BaseCommand):
    help = ''

    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.sources_dir = os.path.join(CUR_DIR, 'makewebpack')
        self.project_frontend_dir = os.path.join(
            settings.BASE_DIR,
            'frontend',
        )

    def add_arguments(self, parser):
        parser.add_argument('-f', '--force', action='store_true')

    def install_packagejson(self, force):
        packagejson_src = os.path.join(
            self.sources_dir,
            'package.json'
        )

        packagejson_dst = os.path.join(
            self.project_frontend_dir,
            'package.json'
        )

        if not os.path.exists(packagejson_dst) or force:
            shutil.copyfile(
                packagejson_src,
                packagejson_dst
            )

    def handle(self, *args, **options):
        force = options['force']

        if not os.path.exists(self.project_frontend_dir):
            os.mkdir(self.project_frontend_dir)

        webpack_config_dst = os.path.join(
            self.project_frontend_dir,
            'webpack.config.js'
        )

        webpack_config_src = os.path.join(
            self.sources_dir,
            'webpack.config.init.js'
        )

        if not os.path.exists(webpack_config_dst) or force:
            shutil.copyfile(
                webpack_config_src,
                webpack_config_dst
            )

        fapps = []
        for app_config in apps.get_app_configs():
            if os.path.exists(os.path.join(app_config.path, 'frontend')):
                fapps.append(
                    FrontApp(app_config)
                )
        
        webpasck_aliases = {}
        webpasck_entries = {}
        for fapp in fapps:
            alias =  '@%s' % fapp.alias
            webpasck_aliases[alias] = fapp.src_dir

            for entry in fapp.entries:
                webpasck_entries[entry] = ["%s/%s" % (alias, entry),]

        webpack_alias_config_dst = os.path.join(
            self.project_frontend_dir,
            'webpack.config.alias.ext.json'
        )
        with open(webpack_alias_config_dst, 'w') as f:
            json.dump(webpasck_aliases, f, indent=4)

        webpack_enty_config_dst = os.path.join(
            self.project_frontend_dir,
            'webpack.config.entry.ext.json'
        )
        with open(webpack_enty_config_dst, 'w') as f:
            json.dump(webpasck_entries, f, indent=4)

        self.install_packagejson(force)
