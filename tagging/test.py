from tagging import taggers
from tagging import tag_class
from tagging import refine
from tagging import process_image
from tagging.taggers import amazon_rekognition
from tagging.taggers import google_recognition
from tagging.taggers import imagga_recognition
import cloudinary

myImage = "D:\Documents\School\Information Science\ISC 220 Information Storage and Retrieval\Projects\\book.jpg"
puppyImage = cloudinary.CloudinaryImage("puppy.jpg").image

def print_tag_list(tag_list):
    if tag_list is None:
        print("empty")
    else:
        for t in tag_list:
            print(t)

def check_if_none(tag_list):
    if tag_list is None:
        print("empty")
    else:
        return tag_list



#taglist = refine.pre_process_tags(myImage)

taglist = process_image(myImage)

for t in taglist:
    print("Name: " + t.name )
    print("Number of results: " + str(t.number_of_results) + "\n")
    print("Amazon confidence: " + str(t.amazon_confidence_score) + "\n")
    print("Google confidence: " + str(t.google_confidence_score) + "\n")
    print("Imagga confidence: " + str(t.imagga_confidence_score) + "\n")


"""
amazon_tag_list = check_if_none(amazon_rekognition(
    myImage)["info"]["categorization"]["aws_rek_tagging"]["data"])
print("Amazon Data List: ")
print_tag_list(amazon_tag_list)
"""


# def pre_process_tags(image_to_be_processed):
#   """ Create lists of tags for amazon, google, and imagga"""
#    amazon_tag_list = taggers.amazon_rekognition(image_to_be_processed)["info"]["categorization"]["aws_rek_tagging"]["data"]
#    google_tag_list = taggers.google_recognition(image_to_be_processed)["info"]["categorization"]["google_tagging"]["data"]
#    imagga_tag_list = taggers.imagga_recognition(image_to_be_processed)["info"]["categorization"]["imagga_tagging"]["data"]
#    final_tag_list = []
#
#    """Add tags from the lists into final_tag_list, if it already exists in final_tag_list don't add it"""
#    for t in amazon_tag_list:
#        if t["tag"] in final_tag_list:
#            amazon_tag_list.pop(t)
#        else:
#            new_tag = tag_class.tag(amazon_tag_list.get(t)["tag"])
#            final_tag_list[t] = new_tag
#
#    for t in google_tag_list:
#        if t["tag"] in final_tag_list:
#            google_tag_list.pop(t)
#        else:
#            new_tag = tag_class.tag(google_tag_list.get(t)["tag"])
#            final_tag_list[t] = new_tag
#
#    for t in imagga_tag_list:
#        if t["tag"] in final_tag_list:
#            imagga_tag_list.pop(t)
#        else:
#            new_tag = tag_class.tag(imagga_tag_list.get(t)["tag"])
#            final_tag_list[t] = new_tag
#
#    final_tag_list = get_confidence_levels(final_tag_list, amazon_tag_list, google_tag_list, imagga_tag_list)
#
#    preprocessed_tag_list = search.search_tags(final_tag_list)
#
#    return preprocessed_tag_list
#
#
# def get_confidence_levels(final_tag_list, amz_tag_list, google_tag_list, imagga_tag_list):
#    for t in final_tag_list:
#        if t["tag"] in amz_tag_list:
#            final_tag_list[t].amazon_confidence_score = amz_tag_list.get(t)["confidence"]
#        if t["tag"] in google_tag_list:
#            final_tag_list[t].google_confidence_score = google_tag_list.get(t)["confidence"]
#        if t["tag"] in imagga_tag_list:
#            final_tag_list[t].imagga_confidence_score = imagga_tag_list.get(t)["confidence"]
#    return final_tag_list
#
#
# preprocessed_tags = pre_process_tags(myImage)
#
# print(preprocessed_tags)
