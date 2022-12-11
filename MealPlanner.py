from flask import Flask, request, render_template
import pandas as pd
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import random

def generatePlan(sun,mon,tue,wed,thu,fri,sat):
    sun = sun.lower()
    mon = mon.lower()
    tue = tue.lower()
    wed = wed.lower()
    thu = thu.lower()
    fri = fri.lower()
    sat = sat.lower()    
    
    recipes = pd.read_excel("recipe_archive.xlsx")
    Protein = []
    for i in recipes.Protien:
        if i == 'pancetta':
            Protein.append('pork')
        elif i in ['haddock','salmon','shrimp','cod']:
            Protein.append('fish')
        else:
            Protein.append(i)
    recipes['Protein'] = Protein
    l1 = [sun,mon,tue,wed,thu,fri,sat]
    l2 = []
    for i in range(7):
        j = l1[i]
        if l1[i] == 'i do not need a recipe for this day':
            l2.append('You have not selected a recipe for today.')
        else:
            l2.append(random.choice(list(recipes[recipes['Protein'] == j]['Recipe'])))

    ing2 = []
    link = []
    for i in l2:
        if i == 'You have not selected a recipe for today.':
            k = ""
            l = ""
        else:
            j = (list(recipes['Recipe']).index(i))
            k = recipes.Link[j]
            l = recipes.Ingredients[j].replace("[",'').replace("]",'').replace("'","").split(", ")
            for p in l:
                if ' spice' in p:
                    n = (l.index(p))
                    l = l[:n]
                else:
                    l = l
        link.append(k)
        ing2.append(l)
        
        ing3 = []
        for i in ing2:
            ing3.append(str(i).replace("['","").replace("']","<br>").replace("', '","<br>"))
        
    ing4 = []
    for i in ing2:
        for j in i:
            ing4.append(j)
    
    ing4 = pd.DataFrame({'Ingredients':ing4})
    
    ing4.to_csv('Grocery_List.csv', index = False)
    
    # HTML
    
    f = open('index_V2.html','w')
    
    m1 = """<!DOCTYPE html>
    <html><meta charset="utf-8" />
    	<head>
    		<title>Weekly Mean Plan</title>
    		<style>
    			.button {
    				height: 75px;
    				width: 150px;  				
    				background-color: red;
      				border: none;
      				color: white;
      				padding: 20px;
      				text-align: center;
      				text-decoration: none;
      				display: inline-block;
      				font-size: 16px;
      				margin: 4px 4px;
    				}
    		</style>
    	</head>
    	<body>
    		<table class="table table_main" border="5">
     			<tr>
      			 	<td>Sunday</td>
      			 	<td>&nbsp;
    					<table class="table table1">
    						<tr>
    							<th><h3>"""
    m2 = str(l2[0])
    m3 = """</h3></th>
    						</tr>
    						<tr>
    							<td>"""
    m4 = str(ing3[0])
    m5 = """</td>
    						</tr>
    					</table>
                        <a href="""
    m6 = "'" + str(link[0]) + "'"
    m7 = """><strong>View Recipe</strong></a>
                    </td>
     			</tr>
     			<tr>
      			 	<td>Monday</td>
      			 	<td>&nbsp;
    					<table class="table table1">
    						<tr>
    							<th><h3>"""
    m8 = str(l2[1])
    m9 = """</h3></th>
    						</tr>
    						<tr>
    							<td>"""
    m10 = str(ing3[1])
    m11 = """</td>
    						</tr>
    					</table>
                        <a href="""
    m12 = "'" + str(link[1]) + "'"
    m13 = """><strong>View Recipe</strong></a>
                    </td>
     			</tr>
                 <tr>
      			 	<td>Tuesday</td>
      			 	<td>&nbsp;
    					<table class="table table1">
    						<tr>
    							<th><h3>"""
    m14 = str(l2[2])
    m15 = """</h3></th>
    						</tr>
    						<tr>
    							<td>"""
    m16 = str(ing3[2])
    m17 = """</td>
    						</tr>
    					</table>
                        <a href="""
    m18 = "'" + str(link[2]) + "'"
    m19 = """><strong>View Recipe</strong></a>
                    </td>
     			</tr>
                 <tr>
      			 	<td>Wednesday</td>
      			 	<td>&nbsp;
    					<table class="table table1">
    						<tr>
    							<th><h3>"""
    m20 = str(l2[3])
    m21 = """</h3></th>
    						</tr>
    						<tr>
    							<td>"""
    m22 = str(ing3[3])
    m23 = """</td>
    						</tr>
    					</table>
                        <a href="""
    m24 = "'" + str(link[3]) + "'"
    m25 = """><strong>View Recipe</strong></a>
                    </td>
     			</tr>
                 <tr>
      			 	<td>Thursday</td>
      			 	<td>&nbsp;
    					<table class="table table1">
    						<tr>
    							<th><h3>"""
    m26 = str(l2[4])
    m27 = """</h3></th>
    						</tr>
    						<tr>
    							<td>"""
    m28 = str(ing3[4])
    m29 = """</td>
    						</tr>
    					</table>
                        <a href="""
    m30 = "'" + str(link[4]) + "'"
    m31 = """><strong>View Recipe</strong></a>
                    </td>
     			</tr>
                 <tr>
      			 	<td>Friday</td>
      			 	<td>&nbsp;
    					<table class="table table1">
    						<tr>
    							<th><h3>"""
    m32 = str(l2[5])
    m33 = """</h3></th>
    						</tr>
    						<tr>
    							<td>"""
    m34 = str(ing3[5])
    m35 = """</td>
    						</tr>
    					</table>
                        <a href="""
    m36 = "'" + str(link[5]) + "'"
    m37 = """><strong>View Recipe</strong></a>
                    </td>
     			</tr>
                 <tr>
      			 	<td>Saturday</td>
      			 	<td>&nbsp;
    					<table class="table table1">
    						<tr>
    							<th><h3>"""
    m38 = str(l2[6])
    m39 = """</h3></th>
    						</tr>
    						<tr>
    							<td>"""
    m40 = str(ing3[6])
    m41 = """</td>
    						</tr>
    					</table>
                        <a href="""
    m42 = "'" + str(link[6]) + "'"
    m43 = """><strong>View Recipe</strong></a>
                    </td>
     			</tr>
    		</table>
    	</body>
    </html>"""
    
    g = [m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,m28,m29,m30,m31,m32,m33,m34,m35,m36,m37,m38,m39,m40,m41,m42,m43]
    
    for i in g:
        f.write(i)
    f.close()
    
    with open('index_V2.html', 'r') as f: 
        html_string = f.read()
    
    html_string.replace("<a>'","<a>").replace("'</a>","</a>")
    
    f = open('index_V2.html','w')
    f.write(html_string)
    f.close()
    
