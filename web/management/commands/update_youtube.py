# -*- coding: utf-8 -*
import logging

from django.core.management.base import BaseCommand

from web.usecase.YoutubeUpdateService import YoutubeUpdateService

logger = logging.getLogger("update_yt")


class Command(BaseCommand):
    """
    " Main Process
    """

    def handle(self, *args, **options):
        logger.info("update_youtube")
        service = YoutubeUpdateService()
        service.update_all()
