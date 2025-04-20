"""
@author: CHUNYI WANG
@file: test_url_with_selenium.py
@time: 2025/4/9 14:17
@desc: Test each url and check whether it support HTTP POST method
"""

import json
import time

from utils.init_chrome_driver import init_driver

# URL list
with open ("home/tests/logs/url_list.txt", "r", encoding="utf-8") as f:
    TEST_URLS = [line.strip() for line in f if line.strip()]
    
OUTPUT_FILE = "home/tests/logs/selenium_test_results.json"


def test_post_support():
    driver = init_driver()
    results = []

    for url in TEST_URLS:
        result = {"url": url, "supports_post": False, "error": None, "status_code": None}
        
        try:
            # Check if url is valid
            driver.get(url)
            time.sleep(1)
            
            # Carry out post test (with CSRF token)
            script = """
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.startsWith(name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            const csrfToken = getCookie('csrftoken');
            
            return fetch(arguments[0], {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({test: true})
            })
            .then(res => ({
                status: res.status,
                ok: res.ok
            }))
            .catch(err => ({ error: err.message }));
            """
            
            response = driver.execute_script(script, url)
            
            if response is None:
                result["error"] = "No response from JavaScript"
            elif 'error' in response:
                result["error"] = response["error"]
            else:
                result["status_code"] = response["status"]
                result["supports_post"] = response["ok"]
                
        except Exception as e:
            result["error"] = str(e)
        
        results.append(result)
        print(f"Tested: {url} -> {'✅' if result.get('supports_post') else '❌'}")

    driver.quit()
    # Output test result into json file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    test_post_support()