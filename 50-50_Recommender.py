# u.data and u.item are not included due to license restrictions

import sys, os
import numpy as np
import pandas as pd
from numpy import linalg as LA
from random import randint
from scipy.sparse.csgraph import _validation

pathname = os.path.dirname(sys.argv[0])
directory = os.path.abspath(pathname)


# If you cannot find the given 'filename', then exit (1)
def exit_if_file_is_not_found(filename):
    if not os.path.exists(filename):
        print("Required data file is missing: {0} ".format(filename))
        sys.exit(1)

# Make it cross-platform (Windows + Linux)
if os.name == 'posix':
    descriptor = '/'
    def clear_screen():
        os.system('clear')
else:
    descriptor = '\\'
    def clear_screen():
        os.system('cls')

# Define the required data
movieLensFile = directory + descriptor + 'u.data' # not included due to license restrictions
movieLensItemFile = directory + descriptor + 'u.item' # not included due to license restrictions
FiveFactorFile= directory + descriptor + '5factortable.csv'
mostRatedFile = directory + descriptor + 'mostratedmovies.csv'

# Test requirements
def exit_if_data_are_not_found():
    exit_if_file_is_not_found(movieLensFile)
    exit_if_file_is_not_found(FiveFactorFile)
    exit_if_file_is_not_found(movieLensItemFile)
    exit_if_file_is_not_found(movieLensFile)


def get_user_movie_id():
    q = 'Put the movie ID of the movie you want to rate, or -1 to refresh list:'
    # Fix the '0{1,2,3,4,5,6,7,8,9}' bug
    while True:
        choice = raw_input(q + '\n')
        if choice == '01' or \
           choice == '02' or \
           choice == '03' or \
           choice == '04' or \
           choice == '05' or \
           choice == '06' or \
           choice == '07' or \
           choice == '08' or \
           choice == '09':
            print 'Wrong Movie ID. Please do not use 0 prefix! Try again ...'
        else:
            # We are not affected from the bug
            try:
                choice = int(choice) # Try to convert string to integer
            except ValueError:
                # If it fails, ask the user again
                print "Wrong Movie ID. This is not a number. Please try again ..."
                continue

            # If the conversion to integer has been succedded, check for its value
            if choice < -1 or choice > 1682 or choice == 0:
                # Not acceptable integer value
                print 'Wrong Movie ID. Please try again ...'
                continue
            # It's an acceptable integer value
            break # Break the loop
    return choice

def get_user_rating(TAINIA):
    movie = str(TAINIA)
    q = "How much would you rate '" + movie + "' ?"
    # Fix the '0{1,2,3,4,5,6,7,8,9}' bug
    while True:
        choice = raw_input(q + '\n')
        if choice == '01' or \
           choice == '02' or \
           choice == '03' or \
           choice == '04' or \
           choice == '05' or \
           choice == '06' or \
           choice == '07' or \
           choice == '08' or \
           choice == '09':
            print 'Wrong Rating. Please do not use 0 prefix. Try again ...'
        else:
            # We are not affected from the bug
            try:
                choice = int(choice) # Try to convert string to integer
            except ValueError:
                # If it fails, ask the user again
                print "Wrong Rating. This is not a number. Please try again ..."
                continue

            # If the conversion to integer has been succedded, check for its value
            if choice < 1 or choice > 5:
                # Not acceptable integer value
                print 'Wrong Rating. Please insert a value between [1-5]:'
                continue
            # It's an acceptable integer value
            break # Break the loop
    return choice

