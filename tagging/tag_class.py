class tag:

    amazon_confidence_score = 0.0
    google_confidence_score = 0.0
    imagga_confidence_score = 0.0
    #average_confidence_score = (amazon_confidence_score + google_confidence_score + imagga_confidence_score) / 3
    tag_one = 0
    tag_two = 0
    map_url = ""
    execution_time = 0

    number_of_results = 0

    def __init__(self, name):
        self.name = name

    def display (self):
        print("Tag name: " + str(self.name))
        print("Amazon confidence: " + str(self.amazon_confidence_score))
        print("Google confidence: " + str(self.google_confidence_score))
        print("Imagga confidence: " + str(self.imagga_confidence_score))
        #print("Average confidence: " + str(self.average_confidence_score))
        print("Number of results: " + str(self.number_of_results))

    def dominant_tag(self):
        if int(self.tag_one.number_of_results) > int(self.tag_two.number_of_results):
            return self.tag_one
        else:
            return self.tag_two
