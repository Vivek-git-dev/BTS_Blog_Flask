import bleach

def sanitize_html(html_content):
    allowed_tags = [
        "p", "br", "strong", "b", "i", "em", "u",
        "ul", "ol", "li",
        "blockquote",
        "a",
        "h1", "h2", "h3", "h4", "h5", "h6",
        "pre", "code"
    ]

    allowed_attrs = {
        "a": ["href", "title", "target", "rel"],
        "img": ["src", "alt"]
    }

    return bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )
