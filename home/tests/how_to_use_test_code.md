# Test API with HTTP GET method
## Usage
```bash
python manage.py test home.tests.test_get_requests
```

## Output
Output file path: `hardhat-enterpise-website/home/tests/logs/auto_discover_test_GET.log`

# Auto discover HTTP POST method accepted API
## Usage
Work directory: `hardhat-enterpise-website/home/tests/` (The following command need to be run under this directory)

```bash
python test_url_with_selenium.py
```

## Output
Once the command is executed, the result will be output into the file `home/tests/logs/selenium_test_results.json`

# Test API with HTTP POST method
## Get the latest URL list
```bash
python manage.py show_urls | awk '{print "http://localhost:8000" $1}' | cut -d' ' -f1 > home/tests/logs/url_list.txt
```

## Construct data for test
Path of contructed data: `hardhat-enterpise-website/home/tests/post_test_data.json`

Data must in JSON format

## Usage
Under the directory: `hardhat-enterpise-website/home/tests/`

```bash
python test_post_requests.py
```

## Output
Test result will be output into `hardhat-enterpise-website/home/tests/post_test_results.json`

# Problems currently faced
Generally for each function in the `views.py`, a decorator should be used to specify the HTTP methods accepted by each view function, e.g:

This view function render a page, then this function should only accept GET method

```python
@require_GET # This decorator should be added to specify this function only accept GET method
def SearchResults(request):
    query = request.POST.get('q', '')  # Get search query from request
    results = {
        'searched': query,
        'webpages': Webpage.objects.filter(title__icontains=query),
        'projects': Project.objects.filter(title__icontains=query),
        'courses': Course.objects.filter(title__icontains=query),
        'skills': Skill.objects.filter(name__icontains=query),
        'articles': Article.objects.filter(title__icontains=query),
    }
    return render(request, 'pages/search-results.html', results)
```



Since each function does not declare the methods it accepts, each URL accepts all HTTP methods when scanning URLs, which makes it difficult for me to determine which HTTP methods should be used to test these URLs.
