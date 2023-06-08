import requests
import xml.etree.ElementTree as ET
import codecs

# sitemap_url = "https://legitt.xyz/sitemap_index.xml"



def sitemap_url_extractor(sitemap_url):
    # Fetch the XML content
    response = requests.get(sitemap_url)

    xml_content = response.content.decode('utf-8')

    # xml_content = response.content

    # Parse the XML and extract the URLs
    tree = ET.fromstring(xml_content)
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    url_elements = tree.findall(".//ns:loc", namespace)

    # Store the URLs in a Python list
    urls = [url.text.split() for url in url_elements]
    urls = [url[0] for url in urls]
    return urls


sitemap_url = "https://legitt.xyz/sitemap_index.xml"

urls = sitemap_url_extractor(sitemap_url)

print("Total number of urls extracted: {}".format(len(urls)))
print(urls)
