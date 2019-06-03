from django.shortcuts import render


def index(request):
    return render(request, 'utils/index.html')


def artii(request, keyword):
    import art
    result = art.text2art(keyword, font='random')
    context = {
        'result': result,
        'keyword': keyword
    }
    return render(request, 'utils/art.html', context)


def stock(request):
    pass  # todo : 완성하기




