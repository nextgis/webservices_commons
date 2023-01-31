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

                now = time.time()
                i = 0
                files = []
                for f in os.listdir(folder):
                    ff = os.path.join(folder, f)
                    files.append(ff)
                files.sort(key=os.path.getmtime)
                fsize_total = 0
                for f in files:
                    file = os.stat(f)
                    ago_180 = now - 180 * 86400
                    # ago_180 = now - 18
                    if file.st_mtime < ago_180:
                        i += 1
                        fsize = os.path.getsize(f)
                        fsize_total += fsize
                        fsize = self._get_fsize_mb(fsize)
                        fcreated = datetime.fromtimestamp(file.st_mtime)
                        fcreated = fcreated.strftime('%Y-%m-%d %H:%M')
                        basename = os.path.basename(f)
                        if do_delete == 1:
                            os.remove(f)
                        print(f'[{i}] {fcreated}   ({fsize} mb) {basename}')
                fsize_total = self._get_fsize_mb(fsize_total)
                print(f'====================================\r\nTOTAL FSIZE: {fsize_total} mb')
            except Exception as e:
                print(e)
            finally:
                time.sleep(3600)

    def _get_fsize_mb(self, fsize):
        fsize = fsize / (1024 * 1024)
        fsize = round(fsize)
        return fsize
