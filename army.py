from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.webkit.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.jagcnet.army.mil/Apps/eDocket/eDocketPublic.nsf/Case_List.xsp?refreshed=true")


    for i in range(1,2):

        name = page.locator('table').locator('tr').nth(i).locator('td').nth(0)
        print(name.inner_text())
        link = name.locator('a').click()
        print(link)

    time.sleep(400)
    browser.close()