def email(email1, email2):
    email_to = [email1, email2]
    
    with open('index_V2.html', 'r') as f: 
            html_string = f.read()
            
    new_html = html_string.replace('''<style>
        			.button {
        				height: 75px;
        				width: 150px;  				
        				background-color: red;
          				border: none;
          				color: white;
          				padding: 20px;
          				text-align: center;
          				text-decoration: none;
          				display: inline-block;
          				font-size: 16px;
          				margin: 4px 4px;
        				}
        		</style>')''','')
    
    username = "${{ secrets.EMAIL_ADDRESS }}"
    password = "${{ secrets.EMAIL_PASSWORD }}"
    smtp_server = "smtp.gmail.com:587"
    email_from = "${{ secrets.EMAIL_ADDRESS }}"
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "This Week's Meal Plan"
    msg['From'] = email_from
    msg['To'] = ", ".join(email_to)
    html = MIMEText(new_html, 'html')
    msg.attach(html)
    
    # Attachements
    filename = "Grocery_List.csv"
    attachment = open("Grocery_List.csv", "rb")
    #htmlname = "index_V2.html"
    #attachment2 = open("index_V2.html", "rb")
      
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    #q = MIMEBase('application', 'octet-stream')
    
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    #q.set_payload((attachment2).read())
    
    # encode into base64
    encoders.encode_base64(p)
    #encoders.encode_base64(q)
       
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    #q.add_header('Content-Disposition', "attachment; filename= %s" % htmlname)  
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    #msg.attach(q)
    
    server = smtplib.SMTP(smtp_server)
    server.starttls()
    server.login(username, password)
    server.sendmail(email_from, email_to, msg.as_string())
    server.quit()    
    
