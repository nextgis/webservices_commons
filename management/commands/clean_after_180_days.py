import shutil

from django.core.management.base import BaseCommand
from django.conf import settings
import os
import time
from datetime import datetime
import argparse


class Command(BaseCommand):
    help = 'Clean old data from FTP'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--folder', type=str)
        parser.add_argument('--do_delete', type=int)

    def handle(self, *args, **options):
        folder = options['folder']
        do_delete = options['do_delete']
        while True:
            try:
                # folder = settings.SENDFILE_ROOT
                print(f'clean_after_180_days: examining folder {folder}')
                if do_delete:
                    print('WITH DELETE OPTION!')

                now = time.time()
                i = 0
                files = []
                for f in os.listdir(folder):
                    ff = os.path.join(folder, f)
                    files.append(ff)
                files.sort(key=os.path.getmtime)
                fsize_total = 0
                for f in files:
                    is_dir = os.path.isdir(f)
                    file = os.stat(f)
                    ago_180 = now - 180 * 86400
                    # ago_180 = now - 18
                    if file.st_mtime < ago_180:
                        i += 1
                        fcreated = datetime.fromtimestamp(file.st_mtime)
                        fcreated = fcreated.strftime('%Y-%m-%d %H:%M')
                        basename = os.path.basename(f)
                        if is_dir:
                            fsize = self._get_folder_size(f)
                            if do_delete == 1:
                                shutil.rmtree(f)
                        else:
                            fsize = os.path.getsize(f)
                            if do_delete == 1:
                                os.remove(f)
                        fsize_mb = self._get_fsize_mb(fsize)
                        fsize_total += fsize
                        print(f'[{i}] {fcreated}   ({fsize_mb} mb) {basename}')
                fsize_total = self._get_fsize_mb(fsize_total)
                print(f'====================================\r\nTOTAL FSIZE: {fsize_total} mb')
            except Exception as e:
                print(e)
            finally:
                time.sleep(3600)

    @classmethod
    def _get_folder_size(cls, start_path='.'):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)

        return total_size

    def _get_fsize_mb(self, fsize):
        fsize = fsize / (1024 * 1024)
        fsize = round(fsize)
        return fsize
