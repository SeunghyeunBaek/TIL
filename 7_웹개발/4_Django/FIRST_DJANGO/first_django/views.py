from django.shortcuts import HttpResponse  # django 는 string 을 출력할 수 없다.
from django.shortcuts import render  # html page 반환


def index(request):
    return render(request, 'index.html')
    # print(request.META)
    # return HttpResponse('hi')


# variable routing, name 을 인자로 받는다.
def hello(request, name):
    greeting = f'Hello, {name} :)'
    return render(request, 'hello.html', {'greeting': greeting})
    # return HttpResponse(greeting)
