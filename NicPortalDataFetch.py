import os
import re
import time
import json
from datetime import datetime, timedelta
import multiprocessing as mp
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import data_google_sheet_ops2 as gs


def findeachlink( exclude_value, url,search_key):
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
            time.sleep(1)
            name = state_name_value  # site_url.removeprefix("https://").removesuffix(".gov.in")
            # driver.implicitly_wait(5)
            # time.sleep(2)
            WebDriverWait(driver, 35).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            search_bar = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.ID, "SearchDescription"))
            )

            print("................................................................")
            search_bar.send_keys(search_key)
            search_bar.send_keys(Keys.RETURN)
            print("Searching again for: ", searchkey)

            updated_content = driver.page_source
            soup = BeautifulSoup(updated_content, 'html.parser')
            # print("HTML Content:", soup.prettify())
            tbody = soup.find('tbody')

        # tbody=find_tbody_with_retry(soup,retries=3, delay=2)
        if tbody:
            even_odd = tbody.find_all('tr', class_=["odd", "even"])
            lnk = []
            for row in even_odd:
                tds = row.find_all('td')
                for td in tds:
                    try:
                        links = td.find_all('a', href=True)
                        for link in links:
                            href = link.get('href')
                            link_text = link.get_text()
                            if exclude_value != [''] or not None:
                                # exclude_check = any(value.lower() in link_text.lower() for value in exclude_value)
                                exclude_pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, exclude_value)) + r')\b',
                                                             flags=re.IGNORECASE)
                                exclude_check = exclude_pattern.search(link_text)
                                if not exclude_check and href:
                                    cleaned_url = re.sub(r'\.gov\.in.*$', '.gov.in', url)
                                    print("Link Not Excluded", cleaned_url + href)

                                    print("Link Not Excluded", link_text)
                                    lnk.append(cleaned_url + href)
                            else:
                                if href:
                                    cleaned_url = re.sub(r'\.gov\.in.*$', '.gov.in', url)
                                    print("Link Not Excluded",cleaned_url+href)
                                    print("Link Not Excluded", link_text)
                                    lnk.append(cleaned_url+href)

                    except StaleElementReferenceException:
                        # pass
                        # Handle stale session by restarting
                        handle_stale_session()
            # Append links from the current page to the overall list
        all_links.extend(lnk)

        next_page_link = get_next_page_link()  # Implement this function to get the next page link

        if next_page_link:
            cleaned_url = re.sub(r'\.gov\.in.*$', '.gov.in', url)
            # print("Current URL: ",url)
            # print("Cleaned URL: ",cleaned_url)
            print("Next Page Link: ",cleaned_url +next_page_link)

            driver.get(cleaned_url + next_page_link)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            time.sleep(1)
        else:
            # No next page, break out of the loop
            break

    return all_links
def get_next_page_link():
    ''''This function is used to grt next page link address'''
    try:
        updated_content = driver.page_source
        soup = BeautifulSoup(updated_content, 'html.parser')

        next_page_link = soup.find('a', id='linkFwd')
        if next_page_link:
            next_page_url = next_page_link.get('href')
            print("Next Page Link:", next_page_url)
            return next_page_url
        else:
            print("No Next Page Link Found")

    except Exception as e:
        print("get_next_page_link exception: ",e)


# def handle_stale_session():
#     restart_link = driver.find_element(By.ID, "restart")
#     restart_link.click()
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

def find_tbody_with_retry(soup, retries=3, delay=2):
    for _ in range(retries):
        tbody = soup.find('tbody')
        if tbody:
            return tbody
        print("Retrying tbody fetch...")
        time.sleep(delay)
    return None


def make_directory(path:str)->None:
    """This function is used to create folder if not exists"""
    if not os.path.exists(path):
        os.makedirs(path)


def time_taken(start):
    """This function is used to calculate time  related calculations"""
    end_time_ = time.strftime("%H-%M-%S")
    total_time = (datetime.strptime(end_time_, '%H-%M-%S') - datetime.strptime(start, '%H-%M-%S')).seconds
    total_time = time.strftime("%H-%M-%S", time.gmtime(total_time))
    return end_time_, total_time


