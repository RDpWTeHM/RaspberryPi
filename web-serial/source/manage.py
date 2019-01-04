#!/usr/bin/env python
import os
import sys

import threading
import traceback
#
# package path
#
try:
    _cwd = os.getcwd()
    _proj_abs_path = _cwd[0:_cwd.find("web-serial")]
    _package_path = os.path.join(_proj_abs_path, "source")
    if _package_path not in sys.path:
        sys.path.append(_package_path)

    # from serialpublisher import HwSubject
except Exception:
    traceback.print_exc()  # -[o] fix later by using argv
    sys.exit(1)


def Is_child_processing():
    from multiprocessing.connection import Listener
    from queue import Queue

    q = Queue()

    def lock_system_port(_port):
        nonlocal q  # it's OK without this announce line 
        try:
            listener = Listener(("", _port))
            q.put(False)
        except Exception:  # port be used by parent
            # traceback.print_exc()
            q.put(True)
            return  # child don't listen

        while True:
            serv = listener.accept()  # just bind the port.

    t = threading.Thread(target=lock_system_port, args=(62771, ))
    t.setDaemon(True)
    t.start(); del t;
    return q.get()


#
# open browser(like $ jupyter notebook)
# Reference `execute_from_command_line`
def delay_enable_browser(argv):
    try:
        subcommand = argv[1]  # manage.py runserver
    except IndexError:
        pass

    if subcommand == 'runserver' and '--noreload' not in argv:
        try:
            parser_port = argv[2]
            port_with_colon = parser_port[parser_port.index(":"):]
        except (IndexError, ValueError):
            port_with_colon = ":8000"
        finally:
            import webbrowser
            # time.sleep(0.5)
            webbrowser.open_new("http://localhost" + port_with_colon + "/serialcom/")


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'source.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if Is_child_processing():
        t = threading.Thread(target=delay_enable_browser, args=(sys.argv, ))
        t.start(); del t;

        #
        # web serial Top subject init
        #
        from serialcom.serial import designpattern as dsigpt
        obj = dsigpt.HwSubject()
        print("[Test] HwSubject().isPlug('COM20'): {!r}".format(obj.isPlug('COM20')),
              file=sys.stderr)
        obj.run()

    execute_from_command_line(sys.argv)
