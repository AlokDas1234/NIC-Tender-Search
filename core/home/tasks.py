import time
import os
import re
import time
import json
from datetime import datetime, timedelta
# import multiprocessing as mp
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from celery import shared_task
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .models import Client, ScraperControl,Search
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from .models import TenderResults
from django.contrib.auth.models import User
# import logging
# logger = logging.getLogger("home.tasks")

# def create_driver():
#     options = Options()
#     options.add_argument("--headless=new")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--window-size=1920,1080")
#     return webdriver.Chrome(options=options)

def create_driver():
    options = Options()
    options.binary_location = os.environ.get("CHROME_BIN")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    return webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        options=options
    )



# @shared_task(bind=True, max_retries=0)
def run_scraper(self,user_id,search_id):
    # logger.warning("🔥 TASK STARTED user_id=%s search_id=%s", user_id, search_id)
    current_date = datetime.now().strftime("%Y%m%d-%H:%M")
    user = User.objects.get(id=user_id)
    # logger.info("User loaded: %s", user)
    if search_id:
        all_client = Search.objects.filter(user=user,id=search_id)
    else:
        all_client = Search.objects.filter(user=user)
    control, _ = ScraperControl.objects.get_or_create(user=user)
    # logger.info("Total searches found: %d", len(all_client))
    # print("All Clients:",all_client)
    for idx,client in enumerate(all_client):
        driver=None
        try:
            # logger.info("🔁 Loop %d | Client=%s", idx, client)
            # print("Client:",client.user)
            # logger.info("Creating Chrome driver")
            driver = create_driver()
            # driver.set_page_load_timeout(120)
            # driver.set_script_timeout(120)
            search_key_values_list = client.search_key.split(',')
            state_name_value = client.state_name
            excluded_values = client.exclude_key.split('|')

            site_url = client.site_url # "https://wbtenders.gov.in"
            searchkeys = search_key_values_list  # ["wire", "conductor"]
            for searchkey in searchkeys:
                control.user=user
                control.is_running = True
                control.searching_state_name =state_name_value
                control.searching_key = searchkey
                control.save()


                url = site_url
                # driver.delete_all_cookies()
                try:
                    driver.get(url)
                    time.sleep(1)
                    name = state_name_value  # site_url.removeprefix("https://").removesuffix(".gov.in")
                    WebDriverWait(driver, 35).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'body'))
                    )
                    search_bar = WebDriverWait(driver, 25).until(
                        EC.presence_of_element_located((By.ID, "SearchDescription"))
                    )
                    assert search_bar is not None, "Error: Search bar not found!"
                    # print("................................................................")
                    search_bar.clear()
                    search_bar.send_keys(searchkey)
                    search_bar.send_keys(Keys.RETURN)
                    # print("Searching for: ", searchkey)
                    time.sleep(2)

                    lnk = findeachlink(driver,excluded_values, url, searchkey,user)

                    # assert len(lnk) > 0, f"Error: No links found for {searchkey}!"
                    # print("State Name: ", state_name_value)
                    # print("Total links: ", len(lnk))
                    # ScraperControl.objects.create(user=user,is_running=True,searching_state_name=name,searching_key=searchkey)
                    data=opensuburl(driver,lnk, name, searchkey, excluded_values,user,current_date)

                except Exception as e:
                    print(f"Error for {client.state_name} | {searchkey}: {e}")
                    # driver.quit()

                    # raise self.retry(exc=e, countdown=10)
        finally:
            if driver:
                driver.quit()
            # finally:
            #     driver.quit()  # 🔥 VERY IMPORTANT
            #     # control.is_running = False
            #     # control.searching_state_name = ""
            #     # control.searching_key = ""
            #     # control.save()

        # control.is_running = False
        # control.searching_state_name = ""
        # control.searching_key = ""
        # control.save()



