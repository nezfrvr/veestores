from django.contrib.auth.decorators import login_required

@login_required
def store_home(request):
    ...
