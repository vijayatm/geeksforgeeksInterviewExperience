from bs4 import BeautifulSoup
from string import ascii_lowercase
import urllib.request
import pdfkit
import os
counter = 0

url ='https://www.geeksforgeeks.org/company-interview-corner/'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
baseLocation = 'F:/git/GeeksForGeeks/Experience_posts/'

strings = soup.find('ul', {"class":"sUlClass"}) #get the list of all company's unordered list 

for link in strings.find_all('a',href=True): #get the listitem of the class sUlClass (company link under the name)
	link = link['href'] #assign the right hand side to left hand side 
	# print (link) #prints the company name link
	companyName = link.replace("https://www.geeksforgeeks.org/tag/","")
	companyName = companyName.replace("/","")
	
	if not os.path.exists(baseLocation+companyName):
		print ('Downloading company files: ' +companyName)
		for counter in range (0,50): #looping from the start page to the last page (given maximum, will break if failed)
			try:
				link_page = (link+"page/{counter}/".format(counter=counter+1)) #appended counter with the link (page number looping)
				# print (link_page)   #printing the link_page with page number
				htmlCompany = urllib.request.urlopen(link_page).read()  #parse the html of the page numbered company name page
				soup_company = BeautifulSoup(htmlCompany,'html.parser') #parse the individual company page
				if not (soup_company.find('h1',text="Nothing Here!")): #check if the page does not contains 'nothing here' page 
					archives = soup_company.find(id="content") 
					for post in archives.select('h2.entry-title a[href]'):
						post = post['href']
						post_fileName = post.replace("https://www.geeksforgeeks.org/","")
						post_fileName = post_fileName.replace("/","")
						absoluteLocation = baseLocation+companyName+"/"+post_fileName

						# print ("absoluteLocation: "+absoluteLocation+".pdf")
						# pdfkit.from_url(post, absoluteLocation+".pdf")
						if not os.path.exists(baseLocation+companyName):
							os.makedirs(baseLocation+companyName)
							if not os.path.exists(absoluteLocation+".pdf"):
								pdfkit.from_url(post, absoluteLocation+".pdf")	
								print ('Pdf Save Success: '+post_fileName) 	# prints all the archive experience links
							else:
								print ('file already exists')	
						else:	
							if not os.path.exists(absoluteLocation+".pdf"):
								pdfkit.from_url(post, absoluteLocation+".pdf")	
								print ('Pdf Save Success: '+post_fileName) 	# prints all the archive experience links
							else:
								print ('file already exists')	
					counter += 1	
				else:
					print ("nothing to fetch here-loop1")
			except urllib.error.HTTPError as err:	
				if (err.code != 404):
					htmlCompany = urllib.request.urlopen(link_page).read()	
				else:

					print("nothing to fetch here-loop2")	
					break	