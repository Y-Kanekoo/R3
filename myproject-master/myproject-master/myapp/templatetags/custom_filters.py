from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """辞書のキーに基づいて値を取得するフィルタ"""
    return dictionary.get(key)
