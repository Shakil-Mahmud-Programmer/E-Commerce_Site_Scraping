from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import threading
import os
from config import SITE_DETAILS

class GetLinks:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.work_product = []
        self.track=[]
        self.img=[]
        self.data = []
        self.threads = []
        self.data_lock = threading.Lock()  # Lock for protecting data shared among threads

        self.get_work_pages()

    def get_work_pages(self):
        try:
            response = requests.get(url=self.url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, features='html.parser')
            page_count_text = soup.find('span', {'class': '_10Ermr'}).text
            match = int(re.search(r'– (\d+)', page_count_text).group(1))

            work_pages = [f'{self.url}&page={i}' for i in range(1, match + 1)]

#page Thread
            count = 0
            for i in work_pages:
                count += 1
                thread = threading.Thread(name=f'Thread- {count}', target=self.product_extract, args=(i,))
                thread.daemon=True
                thread.start()
                self.threads.append(thread)
                if threading.active_count() >= 20:
                    thread.join()
                    print(f'Page-Thread join- {thread.name}')

                
                
            for thread in self.threads:
                thread.join()
                print(f'Page Thread join- {thread.name}')

            self.threads.clear()

            self.work_product = [item for sublist in self.work_product for item in sublist]
            print(len(self.work_product))

#product thread
            num = 0
            for i in self.work_product:
                num += 1
                thread = threading.Thread(name=f'Thread- {num}', target=self.extract, args=(i,))
                thread.daemon=True
                thread.start()
                self.threads.append(thread)
                if threading.active_count() > 30:
                    for td in self.threads:
                        td.join()
                        print(f'Product-Thread join - {td.name}')
                    self.threads.clear()



            for thread in self.threads:
                print(f'Product Thread join - {thread.name}')
                thread.join()
            
            self.threads.clear()

            for i in self.track:
                num += 1
                thread = threading.Thread(name=f'Thread- {num}', target=self.extract, args=(i,))
                thread.daemon=True
                thread.start()
                print(f'Product missed thread - {thread.name}')
                self.threads.append(thread)


            for thread in self.threads:
                print(f'Product Thread join - {thread.name}')
                thread.join()

        except (requests.exceptions.RequestException, AttributeError) as e:
            print(f'Error: {str(e)}')
            return []

    def extract(self, i):
        row = []
        try:
            page = requests.get('https://flipkart.com' + i)
            con = BeautifulSoup(page.content, features='html.parser')
            row.append(con.find('span', attrs={'class': 'B_NuCI'}).text)
            row.append(con.find('div', attrs={'class': '_30jeq3 _16Jk6d'}).text)
            row.append(con.find('div', attrs={'class': '_3LWZlK'}).text)
            row.append(con.find('p').text.strip())


            with self.data_lock:
                self.data.append(row)
                
            print(f'Product {threading.current_thread().name} & Active Threads {threading.active_count()}')
            
        except Exception as e:
            self.track.append(i)
            print(f'Failed {threading.current_thread().name}: {str(e)}')

    def product_extract(self, i):
        product_links=[]
        div_elements = BeautifulSoup(requests.get(url=i, headers=self.headers).content, features='html.parser').find_all('div',{'class':'_1AtVbE col-12-12'})
        for div in div_elements:
            a_tags = list(set(div.find_all('a',rel="noopener noreferrer")))
            for a in a_tags:
                product_links.append(a.get('href'))

        
        # Acquire the lock before extending the shared list  '_1fQZEK'
        with self.data_lock:
            self.work_product.append(product_links)
        
        print(f'Page {threading.current_thread().name} & Active Threads {threading.active_count()}')

if __name__ == '__main__':
    links = GetLinks(SITE_DETAILS['URL'], SITE_DETAILS['HEADERS'])
    file_name = f'data.xlsx'
    folder_path = "data"
    os.makedirs(folder_path, exist_ok=True)
    
    pd.DataFrame(links.data, columns=('Name', 'Price', 'Rating', 'Description')).to_excel(os.path.join(folder_path, file_name), index=True)
    print(f'Number of products: {len(links.work_product)}')
