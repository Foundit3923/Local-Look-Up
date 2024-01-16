from tagging import search
from tagging import refine
from pip._internal import main as pm
pkgs = ['bs4', 'urllib.parse', 'urllib.request', 'webbrowser', 'os', 'time']
for package in pkgs:
    try:
        import package
    except ImportError as e:
        pm(['install', package])
import webbrowser
import os
import time

def process_image ( image_to_be_processed ):
    start = time.time()
    os.system("set CLOUDINARY_URL=cloudinary://611177588635684:LqbCNElTt77LnnMVjgVthglswTo@dkneqbvjb")
    preprocessed_tag_list = refine.pre_process_tags(image_to_be_processed)
    processed_tag_list = refine.compare_tags_for_relevance( preprocessed_tag_list )
    final_tag = search.get_map_url(processed_tag_list)
    webbrowser.open_new_tab(final_tag[0].map_url)
    end = time.time()
    final_tag[0].execution_time = end - start
    return final_tag

def process_image_demo ():
    current_dir = os.path.dirname(os.path.dirname(__file__))
    myimage = current_dir + "/tagging/book.jpg"
    list = process_image(myimage)
    for tag in list:
        tag.display()
        #print("Tag: " + tag.name)
        #print("Number of results: " + tag.number_of_results)
        #print("Confidence score: " + str(tag.amazon_confidence_score))
        #print("Map URL: " + tag.map_url)
        print("Execution time: " + str(tag.execution_time) + " seconds")

process_image_demo()

