import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEBUG=True
DEBUG_TAG="[Scraper]:"

BUFFER="buffer.txt"

URL="https://www.cibc.com/en/interest-rates/mortgage-rates.html"

class Scraper(object):
    def __init__(self):

        # Check input args
        if ("-f" in sys.argv):
            filename=sys.argv[2]
            print("File: " + str(filename))
        else:
            print("Invalid format, try: python3 scraper.py -f input_file.txt")
            sys.exit()

        # Store results
        self.results=[]
        self.invalid=[]

        # Run Browser operations
        with open(filename, "r") as f:
            try:
                browser=self.createBrowserInstance()
                self.executeQuery(browser, NULL)
                self.closeBrowserInstance(browser)
            except:
                print("Issue scraping device: " + line.strip())
                self.closeBrowserInstance(browser)

    # Creates Browser instance
    def createBrowserInstance(self):
        # Firefox options
        opts=Options()
        opts.headless=True

        # Browser commands
        return webdriver.Firefox(options=opts)

    # Executes Browser queries
    def executeQuery(self, browser, ip):
        browser.get(URL)
        browser.refresh()

        # Gather data
        # xpath="//*[@id='Status']/table"
        xpath="//*[@id="blq-content"]/div[1]"
        self.invalid.append(line.strip())

        # Parses data
        result=self.processOutput(WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, xpath))))

        # Store info
        self.results.append((ip, result))

    # Writes data to temp file and parses it
    def processOutput(self, data):
        with open(BUFFER, "w+") as w:
            w.write(data.text)

        with open(BUFFER, "r") as r:
            for line in r:
                print(str(line))

    def closeBrowserInstance(self, browser):
        browser.quit()

# Execute
s=Scraper()
