import asyncio, time
from pyppeteer import launch


async def main(cookie_list):
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-infobars'])

    page = await browser.newPage()  # 打开新的标签页
    for item in cookie_list:
        await page.setCookie(item)
    await page.setViewport({'width': 1920, 'height': 1080})  # 页面大小一致
    await page.goto('https://weibo.com/')  # 访问主页

    # evaluate()是执行js的方法，js逆向时如果需要在浏览器环境下执行js代码的话可以利用这个方法
    # js为设置webdriver的值，防止网站检测
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

    cookie_list = await page.cookies()
    cookies = ""
    for cookie in cookie_list:
        coo = "{}={};".format(cookie.get("name"), cookie.get("value"))
        cookies += coo

    with open("./cookies", 'w') as f:
        f.write(cookies)
    print(cookies)
    time.sleep(2)

    await page.close()
    await browser.close()


if __name__ == '__main__':
    import json

    cookie_file_path = "./cookies.json"
    with open(cookie_file_path) as file:
        cookie_list = json.load(file)
    if not cookie_list:
        raise ValueError("cookie not found")
    asyncio.get_event_loop().run_until_complete(main(cookie_list))  # 调用