def newUser(ratingsmatrix):
    userID = 944
    print 'Welcome!\n'
    print 'We will present you a list of movies for rating. \nPlease enter the ID of the movie you want to rate and press Enter.\nThen put the corresponding rating (integer value in the range 1-5), with 1 being bad and 5 being excellent'
    print '\n\nPress Enter to continue . . .'
    useless = (raw_input())
    print '\n\n'
    myRatedDatabase = pd.read_csv(mostRatedFile, sep=",", header=None, names=['MOVIE_NAME', 'MOVIE_ID'], usecols=[0, 1])
    print '\n\nMOVIE LIST\n\n'
    ii = -9
    jj = 1
    cnt = 1
    movlist = pd.DataFrame(index=range(0, 21, 1), columns=['MOVIE_NAME', 'MOVIE_ID'])
    while cnt <= 20:
        clear_screen()
        print "MOVIE = " + str(cnt) + "/ 20"
        print "-----------------------------------------------------------------"
        icount = 0
        jcount = 0
        ii += 10
        jj += 10
        movlist.loc[0].loc['MOVIE_NAME'] = ' '
        movlist.loc[0].loc['MOVIE_ID'] = ' '

        # Refresh the movie list with [ 21 x 2 ] -- print begins from row[1] and ends at row [20]
        # -----------------------------------------------------------------------------------
        for i in range(ii, jj):

            # row[1,3,5,7,9] are **not** random
            icount += 1
            movlist.loc[icount].loc['MOVIE_NAME'] = myRatedDatabase.iloc[i, 0]
            jcount += 1
            movlist.loc[icount].loc['MOVIE_ID'] = myRatedDatabase.iloc[i, 1]
            jcount -= 1

            # row[2,4,6,8,10] are random
            icount += 1
            ranc = randint(jj, 1682)
            movlist.loc[icount].loc['MOVIE_NAME'] = myRatedDatabase.iloc[ranc, 0]
            jcount += 1
            movlist.loc[icount].loc['MOVIE_ID'] = myRatedDatabase.iloc[ranc, 1]
            jcount -= 1

        # Print to screen
        print '\t\t', movlist.to_string(index = False, header=False)



        # User input: Ask the user either to pick a Movie or refresh the list
        # -----------------------------------------------------------------------------------
        choice = get_user_movie_id()
        if choice == -1:
            # Redesign the movielist dataframe (+10 new movies)
            continue



        # Find the name of the movie based on the User input
        # -----------------------------------------------------------------------------------
        found = False
        for row in enumerate(movlist.values):
            MOVIE_INDEX = row[0]
            MOVIE_NAME = row[1][0]
            MOVIE_ID = row[1][1]
            if ( MOVIE_INDEX == 0 ):
                # The first row is always empty, please SKIP it
                continue
            if choice == int(MOVIE_ID):
                TAINIA = MOVIE_NAME
                found = True
                break
            elif MOVIE_INDEX >= 1 and MOVIE_INDEX <=20:
                # Search withing the 20 Listed movies atm 
                continue

        # User selected a number that's not currently displays on top 20 list (cheat)
        if not found:
            for row2 in enumerate(myRatedDatabase.values):
                MOVIE_INDEX = row2[0]
                MOVIE_NAME  = row2[1][0]
                MOVIE_ID    = row2[1][1]
                if ( MOVIE_INDEX == 0 ):
                    continue
                if choice == int(MOVIE_ID):
                    TAINIA = MOVIE_NAME
                    found = True
                    break
                else:
                    continue

        if not found:
            print "Internal error. I cannot find the movie with such ID."
	    exit(2)



        # User input: Ask the to rate the selected movie
        # -----------------------------------------------------------------------------------

        rate = get_user_rating(TAINIA)
        print 'You rated ', TAINIA, ' with ', rate



        # Record the user's opinion into the database (aka ratingmatrix)
        # -----------------------------------------------------------------------------------
        df = pd.DataFrame([[long(userID), long(choice), long(rate)]], columns=('userId', 'itemId', 'rating'))
        ratingsmatrix.loc[len(ratingsmatrix)] = df.loc[0]



        # Keep voting until 20 Movies
        # -----------------------------------------------------------------------------------
        cnt += 1

    print '\n\nPlease Wait . . .\n\n'
    return ratingsmatrix



def myBestMovies(me,N):

    topNMovies=pd.DataFrame.sort_values(
        myUserDatabase[myUserDatabase.userId==me],['rating'],ascending=[0])[:N]

    return list(topNMovies.title)



def correlation(u,v):
    umu = u.mean()
    vmu = v.mean()
    um = u - umu
    vm = v - vmu
    dist = 1.0 - np.dot(um, vm) / (LA.norm(um) * LA.norm(vm))
    return dist


def userPairSimilarity(user1, user2):
    user1 = np.array(user1) - np.nanmean(user1)
    user2 = np.array(user2) - np.nanmean(user2)


    commonMovies = [i for i in range(len(user1)) if user1[i] > 0 and user2[i] > 0]
    # Gives us movies for which both users have non NaN ratings
    if len(commonMovies) == 0:
        # if there are no common movies that both users have rated then it returns 0
        return 0
    else:
        user1 = np.array([user1[i] for i in commonMovies])
        user2 = np.array([user2[i] for i in commonMovies])
        return correlation(user1, user2)




