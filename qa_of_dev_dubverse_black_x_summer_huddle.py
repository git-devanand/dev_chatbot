# -*- coding: utf-8 -*-
"""Qa of Dev Dubverse Black x Summer Huddle.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uhhr21-bYqboUqG-PId1xX8ZNTKG9IJZ

The workflow can be described as followed:

1. The user poses a question.
2. A Google search is performed using the question.
3. The top-k search results, or the most relevant webpages, are downloaded.
4. Raw HTML data is transformed into a usable format by LangChain.
5. All documents are split into 1,000 character chunks.
6. Compute embeddings for each document chunk and store them in a vector store (chromadb).
7. Build a prompt using the user's question from step 1 and all the scraped web data using LangChain.
8. Query an OpenAI model to generate an answer.
9. Identify the documents that contributed to the answer and return them as references.

## Querying Google and scraping websites

First we need to install the required dependencies.
"""

!pip3 install -U readabilipy langchain openai bs4 requests chromadb tiktoken

import requests # Required to make HTTP requests
from bs4 import BeautifulSoup # Required to parse HTML
import numpy as np # Required to dedupe sites
from urllib.parse import unquote # Required to unquote URLs

# query = 'tell me about legitt.xyz' # The query to search Google for and ask the AI about

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
    return urls


# sitemap_url = "https://legitt.xyz/sitemap_index.xml"

# urls = sitemap_url_extractor(sitemap_url)

import requests # Required to make HTTP requests
from bs4 import BeautifulSoup # Required to parse HTML
import numpy as np # Required to dedupe sites
from urllib.parse import unquote # Required to unquote URLs
# from legitt_sitemap_urls import sitemap_url_extractor   # urls extracted from sitemap
import json


# loop over `links` and keep only the one that have the href starting with "/url?q="
# urls = [
#     'https://legitt.xyz/',
#     'https://legitt.xyz/about-us',
#     'https://legitt.xyz/blog',
#     'https://legitt.xyz/pricing',
#     'https://legitt.xyz/product-tour',
#     'https://legitt.xyz/smart-contract',
# ]

sitemap_url = "https://legitt.xyz/sitemap_index.xml"

urls = sitemap_url_extractor(sitemap_url)
urls = [url[0] for url in urls]

# file_name_url = "./datasets/sitemap_urls"
# with open(file_name_url, "w") as f:
#     f.write(str(urls))

# print("Sitemap urls saved to {} file successfully.".format(file_name_url))

print("Total number of urls extraceted: " + str(len(urls)))

print(type(urls))


# Extra freature: if you want to search for google then the below code works and create an empty 
# for l in [link for link in links if link["href"].startswith("/url?q=")]:
#     # get the url
#     url = l["href"]
#     # remove the "/url?q=" part
#     url = url.replace("/url?q=", "")
#     # remove the part after the "&sa=..."
#     url = unquote(url.split("&sa=")[0])
#     # special case for google scholar
#     if url.startswith("https://scholar.google.com/scholar_url?url=http"):
#         url = url.replace("https://scholar.google.com/scholar_url?url=", "").split("&")[0]
#     elif 'google.com/' in url: # skip google links
#         continue
#     if url.endswith('.pdf'): # skip pdf links
#         continue
#     if '#' in url: # remove anchors (e.g. wikipedia.com/bob#history and wikipedia.com/bob#genetics are the same page)
#         url = url.split('#')[0]
#     # print the url
#     urls.append(url)




# Use numpy to dedupe the list of urls after removing anchors

# urls = list(np.unique(urls))
# urls

# from readabilipy import simple_json_from_html_string # Required to parse HTML to pure text
# from langchain.schema import Document # Required to create a Document object
# # from readabilipy.simple_json import simple_json_from_html_string

# unicodedecodeerrored_urls = []

# def scrape_and_parse(url: str) -> Document:
#     try:
#         """Scrape a webpage and parse it into a Document object"""
#         req = requests.get(url)
#         content = req.content.decode('utf-8')

#         # print("###################### Request Text {} ###############################".format(url))
        
