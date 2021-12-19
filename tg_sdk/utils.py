import re
import logging
from subprocess import check_output, CalledProcessError
from contextlib import contextmanager
from tempfile import NamedTemporaryFile


def get_logger(logger_name=None):
    logger_name = logger_name or 'tg_sdk_logger'
    return logging.getLogger(logger_name)


def basic_executor(command, *args, **kwargs):
    if isinstance(command, str):
        command = command.split(' ')
    if 'logger' in kwargs:
        kwargs.pop('logger')
    try:
        result = check_output(command, *args, **kwargs)
    except CalledProcessError as e:
        result = str(e)
    if isinstance(result, bytes):
        return result.decode('utf-8').strip()
    return result.strip()


def dump_hcl(data, file_obj):
    hcl_data = translate_hcl(data)
    file_obj.write(hcl_data)


def translate_hcl(data):
    pass


def get_version_string(output):
    result = re.search(r'([\d.]+)', output)
    if result:
        return result.group(1)


@contextmanager
def yield_file(content):
    with NamedTemporaryFile() as f:
        f.write(content)
        f.flush()
        yield f.name
