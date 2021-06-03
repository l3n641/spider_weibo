import asyncio, time
from pyppeteer import launch


async def main(cookie_list, dir_path):
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-infobars'])
    try:

        page = await browser.newPage()  # 打开新的标签页
        for item in cookie_list:
            await page.setCookie(item)
        await page.setViewport({'width': 1920, 'height': 1080})  # 页面大小一致
        await page.goto('https://weibo.com/')  # 访问主页

        # evaluate()是执行js的方法，js逆向时如果需要在浏览器环境下执行js代码的话可以利用这个方法
        # js为设置webdriver的值，防止网站检测
        await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

        time.sleep(10)

        screenshot_path = os.path.join(dir_path, "screenshot.png")
        await page.screenshot({'path': screenshot_path})

        cookies = await page.cookies()

        if cookies:
            cookie_srt = ""
            for cookie in cookies:
                coo = "{}={};".format(cookie.get("name"), cookie.get("value"))
                cookie_srt += coo

            cookie_str_path = os.path.join(dir_path, "cookies")
            with open(cookie_str_path, 'w') as f:
                f.write(cookie_srt)
            print(cookie_srt)

            cookie_json_path = os.path.join(dir_path, "cookies.json")
            with open(cookie_json_path, 'w') as f:
                json.dump(cookies, f)

        time.sleep(2)
    except Exception as e:
        raise e
    finally:
        await browser.close()


if __name__ == '__main__':
    import json, argparse, os

    parser = argparse.ArgumentParser(description='argparse')
    parser.add_argument('--dir_path', '-p', help='cookie 保存目录,默认是当前文件夹', default='.')
    args = parser.parse_args()
    dir_path = args.dir_path
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    cookie_file_path = os.path.join(dir_path, "cookies.json")
    with open(cookie_file_path) as file:
        cookie_list = json.load(file)
    if not cookie_list:
        raise ValueError("cookie not found")

    asyncio.get_event_loop().run_until_complete(main(cookie_list, dir_path))  # 调用
