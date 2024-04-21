from typing import Optional

import requests
from bs4 import BeautifulSoup

from common.choises import BaseLinkType
from links.schemas import LinkSchema
from users.models import User


class MetaParser:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def get_meta_content(self, property: str) -> Optional[str]:
        meta = self.soup.find_all('meta', attrs={'property': property})
        return meta[0]['content'] if meta else None


class LinkParser:
    def __init__(self, user: User, url: str) -> None:
        self.url = url
        self.user = user

    def parse(self) -> LinkSchema:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_parser = MetaParser(soup)

        title = meta_parser.get_meta_content('og:title')
        description = meta_parser.get_meta_content('og:description')
        image = meta_parser.get_meta_content('og:image')
        link_type = meta_parser.get_meta_content('og:type')

        return LinkSchema(
            user=self.user,
            url=self.url,
            title=title,
            description=description,
            image=image,
            link_type=link_type,
        )


def get_user_link_data(user, url: str) -> LinkSchema:
    link_parser = LinkParser(user, url)
    return link_parser.parse()


def type_link(link_data: LinkSchema) -> LinkSchema:
    if link_data.link_type is not None:
        if link_data.link_type[0:5] == BaseLinkType.video:
            link_data.link_type = BaseLinkType.video
            return link_data
        elif link_data.link_type[0:4] == BaseLinkType.book:
            link_data.link_type = BaseLinkType.book
            return link_data
        elif link_data.link_type[0:6] == BaseLinkType.article:
            link_data.link_type = BaseLinkType.article
            return link_data
        elif link_data.link_type[0:5] == BaseLinkType.music:
            link_data.link_type = BaseLinkType.music
            return link_data
        else:
            link_data.link_type = BaseLinkType.website
        return link_data
    else:
        link_data.link_type = BaseLinkType.website
        return link_data
