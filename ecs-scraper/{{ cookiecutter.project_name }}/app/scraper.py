#!/usr/bin/env python3
from aws_lambda_powertools import Logger
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

logger = Logger()


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