def opensuburl(driver,lnk, name, searchkey, excluded_values,user,current_date):
    '''' This function is used to perform main operation like extract description, Tender submision end data, emd amount etc'''
    # entries_without_spaces = [entry.strip() for entry in search_field_values_list]

    entries = ["Tender ID", "Work Description", "Organisation Chain", "Bid Submission End Date", "Tender Value in ₹",
               "EMD Amount in ₹", "Tender Fee in ₹"]
    # print("Entries", entries)
    data_list = []

    for link in lnk:
        driver.get(link)
        time.sleep(2)
        WebDriverWait(driver, 35).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        # time.sleep(1)
        updated_content = driver.page_source
        soup = BeautifulSoup(updated_content, 'html.parser')

        entry_dict = {}

        for _, entry in enumerate(entries):
            try:

                # Find the first "td_caption" element containing the specified entry text
                tender_element = soup.find('td', {'class': 'td_caption'}, string=str(entry))
                td_field_element = tender_element.find_next('td', {'class': 'td_field'})
                # Access the text of the "td_field" element
                tender_value = td_field_element.get_text(strip=True)

                if entry == "Work Description" and excluded_values != ['']:
                    # exclude_check = any(value.lower() in tender_value.lower() for value in excluded_values)
                    exclude_pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, excluded_values)) + r')\b',
                                                 flags=re.IGNORECASE)
                    exclude_check = exclude_pattern.search(tender_value)
                    if exclude_check:
                        break
                entry_dict["Current_Date"] = current_date
                # print("Current Date: ", current_date)
                if entry == "Bid Submission End Date":
                    bid_submission_end_date = tender_value.split(" ")[0]
                    bid_submission_end_time = ' '.join(tender_value.split(" ")[1:])
                    entry_dict["Bid Submission End Date"] = bid_submission_end_date
                    entry_dict["Bid Submission End Time"] = bid_submission_end_time
                    entry_dict["Name of Site"] = name
                    entry_dict["Search Key"] = searchkey
                    # print("............................................................")
                    # print("Bid Submission End Date t: ", bid_submission_end_date)
                    # print("Bid Submission End Time t: ", bid_submission_end_time)
                    # print("Name of Site: ",name)
                    # print("Search Key: ",searchkey)
                else:

                    assert isinstance(tender_value, str), f"Error: Invalid value found for {entry}"
                    assert len(tender_value.strip()) > 0, f"Error: Empty value extracted for {entry}"
                    # print("Entry t:",entry)
                    # print("Tender value else t:",tender_value)
                    entry_dict[entry] = tender_value
                    entry_dict["Name of Site"] = name
                    entry_dict["Search Key"] = searchkey
                    entry_dict["Link"] = link
                    # print("Name of Site t: ", name)
                    # print("Search Key t: ", searchkey)
                    # time.sleep(1)
                    # print(entry, ": ", tender_value)
                    if "," in tender_value:
                        tender_value = tender_value.replace(",", "")
            except:

                tender_elements = soup.find_all(
                    lambda tag: tag.name == 'td' and 'td_caption' in tag.get('class',
                                                                             []) and f'{str(entry)}' in tag.text)


                for tender_element in tender_elements:
                    # Find the corresponding "td_field" element
                    td_field_element = tender_element.find_next('td', {'class': 'td_field'})
                    tender_value = td_field_element.get_text(strip=True)
                    if entry == "Work Description" and excluded_values != ['']:
                        # exclude_check = any(value.lower() in tender_value.lower() for value in excluded_values)
                        exclude_pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, excluded_values)) + r')\b',
                                                     flags=re.IGNORECASE)
                        exclude_check = exclude_pattern.search(tender_value)
                        if exclude_check:
                            break
                    entry_dict["Current_Date"] = current_date

                    if entry == "Bid Submission End Date":
                        bid_submission_end_date = tender_value.split(" ")[0]
                        bid_submission_end_time = ' '.join(tender_value.split(" ")[1:])
                        entry_dict["Bid Submission End Date"] = bid_submission_end_date
                        entry_dict["Bid Submission End Time"] = bid_submission_end_time
                        entry_dict["Name of Site"] = name
                        entry_dict["Search Key"] = searchkey
                        # print("............................................................")
                        # print("Bid Submission End Date e: ", bid_submission_end_date)
                        # print("Bid Submission End Time e: ", bid_submission_end_time)

                    else:
                        if "," in tender_value:
                            tender_value.replace(",", " ")

                        entry_dict[entry] =tender_value
                        entry_dict["Name of Site"] = name
                        entry_dict["Search Key"] = searchkey
                        entry_dict["Link"] = link

                        # print("Name of Site e: ", name)
                        # print("Search Key e: ", searchkey)
                        # time.sleep(1)
        if len(entry_dict) > 5:
            # print("entry_dict:",entry_dict)
            data_list.append(entry_dict)

    bulk_objects = [
        TenderResults(
            search_time=row.get("Current_Date", ""),
            tender_id=row.get("Tender ID", ""),
            state_name=row.get("Name of Site", ""),
            search_key=row.get("Search Key", ""),
            site_link=row.get("Link", ""),
            work_description=row.get("Work Description", ""),
            organization_chain=row.get("Organisation Chain", ""),
            bid_submission_end_date=row.get("Bid Submission End Date", ""),
            bid_submission_end_time=row.get("Bid Submission End Time", ""),
            tender_value=row.get("Tender Value in ₹", ""),
            emd_amt=row.get("EMD Amount in ₹", ""),
            tender_fee=row.get("Tender Fee in ₹", ""),
            # user=user,
        )
        for row in data_list
    ]

    TenderResults.objects.bulk_create(
        bulk_objects,
        batch_size=500,
        ignore_conflicts=True
    )

    df = pd.DataFrame(data_list)
    # print("Data List:",data_list)
    # print("DF:",df)

    # df.to_csv(f"Tender-{name}-{searchkey}.csv", index=False)
    # assert not df.empty, "Error: No valid data extracted! DataFrame is empty."
    # if not df.empty:
    #     df.to_csv(f"Tender-{name}-{searchkey}.csv", index=False)



