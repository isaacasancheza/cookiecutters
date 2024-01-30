#!/usr/bin/env python3
import logging

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


logging.basicConfig()
logger = logging.getLogger('scraper')
logger.setLevel(logging.INFO)


def scrap():
    logger.info('starting webdriver...')
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    driver = Chrome(options=options)

    try:
        pass
    except Exception as e:
        logger.exception(e)
    except KeyboardInterrupt:
        logger.info('aborting...')
    finally:
        try:
            driver.quit()
        except:
            pass


if __name__ == '__main__':
    scrap()
