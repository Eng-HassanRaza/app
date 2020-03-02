# -*- coding: utf-8 -*
import logging

from django.core.management.base import BaseCommand

from web.usecase.InstagramUpdateService import InstagramUpdateService

logger = logging.getLogger("update_in")


class Command(BaseCommand):
    """
    " Main Process
    """

    def handle(self, *args, **options):
        logger.info("update_instagram")
        service = InstagramUpdateService()
        service.update_all()