def update():
    url = 'https://www.makegoodfood.ca/en/recipes'
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]
    
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    
    # defining recipe lists
    classic_start = output.index('Classic plan recipes')       # identifying start of classic subscript
    rapido_start = output.index('Rapido recipes')              # identifying start of rapido subscript
    clean_start = output.index('Clean15 recipes')              # indentify start of clean subscript
    vegetarian_start = output.index('Vegetarian recipes')      # indentify start of vegetarian subscript
    family_start = output.index('Family recipes')              # identify start of family subscript
    end = output.index('PREVIOUS WEEK')                        # identify end of all recipes
    
    classic_recipes = (output[classic_start+97:rapido_start].split('\n \n'))                      # subscript ends at end of text
    rapido_recipes = output[rapido_start+91:clean_start].split('\n \n')
    clean_recipes = output[clean_start+103:vegetarian_start].split('\n \n')
    vegetarian_recipes = output[vegetarian_start+98:family_start].split('\n \n')
    family_recipes = output[family_start+93:end].split('\n \n')
    
    recipeTypes = [classic_recipes, rapido_recipes, clean_recipes, vegetarian_recipes, family_recipes]
    
    # deriving the final recipe list
    
    allRecipes = []
    for i in recipeTypes:
        for j in i:
            if j != ' ':
                allRecipes.append(j.lstrip().rstrip().replace('\n ','').replace('& ','').replace(',','').split(' with')[0])
    
    for i in allRecipes:
        if i == '':
            allRecipes.remove(i)
        else:
            continue
    
    all_recipes_no_spaces = []
    for i in allRecipes:
        all_recipes_no_spaces.append(i.replace(' ','').replace('-',''))
        
    recipe_key = []
    for i in all_recipes_no_spaces:
        recipe_key.append(i.lower()[:10])
        
    recipe_dict = {'Recipe':allRecipes,'key':recipe_key}
    recipe_df = pd.DataFrame(recipe_dict)
    
    # trying to grab all hpyerlinks from webpage
    soup = BeautifulSoup(html_page, "lxml")
    
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    
    links = list(dict.fromkeys(links[19:62]))
    
    links_no_lead = []
    for i in links:
        links_no_lead.append(i[38:].replace('-',''))
        
    links_key = []
    for i in links_no_lead:
        links_key.append(i[:10])
        
    links_dict = {'Link':links, 'key':links_key}
    links_df = pd.DataFrame(links_dict)
    
    # create df3
    
    df3 = pd.merge(recipe_df, links_df).drop_duplicates(subset=['Recipe'])
    df3.drop('key', axis=1, inplace=True)
    
    # Begin pulling recipe page data
    
    recipe_ingredients = []
    for i in df3['Link']:  # this is just a placeholder. Make this the looped variable later on
        res = requests.get(i)
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html.parser')
        text = soup.find_all(text=True)
        
        output = ''
        blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head', 
            'input',
            'script',
            # there may be more elements you don't want, such as "style", etc.
        ]
        
        for t in text:
            if t.parent.name not in blacklist:
                output += '{} '.format(t)
        
        ingredients_start = output.index('We will send you:')
        if 'Contains: ' in output:
            ingredients_end = output.index('Contains: ')
        else:
            ingredients_end = output.index('You will need: ')
        
        ingredients = output[ingredients_start:ingredients_end].split('\n \n')
        ingredients_list = []
        for i in ingredients:
            ingredients_list.append(i.replace('\n                       ','').lstrip().rstrip())
        
        for i in ingredients_list:
            if i == "":
                ingredients_list.remove(i)
            elif i == 'We will send you:':
                ingredients_list.remove(i)
            else:
                continue
            
        recipe_ingredients.append(ingredients_list[:-4])
    
    # append ingredients to df 3
    
    df3['Ingredients'] = recipe_ingredients
    
    # create protien type list
    
    Protien = []
    for i in df3['Ingredients']:
        if "Chicken" in i[0]:
            Protien.append("chicken")
        elif "Pork" in i[0]:
            Protien.append("pork")
        elif "pork" in i[0]:
            Protien.append('pork')
        elif "Pancetta" in i[0]:
            Protien.append("pancetta")
        elif "Haddock" in i[0]:
            Protien.append("haddock")
        elif "Salmon" in i[0]:
            Protien.append("salmon")
        elif "Shrimp" in i[0]:
            Protien.append("shrimp")
        elif "Cod" in i[0]:
            Protien.append("Cod")
        elif "cod" in i[0]:
            Protien.append("Cod")
        elif "Beef" in i[0]:
            Protien.append('beef')
        elif "beef" in i[0]:
            Protien.append('beef')
        elif "lamb" in i[0]:
            Protien.append('lamb')
        else:
            Protien.append("veg")
        
    df3['Protien'] = Protien
    
    # append list to excel
    recipe_master = pd.read_excel("recipe_archive.xlsx")
    recipe_master = recipe_master.append(df3).drop_duplicates(subset=['Recipe'])
    recipe_master.to_excel("recipe_archive.xlsx",index = False)

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('Home_V2.html')

@app.route('/', methods=['POST'])
def my_form_post():
    sun = request.form['sun']
    mon = request.form['mon']
    tue = request.form['tue']
    wed = request.form['wed']
    thu = request.form['thu']
    fri = request.form['fri']
    sat = request.form['sat']
    
    email1 = request.form['email1']
    email2 = request.form['email2']
    
    generatePlan(sun,mon,tue,wed,thu,fri,sat)
    
    email(email1, email2)
    
    if email2 == "":
        processed_text = 'An email has been sent to ' + email1
    else:    
        processed_text = 'An email has been sent to ' + email1 + ' & ' + email2
    
    return processed_text

    update()
    
if __name__ == '__main__':
  app.run(debug=True) 
