from django.http import HttpResponse


def SetCookie(request):
    try:
        times = request.COOKIES['times']
        response = HttpResponse(f'You are visiting the page before: {times} times')
        response.set_cookie('times', int(times) +1)
    except KeyError:
        response = HttpResponse('Visiting for the first time')
        response.set_cookie('times', 1)

    return response

def GetCookie(request):
    times = request.COOKIES['times']
    return HttpResponse(f'Visiting to page : {times} times')

