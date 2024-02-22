import google.generativeai as palm
import asyncio
from pyppeteer import launch
import config

url = 'https://www.google.com/maps/place/Dona+J%C3%BA+Cozinha+Bar/@-15.8430724,-48.0307621,15z/data=!4m6!3m5!1s0x935a33d76674d223:0x136e446188b7d344!8m2!3d-15.8477393!4d-48.0265694!16s%2Fg%2F11jlfy2t6v?entry=ttu'

async def scrape_reviews(url):

    reviews = []

    print("Opening browser...")
    browser = await launch({"executablePath":'/usr/bin/google-chrome'  ,"headless": True, "args": ["--window-size=800, 3200"]})


    print("Opening new page...")
    page = await browser.newPage()
    await page.setViewport({"width": 800, "height": 3200})
    print("Going to url...")
    await page.goto(url)
    print("Selecting elements...")
    await page.waitForSelector(".jftiEf")


    elements = await page.querySelectorAll(".jftiEf")

    print("Looping elements...")
    for element in elements:

        more_btn = await element.querySelector(".w8nwRe")
        if more_btn is not None:
            await page.evaluate("button => button.click()", more_btn)
            await page.waitFor(5000)

        await page.waitForSelector(".MyEned")
        snippet = await element.querySelector(".MyEned")
        text = await page.evaluate("selected => selected.textContent", snippet)
        reviews.append(text)
        print(text)

    print("Closing browser...")
    await browser.close()

    return reviews



reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(url))
