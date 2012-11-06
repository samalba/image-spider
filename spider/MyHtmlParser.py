# -*- coding: ascii -*-

from data import data
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag
from validate_url import validate_url

class MyHtmlParser(HTMLParser):

    def __init__(self, url):
        self.url = url
        self.hyperlinks = []
        super(MyHtmlParser, self).__init__()


    def handle_base(self, href):
        if href:
            self.url = href


    def handle_a(self, href):
        if href:
            validated_href = validate_url(href, self.url)
            if validated_href['valid']:
                target = urldefrag(urljoin(self.url, validated_href['url']))[0]
                self.hyperlinks.append(target)


    def handle_img(self, src):
        if src:
            if 2048 < len(src):
                # Ignore obscenely long image URLs. They're probably data: URLs,
                # but in any case they're not worth the storage space.
                return
            relate_image = data.pg.proc('relate_image(text,text)')
            relate_image(self.url, urljoin(self.url, src))


    def handle_starttag(self, tag, attrs):

        def get_attr(arg_attr):
            matching_attrs = [attr for attr in attrs if arg_attr == attr[0]]
            return matching_attrs[0][1] if len(matching_attrs) else None

        if 'base' == tag:
            self.handle_base(get_attr('href'))

        elif 'a' == tag:
            self.handle_a(get_attr('href'))

        elif 'img' == tag:
            self.handle_img(get_attr('src'))
