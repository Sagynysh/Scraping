#!/usr/bin/env python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

book_list = []
page_size = 50
main_url = "http://books.toscrape.com/catalogue/";
rate_map = {'One':1,'Two':2,'Three':3,'Four':4,'Five':5}

def main():
	for pageIndex in range(page_size):
		print(pageIndex)
		page = urlopen(main_url+"page-"+str(pageIndex+1)+".html")
		html_bytes = page.read()
		html = html_bytes.decode("utf-8")
		soup = BeautifulSoup(html,features="html.parser")

		for article in soup.findAll('article', attrs={'class':'product_pod'}):
			book_name = article.h3.a.text
			books_price = article.findAll('div', attrs={'class':'product_price'})[0].find('p').text
			url_inner = article.h3.a['href']
			page_detail = urlopen(main_url+url_inner)
			html_bytes = page_detail.read()
			html_detail = html_bytes.decode("utf-8")
			soup_detail = BeautifulSoup(html_detail,features="html.parser")

			book = Book(book_name,books_price)

			for detail in soup_detail.findAll('article',attrs={'class':'product_page'}):
				genre = soup_detail.find('ul',attrs={'class':'breadcrumb'}).findAll('li')[2].a.text
				detail_desc = detail.findAll('p')[3].text
				rating = rate_map[detail.find('p',attrs={'class':'star-rating'})['class'][1]]
				print(rating)
				UPC = ''
				tax = 0
				inStock = False
				available = 0
				reviews = 0
				for tr in detail.table.findAll('tr'):
					if(tr.th.text == "UPC"):
						UPC = tr.td.text
					elif(tr.th.text == 'Tax'):
						tax = tr.td.text
					elif(tr.th.text == 'Availability'):
						if(tr.td.find('In stock') != -1):
							inStock = True
						available = int(tr.td.text[tr.td.text.find('(')+1:tr.td.text.find(' available')])
					elif(tr.th.text == 'Number of reviews'):
						reviews = int(tr.td.text)

				book.UPC = UPC
				book.tax = tax
				book.inStock = inStock
				book.available = available
				book.reviews = reviews
				book.detail_desc = detail_desc
				book.genre = genre
				book.rating = rating

			book_list.append(book)

		# for book in book_list:
			# print(book.name)

	df = pd.DataFrame([[book.name,book.price,book.detail_desc,book.UPC,book.tax,book.inStock,book.available,book.reviews,book.genre,book.rating] for book in book_list],
		columns=['Name','Price (£)','Detail Info','UPC','Tax (£)','In stock','Available','Number of reviews','Genre','Rating'])

	df.to_csv('bookStore.csv',index=False,encoding='utf-8')




class Book:
	genre = ''
	detail_desc = ''
	UPC = ''
	tax = 0
	inStock = False
	available = 0
	reviews = 0
	rating = 0

	def __init__ (self, name, price):
		self.name = name
		self.price = price


main()


# print(type(html))