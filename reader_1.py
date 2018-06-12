from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unicodedata


def after(value, a):
    # Find and validate first part.
    pos_a = value.rfind(a)
    if pos_a == -1:
        return ""
    # Returns chars after the found string.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value):
        return ""
    return value[adjusted_pos_a:]


def before(value, a):
    # Find first part and return slice before it.
    pos_a = value.find(a)
    if pos_a == -1:
        return ""
    return value[0:pos_a]


chromedriver = 'C:\\chromedriver.exe'
browser = webdriver.Chrome(chromedriver)
browser.get("https://whalewisdom.com/")

element1 = browser.find_element_by_id("ac_filer_stock_name")

element1.send_keys("tiger management")
time.sleep(3)
element1.send_keys(Keys.DOWN, Keys.RETURN)
time.sleep(3)

holdings = browser.find_element_by_css_selector("div[class='filerinfo summary']")

# Top Holding and %
topHold = before(after(holdings.text, 'Port')[0:7], ' ')
topHoldW = holdings.find_element_by_css_selector("span[class='precents']").text

summary = browser.find_element_by_css_selector("div[class='filerinfo activity']")

# Total AUM, Rent and Top 10%
AUM = float(before(summary.text[14:25], ' '))
print(AUM)
PrevAUM = float(before(after(summary.text, 'Prior Market Value $'), ' '))
print(PrevAUM)
rentQ = AUM/PrevAUM - 1
print(rentQ)
Top10 = float(before(after(summary.text, 'Holdings % '), 'Turnover')[:-3])
print(Top10)

browser.find_element_by_id("holdings_tab_link").click()

currentHoldings = browser.find_element_by_id("current_holdings_table")

totalFiled = browser.find_element_by_css_selector("span[class='pagination-info']").text
rows = int(before(totalFiled[18:], ' rows'))
print(rows)

if rows >= 25:
    a = currentHoldings.find_element_by_xpath("//th[@data-field='current_ranking']/div[1]")
    a.click()
    a.click()
    currentHoldings = browser.find_element_by_id("current_holdings_table")

totalPos = rows - currentHoldings.text.count("Sold All")
print(totalPos)

# browser.find_element_by_xpath("//button[@type='submit']").click()

# for i, df in enumerate(pd.read_html(url)):

# df.to_csv('myfile_%s.csv' % i)

# html = browser.get("").content

# df_list = pd.read_html(html)
# df = df_list[-1]
# print(df)

# df.to_csv('my data.csv')
