# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 22:06:34 2022

@author: Max
"""

from flask import Flask, request, render_template
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import pdfkit

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
        elif i == 'vegetarian':
            Protein.append('veg')
        else:
            Protein.append(i)
    recipes['Protein'] = Protein
    l1 = [sun,mon,tue,wed,thu,fri,sat]
    l2 = []
    for i in range(7):
        j = l1[i]
        if l1[i] == 'i do not need a recipe for this day':
            l2.append('You have not requested a recipe for today.')
        else:
            l2.append(random.choice(list(recipes[recipes['Protein'] == j]['Recipe'])))

    ing2 = []
    link = []
    for i in l2:
        if i == 'You have not requested a recipe for today.':
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
    return render_template('Home.html')

@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    if request.method == 'POST':
        if request.form['sun'] == 'Vegetarian':
            sun = 'veg'
        else:
            sun = request.form['sun']
        if request.form['mon'] == 'Vegetarian':
            mon = 'veg'
        else:
            mon = request.form['mon']
        if request.form['tue'] == 'Vegetarian':
            tue = 'veg'
        else:
            tue = request.form['tue']
        if request.form['wed'] == 'Vegetarian':
            wed = 'veg'
        else:
            wed = request.form['wed']
        if request.form['thu'] == 'Vegetarian':
            thu = 'veg'
        else:
            thu = request.form['thu']
        if request.form['fri'] == 'Vegetarian':
            fri = 'veg'
        else:
            fri = request.form['fri']
        if request.form['sat'] == 'Vegetarian':
            sat = 'veg'
        else:
            sat = request.form['sat']
        
        generatePlan(sun,mon,tue,wed,thu,fri,sat)
        
        update()
        
        return render_template('index.html', sun_meal = str(l2[0]), sun_ing = str(ing3[0]), sun_link = "'" + str(link[0]) + "'", mon_meal = str(l2[1]), mon_ing = str(ing3[1]), mon_link = "'" + str(link[1]) + "'", tue_meal = str(l2[2]), tue_ing = str(ing3[2]), tue_link = "'" + str(link[2]) + "'", wed_meal = str(l2[3]), wed_ing = str(ing3[3]), wed_link = "'" + str(link[3]) + "'", thu_meal = str(l2[4]), thu_ing = str(ing3[4]), thu_link = "'" + str(link[4]) + "'", fri_meal = str(l2[5]), fri_ing = str(ing3[5]), fri_link = "'" + str(link[5]) + "'", sat_meal = str(l2[6]), sat_ing = str(ing3[6]), sat_link = "'" + str(link[6]) + "'")
        
    else:
        return 'Error'

#@app.route('/close')
#def plan():
    #return render_template('index.html')
    
if __name__ == '__main__':
  app.run(debug=True) 