def nearestNeighbourPredictions(user, K):

    similarities = pd.DataFrame(index=userVectorMatrix.index,
                                columns=['Similarity'])
    for i in userVectorMatrix.index:
        similarities.loc[i] = userPairSimilarity(userVectorMatrix.loc[user], userVectorMatrix.loc[i])
    similarities = pd.DataFrame.sort_values(similarities, ['Similarity'], ascending=[0])
    nearestNeighbours = similarities[:K]
    neighbourVectors = userVectorMatrix.loc[nearestNeighbours.index]
    predictRating = pd.DataFrame(index=userVectorMatrix.columns, columns=['Rating'])
    for i in userVectorMatrix.columns:
        prediction = np.nanmean(userVectorMatrix.loc[user])
        for j in neighbourVectors.index:
            # for each neighbour in the neighbour list
            if userVectorMatrix.loc[j, i] > 0:
                prediction += (userVectorMatrix.loc[j, i]
                               - np.nanmean(userVectorMatrix.loc[j])) * nearestNeighbours.loc[j, 'Similarity']
        predictRating.loc[i, 'Rating'] = prediction
    return predictRating



def finalNRecommendations(user, N, movieNum, genreNum):

    predictRating = nearestNeighbourPredictions(user, neighbours)
    #print 'KNN predictions ', predictRating
    moviesRated = list(userVectorMatrix.loc[user]
                       .loc[userVectorMatrix.loc[user] > 0].index)
    noGenreList = []
    for i in range(0, movieNum):
        cnt = 0
        for j in range(0, genreNum):
            if myItemDatabase.loc[i][j + 2] == 1:
                cnt = cnt + 1
        if cnt == 0:
            noGenreList.append(predictRating.index.get_loc(i+1))

    noGenreList = set(noGenreList) - set(moviesRated) #remove the movies that exist inside the moviesRated list
    predictRating = predictRating.drop(noGenreList)
    predictRating = predictRating.drop(moviesRated)
    finalRecommendations = pd.DataFrame.sort_values(predictRating, ['Rating'], ascending=[0])[:N]
    titles = (myItemDatabase.loc[myItemDatabase.itemId.isin(finalRecommendations.index)])
    return list(titles.title)


def RatingsNormalized(user):

    predictRating = nearestNeighbourPredictions(user, neighbours)
    #print ("5050 preds "), predictRating
    maximum = predictRating.iloc[:, 0].dropna().max()
    minimum = predictRating.iloc[:, 0].dropna().min()

    b = 0
    if minimum < 0:
        b = -minimum + 0
        maximum = maximum - minimum
        minimum = minimum - minimum

    for i in predictRating.index:
        predictRating.loc[i] = predictRating.loc[i] + b
        predictRating.loc[i] = predictRating.loc[i] * (5 / maximum)
        predictRating.loc[i] = 5 - predictRating.loc[i]
    return predictRating

def knnPersonality5050(genreSum, myItemDatabase, movieNum, genreNum, normalizedTable):
    normalizedTable2 = normalizedTable.copy(deep=1)
    for i in range(0, movieNum):
        cnt = 0
        sum = 0
        for j in range(0, genreNum):
            sum = sum + myItemDatabase.loc[i][j + 2] * genreSum.loc[j, 0]
            if myItemDatabase.loc[i][j + 2] == 1:
                cnt = cnt + 1
        if cnt != 0:
            sum = sum / cnt
            normalizedTable2.loc[i + 1] = (normalizedTable.loc[i + 1] + sum) / 2
        else:
            normalizedTable2.loc[i + 1] = 5

    return normalizedTable2

def knnPersonality8020(genreSum, myItemDatabase, movieNum, genreNum, normalizedTable):
    normalizedTable3 = normalizedTable.copy(deep=1)
    for i in range(0, movieNum):
        cnt = 0
        sum = 0
        for j in range(0, genreNum):
            sum = sum + myItemDatabase.loc[i][j + 2] * genreSum.loc[j, 0]
            if myItemDatabase.loc[i][j + 2] == 1:
                cnt = cnt + 1
        if cnt != 0:
            sum = sum / cnt
            normalizedTable3.loc[i + 1] = (normalizedTable.loc[i + 1] * 0.2) + (sum * 0.8)
        else:
            normalizedTable3.loc[i + 1] = 5

    return normalizedTable3


