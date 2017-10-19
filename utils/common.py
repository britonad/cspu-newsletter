from urllib.parse import urlparse


def parse_url(url):
    site_url = urlparse(url)
    return '{}://{}'.format(site_url.scheme, site_url.hostname)
