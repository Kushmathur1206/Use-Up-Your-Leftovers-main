# Scraping Recipes - All Recipes
import html
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np
import json 

base_url = 'https://www.allrecipes.com/recipes/84/healthy-recipes/'

"""<a id="mntl-card-list-items_1-0-8" class="comp mntl-card-list-items mntl-document-card mntl-card card card--no-image" data-doc-id="6655354" data-tax-levels="" href="https://www.allrecipes.com/article/shop-once-grill-all-week/" data-cta="" data-ordinal="9">
<div class="loc card__top">
<div class="card__media mntl-universal-image card__media universal-image__container">
<div class="img-placeholder" style="padding-bottom:66.6%;">
<img data-src="https://www.allrecipes.com/thmb/hF9EEzbn5VT7_q-kwfygkfCJLHE=/282x188/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/Gass-Grill-2000-abda9b8efccc4bb8a7e58d2da6e2899a.jpg" width="282" height="188" alt="Hamburgers and hot dogs on a gas grill" class="card__img universal-image__image lazyloaded" data-expand="300" src="https://www.allrecipes.com/thmb/hF9EEzbn5VT7_q-kwfygkfCJLHE=/282x188/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/Gass-Grill-2000-abda9b8efccc4bb8a7e58d2da6e2899a.jpg">
<noscript>
<img
src="https://www.allrecipes.com/thmb/hF9EEzbn5VT7_q-kwfygkfCJLHE=/282x188/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/Gass-Grill-2000-abda9b8efccc4bb8a7e58d2da6e2899a.jpg"
width="282"
height="188"
class="img--noscript card__img universal-image__image"
alt="Hamburgers and hot dogs on a gas grill"
/>
</noscript>
</div></div>
</div>
<div class="card__content" data-tag="Buying">
<div class="card__header"></div>
<span class="card__title"><span class="card__title-text ">Shop Once, Grill All Week</span></span>
</div>
</a>"""

recipe_titles = []
recipe_img_links = []
recipe_ingredients = []
recipe_intructions = []

recipes_dict = dict()

recipe_count = 0


for i in range(2, 3):# 417):
    
    print("Page "+str(i)+" scraping started!!!")
    
    url = base_url
    req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage,"html.parser")
    
    recipe_links_on_page = []
    
    anchors = page_soup.find_all('a', {'class': 'comp mntl-card-list-items mntl-document-card mntl-card card card--no-image'})
    
    for anchor in anchors:
        recipe_links_on_page.append(anchor['href'])
        
    for recipe_url in recipe_links_on_page:
        req_recipe = Request(recipe_url, headers={'User-Agent':'Mozilla/5.0'})
        webpage_recipe = urlopen(req_recipe).read()
        page_soup_recipe = soup(webpage_recipe,"html.parser")
        
        # Name of Recipe
        name = page_soup_recipe.find('h1',class_='comp type--lion article-heading mntl-text-block').text
        
        print('name = ',name)
        
        # Ingredients
        try:
            ingredients = page_soup_recipe.find('ul',class_ = 'mntl-structured-ingredients__list').find_all('li', class_ ='mntl-structured-ingredients__list-item')
            temp_ingredients = []
            for ingredient in ingredients:
                temp_ingredients.append(ingredient.text.strip())
        except Exception:
            temp_ingredients=[]
        
        
        
        recipe_ingredients.append(temp_ingredients)
        print('temp_ingredients = ',len(temp_ingredients))
        print(" ")
        
        
        if(len(temp_ingredients)>0): 
            # Recipe 
            recipe_titles.append(name)
            recipes = page_soup_recipe.find('ol',  {"class": "comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup"}).findAll("li", recursive=False)
            temp_recipe = []
            
            for i in range(len(recipes)):
                temp_recipe.append(recipes[i].find('p').text)
            
            recipe_intructions.append(temp_recipe)
        
            # Image
           

            # Data to be written 
            dictionary ={ 
                "title" : recipe_titles[recipe_count], 
                "ingredients" : recipe_ingredients[recipe_count], 
                "instructions" : recipe_intructions[recipe_count], 
                #"picture_link" : recipe_img_links[recipe_count]
            }

            # Done with the recipe
            print("Recipe "+str(recipe_count)+" Scrapped")
            recipe_count += 1
            # Adding to recipes_dict
            recipes_dict[recipe_count] = dictionary
        else:
            continue
        
    print("Page "+str(i)+" Scraped!!!")
         
# Storing Dataframe to JSON file format for training
# Serializing json  
json_object = json.dumps(recipes_dict, indent = 4) 
  
# Writing to dataset_ar.json 
with open("dataset_ar.json", "w") as outfile: 
    outfile.write(json_object)

# Storing in CSV File
dataset_ar = pd.DataFrame(list(zip(recipe_titles, recipe_ingredients, recipe_intructions)), 
               columns =['title', 'ingredients', 'instructions'])
dataset_ar.to_csv('.\dataset_ar2.csv')
