from django import template

register = template.Library()


@register.filter
def hash_tag_link(post):
    # content 를 hash_tag 와 content_text 로 분리
    # hash_tag 에 a tag 를 붙여서 반환
    content = post.content
    hash_tags = post.hash_tags.all()
    for hash_tag in hash_tags:
        content = content.replace(
            f'{hash_tag.content}',
            f'<a href="/posts/hash_tags/{hash_tag.id}">{hash_tag.content}</a>'
        )
    return content
