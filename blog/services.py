import anthropic
from django.conf import settings

def generate_blog_post(topic: str) -> dict:
    """
    Takes a topic string and returns a dict with
    generated title and content from Claude.
    """
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

    # Parse the response
    lines = response_text.strip().split('\n')
    title = ''
    content = ''

    for i, line in enumerate(lines):
        if line.startswith('TITLE:'):
            title = line.replace('TITLE:', '').strip()
        elif line.startswith('CONTENT:'):
            content = '\n'.join(lines[i:]).replace('CONTENT:', '').strip()
            break

    return {
        'title': title,
        'content': content
    }