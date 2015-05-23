# -*- coding: utf-8 -*-

# Scrapy settings for scrapers project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import sys
sys.path.append('/code/stereo8')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'stereo8.settings'

BOT_NAME = 'scrapers'
SPIDER_MODULES = ['scrapers.spiders']
NEWSPIDER_MODULE = 'scrapers.spiders'
ITEM_PIPELINES = {'scrapers.pipelines.DjangoItemPipeline': 1}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'scrapers (+https://github.com/gjeck/stereo8)'
COOKIES_ENABLED = False