#         article = simple_json_from_html_string(content, 
#                                                 content_digests=False,  # (optional, default: False): When set to True, this parameter enables the extraction of content digests from the HTML. Content digests are short summaries or representations of the main content of a web page.
#                                                 node_indexes=False, # (optional, default: False): When set to True, this parameter includes the node indexes in the JSON output. Node indexes are the positions of HTML elements in the document tree.
#                                                 use_readability=True,   # (optional, default: False): When set to True, this parameter activates the usage of the Readability algorithm to extract the main content from the HTML. The Readability algorithm attempts to identify and isolate the relevant textual content from the noise and clutter present in a web page.
#                                                 )
        
#         # print("##################### Article Text {} #############################".format(url))
       
#         # The following line seems to work with the package versions on my local machine, but not on Google Colab
#         if article is not None:
#             return Document(page_content=article['plain_text'][0]['text'], metadata={'source': url, 'page_title': article['title']})
#         else:
#             return None
        
#         # The following line works on Google Colab
#         # return Document(page_content='\n\n'.join([a['text'] for a in article['plain_text']]), metadata={'source': url, 'page_title': article['title']})


#     except UnicodeDecodeError:
#         unicodedecodeerrored_urls.append(url)
#         # print(f"Appended Error decoding content for URL to list {len(unicodedecodeerrored_urls)}: {url}")
#         print(f"{len(unicodedecodeerrored_urls)}. UnicodeDecodeError: Error decoding content for URL at: {url}")
#         # return None
#         pass


# #  remove url values from url which exists in    
# # It's possible to optitimize this by using asyncio
# documents = [scrape_and_parse(f) for f in urls] # Scrape and parse all the urls


# # log_err = "./logs/unicodedecodeerrored_urls"

# # with open(log_err, "w") as log:
# #     # log.write(str(unicodedecodeerrored_urls))
# #     log.write(",".join(unicodedecodeerrored_urls))



# # print("UnicodeDecodeError urls logged to {} file.".format(log_err))

# # file_name = "./datasets/legitt_documents"
# # with open(file_name, "w") as f:
# #     f.write(str(documents))



# # print("Documents saved to the {} file.".format(file_name))

# response = requests.get(f"https://www.google.com/search?q={query}") # Make the request
# soup = BeautifulSoup(response.text, "html.parser") # Parse the HTML
# links = soup.find_all("a") # Find all the links in the HTML

# loop over `links` and keep only the one that have the href starting with "/url?q="
# urls = ['https://legitt.xyz/',
#  'https://legitt.xyz/about-us',
#  'https://legitt.xyz/blog',
#  'https://legitt.xyz/pricing',
#  'https://legitt.xyz/product-tour',
#  'https://legitt.xyz/smart-contract',]

# for l in [link for link in links if link["href"].startswith("/url?q=")]:
#     # get the url
#     url = l["href"]
#     # remove the "/url?q=" part
#     url = url.replace("/url?q=", "")
#     # remove the part after the "&sa=..."
#     url = unquote(url.split("&sa=")[0])
#     # special case for google scholar
#     if url.startswith("https://scholar.google.com/scholar_url?url=http"):
#         url = url.replace("https://scholar.google.com/scholar_url?url=", "").split("&")[0]
#     elif 'google.com/' in url: # skip google links
#         continue
#     if url.endswith('.pdf'): # skip pdf links
#         continue
#     if '#' in url: # remove anchors (e.g. wikipedia.com/bob#history and wikipedia.com/bob#genetics are the same page)
#         url = url.split('#')[0]
#     # print the url
#     urls.append(url)

# Use numpy to dedupe the list of urls after removing anchors
urls = list(np.unique(urls))
urls

from readabilipy import simple_json_from_html_string # Required to parse HTML to pure text
from langchain.schema import Document # Required to create a Document object

def scrape_and_parse(url: str) -> Document:
    """Scrape a webpage and parse it into a Document object"""
    req = requests.get(url)
    article = simple_json_from_html_string(req.text, use_readability=True)
    # The following line seems to work with the package versions on my local machine, but not on Google Colab
    # return Document(page_content=article['plain_text'][0]['text'], metadata={'source': url, 'page_title': article['title']})
    if article is not None:
      return Document(page_content='\n\n'.join([a['text'] for a in article['plain_text']]), metadata={'source': url, 'page_title': article['title']})

# It's possible to optitimize this by using asyncio
documents = [scrape_and_parse(f) for f in urls] # Scrape and parse all the urls

documents

