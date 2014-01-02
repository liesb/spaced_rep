from math import exp
import cPickle
import random
import numpy

def fib(n):
    if n==0:
        return 1
    if n==1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def fib2(n):
    if n < 2:
        return 1
    else:
        df = {}
        df[0] = 1
        df[1] = 1
        for x in range(2,n+1):
            df[x] = df[x-1] + df[x-2]
        return df[n]


def init_clean(filename):
    lines = None
    while lines is None:
        try:
            with open(filename) as f: 
                lines = f.readlines()
        except IOError:
            print "Something went bad with:",filename,"enter another_filename:"
            filename = raw_input()
    lines = map(lambda x:x.strip(), lines)
    lines = map(lambda x:x[2:], lines)
    lines = map(lambda x:x.split(" :: "), lines)
    return lines

def make_voc_dict(voc_list):
    d = {k:v for [k,v] in voc_list}
    return d

def make_box_dict(prog_filename, voc_dict):
    keys_voc = voc_dict.keys()
    if not prog_filename=='':
        # lines_prog1 =  init_clean(prog_filename)
        # dict_prog1 = {k:v for [k,v] in lines_prog1}
        with open(prog_filename) as f:
            dict_prog1 = cPickle.load(f)
    else:
        dict_prog1 = {}
    keys_prog1 = dict_prog1.keys()
    new_prog = {k:0 for k in keys_voc if not k in keys_prog1}
    return  dict(dict_prog1.items() + new_prog.items())

def inv_cdf_samp(prob_dict):
    r = random.random()
    found = False
    check_against = max(prob_dict.values())
    box = [i for (i,v) in prob_dict.items() if v == max(prob_dict.values())][0]
    prob_dict = {i:v for (i,v) in prob_dict.items() if not i == box}
    while found == False:
        if r < check_against:
            found = True
        else:
            #old_check_against = check_against
            check_against = check_against + max(prob_dict.values())
            box = [i for (i,v) in prob_dict.items() if v == max(prob_dict.values())][0]
            prob_dict = {i:v for (i,v) in prob_dict.items() if not i == box}
    return box
    # boelen, you're a total fuckwit
        
def inv_cdf_samp2(prob_dict):
    # print prob_dict
    r = random.random()
    acc = 0
    for x,p in prob_dict.items():
        acc += p
        if r <= acc:
            return x

def choose_english(box_dict):
    #unique_box_nums = set(box_dict.values())
    beta = 1
    dict_probs = {word:exp(-beta*box) for (word,box) in box_dict.items() }
    # zed is partition function
    zed = sum([prob for prob in dict_probs.values()])
    dict_probs = {word:prob/float(zed) for (word,prob) in dict_probs.items()}
    # choose box using inverse cdf sampling
    return inv_cdf_samp2(dict_probs)
    
    

def space_rep_main():
    # print a message
    print "hello user"
    
    # ask for input file
    print "where's the stuff"
    voc_filename = raw_input()
    
    # load input file and clean a bit
    clean1 = init_clean(voc_filename)
    
    # make dictionary-dictionary
    voc_dict = make_voc_dict(clean1)


    # match progress report to vocab input
    print("give me your previous results")
    prog_filename = raw_input()
    box_dict = make_box_dict(prog_filename, voc_dict)
        

    print "type QUIT to exit the game"

    answer = ""
    # start the reps
    # can I do an 'empty' while loop statement? yes
    while True: 
        # show word and get answer from user
        question = choose_english(box_dict) ## find a way to pick a word that needs to be translated
        print question, box_dict[question]
        user_answer = raw_input()
        if user_answer == "QUIT":
            break
        else: # do I need this else?? nope
            correct_answer = [a for (w,a) in voc_dict.items() if w==question][0]
            # check whether answer is correct
            if user_answer in correct_answer:
                print("well done")
                box_dict[question] += 1
                print box_dict[question]
            else:
                print "you're an idiot"
                print "the correct answer was:", correct_answer
                print "do you still think you had it right? [Y/N]"
                if raw_input()=="Y":
                    box_dict[question] += 1
                else:
                    box_dict[question] = max(0, box_dict[question]-1)
        
    print "do you want to save your progress?[Y/N]"
    if raw_input()=="Y":
        print "give a file name"
        with open(raw_input(),'w') as f: 
            cPickle.dump(box_dict, f)



print "loaded"

