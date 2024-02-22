import google.generativeai as palm
import asyncio
from pyppeteer import launch
import config

print("--------------------------------")
url = input("Enter a URL from a place in Google Maps (in english): ")

async def scrape_reviews(url):

    reviews = []
    print("--------------------------------")
    print("Fetching reviews")
    browser = await launch({"executablePath":'/usr/bin/google-chrome'  ,"headless": True, "args": ["--window-size=800, 3200"]})
    print(".")


    
    page = await browser.newPage()
    print("..")
    await page.setViewport({"width": 800, "height": 3200})
    print("...")
    
    await page.goto(url)
    print("....")
    
    await page.waitForSelector(".jftiEf")
    print(".....")


    elements = await page.querySelectorAll(".jftiEf")
    print("......")

    
    for element in elements:

        try:
            more_btn = await element.querySelector(".w8nwRe")
            if more_btn is not None:
                await page.evaluate("button => button.click()", more_btn)
                await page.waitFor(5000)
        except:
            pass

        await page.waitForSelector(".MyEned")
        snippet = await element.querySelector(".MyEned")
        text = await page.evaluate("selected => selected.textContent", snippet)
        reviews.append(text)
        

    
    await browser.close()
    print(".......")
    print("........ Done")

    return reviews

def summarize(reviews, model):
    
    prompt = "I collected some reviews of a place I was considering visiting. Can you summarize the reviews for me?"
    
    for review in reviews:
        prompt += "\n" + review

    print("--------------------------------")
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=800,
    )

    print(completion.result)
    print("--------------------------------")


palm.configure(api_key=config.API_KEY)
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name


reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(url))

summarize(reviews, model)
