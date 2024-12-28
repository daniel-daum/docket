from playwright.sync_api import sync_playwright, Page, expect
import pandas as pd
import time

trial_data = []
TIMEOUT = 7000  # Consistent timeout value

with sync_playwright() as p:
    browser = p.webkit.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.jagcnet.army.mil/Apps/eDocket/eDocketPublic.nsf/Case_List.xsp?refreshed=true")

    for i in range(1,31):

        link = page.locator('table').locator('tr').nth(i).locator('td').nth(0)
        name = page.locator('table').locator('tr').nth(i).locator('td').nth(0).inner_text()
        rank = page.locator('table').locator('tr').nth(i).locator('td').nth(1).inner_text()
        date = page.locator('table').locator('tr').nth(i).locator('td').nth(2).inner_text()
        judge = page.locator('table').locator('tr').nth(i).locator('td').nth(3).inner_text()
        base = page.locator('table').locator('tr').nth(i).locator('td').nth(4).inner_text()
        circuit = page.locator('table').locator('tr').nth(i).locator('td').nth(5).inner_text()


        popup:Page
        with page.expect_popup() as popup:
            link.locator('a').click()
            popup = popup.value

            url = popup.url
            charges = popup.locator('span').nth(3).inner_html()
            proceeding_type = popup.locator('table').nth(1).locator('tr').nth(0).locator('td').inner_text()
            plea_forum = popup.locator('table').nth(2).locator('tr').nth(0).locator('td').nth(0).inner_text()


            # popup.close()

        trial_data.append({
            'name':name,
            'rank':rank,
            'date':date,
            'judge':judge,
            'base':base,
            'circuit':circuit,
            # 'url':url,
            # 'charges':charges,
            # 'proceeding_type':proceeding_type,
            # 'plea_forum':plea_forum
        })

    time.sleep(400)
    browser.close()

# df = pd.DataFrame(trial_data)
# df.to_csv('test.csv')