def extract_tender_id_from_td(td):
    tender_id=td.split("[")[3].replace("]", "")
    return tender_id

def findeachlink(driver, exclude_value, url,search_key,user):
    """"This function is used to find each sublink of tender  as pere search key"""
    all_links = []  # List to store links across multiple pages
    while True:
        updated_content = driver.page_source
        soup = BeautifulSoup(updated_content, 'html.parser')
        # print("HTML Content:",soup.prettify())
        tbody = soup.find('tbody')
        if not tbody:
            # print("No tbody")
            driver.delete_all_cookies()
            time.sleep(1)
            driver.get(url)
            time.sleep(2)
            # driver.implicitly_wait(5)
            # time.sleep(2)
            WebDriverWait(driver, 35).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            search_bar = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.ID, "SearchDescription"))
            )

            # print("................................................................")
            search_bar.send_keys(search_key)
            search_bar.send_keys(Keys.RETURN)
            # print("Searching again for: ", search_key)

            updated_content = driver.page_source
            soup = BeautifulSoup(updated_content, 'html.parser')
            # print("HTML Content:", soup.prettify())
            tbody = soup.find('tbody')

        if tbody:
            even_odd = tbody.find_all('tr', class_=["odd", "even"])
            lnk = []
            for row in even_odd:
                tds = row.find_all('td')
                try:
                    td_text = tds[4].get_text(" ", strip=True)
                    # print(td_text)
                    tender_id = extract_tender_id_from_td(td_text)
                    # print(tender_id)
                    if TenderResults.objects.filter(tender_id=tender_id).exists():
                        # print("⏭️ Skipping existing tender:", tender_id)
                        continue

                except Exception as e:
                    print(e)
                for td in tds:
                    try:
                        links = td.find_all('a', href=True)
                        for link in links:
                            href = link.get('href')
                            link_text = link.get_text()
                            # if exclude_value != [''] or not None:
                            if exclude_value and exclude_value != ['']:
                                # exclude_check = any(value.lower() in link_text.lower() for value in exclude_value)
                                exclude_pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, exclude_value)) + r')\b',
                                                             flags=re.IGNORECASE)
                                exclude_check = exclude_pattern.search(link_text)
                                if not exclude_check and href:
                                    cleaned_url = re.sub(r'\.gov\.in.*$', '.gov.in', url)
                                    # print("Link Not Excluded", cleaned_url + href)

                                    # print("Link Not Excluded", link_text)
                                    lnk.append(cleaned_url + href)
                            else:
                                if href:
                                    cleaned_url = re.sub(r'\.gov\.in.*$', '.gov.in', url)
                                    # print("Link Not Excluded",cleaned_url+href)
                                    # print("Link Not Excluded", link_text)
                                    lnk.append(cleaned_url+href)

                    except StaleElementReferenceException:
                        # pass
                        # Handle stale session by restarting
                        handle_stale_session(driver)
            # Append links from the current page to the overall list
        all_links.extend(lnk)

        next_page_link = get_next_page_link(driver)  # Implement this function to get the next page link

        if next_page_link:
            cleaned_url = re.sub(r'\.gov\.in.*$', '.gov.in', url)
            # print("Current URL: ",url)
            # print("Cleaned URL: ",cleaned_url)
            # print("Next Page Link: ",cleaned_url +next_page_link)

            driver.get(cleaned_url + next_page_link)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            time.sleep(1)
        else:
            # No next page, break out of the loop
            break

    return all_links


def handle_stale_session(driver: webdriver.Chrome) -> None:
    """
    Click the restart link to handle a stale session.
    Args:
        driver (webdriver.Chrome): The Selenium webdriver instance.
    """
    try:
        restart_link = driver.find_element(By.ID, "restart")
        restart_link.click()
    except Exception as e:
        print(f"Error handling stale session: {e}")



def get_next_page_link(driver):
    ''''This function is used to grt next page link address'''
    try:
        updated_content = driver.page_source
        soup = BeautifulSoup(updated_content, 'html.parser')

        next_page_link = soup.find('a', id='linkFwd')
        if next_page_link:
            next_page_url = next_page_link.get('href')
            # print("Next Page Link:", next_page_url)
            return next_page_url
        else:
            print("No Next Page Link Found")

    except Exception as e:
        print("get_next_page_link exception: ",e)

