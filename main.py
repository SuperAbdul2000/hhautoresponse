from playwright.sync_api import sync_playwright
from app.auth import HH_PHONE, HH_PASSWORD
from app.config import SEARCH_CONFIG
from app.create_url import build_search_url
from app.utils import load_cover_letter

import random
import re

def extract_vacancy_id(url: str):
    match = re.search(r"vacancyId=(\d+)", url)
    return match.group(1) if match else None

def save_test_url(url: str):
    with open("test_vacancies.txt","a",encoding="utf-8") as f:
        f.write(url + "\n")

def wait_for_captcha(page):
    try:
        captcha = page.locator('[data-qa="account-captcha-input"]')
        captcha.wait_for(timeout=3000)

        print("\n[!] CAPTCHA detected. Please solve it in the browser.")

        captcha.wait_for(state="hidden", timeout=120000)

        print("[+] CAPTCHA solved. Continuing with the automation.")
    except:
        pass

cover_letter = load_cover_letter()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto("https://hh.ru/")

    page.locator('[data-qa="login"]').click()

    wait_for_captcha(page)

    page.locator('[data-qa="submit-button"]').click()

    page.locator('[data-qa="magritte-phone-input-national-number-input"]').fill(HH_PHONE)

    page.locator('[data-qa="expand-login-by-password"]').click()

    wait_for_captcha(page)

    page.locator('[data-qa="applicant-login-input-password"]').fill(HH_PASSWORD)

    page.locator('[data-qa="submit-button"]').click()

    wait_for_captcha(page)

    print("[+] Login flow finished")

    current_page = 0
    total_results = 0
    blocked_vacancies = set()

    while True:
        search_url = build_search_url(
            SEARCH_CONFIG,
            page=current_page
        )

        print(f"\n[+] Opening page {current_page}")

        page.goto(search_url)

        page.wait_for_timeout(
            random.randint(2000, 5000)
        )

        buttons = page.locator(
            '[data-qa="vacancy-serp__vacancy_response"]'
        )

        count = buttons.count()

        print(f"[+] Found {count} vacancies")

        if count == 0:
            print("[+] No more vacancies")
            break

        while True:
            buttons = page.locator(
                '[data-qa="vacancy-serp__vacancy_response"]'
            )

            count = buttons.count()

            if count == 0:
                print("[+] Page completed")
                break

            print(f"[+] Remaining vacancies: {count}")

            try:
                button = buttons.first

                href = button.get_attribute("href") or ""

                vacancy_id = extract_vacancy_id(href)

                if vacancy_id in blocked_vacancies:
                    print(f"[!] Skipping previously blocked vacancy ID: {vacancy_id}")

                    button.evaluate("el => el.remove()")

                    continue

                if not button.is_visible():
                    continue

                button.scroll_into_view_if_needed()

                page.wait_for_timeout(
                    random.randint(300, 700)
                )

                button.click()


                print("[+] Clicked apply button")

                page.wait_for_timeout(
                    random.randint(300, 700)
                )

                current_url = page.url

                if "vacancy_response" in current_url:

                    vacancy_id = extract_vacancy_id(current_url)
                    print(f"[!] Test/response URL: {current_url}")

                    save_test_url(current_url)

                    if vacancy_id:
                        blocked_vacancies.add(vacancy_id)

                    page.goto(search_url)

                    page.wait_for_timeout(800)

                    continue

                textarea = page.locator(
                    '[data-qa="textarea-wrapper"] textarea'
                )

                if textarea.count() > 0:
                    print("[+] Cover letter required")

                    textarea.fill(cover_letter)

                    page.wait_for_timeout(
                        random.randint(300, 700)
                    )

                    submit_button = page.locator(
                        '[data-qa="vacancy-response-submit-popup"]'
                    )

                    submit_button.click()

                    print(
                        "[+] Response submitted with cover letter"
                    )
                    total_results += 1

                else:
                    print("[+] Quick apply completed")
                    total_results += 1

                page.wait_for_timeout(
                    random.randint(300, 700)
                )

            except Exception as e:
                print(f"[!] Error: {e}")

                page.wait_for_timeout(
                    random.randint(300, 700)
                )

        current_page += 1

    input("Press Enter to close the browser...")

    browser.close()

    print(f"[+] Total responses submitted: {total_results}")
