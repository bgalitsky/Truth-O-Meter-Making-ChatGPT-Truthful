import os
import webbrowser

from pandas.io.clipboard import clipboard_get

from fact_checker_via_web import FactCheckerViaWeb

fact_checker = FactCheckerViaWeb()

text = clipboard_get()

filename = fact_checker.perform_and_report_fact_check_for_text(text)
path = os.getcwd() + '/'+ filename

osname = os.name
if osname == 'posix':
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
elif osname == 'ntt':
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
else:
    chrome_path = '/usr/bin/google-chrome %s'

webbrowser.get(chrome_path).open(path)



