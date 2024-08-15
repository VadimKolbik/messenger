from django import template
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser

register = template.Library()

@register.inclusion_tag('chats/tags/menu.html')
def menu_tag(request, active_page=0):
    if not isinstance(request.user, AnonymousUser):
        menu = [{'title': 'Мой профиль', 'href': reverse('users:profile', args=[request.user.pk]), 'active_num': 1},
                {'title': 'Мои сообщения', 'href': reverse('chats:all_chats'), 'active_num': 2},
                {'title': 'Люди', 'href': reverse('users:people'), 'active_num': 3}]
    else:
        menu = [{'title': 'Войти', 'href': reverse('users:login'), 'active_num': 4},
                {'title': 'Зарегистрироваться', 'href': reverse('users:signup'), 'active_num': 5}]
    return {'request': request, 'menu': menu, 'active_page': active_page}