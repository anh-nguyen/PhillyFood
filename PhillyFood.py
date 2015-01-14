from bs4 import BeautifulSoup
import urllib2

# grab all food options and URLs from PhillyMag website, store in dictionary
# if user chooses a certain food that is in the list, go to the webpage for that food item and get the information of the best restaurant. Cache this information.
# otherwise, check if there are foods list with similar spellings and make suggestions as appropriate.

def best_of_philly():
    food_dict = {}
    
    def grab_info(item_key):
        if len(food_dict[item_key]) == 1:
            link_soup = BeautifulSoup(urllib2.urlopen(food_dict[item_key][0]))
            best_restaurant = link_soup.find("article", class_ = "entry-best_of")
            r_name = best_restaurant("h3")[0].text.strip()
            r_title = best_restaurant("h2")[0].text.strip()
            r_description = best_restaurant("p", limit = 1)[0].text.strip()
            r_address = best_restaurant("b")[0].text.strip()
            if "Website" in r_address:
                r_address = r_address[:-10]
            food_dict[item_key].append(r_name)
            food_dict[item_key].append(r_title)
            food_dict[item_key].append(r_description)
            food_dict[item_key].append(r_address)
        
        print ("Let's go to " + food_dict[item_key][1] + ".")
        print ("It is rated " + food_dict[item_key][2] + " by the PhillyMag.")
        print ("Here is what PhillyMag says about it: " + food_dict[item_key][3])
        print ("It's at " + food_dict[item_key][4] + ".")
        print "\n"
    
    
    link_soup = BeautifulSoup(urllib2.urlopen("http://www.phillymag.com/best-of-philly/category/restaurants-and-bars/"))
    raw_links =  link_soup.find("ul", class_="best_of_list")("a")
    for item in raw_links:
        food_dict[item.text.strip().title()[5:-2]] = [item["href"]]
    while True:
        input = raw_input("What would you like to eat? To see all food options, type \"options\". If you are done, type \"exit\".").lower()    
        if input == "options":
            for item in food_dict.keys():
                print item
        elif input == "exit":
            exit()
        else:
            if input.title() not in food_dict.keys():
                if input[-1] == "s": input = input[:-1]
                list_of_options = [i for i in food_dict.keys() if input.title() in i]
                if list_of_options != []:
                    options_as_string = ' or '.join(list_of_options)
                    extra = raw_input("Were you looking for any of these food options? Either type the name of the food or \"no\" to go back. \n" + options_as_string)
                    if extra.lower() == "no":
                        pass
                    elif extra.title() not in food_dict.keys():
                        print ("Input invalid! Type \"options\" to see what food is available. \n")
                    else:
                        grab_info(extra.title())  
                else:
                    print ("Input invalid! Type \"options\" to see what food is available. \n")
            else:
                grab_info(input.title())
            
   
        
if __name__ == "__main__":
    best_of_philly()

