import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def convert_static_links_to_django(html_file):
    # Load the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tags that might have static paths (link, script, img, a, source, etc.)
    for tag in soup.find_all(['link', 'script', 'img', 'a', 'source']):
        if tag.has_attr('href'):
            if tag['href'].startswith('assets/') or tag['href'].startswith('../assets/') or tag['href'].startswith('../../assets/') or tag['href'].startswith('/assets/'):
                tag['href'] = "{% static '" + tag['href'] + "' %}"
        if tag.has_attr('src'):
            if tag['src'].startswith('assets/') or tag['src'].startswith('../assets/') or tag['src'].startswith('../../assets/') or tag['src'].startswith('/assets/'):
                tag['src'] = "{% static '" + tag['src'] + "' %}"

    # Write back the modified HTML content
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    print(f"Converted static links in {html_file}")

# Function to convert static paths to Django template format in all HTML files in a directory
def convert_static_paths(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    num_files_processed = 0

    for html_file in html_files:
        html_file_path = os.path.join(directory, html_file)
        convert_static_links_to_django(html_file_path)
        num_files_processed += 1

    return num_files_processed

# Main function to execute the conversion
if __name__ == '__main__':
    directory = 'C:/Users/erfan/OneDrive/Documents/GitHub/IranianChat/Chat/templates'  # Replace with your directory path
    num_files_processed = convert_static_paths(directory)

    print(f"Total number of HTML files processed: {num_files_processed}")
