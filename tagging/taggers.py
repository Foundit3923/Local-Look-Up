import cloudinary
import cloudinary.uploader as cl
"""
cloudinary.config(
  cloud_name = 'suny-oswego',
  api_key = '842545957931494',
  api_secret = 'rapiSZ63Eg8RAej0WvMaH1b5nzg'
)
cloudinary.config(
  cloud_name = 'ddlpjd6l2',
  api_key = '794562159432825',  api_secret = 'bd7PYgoOqurnameJt5dBEp2cEbk'
)
#CLOUDINARY_URL=cloudinary://794562159432825:bd7PYgoOqurnameJt5dBEp2cEbk@ddlpjd6l2
"""
cloudinary.config(
  cloud_name = 'dkneqbvjb',
  api_key = '611177588635684',  api_secret = 'LqbCNElTt77LnnMVjgVthglswTo'
)
#CLOUDINARY_URL=cloudinary://611177588635684:LqbCNElTt77LnnMVjgVthglswTo@dkneqbvjb

""" Amazon tagger """


def amazon_rekognition(image_to_be_tagged):
    return cl.upload(image_to_be_tagged, categorization="aws_rek_tagging")



def amazon_rekognition_with_threshold(image_to_be_tagged, threshold):
    cl.upload(image_to_be_tagged, categorization="aws_rek_tagging", auto_tagging=threshold)


""" Google Tagger """


def google_recognition(image_to_be_tagged):
    cl.upload(image_to_be_tagged, categorization="google_tagging")


def google_recognition_with_threshold(image_to_be_tagged, threshold):
    cl.upload(image_to_be_tagged, categorization="google_tagging", auto_tagging=threshold)


""" Imagga tagger """


def imagga_recognition(image_to_be_tagged):
    cl.upload(image_to_be_tagged, categorization="imagga_tagging")


def imagga_recognition_with_threshold(image_to_be_tagged, threshold):
    cl.upload(image_to_be_tagged, categorization="imagga_tagging", auto_tagging=threshold)
