from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from .models import UserAccount


def client_required(
        function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='api/v1/login'):
    '''
    Decorator for views that checks that the logged in user is a client,
    redirects to the log-in page if necessary.

    :param function: The view function to decorate.
    :param redirect_field_name: The name of the query string parameter representing the URL to redirect to after login.
    :param login_url: The URL to redirect to if the user is not authenticated.
    :return: The decorated view function.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == UserAccount.Roles.CLIENT,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def lawyer_required(
        function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='api/v1/login'):
    '''
    Decorator for views that checks that the logged in user is a lawyer,
    redirects to the log-in page if necessary.

    :param function: The view function to decorate.
    :param redirect_field_name: The name of the query string parameter representing the URL to redirect to after login.
    :param login_url: The URL to redirect to if the user is not authenticated.
    :return: The decorated view function.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == UserAccount.Roles.LAWYER,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def judge_required(
        function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='api/v1/login'):
    '''
    Decorator for views that checks that the logged in user is a judge,
    redirects to the log-in page if necessary.

    :param function: The view function to decorate.
    :param redirect_field_name: The name of the query string parameter representing the URL to redirect to after login.
    :param login_url: The URL to redirect to if the user is not authenticated.
    :return: The decorated view function.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.user_type == UserAccount.Roles.JUDGE,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
