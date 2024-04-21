from django.db.models import TextChoices


class BaseLinkType(TextChoices):
    website = "website"
    book = "book"
    article = "article"
    music = "music"
    video = "video"