import logging

import anthropic
from django.conf import settings

logger = logging.getLogger('blog')

def generate_blog_post(topic: str) -> dict:
    logger.debug('Calling Claude API: topic=%s', topic)
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Write a blog post about: {topic}

                Return your response in this exact format:
                TITLE: <the title here>
                CONTENT: <the full blog post content here>
                """
            }
        ]
    )

    response_text = message.content[0].text
    logger.debug('Claude API response received: tokens_used=%s', message.usage.output_tokens)

    lines = response_text.strip().split('\n')
    title = ''
    content = ''

    for i, line in enumerate(lines):
        if line.startswith('TITLE:'):
            title = line.replace('TITLE:', '').strip()
        elif line.startswith('CONTENT:'):
            content = '\n'.join(lines[i:]).replace('CONTENT:', '').strip()
            break

    if not title or not content:
        logger.warning('Claude response missing title or content: topic=%s', topic)

    return {
        'title': title,
        'content': content
    }