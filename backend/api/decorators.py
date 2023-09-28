from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def client_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='api/v1/login'):
    '''
    Decorator for views that checks that the logged in user is a client,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_client,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def lawyer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='api/v1/login'):
    '''
    Decorator for views that checks that the logged in user is a lawyer,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_lawyer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def judge_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='api/v1/login'):
    '''
    Decorator for views that checks that the logged in user is a judge,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_judge,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator