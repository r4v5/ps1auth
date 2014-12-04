# -*- coding: utf-8 -*-

# Scrapy settings for zoho project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'zoho'

SPIDER_MODULES = ['zoho.spiders']
NEWSPIDER_MODULE = 'zoho.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zoho (+http://www.yourdomain.com)'
#COOKIES_DEBUG = True
#LOG_LEVEL = 'INFO'
LOG_FILE = "zoho.log"
DUPEFILTER_DEBUG = True
#DOWNLOAD_DELAY = 0.25
