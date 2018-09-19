import pandas as pd
#-------------------------------------------------------------------------
'''
    Problem 1: Sabermetrics
    In this problem, you will implement a version of the baseball player ranking system.
    You could test the correctness of your code by typing `nosetests test1.py` in the terminal.
'''

#--------------------------
def batting_average(H, AB):
    '''
        compute the batting average of a player.
        For more details, see here https://en.wikipedia.org/wiki/Batting_average.
        Input:
            H: the number of hits, an integer scalar.
            AB: the number of "at bats",  an integer scalar
        Output:
            BA: the batting average of a player, a float scalar.
    '''
    #########################################
    BA = H/AB

    #########################################
    return BA


#--------------------------
def on_base_percentage(H, AB, BB, HBP, SF):
    '''
        compute the on base percentage of a player.
        For more details, see here https://en.wikipedia.org/wiki/On-base_percentage.
        Input:
            H: the number of hits, an integer scalar.
            AB: the number of "at bats",  an integer scalar
            BB: the number of bases on balls (walks),  an integer scalar
            HBP: the number of hit by pitch,  an integer scalar
            SF: the number of sacrifice fly,  an integer scalar
        Output:
            OBP: the on base percentage of a player, a float scalar.
    '''
    #########################################
    ## INSERT YOUR CODE HERE

    OBP = (H + BB + HBP) / (AB + BB + HBP + SF)

    #########################################
    return OBP

#--------------------------
def slugging_percentage(H, _2B, _3B, HR, AB):
    '''
        compute the slugging percentage of a player.
        For more details, see here https://en.wikipedia.org/wiki/Slugging_percentage.
        Input:
            H: the number of hits, an integer scalar.
            _2B: the number of 2nd base,  an integer scalar (note: python variable names cannot start with a number, so _ is added)
            _3B: the number of 3rd base,  an integer scalar
            HR: the number of home runs,  an integer scalar
            AB: the number of at bats,  an integer scalar
        Output:
            SLG: the slugging percentage of a player, a float scalar.
    '''
    #########################################
    ## INSERT YOUR CODE HERE

    # compute the total bases
    _1B = H - (_2B + _3B + HR)
    TB = _1B + (2 * _2B) + (3 * _3B) + (4 * HR)

    # compute SLG
    SLG = TB/AB


    #########################################
    return SLG


#--------------------------
def runs_created(H, _2B, _3B, HR, BB, AB):
    '''
        compute the expected runs created by a team based upon Bill James' runs created formula.
        For more details, see here https://en.wikipedia.org/wiki/Runs_created.
        Input:
            H: the number of hits, an integer scalar.
            _2B: the number of 2nd base,  an integer scalar (note: python variable names cannot start with a number, so _ is added)
            _3B: the number of 3rd base,  an integer scalar
            HR: the number of home runs,  an integer scalar
            BB: the number of bases on balls (walks),  an integer scalar
            AB: the number of at bats,  an integer scalar
        Output:
            RC: the expected runs created/scored by a team, a float scalar.
    '''
    #########################################
    ## INSERT YOUR CODE HERE

    # compute the total bases
    _1B = H - (_2B + _3B + HR)
    TB = _1B + (2 * _2B) + (3 * _3B) + (4 * HR)

    # compute runs created
    RC = ((H + BB) * TB) / (AB + BB)

    #########################################
    return RC


#--------------------------
def win_ratio(RC, RA):
    '''
        compute the expected wining ratio of a team based upon Bill James' Pythagorean expectation.
        For more details, see here https://en.wikipedia.org/wiki/Pythagorean_expectation.
        Input:
            RC: the number of runs created/scored, an integer scalar.
            RA: the number of runs allowed,  an integer scalar
        Output:
            WR: the projected winning ratio of a team, a float scalar.
    '''
    #########################################
    ## INSERT YOUR CODE HERE
    A_by_C = (RA/RC) ** 2

    WR = 1 / (1 + A_by_C)

    #########################################
    return WR

#--------------------------
def eval_player(ID='hattesc01'):
    '''
        compute the BA, OBP and SLG of a player (ID) from the data in "Batting.csv" (year 2001).
        This dataset is downloaded from Lahman's baseball database (http://www.seanlahman.com/baseball-archive/statistics/)
        Input:
            ID: the player ID of a player, a string.  For example, "hattesc01" is for Scott Hatteberg. You can find the player names and IDs in People.csv.
        Output:
            BA: the batting average of a player, a float scalar.
            OBP: the on base percentage of a player, a float scalar.
            SLG: the slugging percentage of a player, a float scalar.
        Hint: you could use pandas package to load csv file and search player. Here is a tutorial: http://pandas.pydata.org/pandas-docs/stable/10min.html
    '''
    #########################################
    ## INSERT YOUR CODE HERE

    # read Batting.csv
    batting_data_ = pd.read_csv('Batting.csv')

    # search player by player ID

    player_batting_data_ = batting_data_[(batting_data_['playerID'] == ID)]

    player_info_ = player_batting_data_.to_dict(orient='records').pop()

    var_list = ['AB', 'H', '2B', '3B', 'HR', 'BB', 'HBP', 'SF']

    AB, H, _2B, _3B, HR, BB, HBP, SF = [player_info_.get(x) for x in var_list]

    BA = batting_average(H, AB)
    OBP = on_base_percentage(H, AB, BB, HBP, SF)
    SLG = slugging_percentage(H, _2B, _3B, HR, AB)
    #########################################
    return BA, OBP, SLG



#--------------------------
def salary(ID='hattesc01'):
    '''
        find the salary of a player in "Salaries.csv" (year 2002).
        Input:
            ID: the player ID of a player, a string.  For example, "hattesc01" is for Scott Hatteberg. You can find the player names and IDs in People.csv.
        Output:
            S: the salary of a player in year 2002, a float scalar.
        Hint: you could use pandas package to load csv file and search player. Here is a tutorial: http://pandas.pydata.org/pandas-docs/stable/10min.html
    '''
    #########################################
    ## INSERT YOUR CODE HERE

    # read Batting.csv
    salary_data_ = pd.read_csv('Salaries.csv')

    # search player by player ID

    player_salary_data_ = salary_data_[(salary_data_['playerID'] == ID)]

    player_salary = player_salary_data_.to_dict(orient='records').pop()

    S = player_salary.get('salary')

    #########################################
    return S
