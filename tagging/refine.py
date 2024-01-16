from tagging import taggers
from tagging import tag_class
from tagging import search


def pre_process_tags(image_to_be_processed):
    """ Create lists of tags for amazon, google, and imagga"""
    amazon_tag_list = taggers.amazon_rekognition(image_to_be_processed)["info"]["categorization"]["aws_rek_tagging"][
        "data"]
    # google_tag_list = taggers.google_recognition(image_to_be_processed)["info"]["categorization"]["google_tagging"]["data"]
    # imagga_tag_list = taggers.imagga_recognition(image_to_be_processed)["info"]["categorization"]["imagga_tagging"]["data"]
    final_tag_list = []

    # print amazon_tag_list for testing purposes
    for t in amazon_tag_list:
        print(t)

    """Add tags from the lists into final_tag_list, if it already exists in final_tag_list don't add it"""
    for t in amazon_tag_list:
        if not final_tag_list:
            new_tag = tag_class.tag(t["tag"])
            new_tag.amazon_confidence_score = t["confidence"]
            final_tag_list.append(new_tag)
        else:
            for i in final_tag_list:
                if contains_tag(final_tag_list, t["tag"]):
                    i.amazon_confidence_score = t["confidence"]
                else:
                    # new_tag = tag_class.tag(amazon_tag_list[t]["tag"])
                    new_tag = tag_class.tag(t["tag"])
                    new_tag.amazon_confidence_score = t["confidence"]
                    final_tag_list.append(new_tag)

    # this code can be added in at a later date. some variables as well as a method or two will need changed to accomodate it. It will also need updated to look like the amazon_tag_list loop
    # for t in google_tag_list:
    #    if t["tag"] in final_tag_list:
    #        google_tag_list.pop(t)
    #    else:
    #        new_tag = tag_class.tag(google_tag_list.get(t)["tag"])
    #        final_tag_list[t] = new_tag

    # for t in imagga_tag_list:
    #    if t["tag"] in final_tag_list:
    #        imagga_tag_list.pop(t)
    #    else:
    #        new_tag = tag_class.tag(imagga_tag_list.get(t)["tag"])
    #        final_tag_list[t] = new_tag

    # this code is obsolete, confidence levels are added
    # final_tag_list = get_confidence_levels(final_tag_list, amazon_tag_list) #(final_tag_list, amazon_tag_list, google_tag_list, imagga_tag_list)

    preprocessed_tag_list = search.search_tags(final_tag_list)

    return preprocessed_tag_list


# various lines of code are commented out so that only amazon will run, simply replace uncommented code with commented code to restore full functionality
def get_confidence_levels(final_tag_list,
                          amz_tag_list):  # ( final_tag_list, amz_tag_list, google_tag_list, imagga_tag_list ):
    for t in final_tag_list:
        if t in amz_tag_list:
            # final_tag_list[t].amazon_confidence_score = amz_tag_list.get(t)["confidence"]
            final_tag_list[t].amazon_confidence_score = amz_tag_list[amz_tag_list.index(t["confidence"])]
        # if t["tag"] in google_tag_list:
        #    final_tag_list[t].google_confidence_score = google_tag_list.get(t)["confidence"]
        # if t["tag"] in imagga_tag_list:
        #    final_tag_list[t].imagga_confidence_score = imagga_tag_list.get(t)["confidence"]
    return final_tag_list


# tags are first sorted by confidence level, then compared against tags of the same level, highest ranking tags are compared to the highest ranking tags of other levels
def compare_tags_for_relevance(tag_list):
    sorted_tags = sort_tags_by_stats(tag_list)
    first_pass_sorted_tags = within_layer_sort(sorted_tags)
    second_pass_sorted_tags = between_layers_sort(first_pass_sorted_tags)
    return second_pass_sorted_tags


# tags are sorted by confidence level
def sort_tags_by_stats(tag_list):
    first_layer = []
    first_layer_threshold = .9

    second_layer = []
    second_layer_threshold = .75

    third_layer = []
    third_layer_threshold = .3

    sorted_list = []
    sorted_list.append(first_layer)
    sorted_list.append(second_layer)
    sorted_list.append(third_layer)

    for t in tag_list:
        if t.amazon_confidence_score >= first_layer_threshold:
            sorted_list[sorted_list.index(first_layer)].append(t)

        elif t.amazon_confidence_score >= second_layer_threshold:
            sorted_list[sorted_list.index(second_layer)].append(t)

        elif t.amazon_confidence_score >= third_layer_threshold:
            sorted_list[sorted_list.index(third_layer)].append(t)

    return sorted_list


