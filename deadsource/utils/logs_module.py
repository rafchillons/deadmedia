from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
import traceback


def get_logs_from_file(file):
    with open(file, 'r') as f:
        r = f.read()
        lines = r.splitlines()

    result = ''
    for line in lines:
        result = result + str(line) + '\n'

    return lines


def log_critical_decorator(logger):

    def inner_decorator(function_to_decorate):

        def wrapped(*args, **kwargs):
            try:
                return function_to_decorate(*args, **kwargs)

            except Exception as e:
                logger.critical(traceback.format_exc())
                return redirect('error500-page')

        return wrapped

    return inner_decorator
