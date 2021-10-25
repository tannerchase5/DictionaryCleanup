import sys, time

# Function to remove data from other data
def filter(target, filters, op="in"):
    ty = type(target)
    target = list(target)
    filters = list(filters)
    for word in target:
        for regix in filters:
            if (op == "in") and (regix.lower() in word.lower()): 
                target.remove(word)
                break
            elif (op == "eq") and (regix.lower() == word.lower()):
                target.remove(word)
                break
    if(isinstance("",ty)):
        return ("".join(target))
    elif(isinstance([], ty)):
        return target
    else:
        raise TypeError("Data type not supported")

#Remove all excess spaces, guarantee only one of each vaulue, and remove words with unwanted characters
def format_dictionary(input, bad_chars, case=False):
    temp = set()
    index = 0
    for word in input:
        fixed = " ".join(str(word).split())
        if case == True:
            fixed = fixed.lower()
        input[index] = fixed
        index += 1
    temp.update(input)
    temp = filter(list(temp), bad_chars)
    temp.sort()
    return temp

# Convert a file name to list
def file_to_list(filename, extension="txt"):
    with open((filename+"."+extension), "r") as f:
        data = (f.read()).split("\n")
    return data
    
no_spaces = " "
no_compound = " _-"
no_nonletter = no_compound + "%^&*()=:;?/,.`\'<>"
no_symbols = no_nonletter + "!@#$+"
no_numbers = "0123456789"

args = sys.argv[1:]
word_style = no_symbols
lowercase = False

if ("word_style=no_" in " ".join(args)):
    for entry in args:
        if "word_style=no_" in entry:
            try:
                word_style = eval(entry.split("word_style=")[1])
                print(word_style)
                break
            except:
                break

if ("-l" in args):
    lowercase = True

dictionary = tuple((raw_input("What is the name of the text file to format?: ")).split(".") + ["txt"])

# Remove any words with certain unwanted words in them
if ("-b" in args):
    bad_words_dictionary = tuple((raw_input("What is the name unwanted words dictionary text file?: ")).split(".") + ["txt"])
    t = time.time()

    words = format_dictionary(file_to_list(dictionary[0], dictionary[1]), word_style, lowercase)
    bad_words_list = file_to_list(bad_words_dictionary[0], bad_words_dictionary[1])

    if("any_instance_equals_termination" in bad_words_list[0]):
        bad_words = bad_words_list.pop(0).split()[1].strip("[]").split(",")
        for word in bad_words:
            while word in " ".join(words):
                words = filter(words, bad_words)

    bad_words_list = format_dictionary(bad_words_list, word_style, True)
    words = filter(words, bad_words_list, "eq")
else:
    t = time.time()
    words = format_dictionary(file_to_list(dictionary[0], dictionary[1]), word_style, lowercase)

# Write new list to output file
with open(("new_"+ dictionary[0] +"."+ dictionary[1]), "w") as n:
    n.write("\n".join(words))

print("It took %s seconds to complete.") % (time.time()-t)
