import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import concurrent.futures
import time
import threading
from queue import Queue

def write_to_file(file_path, text):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file = open(file_path, "a", encoding="utf-8")
    file.write(text)

def get_file_path(url):
    file_path_subfix = url[28:].replace("/tasks", "")
    return "./testOutput/competitions/" + file_path_subfix + "/"

def get_problem_statement(soup, url):
    problem_statement_dict = None
    try:
        header = soup.find('h3', string='Problem Statement')
        problem_statement_html = str(header) + ''.join(str(sibling) for sibling in header.find_next_siblings())
        file_path = get_file_path(url) + "problem_statement.html"
        problem_statement_dict = {file_path: problem_statement_html}
    finally:
        return problem_statement_dict

def get_constraints(soup, url):
    constraints_dict = None
    try:
        header = soup.find('h3', string='Constraints')
        constraints_html = str(header) + ''.join(str(sibling) for sibling in header.find_next_siblings())
        file_path = get_file_path(url) + "constraints.html"
        constraints_dict = {file_path: constraints_html}
    finally:
        return constraints_dict

def get_input(soup, url):
    input_dict = None
    try:
        header = soup.find('h3', string=lambda text: text and text.lower() in ('input', 'inputs'))
        input_html = str(header) + ''.join(str(sibling) for sibling in header.find_next_siblings())
        file_path = get_file_path(url) + "input.html"
        input_dict = {file_path: input_html}
    finally:
        return input_dict
    
def get_output(soup, url):
    output_dict = None
    try:
        header = soup.find('h3', string=lambda text: text and text.lower() in ('output', 'outputs'))
        output_html = str(header) + ''.join(str(sibling) for sibling in header.find_next_siblings())
        file_path = get_file_path(url) + "output.html"
        output_dict = {file_path: output_html}
    finally:
        return output_dict
        

def get_score(soup, url):
    score_dict = None
    try:
        p_tags = soup.find_all('p')
        score = None
        for p_tag in p_tags:
            p_text = p_tag.get_text()
            if p_text.startswith('Score : '):
                score = int(p_text.split(':')[1].split()[0])
                break
        file_path = get_file_path(url) + "score.txt"
        score_dict = {file_path: score}
    finally:
        return score_dict

def get_sample_inputs_and_outputs(soup, url):
    inputs_outputs_dict = None
    try:
        h3_tags = soup.find_all('h3')
        for h3_tag in h3_tags:
            if h3_tag.get_text().startswith(('Sample Input ', 'Sample Output ')):
                file_path = get_file_path(url) + h3_tag.get_text().lower().replace(' ', '_') + ".txt"
                input_or_output_text = h3_tag.find_next_sibling().get_text()
                if inputs_outputs_dict is None: inputs_outputs_dict=dict()
                inputs_outputs_dict[file_path] = input_or_output_text
    finally:
        return inputs_outputs_dict
    
def write_dict_to_file(file_text_dict):
    for path, text in file_text_dict.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding="utf-8") as file:
            file.write(str(text))

# Crawl the input URL
def crawl(url):
    soup = BeautifulSoup(requests.get(url).content, "lxml")

    #Gets the problem statement html and writes the url to an error doc if there is an error
    problem_statment = get_problem_statement(soup, url)
    if(problem_statment != None):
        write_dict_to_file(problem_statment)
    else:
        with open('./problem_statement_errors.txt', 'a') as file:
            file.write(url + '\n')

    #Gets the constraints html and writes the url to an error doc if there is an error
    constraints = get_constraints(soup, url)
    if(constraints != None):
        write_dict_to_file(constraints)
    else:
        with open('./constraints_errors.txt', 'a') as file:
            file.write(url + '\n')

    #Gets the input html and writes the url to an error doc if there is an error
    input = get_input(soup, url)
    if(input != None):
        write_dict_to_file(input)
    else:
        with open('./input_errors.txt', 'a') as file:
            file.write(url + '\n')

    #Gets the output html and writes the url to an error doc if there is an error
    output = get_output(soup, url)
    if(output != None):
        write_dict_to_file(output)
    else:
        with open('./output_errors.txt', 'a') as file:
            file.write(url + '\n')

    #Gets the score and writes the url to an error doc if there is an error
    score = get_score(soup, url)
    if(score != None):
        write_dict_to_file(score)
    else:
        with open('./score_errors.txt', 'a') as file:
            file.write(url + '\n')

    #Gets the sample inputs and sample outputs and writes the url to an error doc if there is an error
    sample_inputs_and_outputs = get_sample_inputs_and_outputs(soup, url)
    if(sample_inputs_and_outputs != None):
        write_dict_to_file(sample_inputs_and_outputs)
    else:
        with open('./sample_input_output_errors.txt', 'a') as file:
            file.write(url + '\n')

#Reads in all lines from path.txt (ex: "/media/sf_programming/research/atcoderCrawlerClone/competitions/abc218")
with open('./competitions/path.txt', 'r') as file:
    lines = file.readlines()

with open('./competitions/path1.txt', 'r') as file:
    lines += file.readlines()

with open('./competitions/path2.txt', 'r') as file:
    lines += file.readlines()

with open('./competitions/path3.txt', 'r') as file:
    lines += file.readlines()

urls = set()

#Gathering page urls
for line in lines:
    # Finds the name of the contest and creates a prefix. For each task, adds the url of the task to the set urls
    if line.count('/') == 6: 
        url_prefix = "https://atcoder.jp/contests/" + line[64:].rstrip('\n') + "/tasks"
    else:
        last_slash_index = line.rfind('/')
        urls.add(url_prefix + line[last_slash_index:].rstrip('\n'))

# #Crawling page urls
# counter = 0
# for url in urls:
#     print(f"URLs Visited: {counter}", end='\r')
#     crawl(url.strip())
#     counter += 1

class RateLimiter:
    def __init__(self, rate):
        self.delay = 1 / rate
        self.last_request = 0
        self.lock = threading.Lock()

    def wait_for_request_slot(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_request
            wait_time = max(0, self.delay - elapsed)

            if wait_time > 0:
                time.sleep(wait_time)
            
            self.last_request = time.time()

# Anything above this number results in an IP ban
rate_limiter = RateLimiter(2)

# Number of URLs crawled
counter = 0

def worker(url):
    global counter
    rate_limiter.wait_for_request_slot()

    crawl(url.strip())

    with lock:
        counter += 1
        print(f"\rURLs Crawled: {counter}", end='')

lock = threading.Lock()


#Concurrently crawling page urls
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(worker, url) for url in urls]

concurrent.futures.wait(futures)
print(f"Crawling complete. Processed {counter} URLs")