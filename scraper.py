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
            for line in f:
                print("Processing: " + str(line.strip()))
                try:
                    browser=self.createBrowserInstance()
                    self.executeQuery(browser, line)
                    self.closeBrowserInstance(browser)
                except:
                    print("Issue scraping device: " + line.strip())
                    self.closeBrowserInstance(browser)
                    self.invalid.append(line.strip())

        # View results
        self.viewResults(filename)

    # Creates Browser instance
    def createBrowserInstance(self):
        # Firefox options
        opts=Options()
        opts.headless=True

        # Browser commands
        return webdriver.Firefox(options=opts)

    # Executes Browser queries
    def executeQuery(self, browser, ip):
        browser.get("http://" + str(ip) + "/basic")
        browser.refresh()

        # Gather data
        xpath="//*[@id='Status']/table"

        # Parses data
        result=self.processOutput(WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, xpath))))

        # Store info
        self.results.append((ip, result))

    # Writes data to temp file and parses it
    def processOutput(self, data):
        m=""
        p=""
        s=""

        with open(BUFFER, "w+") as w:
            w.write(data.text)

        with open(BUFFER, "r") as r:
            for line in r:
                if ("Product Name" in line and "Serial Number" in line):
                    line=line.replace("Serial Number",":Serial Number").split(':')
                    if ("Product Name" == line[0] and "Serial Number" == line[2]):
                        p=line[1].strip()
                        s=line[3].strip()
                if ("MAC Address" in line):
                    line=line.replace("MAC Address",":MAC Address").split(':')
                    if ("MAC Address" == line[2] or ":MAC Address" == line[2]):
                        m=line[3].strip()
                    elif ("MAC Address" == line[1]):
                        m=line[2].strip().split(" ")[0]

        # Returns data as tuple
        return (p,s,m)

    def closeBrowserInstance(self, browser):
        browser.quit()

    def viewResults(self, filename):
        with open("results/" + filename.replace(".txt", "") + "_results.csv", "w") as f:
            for r in self.results:
                f.write(r[0].strip() + "," + str(r[1][0]) + "," + str(r[1][1]) + "," + str(r[1][2]) + "\n")

    def viewInvalid(self):
        for i in self.invalid:
            print("[" + i + "]")

# Execute
s=Scraper()
