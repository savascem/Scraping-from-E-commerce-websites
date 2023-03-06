# imports

import pandas as pd
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Target Variables

product_id = []
product_image = []
brand = []
title = []
rate = []
price = []
color_option = []
product_link = []
free_shipping = []
fast_delivery = []
buy_more_pay_less = []
coupon = []
buy_with_selected_products = []
product_video = []
size_option = []
comment_with_photo = []


# Scraping

def product_scraping(target_url, page_start=1, page_end=50):

    for page_number in range(page_start, page_end):

        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get(target_url.format(page_number))
        browser.maximize_window()
        time.sleep(3)

        if page_number <= page_end:

            for product in range(0,24):

                if product <= 23:

                    #get product id

                    product_id_ = browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].get_attribute("data-id")
                    product_id.append(product_id_)


                    # get product image

                    product_image_link_ = browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].find_element(by=By.CLASS_NAME, value= "p-card-img").get_attribute("src")
                    product_image.append(product_image_link_)


                    # get brand

                    brand_ = browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].find_element(by= By.CLASS_NAME , value="prdct-desc-cntnr-ttl").text
                    brand.append(brand_)


                    # get title

                    title_ = browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].find_element(by=By.CLASS_NAME, value="prdct-desc-cntnr-name").text
                    title.append(title_)


                    # get rate

                    rate_ = browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].find_element(by=By.CLASS_NAME, value="ratingCount").text
                    rate.append(rate_)


                    # get price

                    price_ = browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].find_element(by=By.CLASS_NAME, value="prc-box-dscntd").text
                    price.append(price_)


                    # get color option

                    try:
                        color_option_ = browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].find_element(by=By.CLASS_NAME, value="color-variant-count").text
                        color_option.append(color_option_)
                    except:
                        color_option.append(0)


                    # get product link

                    product_link_ = browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].find_element(by=By.CSS_SELECTOR, value="div.p-card-chldrn-cntnr.card-border > a").get_attribute("href")
                    product_link.append(product_link_)


                    # get (Free shipping) and (Fast delivery)

                    shipping_ = browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].find_elements(by=By.CLASS_NAME, value="image-overlay")[0].text
                    [free_shipping.append(1) if ("KARGO BEDAVA" in shipping_) == True else free_shipping.append(0)]
                    [fast_delivery.append(1) if ("HIZLI TESLİMAT" in shipping_) == True else fast_delivery.append(0)]


                    # get (Buy More Pay Less) /// (Coupon) /// (Buy with Selected Products) /// (Product Video)

                    any_coupon = browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].find_elements(by=By.CLASS_NAME, value="campaign-view-v2")[0].text
                    [buy_more_pay_less.append(1) if ("Çok Al Az Öde" in any_coupon) == True else buy_more_pay_less.append(0)]
                    [coupon.append(1) if ("Kupon Fırsatı" in any_coupon) == True else coupon.append(0)]
                    [buy_with_selected_products.append(1) if ("Birlikte Al Kazan" in any_coupon) == True else buy_with_selected_products.append(0)]
                    [product_video.append(1) if ("Videolu Ürün" in any_coupon) == True else product_video.append(0)]


                    # get size-option

                    try:
                        size_option_ =  browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].find_elements(by=By.CSS_SELECTOR, value="img[src*='genisbeden']")[0].get_attribute("src")
                        [size_option.append(1) if ("genisbeden" in size_option_) == True else size_option.append(0)]
                    except:
                        size_option.append(0)


                    # get comment with photo

                    comment_with_photo_ = browser.find_elements(by=By.CLASS_NAME, value="with-campaign-view")[product].find_elements(by=By.CLASS_NAME, value="review-icon")
                    [comment_with_photo.append(1) if len(comment_with_photo_) == 1 else comment_with_photo.append(0)]

            browser.quit()
            time.sleep(2)


        else:
            break


url = "https://www.trendyol.com/sr?q=kad%C4%B1n%20ti%C5%9F%C3%B6rt&qt=kad%C4%B1n%20ti%C5%9F%C3%B6rt&st=kad%C4%B1n%20ti%C5%9F%C3%B6rt&os={}"
start = 1
end = 4

product_scraping(url, page_start=start, page_end=end)

# DataFrame creating

variables = [product_id, product_image, brand, title, rate, price,
             color_option, product_link, free_shipping, fast_delivery,
             buy_with_selected_products, coupon, buy_with_selected_products,
             product_video, size_option, comment_with_photo]

columns_ = ["product_id", "product_image", "brand", "title", "rate", "price",
             "color_option", "product_link", "free_shipping", "fast_delivery",
             "buy_with_selected_products", "coupon", "buy_with_selected_products",
             "product_video", "size_option", "comment_with_photo"]

df = pd.DataFrame()

for index,col in enumerate(columns_):
    df[col] = variables[index]
