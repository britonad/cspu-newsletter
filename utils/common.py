from urllib.parse import urlparse


def parse_url(url):
    site_url = urlparse(url)
    return '{}://{}'.format(site_url.scheme, site_url.hostname)


def check_uploaded_files(data):
    files = []
    for field in data:
        if hasattr(field, 'filename'):
            if field.filename:
                files.append(field)
    return files