"""## Splitting documents into chunks

"""

from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(separator=' ', chunk_size=1000, chunk_overlap=200)

texts = text_splitter.split_documents(documents)

len(texts)

from chromadb.api.types import Metadatas
print(type(texts))
# print(texts)
for t in range(5):
  print(texts[t].metadata)

"""Batch Process using generators

"""

# def batch_generator(texts, batch_size):
#     # Generate batches of texts
#     for i in range(0, len(texts), batch_size):
#         yield texts[i:i+batch_size]
# # batch_size = 5
# # batch = batch_generator(texts, batch_size)

"""Batch Processes"""

# import time

# def process_texts(texts, batch_size, rpm_limit, tpm_limit):
#     request_count = 0
#     token_count = 0
    
#     # Get the generator for batches of texts
#     batches = batch_generator(texts, batch_size)
    
#     for batch in batches:
#         # Check RPM limit
#         if request_count >= rpm_limit:
#             # Wait for a minute before continuing
#             time.sleep(60)
#             request_count = 0
        
#         # Process the batch of texts
#         process_batch(batch)
        
#         # Update request and token counts
#         request_count += 1
#         token_count += len(batch) * tokens_per_request
        
#         # Check TPM limit
#         if token_count >= tpm_limit:
#             # Calculate the sleep time based on remaining seconds in the current minute
#             sleep_time = 60 - time.time() % 60
#             time.sleep(sleep_time)
#             token_count = 0

# def process_batch(batch):
#     # Your logic to process each batch of texts goes here
#     # Make the API request, handle the response, etc.
#     pass

# # Set your desired RPM and TPM limits
# rpm_limit = 3
# tpm_limit = 1

# # Set the number of tokens consumed per request
# tokens_per_request = 5

# # Set the batch size
# batch_size = 5  # Adjust this value based on the API's maximum batch size

# # Call the function to process the texts
# process_texts(texts, batch_size, rpm_limit, tpm_limit)

"""## Computing embeddings of chunks and storage in a vector store

"""

from langchain.embeddings.openai import OpenAIEmbeddings

OPENAI_API_KEY = "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"

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

from langchain.vectorstores import Chroma

docsearch = Chroma.from_documents(texts, embeddings)

"""## Configuring what model we use and ask questions

We can now pick which model to use and start asking questions!
"""

from langchain.llms import OpenAIChat # Required to create a Language Model

# Pick an OpenAI model
llm = OpenAIChat(model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY)

from langchain import  VectorDBQA # Required to create a Question-Answer object using a vector

import pprint # Required to pretty print the results

# Stuff all the information into a single prompt (see https://docs.langchain.com/docs/components/chains/index_related_chains#stuffing)
qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=docsearch, return_source_documents=True)
query = "What is legitt? What the company do? what is the motive of legitt?"
result = qa({"query": query})

pprint.pprint(result)

[a.metadata['source'] for a in result['source_documents']] # Print the source documents

qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=docsearch, return_source_documents=True)
query = "How to create a contract in legitt?"
result = qa({"query": query})

pprint.pprint(result)

qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=docsearch, return_source_documents=True)
query = "tell me about legitt in detail"
result = qa({"query": query})

pprint.pprint(result)

qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=docsearch, return_source_documents=True)
query = "How to make smart contract on legitt?."
result = qa({"query": query})

pprint.pprint(result)

# query function to ask for question here
def legitt_chatbot(query):
  qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=docsearch, return_source_documents=True)
  result = qa({"query": query})
  # pprint.pprint(result)
  return result

legitt_chatbot("which number to reach out for contacting legitt")

legitt_chatbot("create a sale contract")

chat_res = legitt_chatbot("create a smart contract")
# print(type(chat_res))
# print(type(chat_res.keys()))
# print(type(chat_res.values()))
print("Bot Response: {}".format(chat_res['result']))
print("Source Documents: {}".format(chat_res['source_documents']))

def bot_conversation():
  while True:
    query = input("User Query: ")
    if (query != 'exit'):
      chat_res = legitt_chatbot(query)
      print("Bot Response: {}\n".format(chat_res['result']))
      print("Source of Response: {}\n".format(chat_res['source_documents']))
    else:
      print("Goodby! Have a nice day.\n")
      break

bot_conversation()

!pip freeze