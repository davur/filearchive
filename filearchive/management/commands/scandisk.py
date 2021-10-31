from django.core.management.base import BaseCommand, CommandError
from filearchive.models import *

import os

from datetime import datetime, timezone

class Command(BaseCommand):
    help = 'Scans a given path'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        for path in options['path']:
            self.stdout.write(self.style.SUCCESS(path))

            if os.path.isdir(path):
                name = os.path.basename(path)
                abspath = os.path.abspath(path)
                
                root = Root.objects.create(
                    name=name,
                    abspath=abspath,
                )

                self.scandir(path, root)
                print("")


    def scandir(self, path, root, indent=0, parent=None):
        print("%s%s" % ('\x1b[1K\r', path), end="")

        for entry in os.scandir(path):
            file_type = None
            scan = False

            if entry.is_symlink():
                typ = '> '
            elif entry.is_dir():
                if entry.name in ['.svn', '.git', 'venv', 'env', '__pycache__', 'node_modules', 'npm_modules']:
                    typ = '0 '
                else:
                    typ = '+ '
                    file_type = Path.FileType.DIRECTORY
                    if entry.name[-4:] == '.app':
                        scan = False
                    else:
                        scan = True
            elif entry.is_file():
                typ = '- '
                file_type = Path.FileType.FILE
            else:
                typ = '? '

            # print('%s%s%s' % ('    ' * indent, typ, entry.name))

            if file_type:
                st = entry.stat()

                if st.st_mtime:
                    dt = datetime.fromtimestamp(st.st_mtime, timezone.utc)
                else:
                    dt = None

                p = Path.objects.create(
                    name=entry.name,
                    root=root,
                    file_type=file_type,
                    parent=parent,
                    modified_time=dt
                )

            if scan:
                self.scandir(os.path.join(path, entry.name), root, indent=indent+1, parent=p)
