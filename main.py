from bs4 import BeautifulSoup as soup
import requests


def get_repo_names(response):
	soupy = soup(response.text,features ='html.parser')
	li_tags = soupy.find_all('li',class_='col-12 d-flex width-full py-4 border-bottom color-border-secondary public source')

	repo_names=[]
	for tag in li_tags:
		a_tag = tag.find('a',itemprop="name codeRepository")
		name = a_tag.attrs['href'].split('/')[-1]
		repo_names.append(name)
	return repo_names

def get_next_url(url):
	soupy = soup(response.text,features='html.parser')
	#div_tag = soupy.find('div',class_='paginate-container') #.find_all('a',value='Next').attrs['href']
	#print(div_tag)
	a_tag =  soupy.find('a',text='Next').attrs['href']
	#print(a_tag)
	return a_tag


user_name = input('Enter the URL to extract the repo names: ')
url = f'https://github.com/{user_name}?tab=repositories' 
#url = 'https://github.com/karthikmprakash?tab=repositories'
repo_names_list = []
dont_print = False
while url != None:
	response = requests.request('GET',url)
	
	if  '404' in str(response):
		print('\n You entered an invalid username')
		dont_print = True
		break
	repo_names = get_repo_names(response)
	repo_names_list = repo_names_list+repo_names
	
	try:
		next =  get_next_url(url)
		url = next
	except:
		break

if dont_print != True:	
	print(repo_names_list)
	file_flag = input('\n Do you want to save the output in a  file (Y/n) : ')
	if file_flag.lower() == 'y':
		with open(f'./OUTPUT/{user_name}.txt','w') as file:
			for item in repo_names_list:
        			file.write("%s\n" % item)
	elif file_flag.lower() == 'n':
		pass
	else:
		print('\n Enter a valid option')