def opensuburl(lnk, name, searchkey, sheetname, excluded_values):
    '''' This function is used to perform main operation like extract description, Tender submision end data, emd amount etc'''
    # entries_without_spaces = [entry.strip() for entry in search_field_values_list]

    entries = ["Tender ID", "Work Description", "Organisation Chain", "Bid Submission End Date", "Tender Value in ₹",
               "EMD Amount in ₹", "Tender Fee in ₹"]
    # print("Entries", entries)
    data_list = []

    for link in lnk:
        driver.get(link)

        # time.sleep(3)
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
                    print("............................................................")
                    print("Bid Submission End Date t: ", bid_submission_end_date)
                    print("Bid Submission End Time t: ", bid_submission_end_time)
                    # print("Name of Site: ",name)
                    # print("Search Key: ",searchkey)
                else:

                    assert isinstance(tender_value, str), f"Error: Invalid value found for {entry}"
                    assert len(tender_value.strip()) > 0, f"Error: Empty value extracted for {entry}"
                    print("Entry t:",entry)
                    print("Tender value else t:",tender_value)
                    entry_dict[entry] = tender_value
                    entry_dict["Name of Site"] = name
                    entry_dict["Search Key"] = searchkey
                    entry_dict["Link"] = link
                    print("Name of Site t: ", name)
                    print("Search Key t: ", searchkey)
                    # time.sleep(1)
                    print(entry, ": ", tender_value)
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
                        print("............................................................")
                        print("Bid Submission End Date e: ", bid_submission_end_date)
                        print("Bid Submission End Time e: ", bid_submission_end_time)

                    else:
                        if "," in tender_value:
                            tender_value.replace(",", " ")

                        entry_dict[entry] =tender_value
                        entry_dict["Name of Site"] = name
                        entry_dict["Search Key"] = searchkey
                        entry_dict["Link"] = link


                        print("Name of Site e: ", name)
                        print("Search Key e: ", searchkey)
                        # time.sleep(1)
        if len(entry_dict) > 5:
            # tender_value=entry_dict.get('Tender Value in ₹')
            # tender_val = ["," in tender_value, int(tender_value.replace(",", "")), tender_value][1]
            # entry_dict.pop('Tender Value in ₹')
            # entry_dict['Tender Value in ₹']=tender_val
            #
            # if int(tender_val)>=int(tender_val_ab):
            #     print("Tender Value Filtered:",tender_val)
                data_list.append(entry_dict)

    df = pd.DataFrame(data_list)

    # df.to_csv(f"Tender-{name}-{searchkey}.csv", index=False)
    # assert not df.empty, "Error: No valid data extracted! DataFrame is empty."
    if not df.empty:
        sheet_name = sheetname
        worksheet_name =config["NICPortal_Output_Tab_Name"]# "NIC Tender Output Details"

        gs_.add_data_(df, sheet_name=sheet_name, worksheet_name=str(worksheet_name), header=False, spacing=0,
                      table_range=None)




if __name__ == '__main__':
    mp.freeze_support()
    # Open and read the JSON file
    with open('config.json', 'r',encoding="utf-8") as file:
        config= json.load(file)
    start_time_ = time.strftime("%H-%M-%S")
    current_date = datetime.now().strftime("%Y%m%d-%H:%M")
    previous_date = datetime.now() - timedelta(days=1)
    previous_date = previous_date.strftime("%Y%m%d")

    gs_ = gs.GoogleSheetOps("creds.json")
    existing_sheet_url = config["NICPortal_Sheet_Link"]#"https://docs.google.com/spreadsheets/d/1IzpGqVIKDqeb-QwqQL5E5uX6u32-stge46vpdCNz4lk/edit#gid=494796437"
    print("Sheet Link:", existing_sheet_url)
    # other_path_sheet = gs_.get_worksheet_as_df(sheet_name=existing_sheet_url, worksheet_name="Other Paths")
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    # Setup Chrome options if needed
    chrome_options = webdriver.ChromeOptions()
    # Example: Run headless or disable extensions, if needed
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-extensions")

    # Initialize Chrome driver using webdriver-manager
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    # Now use the driver as usual
    nic_input_tab = config["NICPortal_Input_Tab_Name"]

    sheet = gs_.get_worksheet_as_df(sheet_name=existing_sheet_url, worksheet_name=nic_input_tab)
    # ✅ Assert: Check if the sheet is not empty
    assert not sheet.empty, "Error: Google Sheet data is empty!"
    # ✅ Assert: Check if required columns exist
    required_columns = ["Site Url", "Search Keys", "State Name", "Exclude"]
    for col in required_columns:
        assert col in sheet.columns, f"Error: '{col}' column is missing in Google Sheet!"
    # save_html_page = sheet['Save Static HTML Page'][0]
    for index, row in sheet.iterrows():
        site_url_value = row['Site Url']
        search_key_value = row['Search Keys']
        search_key_values_list = search_key_value.split(',')
        state_name_value = row['State Name']
        exclude_name_value = row['Exclude']
        excluded_values = exclude_name_value.split('|')
        # tender_val_ab = row['Tender Value Above']

        eachrow = row
        # print(row)
        sh = gs_.sa.open_by_url(existing_sheet_url)
        sheetname = existing_sheet_url
        site_url = site_url_value  # "https://wbtenders.gov.in"
        searchkeys = search_key_values_list  # ["wire", "conductor"]
        for searchkey in searchkeys:
            url = site_url
            driver.delete_all_cookies()

            driver.get(url)
            time.sleep(1)
            name = state_name_value  # site_url.removeprefix("https://").removesuffix(".gov.in")
            # driver.implicitly_wait(5)
            # time.sleep(2)
            WebDriverWait(driver, 35).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            search_bar = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.ID, "SearchDescription"))
            )
            assert search_bar is not None, "Error: Search bar not found!"
            print("................................................................")
            search_bar.send_keys(searchkey)
            search_bar.send_keys(Keys.RETURN)
            print("Searching for: ", searchkey)
            time.sleep(2)

            lnk = findeachlink(excluded_values, url,searchkey)
            # assert len(lnk) > 0, f"Error: No links found for {searchkey}!"
            print("State Name: ",state_name_value)
            print("Total links: ",len(lnk))
            opensuburl(lnk, name, searchkey, sheetname, excluded_values)

    driver.quit()
    end_time, total_time_taken_ = time_taken(start=start_time_)
    print("Total_time_taken for nic data fetching", total_time_taken_)

