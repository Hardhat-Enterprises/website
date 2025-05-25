"""
Enhanced search result formatting using rich text, tables, and Jinja2 templates.
Integrated with chat interface styling.
"""
from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown
from tabulate import tabulate
import emoji
from jinja2 import Environment, PackageLoader, select_autoescape, Template
import logging
import inspect

#?Initialize logger
logger = logging.getLogger('chatbot_app.formatter')

#? Initialize Jinja2 environment
jinja_env = Environment(
    loader=PackageLoader('chatbot_app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

def log_formatter_info(func):
    """Decorator to log information about the formatting process"""
    def wrapper(*args, **kwargs):
        # ?Get the module of the formatting function
        module = inspect.getmodule(func)
        # Get the actual packages being used in the function
        source_lines = inspect.getsource(func)
        packages_used = [line.strip().split()[1] for line in source_lines.split('\n') 
                        if line.strip().startswith('from') or line.strip().startswith('import')]
        
        logger.info(f"Using formatter: {func.__name__} from module {module.__name__}")
        logger.debug(f"Formatter dependencies: {', '.join(packages_used)}")
        
        result = func(*args, **kwargs)
        
        logger.debug(f"Formatting completed using {func.__name__}")
        return result
    return wrapper

@log_formatter_info
def format_for_chat(content: str) -> str:
    """Format content for chat display with proper HTML/CSS classes."""
    logger.debug("Using HTML/CSS formatting for chat display")
    return f'<div class="formatted-response">{content}</div>'

@log_formatter_info
def render_template_string(template_str: str, **kwargs) -> str:
    """Render a template string with the given context."""
    logger.debug(f"Using Jinja2 template engine for string template with context: {kwargs}")
    template = Template(template_str)
    rendered = template.render(**kwargs)
    return format_for_chat(rendered)

@log_formatter_info
def render_template(template_name: str, **kwargs) -> str:
    """Render a template file with the given context."""
    logger.debug(f"Using Jinja2 template engine for file '{template_name}' with context: {kwargs}")
    template = jinja_env.get_template(template_name)
    rendered = template.render(**kwargs)
    return format_for_chat(rendered)

@log_formatter_info
def format_result_title(result: Dict[str, Any]) -> str:
    """Format a result title with appropriate emoji and styling."""
    model_type = result.get('model', '').lower()
    title = result.get('title', result.get('name', 'Untitled'))
    
    # Add appropriate emoji based on model type
    emoji_map = {
        'article': ':page_facing_up:',
        'apimodel': ':gear:',
        'cyberchallenge': ':trophy:',
        'faq': ':question:',
        'pagecontent': ':book:',
        'user': ':bust_in_silhouette:',
        'project': ':computer:',
        'course': ':mortar_board:',
        'skill': ':star:'
    }
    
    result_emoji = emoji_map.get(model_type, ':mag:')
    logger.debug(f"Using emoji package for model type '{model_type}' with emoji '{result_emoji}'")
    formatted_title = f"{emoji.emojize(result_emoji)} {title}"
    return f'<span class="result-title">{formatted_title}</span>'

@log_formatter_info
def create_result_table(results: List[Dict[str, Any]], query: str) -> str:
    """Create an HTML table for search results."""
    logger.debug(f"Using HTML table formatting for {len(results)} results")
    table_rows = []
    for result in results:
        title = format_result_title(result)
        model_type = result.get('model', '').replace('_', ' ').title()
        description = result.get('description', result.get('content', ''))
        if len(description) > 100:
            description = description[:97] + "..."
        
        details = []
        if 'difficulty' in result:
            details.append(f"Difficulty: {result['difficulty']}")
        if 'category' in result:
            details.append(f"Category: {result['category']}")
        if 'points' in result:
            details.append(f"Points: {result['points']}")
        details_str = "<br>".join(details) if details else "-"
        
        table_rows.append([title, model_type, description, details_str])
        logger.debug(f"Added HTML table row for {model_type}: {title}")
    
    table_html = '<table class="search-results-table">'
    table_html += '<thead><tr><th>Title</th><th>Type</th><th>Description</th><th>Details</th></tr></thead>'
    table_html += '<tbody>'
    for row in table_rows:
        table_html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
    table_html += '</tbody></table>'
    
    return table_html

@log_formatter_info
def format_challenge_result(result: Dict[str, Any]) -> str:
    """Format a challenge result with all available fields."""
    logger.debug(f"Using emoji and text formatting for challenge: {result.get('title', 'Untitled')}")
    return f"""
⸻
📘 {result['title']}
{result['detailed_description']}
🕒 Estimated Time: {result['estimated_duration']}
🔒 Lock Status: {result['is_locked']}
...
⸻
"""

@log_formatter_info
def format_course_result(result: Dict[str, Any]) -> str:
    """Format a course result in a similar style."""
    title = result.get('title', '')
    logger.debug(f"Using emoji and HTML formatting for course: {title}")
    description = result.get('description', '')
    level = result.get('level', 'Beginner')
    duration = result.get('duration', '')
    course_id = result.get('id', 0)
    
    course_block = f"""
⸻

📚 {title}
{description}
📊 Level: {level}
⏱️ Duration: {duration}
🔗 <a href="/courses/detail/{course_id}">View Course</a>

⸻
"""
    return course_block

@log_formatter_info
def format_job_result(result: Dict[str, Any]) -> str:
    """Format a job listing in a similar style."""
    title = result.get('title', '')
    logger.debug(f"Using emoji and HTML formatting for job: {title}")
    description = result.get('description', '')
    location = result.get('location', 'Remote')
    job_type = result.get('job_type', 'Full-time')
    job_id = result.get('id', 0)
    
    job_block = f"""
⸻

💼 {title}
{description}
📍 Location: {location}
⚡ Type: {job_type}
🔗 <a href="/careers/detail/{job_id}">Apply Now</a>

⸻
"""
    return job_block

@log_formatter_info
def format_search_results_rich(results: Dict[str, Any], query: str) -> str:
    """Format search results for chat display."""
    logger.info(f"Starting rich formatting for query: '{query}'")
    
    if 'error' in results:
        logger.warning(f"Using error template for: {results['error']}")
        error_template = """
        <div class="error-message">
            <strong>Search Error:</strong> {{ error }}
        </div>
        """
        return render_template_string(error_template, error=results['error'])
    
    if not results.get('results', []):
        logger.info("Using empty results template")
        return render_template_string('<div class="no-results">No results found</div>')
    
    # Group results by model type
    model_counts = {}
    formatted_results = []
    
    # Add greeting for challenges
    if any(r.get('model', '').lower() == 'cyberchallenge' for r in results['results']):
        logger.debug("Using challenge greeting template")
        formatted_results.append(f"👋 Hi! Here are the top {len(results['results'])} Cyber Challenges ready for you to tackle:")
    
    # Format each result based on its type
    for result in results['results']:
        model_type = result.get('model', 'unknown').lower()
        model_counts[model_type] = model_counts.get(model_type, 0) + 1
        logger.debug(f"Using {model_type} formatter")
        
        if model_type == 'cyberchallenge':
            formatted_results.append(format_challenge_result(result))
        elif model_type == 'course':
            formatted_results.append(format_course_result(result))
        elif model_type == 'job':
            formatted_results.append(format_job_result(result))
    
    # Add "Show more" prompt if there are results
    if formatted_results:
        model_type = results['results'][0].get('model', '').lower()
        if model_type == 'cyberchallenge':
            logger.debug("Adding challenge prompt template")
            formatted_results.append("\n💬 Would you like to see more cyber challenges?")
            formatted_results.append("👉 Show me more cyber challenges")
    
    # Join all formatted results
    response = '\n'.join(formatted_results)
    logger.info(f"Completed rich formatting for {len(formatted_results)} results")
    
    return format_for_chat(response)

@log_formatter_info
def format_as_markdown(results: Dict[str, Any], query: str) -> str:
    """Format search results as markdown text with chat-friendly styling."""
    logger.info(f"Starting markdown formatting for query: '{query}'")
    
    if 'error' in results:
        logger.warning(f"Using markdown error template for: {results['error']}")
        return format_for_chat(f"## Search Error\n\n**Error:** {results['error']}")
    
    if not results.get('results', []):
        logger.info("Using markdown empty results template")
        return format_for_chat("## Search Results\n\nNo results found.")
    
    logger.debug("Using tabulate package for markdown table formatting")
    # Create markdown content
    markdown_content = [
        f"## Search Results for: {query}\n",
        f"**Total Results:** {len(results['results'])}\n",
        "### Results by Type\n"
    ]
    
    # Add type counts
    model_counts = {}
    for result in results['results']:
        model_type = result.get('model', 'unknown').replace('_', ' ').title()
        model_counts[model_type] = model_counts.get(model_type, 0) + 1
    
    for model_type, count in model_counts.items():
        markdown_content.append(f"* {model_type}: {count}\n")
        logger.debug(f"Added markdown count for {model_type}: {count}")
    
    # Add results table
    headers = ["Title", "Type", "Description", "Details"]
    table_data = []
    for result in results['results']:
        title = format_result_title(result)
        model_type = result.get('model', '').replace('_', ' ').title()
        description = result.get('description', result.get('content', ''))
        if len(description) > 100:
            description = description[:97] + "..."
        
        details = []
        if 'difficulty' in result:
            details.append(f"Difficulty: {result['difficulty']}")
        if 'category' in result:
            details.append(f"Category: {result['category']}")
        if 'points' in result:
            details.append(f"Points: {result['points']}")
        details_str = "<br>".join(details) if details else "-"
        
        table_data.append([title, model_type, description, details_str])
        logger.debug(f"Added markdown table row for {model_type}: {title}")
    
    table = tabulate(table_data, headers=headers, tablefmt="pipe")
    markdown_content.append("\n" + table)
    
    logger.info(f"Completed markdown formatting for {len(table_data)} results")
    return format_for_chat("\n".join(markdown_content)) 