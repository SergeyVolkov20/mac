from django.shortcuts import render

def index(request):
    context = {
        'club_name': 'COLIZEUM МИРА 55',
        'address': 'ПРОСПЕКТ МИРА 55, СУРГУТ',
        'description': 'COLIZEUM Сургут - это компьютерный клуб, оснащенный передовым оборудованием, которое соответствует всем требованиям современных игр.',
    }
    return render(request, 'index.html', context)