# tags are compared to other tags of the same level
def within_layer_sort(tag_list):
    temp_tag_list = tag_list

    for layer in temp_tag_list:
        layer_buffer = []
        # for each layer check for null state
        if len(layer) != 0:
            # for each layer check for singleton state
            if len(layer) != 1:
                for tag in layer:
                    for second_tag in layer:
                        if tag != second_tag:
                            name = tag.name + " + " + second_tag.name
                            new_tag = tag_class.tag(name)
                            new_tag.tag_one = tag
                            new_tag.tag_two = second_tag
                            layer_buffer.append(new_tag)
            else:
                layer_buffer.append(layer[0])
        # empty layer_buffer into the apropriate layer
        temp_tag_list[temp_tag_list.index(layer)] = layer_buffer

    layer_one_searched = search.search_tags(temp_tag_list[0])
    layer_two_searched = search.search_tags(temp_tag_list[1])
    layer_three_searched = search.search_tags(temp_tag_list[2])

    # for each layer compare each tag to every other tag in that layer
    layer_one_top_five = []
    layer_two_top_five = []
    layer_three_top_five = []
    final_layer_list = []

    # check for empty state
    if len(layer_one_searched) != 0:
        # for each layer compare each tag to every other tag in that layer
        layer_one_top_five = get_top_five(layer_one_searched)

    if len(layer_two_searched) != 0:
        layer_two_top_five = get_top_five(layer_two_searched)

    if len(layer_three_searched) != 0:
        layer_three_top_five = get_top_five(layer_three_searched)


    final_layer_list.insert(0, layer_one_top_five)
    final_layer_list.insert(1, layer_two_top_five)
    final_layer_list.insert(2, layer_three_top_five)

    return final_layer_list


# tags are compared to other tags of different levels
def between_layers_sort(sorted_list):
    if sorted_list[0] != 0:
        layer_one_tag_list = sorted_list[0]
    else:
        layer_one_tag_list = []
    if sorted_list[1] != 0:
        layer_two_tag_list = sorted_list[1]
    else:
        layer_two_tag_list = []
    if sorted_list[2] != 0:
        layer_three_tag_list = sorted_list[2]
    else:
        layer_three_tag_list = []

    first_round_winners = between_third_and_second_sort(layer_three_tag_list, layer_two_tag_list)
    second_round_winners = between_second_and_first_sort(first_round_winners, layer_one_tag_list)

    return second_round_winners


# The highest ranking tags of the third and second level are compared
def between_third_and_second_sort(bottom_tag_list, middle_tag_list):
    temp_bottom_tag_list = bottom_tag_list
    temp_middle_tag_list = middle_tag_list
    new_list = []
    winners_list = []

    if len(temp_bottom_tag_list) > 0 and len(temp_middle_tag_list) > 0:
        for tag in temp_bottom_tag_list:
            for second_tag in temp_middle_tag_list:
                name = tag.name + " + " + second_tag.name
                new_tag = tag_class.tag(name)
                new_tag.tag_one = tag
                new_tag.tag_two = second_tag
                new_list.append(new_tag)
    elif len(temp_bottom_tag_list) == 0 and len(temp_middle_tag_list) > 0:
        new_list = temp_middle_tag_list
    elif len(temp_bottom_tag_list) > 0 and len(temp_middle_tag_list) == 0:
        new_list = temp_bottom_tag_list

    new_searched_tags_list = search.search_tags(new_list)

    if len(new_searched_tags_list) > 0:
        winners_list = get_top_five(new_searched_tags_list)

    return winners_list


# The highest ranking tags of the second and third level are compared
def between_second_and_first_sort(middle_tag_list, top_tag_list):
    temp_middle_tag_list = middle_tag_list
    temp_top_tag_list = top_tag_list
    new_list = []
    winners_list = []

    if len(temp_middle_tag_list) > 0 and len(temp_top_tag_list) > 0:
        for tag in temp_middle_tag_list:
            for second_tag in temp_top_tag_list:
                name = tag.dominant_tag().name + " + " + second_tag.name
                new_tag = tag_class.tag(name)
                new_tag.tag_one = tag
                new_tag.tag_two = second_tag
                new_list.append(new_tag)
    elif len(temp_middle_tag_list) == 0 and len(temp_top_tag_list) > 0:
        new_list = temp_top_tag_list
    elif len(temp_middle_tag_list) > 0 and len(temp_top_tag_list) == 0:
        new_list = temp_middle_tag_list

    new_searched_tags_list = search.search_tags(new_list)

    if len(new_searched_tags_list) > 0:
        winners_list = get_top_five(new_searched_tags_list)

    return winners_list


# small function that makes comparing tag lists for overlapping elements easier
def contains_tag(tag_list, tag):
    result = False
    for t in tag_list:
        if t.name == tag:
            result = True
            return result
    return result


def get_top_five(tag_list):
    placeholder_tag = tag_class.tag("placeholder")
    placeholder_tag.number_of_results = '0'
    results = [placeholder_tag]

    if len(tag_list) != 0:
        for tag in tag_list:
            if compare_against_list(tag, results):
                results = change_top_five_list(tag, results)

    results = remove_placeholders(results)
    return results


def compare_against_list(tag, number_list):
    tag_number = tag.number_of_results
    for number in number_list:
        if int(tag_number) > int(number.number_of_results):
            return True
    return False


def change_top_five_list(tag, tag_list):
    temp_list = tag_list
    tag_number = tag.number_of_results
    for number in tag_list:
        if int(tag_number) > int(number.number_of_results):
            temp_list.insert(temp_list.index(number), tag)
            break
    number_list = temp_list
    if len(number_list) > 5:
        number_list.pop(4)
    return number_list

def remove_placeholders(list):
    temp_list = list
    for tag in list:
        if tag.name == 'placeholder':
            temp_list.pop(temp_list.index(tag))

    return temp_list