def finalNRecommendationsPersonality(tab, user, N):
    moviesRated = list(userVectorMatrix.loc[user]
                       .loc[userVectorMatrix.loc[user] > 0].index)


    tabRated = tab.drop(moviesRated)

    finalRecommendations = pd.DataFrame.sort_values(tabRated,
                                                    ['Rating'], ascending=[1])[:N]

    titles = (myItemDatabase.loc[myItemDatabase.itemId.isin(finalRecommendations.index)])
    return list(titles.title)



############################################################################################
# Basic tests #  If one of the following tests fails, then exit the programm immediatelly  #
############################################################################################

exit_if_data_are_not_found()



############
### Main ###
############

myUserDatabase = pd.read_csv(movieLensFile, sep="\t", header=None, names=['userId', 'itemId', 'rating'], usecols=[0, 1, 2])
myUserDatabase = newUser(myUserDatabase)
myItemDatabase=pd.read_csv(movieLensItemFile,sep="|", header=None, names=['itemId','title', 'Action',' Adventure', 'Animation', 'Cartoon', 'Comedy','Drama', 'Film-Noir', 'Horror',  'Romance', 'Sci-Fi', 'War' ], usecols=[0,1,6,7,8,9,10,13,15,16,19,20,22])
myUserDatabase=pd.merge(myUserDatabase,myItemDatabase,left_on='itemId',right_on="itemId")
userVectorMatrix=pd.pivot_table(myUserDatabase, values='rating', index=['userId'], columns=['itemId'])
userID = 944;
neighbours=50

a = 0
c = 0
o = 0
e = 0
n = 0
while(True):
    print '\nWELCOME TO THE BIG FIVE PERSONALITY TEST\n\n'
    s='This is a personality test to help us understand  how your personality is structured and find the best movie recommendations for you.'
    l='Please answer all the following questions with a number in the range of 1-5, where 1=disagree, 2=slightly disagree, 3=neutral, 4=slightly agree and 5=agree.'
    print s
    print l

    print '\n\nAnswer the following questions, with the prefix "I think that.."\n\n\n'
    q = 'I am the life of the party.'

    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    e = e+num


    q = 'I feel little concern for others.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    a = a-num

    q = 'I am always prepared.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    c = c+num

    q = 'I get stressed out easily.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    n = n-num

    q = 'I have a rich vocabulary.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    o = o+num

    q = 'I do not talk a lot.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    e = e-num

    q = 'I am interested in people.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    a = a+num

    q = 'I leave my belongings around.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    c = c-num

    q = 'I am relaxed most of the time.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    n = n+num

    q = 'I have difficulty understanding abstract ideas.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    o = o-num

    q = 'I feel comfortable around people.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    e = e+num

    q = 'I insult people.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    a = a-num

    q = 'I pay attention to details.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    c = c+num


    q = 'I worry about things.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    n = n-num

    q = 'I have a vivid imagination.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    o = o+num

    q = 'I keep in the background.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    e = e-num


    q = 'I sympathize with others feelings.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    a = a+num


    q = 'I make a mess of things.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    c = c-num

    q = 'I seldom feel blue.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    n = n+num

    q = 'I am not interested in abstract ideas.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    o = o-num


    q = 'I start conversations.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    e = e+num

    q = 'I am not interested in other peoples problems.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    a = a-num


    q = 'I get chores done right away.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    c = c+num

    q = 'I am easily disturbed.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    n = n-num


    q = 'I have excellent ideas.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    o = o+num

    q = 'I have little to say.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    e = e-num

    q = 'I have a soft heart.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    a = a+num


    q = 'I often forget to put things back in their proper place.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    c = c-num

    q = 'I get upset easily.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    n = n-num


    q = 'I do not have a good imagination.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    o = o-num

    q = 'I talk to a lot of different people at parties.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    e = e+num

    q = 'I am not really interested in others.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    a = a-num


    q = 'I like order.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    c = c+num


    q = 'I change my mood a lot.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    n = n-num


    q = 'I am quick to understand things.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    o = o+num

    q = 'I do not like to draw attention to myself.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    e = e-num

    q = 'I take time out for others.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    a = a+num


    q = 'I shirk my duties.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    c = c-num


    q = 'I have frequent mood swings.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    n = n-num


    q = 'I use difficult words.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    o = o+num

    q = 'I do not mind being the center of attention.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    e = e+num


    q = 'I feel others emotions.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    a = a+num


    q = 'I follow a schedule.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    c = c+num


    q = 'I get irritated easily.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    n = n-num


    q = 'I spend time reflecting on things.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    o = o+num

    q = 'I am quiet around strangers.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    e = e-num

    q = 'I make people feel at ease.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    a = a+num


    q = 'I am exacting in my work.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    c = c+num

    q = 'I often feel blue.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    n = n-num


    q = 'I am full of ideas.'
    while (True):
        try:
            num = int(raw_input(q + '\n'))
        except ValueError:
            print 'Wrong input, please try again'
            continue
        if (num<1 or num>5):
            print 'Value must be in the range 1-5: Try again.'
            continue
        break
    o = o+num



    agreeableness_final = (24 + a)/10.0
    openness_final = (18 + o)/10.0
    conscientiousness_final =(24 + c)/10.0
    extraversion_final = (30 + e)/10.0
    neuroticism_final = (48 + n)/10.0
    print '\n\n'

    print "Extraversion=", extraversion_final

    print "Agreeableness=", agreeableness_final

    print "conscientiousness=", conscientiousness_final

    print "neuroticism=", neuroticism_final

    print "openness=", openness_final
    print '\n'


    print ("THANK YOU FOR FILLING THE BIG FIVE QUESTIONAIRE. ")
    break
