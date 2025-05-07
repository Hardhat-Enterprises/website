import json

from utils.init_chrome_driver import init_driver

# This code automatically test urls by using HTTP POST method
# usage: python test_post_requests.py
# required files: post_test_data.json - sample test data

TEST_DATA_FILE = "post_test_data.json"
RESULTS_FILE = "post_test_results.json"

def load_test_cases():
    with open(TEST_DATA_FILE, "r") as f:
        return json.load(f)

def get_csrf_token(driver):
    """Extract CSRF token from cookie"""
    driver.get("http://localhost:8000")  # Get cookie by access random page
    return driver.execute_script(
        "return document.cookie.match(/csrftoken=([^;]+)/)?.[1]"
    )

def run_post_test(driver, url, data, csrf_token):
    script = """
    const response = await fetch(arguments[0], {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': arguments[2]
        },
        body: JSON.stringify(arguments[1])
    });

    // Convert headers to key-value
    const headers = {};
    response.headers.forEach((value, key) => {
        headers[key] = value;
    });

    return {
        status: response.status,
        ok: response.ok,
        headers: headers
    };
    """
    return driver.execute_script(script, url, data, csrf_token)

def main():
    driver = init_driver()
    test_cases = load_test_cases()
    results = []

    try:
        csrf_token = get_csrf_token(driver)
        if not csrf_token:
            raise ValueError("CSRF Token not found in cookies!")

        for case in test_cases:
            result = {"url": case["url"], "passed": False, "response": None}
            try:
                response = run_post_test(
                    driver, 
                    case["url"], 
                    case["data"], 
                    csrf_token
                )
                result["response"] = response
                result["passed"] = response["ok"]
                result["comment"] = case["comment"]
            except Exception as e:
                result["error"] = str(e)
            results.append(result)
            print(f"Tested {case['url']} -> {'✅' if result['passed'] else '❌'}")

    finally:
        driver.quit()
        with open(RESULTS_FILE, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    main()