#execfile('Analyzer.py')
print 'Please Wait . . .'







myFiveFactorDatabase=pd.read_csv(FiveFactorFile,sep=",",header=None,
                 names=['MOVIE GENRE','OPE','CON','EXT','AGR','NEU'], usecols=[0,1,2,3,4,5])


myFiveFactorDatabase.loc[:, 'OPE']-=openness_final
myFiveFactorDatabase.loc[:, 'OPE'] = myFiveFactorDatabase.loc[:, 'OPE'].abs()
myFiveFactorDatabase.loc[:, 'CON']-=conscientiousness_final
myFiveFactorDatabase.loc[:, 'CON'] = myFiveFactorDatabase.loc[:, 'CON'].abs()
myFiveFactorDatabase.loc[:, 'EXT']-=extraversion_final
myFiveFactorDatabase.loc[:, 'EXT'] = myFiveFactorDatabase.loc[:, 'EXT'].abs()
myFiveFactorDatabase.loc[:, 'AGR']-=agreeableness_final
myFiveFactorDatabase.loc[:, 'AGR'] = myFiveFactorDatabase.loc[:, 'AGR'].abs()
myFiveFactorDatabase.loc[:, 'NEU']-=neuroticism_final
myFiveFactorDatabase.loc[:, 'NEU'] = myFiveFactorDatabase.loc[:, 'NEU'].abs()

numbah = myFiveFactorDatabase.sum(axis=1, numeric_only=True)
numbahNames = myFiveFactorDatabase.loc[:, 'MOVIE GENRE']

genreSum=pd.concat([numbahNames, numbah], axis=1)

normalizedTable=RatingsNormalized(userID)






tab = knnPersonality5050(genreSum, myItemDatabase, 1682, 11, normalizedTable)




tab2 = knnPersonality8020(genreSum, myItemDatabase, 1682, 11, normalizedTable)





print nearestNeighbourPredictions(userID, neighbours)



#print 'Your highest rated movies are: \n', myBestMovies(userID, 10)
l5050 = finalNRecommendationsPersonality(tab, userID, 10)
print '50/50 recomendations:'
for i in l5050:
    print(i)
print '\n\n'
lknn = finalNRecommendations(userID, 10, 1682, 11) #knn
print 'KNN recomendations:'
for i in lknn:
    print(i)
print '\n\n'
l8020 = finalNRecommendationsPersonality(tab2, userID, 10) #80/20
print '80/20 recomendations:'
for i in l8020:
    print(i)
print '\n\nPress Enter to Exit . . .'
useless = (raw_input())
