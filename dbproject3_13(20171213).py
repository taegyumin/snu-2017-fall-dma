from orangecontrib.associate.fpgrowth import * #Error occurs when above statement is included(located) in the block of def associtaiton, then notice 'SyntaxError: import * only allowed at module level'

def dropDB(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
    #BEGIN------DROP DATABASE db2017_13-------
    conn = pymysql.connect(host=host, user=user, password=password) #db='db2017_13', charset='utf8'
    try:
        with conn.cursor() as cursor :
            sql = 'DROP DATABASE db2017_13'
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
    #END--------DROP DATABASE db2017_13-------

def createDBandTables(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
    #BEGIN------CREATE DATABASE db2017_13-------
    conn = pymysql.connect(host=host, user=user, password=password) #db='db2017_13', charset='utf8'
    try:
        with conn.cursor() as cursor :
            sql = 'CREATE DATABASE IF NOT EXISTS db2017_13 CHARACTER SET=utf8' #'SET=utf-8' occurs error.
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
    #END--------CREATE DATABASE db2017_13-------

    #BEGIN------CREATE TABLES db2017_13-------
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')

    try:
        with conn.cursor() as cursor :

            #---------CREATE TABLE userInfo------------
            #attrbiutes that allow null value : Age, WebsiteUrl, Location, AboutMe
            sql = '''CREATE TABLE IF NOT EXISTS userInfo (
    	       Id			INT(11)			NOT NULL,
    	       Reputation	INT(11)		    NOT NULL,
    	       DisplayName	varchar(255)    NOT NULL,
    	       Age			INT(11),
    	       CreationDate	DATETIME	    NOT NULL,
    	       LastAccessDate	DATETIME	NOT NULL,
    	       WebsiteUrl	varchar(255),
    	       Location		varchar(255),
    	       AboutMe		LONGTEXT,

               Primary key (Id));'''
            cursor.execute(sql)


            #---------CREATE TABLE posts---------------
            #attrbiutes that allow null value : not exists
            #altered table posts modify column Body LONGTEXT;
            sql = '''CREATE TABLE IF NOT EXISTS posts (
                Id		    INT(11)		NOT NULL,
	            OwnerUserId	INT(11)		NOT NULL,
	            Body	    LONGTEXT    NOT NULL,
	            CreationDate	DATETIME	NOT NULL,
                LastActivityDate    DATETIME	NOT NULL,

                Primary key (Id),
                Foreign key (OwnerUserId) references userInfo(Id));'''
            cursor.execute(sql)


            #---------CREATE TABLE tags----------------
            #attrbiutes that allow null value : WikiPostId, ExcerptPostId
            sql = '''CREATE TABLE IF NOT EXISTS tags (
                Id		        INT(11) 		NOT NULL,
	            TagName	        varchar(255)	NOT NULL,
	            ExcerptPostId	INT(11), /*백과사전과 백과사전요약문 사이에 Functional Dependency가 없다고 가정*/
	            WikiPostId     	INT(11),

	            Primary key (TagName),
	            Foreign key (WikiPostId) references posts(Id),
	            Foreign key (ExcerptPostId) references posts(Id));'''
            cursor.execute(sql)


            #---------CREATE TABLE questionPosts-------
            #attrbiutes that allow null value : not exists
            sql = '''CREATE TABLE IF NOT EXISTS questionPosts (
                Id	        INT(11) 	    NOT NULL,
                PostId		INT(11)		    NOT NULL,
	           	ViewCount	INT(11)		    NOT NULL,
	           	Title		varchar(255)	NOT NULL,

		        Primary key (Id),
		        Foreign key (PostId) references posts(Id));'''
            cursor.execute(sql)


            #---------CREATE TABLE questionQuoteTags---
            #attrbiutes that allow null value : not exists
            sql = '''CREATE TABLE IF NOT EXISTS questionQuoteTags (
                QuestionId	INT(11) NOT NULL,
	           	TagsName	varchar(255) NOT NULL,

		        Primary key (QuestionId,TagsName),
		        Foreign key (QuestionId) references questionPosts(Id),
		        Foreign key (TagsName) references tags(TagName));'''
            cursor.execute(sql)


            #---------CREATE TABLE answerPosts---------
            #attrbiutes that allow null value : not exists
            sql = '''CREATE TABLE IF NOT EXISTS answerPosts (
                Id	        INT(11)		NOT NULL,
                PostId		INT(11)		NOT NULL,
                Accepted    INT(11)		NOT NULL,
	            ParentId	INT(11)		NOT NULL,

	            Primary key (Id),
	            Foreign key (PostId) references posts(Id),
	            Foreign key (ParentId) references questionPosts(Id));'''
            cursor.execute(sql)


            #---------CREATE TABLE postLinks-----------
            #attrbiutes that allow null value : not exists
            sql = '''CREATE TABLE IF NOT EXISTS postLinks (
	           Id		        INT(11) 	NOT NULL,
	           PostId	        INT(11)		NOT NULL,
	           RelatedPostId	INT(11)		NOT NULL,
	           CreationDate	    DATETIME	NOT NULL,
	           LinkTypeId	    INT(11)	    NOT NULL,

               Primary key (Id),
	           Foreign key (PostId) references posts(Id),
	           Foreign key (RelatedPostId) references posts(Id));'''
            cursor.execute(sql)


            #---------CREATE TABLE badges--------------
            #attrbiutes that allow null value : not exists
            sql = '''CREATE TABLE IF NOT EXISTS badges (
                Id	         INT(11) 		NOT NULL,
                UserInfoId	 INT(11)		NOT NULL,
                Name	     varchar(255)	NOT NULL,
                Date	     DATETIME	    NOT NULL,

                Primary key (Id),
                Foreign key (UserInfoId) references userInfo(Id));'''
            cursor.execute(sql)


            #---------CREATE TABLE badgesName----------
            #attrbiutes that allow null value : not exists
            sql = '''CREATE TABLE IF NOT EXISTS badgesName (
                Name	     varchar(255)	NOT NULL,

                Primary key (Name));'''
            cursor.execute(sql)


            #---------CREATE TABLE comments------------
            #attrbiutes that allow null value : not exists
            sql = '''CREATE TABLE IF NOT EXISTS comments (
                Id		        INT(11)		NOT NULL,
	            PostId		    INT(11)		NOT NULL,
	            Score		    INT(11)		NOT NULL,
	            CreationDate	DATETIME	NOT NULL,
	            UserInfoId	    INT(11)		NOT NULL,

	            Primary key (Id),
	            Foreign key (PostId) references posts(Id),
	            Foreign key (UserInfoId) references userInfo(Id));'''
            cursor.execute(sql)


            #---------CREATE TABLE postHistory---------
            #attrbiutes that allow null value : Text, Comment
            sql = '''CREATE TABLE IF NOT EXISTS postHistory (
                Id		            INT(11)		NOT NULL,
	            PostHistoryTypeId	INT(11) 	NOT NULL,
	            CreationDate	    DATETIME	NOT NULL,
	            Text	    LONGTEXT,
		        Comment   	LONGTEXT,
	           	UserInfoId	INT(11)		NOT NULL,
	            PostId      INT(11)	    NOT NULL,

	            Primary key (Id),
	            Foreign key (UserInfoId) references userInfo(Id),
	            Foreign key (PostId) references posts(Id));'''
            cursor.execute(sql)


            #---------CREATE TABLE votes---------------
            #attrbiutes that allow null value : UserInfoId, BountyAmount
            sql = '''CREATE TABLE IF NOT EXISTS votes (
                Id		        INT(11) 	NOT NULL,
	            PostId	        INT(11)		NOT NULL,
	            VoteTypeId	    INT(11)	    NOT NULL,
	            CreationDate	DATE	NOT NULL,
	            UserInfoId	    INT(11),
	            BountyAmount	INT(11),

	            Primary key (Id),
	            Foreign key (PostId) references posts(Id),
	            Foreign key (UserInfoId) references userInfo(Id));'''
            cursor.execute(sql)

        conn.commit()
    finally:
        conn.close()
    #END--------CREATE TABLES db2017_13-------

def insertCSVfiles(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')
    from datetime import datetime
    import csv
    #BEGIN------csv file to python-------

    #------insert userInfo.csv------------
    #------into userInfo table------------
    #attributeName and index in userInfo.csv : Id 0, Reputation 1, DisplayName 2, Age 3, CreationDate 4, LastAccessDate 5, WebsiteUrl 6, Location 7, AboutMe 8
    userInfo = [] #데이터들을 담을 공간을 list 자료형으로 생성.
    f = open('dataset/userInfo.csv','r',encoding='utf-8',errors='replace') #csv 파일과 python 프로그램을 연결한다.
    rdr = csv.reader(f) #해당 csv 파일의 데이터를 받아들인다.
    next(rdr,None) #ColumnName에 해당하는 row를 제외시킨다.
    for line in rdr:
        for i in [0,1,3]: #String to Integer that is not null
            if line[i] != '':
                line[i] = int(line[i])
            else : #empty data to null
                line[i] = None
        for i in [2,4,5,6,7,8]: #empty data to null
            if line[i] =='':
                line[i] = None
        for i in [4,5]: #String to datetime that is not null
            dt = datetime.strptime(line[i], "%Y-%m-%d %H:%M")
            line[i]=dt.isoformat()
        userInfo.append(line)
    f.close()


    #------insert posts.csv---------------
    #------into posts table---------------
    #attributeName and index in posts.csv : Id 0, CreationDate 1, Body 2, OwnerUserId 3, LasActivityDate 4
    #LasActivityDate는 derived attribute이므로 저장하지 않는다.
    posts = []
    f = open('dataset/posts.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    for line in rdr:
        for i in [0,3]: #String to Integer that is not null
            if line[i] !='':
                line[i] = int(line[i])
            else : #empty data to null
                line[i] = None
        for i in [1,2,4]: #empty data to null
            if line[i] =='':
                line[i] = None
        for i in [1,4]: #String to datetime that is not null
            dt = datetime.strptime(line[i], "%Y-%m-%d %H:%M")
            line[i]=dt.isoformat()
        tempLine=[line[0],line[3],line[2],line[1],line[4]] #csv파일과 database 해당 table의 attribute degree 또는 순서가 다르면 이와 같이 tempLine을 만들어 table의 제약조건에 맞게끔 데이터들을 재조합했다.
        posts.append(tempLine)
    f.close()


    #------insert tags.csv----------------
    #------into tags table----------------
    #attributeName and index in csv file : Id 0, TagName 1, ExcerptPostId 2, WikiPostId 3
    tags = []
    f = open('dataset/tags.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    for line in rdr:
        for i in [0,2,3]: #String to Integer that is not null
            if line[i] !='':
                line[i] = int(line[i])
            else : #empty data to null
                line[i] = None
        for i in [1]: #empty data to null
            if line[i] =='':
                line[i] = None
        tags.append(line)
    f.close()


    #------insert questionPosts.csv-------
    #------into questionPosts table-------
    #attributeName and index in questionPosts.csv : Id 0, PostId 1, AcceptedAnswerId 2, ViewCount 3, Title 4, Tags 5
    questionPosts = []
    f = open('dataset/questionPosts.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    for line in rdr:
        for i in [0,1,3]: #String to Integer that is not null
            if line[i] !='':
                line[i] = int(line[i])
            else : #empty data to null
                line[i] = None
        for i in [4]: #empty data to null
            if line[i] =='':
                line[i] = None
        tempLine=[line[0],line[1],line[3],line[4]]
        questionPosts.append(tempLine)
    f.close()


    #------insert questionPosts.csv, tags.csv---
    #------into questionQuoteTags table---
    #주어진 csv파일의 경우 tags 내에 동음이의어가 없다. 추가되는 data 중에도 기존의 data 중 태그 이름이 동일한 경우는 없다는 가정 하에 위와 같이 코드를 작성하였다.
    questionQuoteTags = []
    # tempTags = dict()
    # f2 = open('dataset/tags.csv','r',encoding='utf-8',errors='replace')
    # rdr2 = csv.reader(f2)
    # next(rdr2,None)
    # for line2 in rdr2:
    #     for i in [0]: #String to Integer that is not null
    #         if line2[i] !='':
    #             line2[i] = int(line2[0])
    #         else :  #empty data to null
    #             line2[i] = None
    #     for i in [1]:  #empty data to null
    #         if line2[i] =='':
    #             line2[i] = None
    #     tempTags[line2[1]] = line2[0]

    f = open('dataset/questionPosts.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    for line in rdr:
        for i in [0]:
            if line[i] !='': #String to Integer that is not null
                line[i] = int(line[i])
            else : #empty data to null
                line[i] = None
        for i in [5]:
            if line[i] =='':  #empty data to null
                line[i] = None
        splitTags = line[5]
        splitTags = splitTags.replace('<',' ')
        splitTags = splitTags.replace('>',' ')
        splitTags = splitTags.split()
        for j in splitTags:
            tempLine=[line[0],j]
            questionQuoteTags.append(tempLine)
            # f2.close()
    f.close()


    #------insert answerPosts.csv---------
    #------into answerPosts table---------
    #attributeName and index in answerPosts.csv : Id 0, PostId 1, Accepted 2, ParentId 3
    answerPosts = []
    f = open('dataset/answerPosts.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    for line in rdr:
        for i in [0,1,2,3]: #String to Integer that is not null
            if line[i] !='':
                line[i] = int(line[i])
            else :
                line[i] = None
        answerPosts.append(line)
    f.close()


    #------insert postLinks.csv-----------
    #------into postLinks table-----------
    #attributeName and index in postLinks.csv : Id 0, CreationDate 1, PostId 2, RelatedPostId 3, LinkTypeId 4
    postLinks = []
    f = open('dataset/postLinks.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    for line in rdr:
        for i in [0,2,3,4]: #String to Integer that is not null
            if line[i] !='':
                line[i] = int(line[i])
            else : #empty data to null
                line[i] = None
        for i in [1]: #empty data to null
            if line[i] =='':
                line[i] = None
        dt = datetime.strptime(line[1], "%Y-%m-%d %H:%M")  #String to datetime that is not null
        line[1]=dt.isoformat()
        tempLine=[line[0],line[2],line[3],line[1],line[4]]
        postLinks.append(tempLine)
    f.close()


    #------insert badges.csv--------------
    #------into badges table--------------
    #attributeName and index in badges.csv : Id 0, UserInfoId 1, Name 2, Date 3
    badges = []
    f = open('dataset/badges.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    for line in rdr:
        for i in [0,1]: #String to Integer that is not null
            if line[i] !='':
                line[i] = int(line[i])
            else : #empty data to null
                line[i] = None
        for i in [2,3]: #empty data to null
            if line[i] =='':
                line[i] = None
        try:  #String to datetime that is not null
            dt = datetime.strptime(line[3], "%Y-%m-%d %H:%M")
        except:
            dt = datetime.strptime(line[3], "%Y-%m-%dT%H:%M")
        finally:
            line[3]=dt.isoformat()
        badges.append(line)
    f.close()


    #------insert badges.csv--------------
    #------into badgesName table----------
    #attributeName and index in badges.csv : Id 0, UserInfoId 1, Name 2, Date 3
    badgesName = []  #set() 으로 담으려다가 코드의 가독성 및 일관성을 위해 list형태로 담기로 했다.
    f = open('dataset/badges.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    for line in rdr:
        for i in [2]: #empty data to null
            if line[i] =='':
                line[i] = None
        if not(line[2] in badgesName): #duplicate data is not allowed.
            badgesName.append(line[2])
    f.close()


    #------insert comments.csv------------
    #------into comments table------------
    #attributeName and index in csv file : Id 0, PostId 1, Score 2, CreationDate 3, UserInfoId 4
    comments = []
    f = open('dataset/comments.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    for line in rdr:
        for i in [0,1,2,4]: #String to Integer that is not null
            if line[i] !='':
                line[i] = int(line[i])
            else : #empty data to null
                line[i] = None
        for i in [3]: #empty data to null
            if line[i] == '':
                line[i] = None
        dt = datetime.strptime(line[3], "%Y-%m-%d %H:%M")  #String to datetime that is not null
        line[3]=dt.isoformat()
        comments.append(line)
    f.close()


    #------insert postHistory.csv---------
    #------into postHistory table---------
    #attributeName and index in csv file : Id 0, PostHistoryTypeId 1, PostId 2, CreationDate 3, UserInfoId 4, Text 5, Comment 6
    postHistory = []
    f = open('dataset/postHistory.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    for line in rdr:
        for i in [0,1,2,4]: #String to Integer that is not null
            if line[i] != '':
                line[i] = int(line[i])
            else : #empty data to null
                line[i] = None
        for i in [3,5,6]: #empty data to null
            if line[i] == '':
                line[i] = None
        dt = datetime.strptime(line[3], "%Y-%m-%d %H:%M")  #String to datetime that is not null
        line[3]=dt.isoformat()
        tempLine=[line[0],line[1],line[3],line[5],line[6],line[4],line[2]]
        postHistory.append(tempLine)
    f.close()


    #------insert votes.csv---------------
    #------into votes table---------------
    #attributeName and index in csv file : Id 0, PostId 1, VoteTypeId 2, CreationDate 3, UserInfoId 4, BountyAmount 5
    votes = []
    f = open('dataset/votes.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    for line in rdr:
        for i in [0,1,2,4,5]: #String to Integer that is not null
            if line[i] != '':
                line[i] = int(line[i])
            else : #empty data to null
                line[i] = None
        for i in [3]: #empty data to null
            if line[i] == '':
                line[i] = None
        dt = datetime.strptime(line[3], "%Y-%m-%d")  #String to datetime that is not null
        line[3]=dt.isoformat()
        votes.append(line)
    f.close()
    #END--------csv file to python-------

    #BEGIN-----python to database--------
    try:
        with conn.cursor() as cursor:
            cursor.executemany("insert into userInfo(Id,Reputation,DisplayName,Age,CreationDate,LastAccessDate,WebsiteUrl,Location,AboutMe) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",userInfo)
            conn.commit()

            cursor.executemany("insert into posts(Id,OwnerUserId,Body,CreationDate,LastActivityDate) values (%s,%s,%s,%s,%s)",posts)
            conn.commit()

            cursor.executemany("insert into tags(Id,TagName,ExcerptPostId,WikiPostId) values (%s,%s,%s,%s)",tags)
            conn.commit()

            cursor.executemany("insert into questionPosts(Id,PostId,ViewCount,Title) values (%s,%s,%s,%s)",questionPosts)
            conn.commit()

            cursor.executemany("insert into questionQuoteTags(QuestionId,TagsName) values (%s,%s)",questionQuoteTags)
            conn.commit()

            cursor.executemany("insert into answerPosts(Id,PostId,Accepted,ParentId) values (%s,%s,%s,%s)",answerPosts)
            conn.commit()

            cursor.executemany("insert into postLinks(Id,PostId,RelatedPostId,CreationDate,LinkTypeId) values (%s,%s,%s,%s,%s)",postLinks)
            conn.commit()

            cursor.executemany("insert into badges(Id,UserInfoId,Name,Date) values (%s,%s,%s,%s)",badges)
            conn.commit()

            cursor.executemany("insert into badgesName(Name) values (%s)",badgesName)
            conn.commit()

            cursor.executemany("insert into comments(Id,PostId,Score,CreationDate,UserInfoId) values (%s,%s,%s,%s,%s)",comments)
            conn.commit()

            cursor.executemany("insert into postHistory(Id,PostHistoryTypeId,CreationDate,Text,Comment,UserInfoId,PostId) values (%s,%s,%s,%s,%s,%s,%s)",postHistory)
            conn.commit()

            cursor.executemany("insert into votes(Id,PostId,VoteTypeId,CreationDate,UserInfoId,BountyAmount) values (%s,%s,%s,%s,%s,%s)",votes)
            conn.commit()
    finally:
        conn.close()
    #END-------python to database--------

# dropDB(host, user, password)
createDBandTables(host, user, password)
insertCSVfiles(host, user, password)
# If you run this method for the first time, run the code as it is.
# But from the second run, please run the dropDB(host, user, password) method, as well.

def association(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
    import csv

    #-------------(R1)BEGIN-----------
    #------insert tagname.csv---------
    #------into TagMatrix VIEW--------
    f = open('dataset/tagname.csv','r',encoding='utf-8',errors='replace')
    rdr = csv.reader(f)
    next(rdr,None)
    iterateCode = ''
    for line in rdr: #인용수 상위 100위까지의 태그들을 대상으로 TagMatrix VIEW의 Column을 생성한다.
        if int(line[0])>100:
            break;
        iterateCode = iterateCode+"max(IF(questionQuoteTags.TagsName = '{0}',1,0)) as `Tags에 '{1}'이 포함되어 있음(0혹은 1)`,".format(line[1],line[1])
    f.close()
    iterateCode = iterateCode[:-1] #String 맨 끝에 위치한 ','(comma)를 제거한다. 이 ','는 index len(iterateCode)-1에 위치한다.

    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')
    try:
        with conn.cursor() as cursor :
            sql ='''CREATE VIEW TagMatrix AS
                    SELECT questionPosts.Id,'''+iterateCode+'''
                    FROM questionPosts, questionQuoteTags
                    WHERE questionPosts.Id = questionQuoteTags.QuestionId
                    GROUP BY questionPosts.Id;'''
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
    #-------------(R1)END-------------

    #-------------(R2)BEGIN-----------
    import numpy as np
    import pandas as pd
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')
    XDataframe = pd.read_sql('SELECT * FROM TagMatrix',conn)
    Xmatrix = XDataframe.as_matrix()
    XmatrixWithoutId = np.delete(Xmatrix,0,1)
    Xboolean = (XmatrixWithoutId>0)
    itemsets = dict(frequent_itemsets(Xboolean,.01))
    print('frequent_itemsets')
    for i in itemsets:
        print(i)
    rules = association_rules(itemsets,.05,None)
    rule_stat = list(rules_stats(rules,itemsets,len(Xmatrix)))
    print('\nrule_stat')
    for i in rule_stat:
        print(i)
    # -------------(R2)END-------------

def decisiontree1(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)

    #-------------(R4)BEGIN-----------
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')
    try:
        with conn.cursor() as cursor :
            sql ='''CREATE VIEW ReputStatMatrix AS
                    (SELECT derived1.Id, derived1.Reputation, IFNULL(derived2.NumOfPosts,0) AS NumOfPosts, IFNULL(derived3.NumOfComments,0) AS NumOfComments, IFNULL(derived4.NumOfBadges,0) AS NumOfBadges

                    FROM
                    (SELECT Id, Reputation
                    FROM userInfo
                    WHERE Reputation>110) derived1

                    /*ColumnName: NumOfPosts; Each User's Number of Posts*/
                    LEFT JOIN (
                    SELECT userInfo.Id, COUNT(posts.Id) AS NumOfPosts
                    FROM userInfo, posts
                    WHERE userInfo.Id = posts.OwnerUserId
                    GROUP BY userInfo.Id) AS derived2
                    ON derived1.Id = derived2.Id

                    /*ColumnName: NumOfComments; Each User's Number of Comments*/
                    LEFT JOIN (
                    SELECT userInfo.Id, COUNT(comments.Id) AS NumOfComments
                    FROM userInfo, comments
                    WHERE userInfo.Id = comments.UserInfoId
                    GROUP BY userInfo.Id) AS derived3
                    ON derived1.Id = derived3.Id

                    /*ColumnName: NumOfBadges; Each User's Number of Badges*/
                    LEFT JOIN (
                    SELECT userInfo.Id, COUNT(badges.Id) AS NumOfBadges
                    FROM userInfo, badges
                    WHERE userInfo.Id = badges.UserInfoId
                    GROUP BY userInfo.Id) AS derived4
                    ON derived1.Id = derived4.Id
                    );'''

            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
    #-------------(R4)END-------------

    #-------------(R5)BEGIN-----------
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')
    import numpy as np
    import pandas as pd
    data = pd.read_sql('SELECT * FROM ReputStatMatrix',conn)
    frame = pd.DataFrame(data)

    from sklearn import tree
    x = frame[['NumOfPosts','NumOfComments','NumOfBadges']]
    y_temp = frame[['Reputation']]
    y = pd.DataFrame([1 if int(y_value) > 180 else 0 for y_value in y_temp.values],columns=['ReputationOver180']) #after class labeling

    import graphviz

    from sklearn.metrics import accuracy_score

    #separate list x in 3 sections for cross validation.
    x_set1 = x[0*int(len(y))//3:1*int(len(y))//3] #[0:1316]
    x_set2 = x[1*int(len(y))//3:2*int(len(y))//3] #[1317:2633]
    x_set3 = x[2*int(len(y))//3:3*int(len(y))//3] #[2634:3950]

    #separate list y in 3 sections for cross validation.
    y_set1 = y[0*int(len(y))//3:1*int(len(y))//3] #[0:1316]
    y_set2 = y[1*int(len(y))//3:2*int(len(y))//3] #[1317:2633]
    y_set3 = y[2*int(len(y))//3:3*int(len(y))//3] #[2634:3950]


    #--------criterion:gini----------
    clf = tree.DecisionTreeClassifier(criterion='gini',min_samples_split=10)
    clf = clf.fit(x,y)

    print('--------criterion:gini----------')
    #--------predict:class label--------
    print('[NumOfPosts:5,NumOfComments:5,NumOfBadges:5] predict label:',end=' ')
    print(clf.predict([[5., 5., 5.]])) #0 127
    print('[NumOfPosts:2,NumOfComments:6,NumOfBadges:18] predict label:',end=' ')
    print(clf.predict([[2., 6., 18.]])) #1 155(most frequent) or 148(sometimes occur)
    print('[NumOfPosts:6,NumOfComments:3,NumOfBadges:10] predict label:',end=' ')
    print(clf.predict([[6., 3., 10.]])) #0 116
    #--------predict:probability--------
    print('[NumOfPosts:5,NumOfComments:5,NumOfBadges:5] predict proba:',end=' ')
    print(clf.predict_proba([[5., 5., 5.]])) #0.875 0.125
    print('[NumOfPosts:2,NumOfComments:6,NumOfBadges:18] predict proba:',end=' ')
    print(clf.predict_proba([[2., 6., 18.]])) #0 1
    print('[NumOfPosts:6,NumOfComments:3,NumOfBadges:10] predict proba:',end=' ')
    print(clf.predict_proba([[6., 3., 10.]])) #0.5 0.5

    #--------export:DTgraph-------------
    dot_data = tree.export_graphviz(clf,out_file=None)
    graph = graphviz.Source(dot_data,format='png')
    graph.render('Decisiontree_Images/r5_gini')

    #--------cross validation-----------
    clf.fit(x_set1.append(x_set2),y_set1.append(y_set2))
    y_pred = clf.predict(x_set3)
    accuracy_set3 = accuracy_score(y_pred, y_set3)

    clf.fit(x_set2.append(x_set3),y_set2.append(y_set3))
    y_pred = clf.predict(x_set1)
    accuracy_set1 = accuracy_score(y_pred, y_set1)

    clf.fit(x_set3.append(x_set1),y_set3.append(y_set1))
    y_pred = clf.predict(x_set2)
    accuracy_set2 = accuracy_score(y_pred, y_set2)

    avgOfAccuracy = np.mean([accuracy_set1,accuracy_set2,accuracy_set3])
    print('accuracy:',end=' ')
    print(avgOfAccuracy)

    #--------criterion:entropy----------
    clf = tree.DecisionTreeClassifier(criterion='entropy',min_samples_split=10)
    clf = clf.fit(x,y)

    print('--------criterion:entropy----------')
    #--------predict:class label--------
    print('[NumOfPosts:5,NumOfComments:5,NumOfBadges:5] predict label:',end=' ')
    print(clf.predict([[5., 5., 5.]])) #0 135
    print('[NumOfPosts:2,NumOfComments:6,NumOfBadges:18] predict label:',end=' ')
    print(clf.predict([[2., 6., 18.]])) #1 257
    print('[NumOfPosts:6,NumOfComments:3,NumOfBadges:10] predict label:',end=' ')
    print(clf.predict([[6., 3., 10.]])) #1 116
    #--------predict:probability--------
    print('[NumOfPosts:5,NumOfComments:5,NumOfBadges:5] predict proba:',end=' ')
    print(clf.predict_proba([[5., 5., 5.]])) #0.875 0.125
    print('[NumOfPosts:2,NumOfComments:6,NumOfBadges:18] predict proba:',end=' ')
    print(clf.predict_proba([[2., 6., 18.]])) #0 1
    print('[NumOfPosts:6,NumOfComments:3,NumOfBadges:10] predict proba:',end=' ')
    print(clf.predict_proba([[6., 3., 10.]])) #0.44 0.56

    #--------export:DTgraph-------------
    dot_data = tree.export_graphviz(clf,out_file=None)
    graph = graphviz.Source(dot_data,format='png')
    graph.render('Decisiontree_Images/r5_entropy')

    #--------cross validation-----------
    clf.fit(x_set1.append(x_set2),y_set1.append(y_set2))
    y_pred = clf.predict(x_set3)
    accuracy_set3 = accuracy_score(y_pred, y_set3)

    clf.fit(x_set2.append(x_set3),y_set2.append(y_set3))
    y_pred = clf.predict(x_set1)
    accuracy_set1 = accuracy_score(y_pred, y_set1)

    clf.fit(x_set3.append(x_set1),y_set3.append(y_set1))
    y_pred = clf.predict(x_set2)
    accuracy_set2 = accuracy_score(y_pred, y_set2)

    avgOfAccuracy = np.mean([accuracy_set1,accuracy_set2,accuracy_set3])
    print('accuracy:',end=' ')
    print(avgOfAccuracy)
    #-------------(R5)END-------------

def decisiontree2(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)

    #-------------(R6)BEGIN-----------
    #-------------CREATE VIEW: ReputStatMatrix2-----------
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')
    try:
        with conn.cursor() as cursor :
            sql ='''CREATE VIEW ReputStatMatrix2 AS
                    (SELECT derived1.Id, derived1.Reputation, IFNULL(derived2.NumOfPosts,0) AS NumOfPosts, IFNULL(derived3.NumOfComments,0) AS NumOfComments, IFNULL(derived4.NumOfBadges,0) AS NumOfBadges, IFNULL(derived6.Score,0) AS Score, IFNULL(derived7.NumOfAccepted,0) AS NumOfAccepted

                    FROM
                    (SELECT Id, Reputation
                    FROM userInfo
                    WHERE Reputation>110) derived1

                    /*ColumnName: NumOfPosts; Each User's Number of Posts*/
                    LEFT JOIN (
                    SELECT userInfo.Id, COUNT(posts.Id) AS NumOfPosts
                    FROM userInfo, posts
                    WHERE userInfo.Id = posts.OwnerUserId
                    GROUP BY userInfo.Id) AS derived2
                    ON derived1.Id = derived2.Id

                    /*ColumnName: NumOfComments; Each User's Number of Comments*/
                    LEFT JOIN (
                    SELECT userInfo.Id, COUNT(comments.Id) AS NumOfComments
                    FROM userInfo, comments
                    WHERE userInfo.Id = comments.UserInfoId
                    GROUP BY userInfo.Id) AS derived3
                    ON derived1.Id = derived3.Id

                    /*ColumnName: NumOfBadges; Each User's Number of Badges*/
                    LEFT JOIN (
                    SELECT userInfo.Id, COUNT(badges.Id) AS NumOfBadges
                    FROM userInfo, badges
                    WHERE userInfo.Id = badges.UserInfoId
                    GROUP BY userInfo.Id) AS derived4
                    ON derived1.Id = derived4.Id

                    /*ColumnName: Score; Each User's Score(Summation of NumOfLike - Summation of NumOfDislike)*/
                    LEFT JOIN (
                    SELECT posts.OwnerUserId , SUM(`Like`-`Dislike`) AS Score
                    FROM posts, (SELECT PostId,
                    SUM(case when VoteTypeId=2 then 1 else 0 end) AS `Like`, SUM(case when VoteTypeId=3 then 1 else 0 end) AS `Dislike`
                    FROM votes
                    GROUP BY PostId) AS derived7
                    WHERE posts.Id = derived7.PostId
                    GROUP BY posts.OwnerUserId) AS derived6
                    ON derived1.Id = derived6.OwnerUserId

                    /*ColumnName: NumOfAccepted; Each User's Number of Accepted*/
                    LEFT JOIN (
                    SELECT posts.OwnerUserId, SUM(IF(answerPosts.Accepted = 1,1,0)) AS NumOfAccepted
                    FROM posts, answerPosts
                    WHERE posts.Id = answerPosts.PostId
                    GROUP BY posts.OwnerUserId) AS derived7
                    ON derived1.Id = derived7.OwnerUserId
                    );'''
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
    #-------------CREATE VIEW: ReputStatMatrix2-----------

    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')
    import numpy as np
    import pandas as pd
    data = pd.read_sql('SELECT * FROM ReputStatMatrix2',conn)
    frame = pd.DataFrame(data)

    from sklearn import tree
    x = frame[['NumOfPosts','NumOfComments','NumOfBadges','Score','NumOfAccepted']]
    y_temp = frame[['Reputation']]
    y = pd.DataFrame([1 if int(x) > 180 else 0 for x in y_temp.values],columns=['ReputationOver180']) #after class labeling

    import graphviz

    from sklearn.metrics import accuracy_score


    #separate list x in 3 sections for cross validation.
    x_set1 = x[0*int(len(y))//3:1*int(len(y))//3] #[0:1316]
    x_set2 = x[1*int(len(y))//3:2*int(len(y))//3] #[1317:2633]
    x_set3 = x[2*int(len(y))//3:3*int(len(y))//3] #[2634:3950]

    #separate list y in 3 sections for cross validation.
    y_set1 = y[0*int(len(y))//3:1*int(len(y))//3] #[0:1316]
    y_set2 = y[1*int(len(y))//3:2*int(len(y))//3] #[1317:2633]
    y_set3 = y[2*int(len(y))//3:3*int(len(y))//3] #[2634:3950]


    #--------criterion:gini----------
    clf = tree.DecisionTreeClassifier(criterion='gini',min_samples_split=10)
    clf = clf.fit(x,y)

    #--------export:DTgraph-------------
    dot_data = tree.export_graphviz(clf,out_file=None)
    graph = graphviz.Source(dot_data,format='png')
    graph.render('Decisiontree_Images/r6_gini')

    #--------cross validation-----------
    clf.fit(x_set1.append(x_set2),y_set1.append(y_set2))
    y_pred = clf.predict(x_set3)
    accuracy_set3 = accuracy_score(y_pred, y_set3)

    clf.fit(x_set2.append(x_set3),y_set2.append(y_set3))
    y_pred = clf.predict(x_set1)
    accuracy_set1 = accuracy_score(y_pred, y_set1)

    clf.fit(x_set3.append(x_set1),y_set3.append(y_set1))
    y_pred = clf.predict(x_set2)
    accuracy_set2 = accuracy_score(y_pred, y_set2)

    avgOfAccuracy = np.mean([accuracy_set1,accuracy_set2,accuracy_set3])
    print('accuracy:',end=' ')
    print(avgOfAccuracy)


    #--------criterion:entropy----------
    clf = tree.DecisionTreeClassifier(criterion='entropy',min_samples_split=10)
    clf = clf.fit(x,y)

    #--------export:DTgraph-------------
    dot_data = tree.export_graphviz(clf,out_file=None)
    graph = graphviz.Source(dot_data,format='png')
    graph.render('Decisiontree_Images/r6_entropy')

    #--------cross validation-----------
    clf.fit(x_set1.append(x_set2),y_set1.append(y_set2))
    y_pred = clf.predict(x_set3)
    accuracy_set3 = accuracy_score(y_pred, y_set3)

    clf.fit(x_set2.append(x_set3),y_set2.append(y_set3))
    y_pred = clf.predict(x_set1)
    accuracy_set1 = accuracy_score(y_pred, y_set1)

    clf.fit(x_set3.append(x_set1),y_set3.append(y_set1))
    y_pred = clf.predict(x_set2)
    accuracy_set2 = accuracy_score(y_pred, y_set2)

    avgOfAccuracy = np.mean([accuracy_set1,accuracy_set2,accuracy_set3])
    print('accuracy:',end=' ')
    print(avgOfAccuracy)
    #-------------(R6)END-------------

#---------------Run-------------------
# association('localhost','root','1234')
# decisiontree1('localhost','root','1234')
# decisiontree2('localhost','root','1234')


#아래 String은 R3의 대한 설명문입니다.
'''
(R3)
frozenset({0}):r
frozenset({1}):regression
frozenset({2}):time-series
frozenset({3}):machine-learning
frozenset({8}):logistic
frozenset({12}):classification

frequent_itemsets
frozenset({0})
frozenset({1})
frozenset({0, 1})
frozenset({2})
frozenset({0, 2})
frozenset({3})
frozenset({4})
frozenset({5})
frozenset({6})
frozenset({7})
frozenset({8})
frozenset({8, 1})
frozenset({9})
frozenset({10})
frozenset({11})
frozenset({12})
frozenset({3, 12})
frozenset({13})
frozenset({14})
frozenset({15})
frozenset({16})
frozenset({17})
frozenset({18})
frozenset({19})
frozenset({20})
frozenset({21})
frozenset({22})
frozenset({23})
frozenset({24})
frozenset({25})
frozenset({26})
frozenset({27})
frozenset({28})
frozenset({29})
frozenset({30})
frozenset({31})
frozenset({32})
frozenset({33})
frozenset({34})
frozenset({35})
frozenset({36})
frozenset({37})
frozenset({38})
frozenset({39})
frozenset({40})
frozenset({41})
frozenset({42})
frozenset({43})
frozenset({44})
frozenset({45})
frozenset({46})
frozenset({47})
frozenset({48})
frozenset({49})
frozenset({50})
frozenset({51})
frozenset({52})
frozenset({53})
frozenset({54})
frozenset({55})
frozenset({56})
frozenset({57})
frozenset({58})
frozenset({59})

rule_stat
(frozenset({1}), frozenset({0}), 1059, 0.19564012562349897, 0.12611542135551362, 1.3382597450581932, 1.1591758464779403, 0.003388082470134884)
(frozenset({0}), frozenset({1}), 1059, 0.1461899503036996, 0.16877519163113627, 0.7472390944229708, 1.1591758464779403, 0.003388082470134884)
(frozenset({2}), frozenset({0}), 607, 0.2217756667884545, 0.06376831853871065, 2.646693459992693, 1.3140300102467224, 0.0033797511825348903)
(frozenset({0}), frozenset({2}), 607, 0.08379348426283821, 0.16877519163113627, 0.377829928216455, 1.3140300102467224, 0.0033797511825348903)
(frozenset({1}), frozenset({8}), 576, 0.10641049325697395, 0.12611542135551362, 0.3000184740439682, 2.8123428454941988, 0.008648180511140139)
(frozenset({8}), frozenset({1}), 576, 0.35467980295566504, 0.03783695626849328, 3.333128078817734, 2.812342845494199, 0.008648180511140139)
(frozenset({12}), frozenset({3}), 431, 0.3221225710014948, 0.031173551408401484, 1.9162929745889388, 5.3922866107469405, 0.008179469588053833)
(frozenset({3}), frozenset({12}), 431, 0.16809672386895474, 0.059737657556906874, 0.5218408736349454, 5.3922866107469405, 0.008179469588053833)

위 결과(rule_stat)에서 association rule(X->Y), confidence, lift 값만 tuple 형태로 정리하면 아래와 같다.

(X->Y, Confidence, Lift)
(frozenset({1}), frozenset({0}), 0.19564012562349897, 1.1591758464779403) 독립에 가까움. 약한 양의 상관관계
(frozenset({0}), frozenset({1}), 0.1461899503036996, 1.1591758464779403) 독립에 가까움. 약한 양의 상관관계
(frozenset({2}), frozenset({0}), 0.2217756667884545, 1.3140300102467224) 독립에 가까움. 약한 양의 상관관계
(frozenset({0}), frozenset({2}), 0.08379348426283821, 1.3140300102467224) 독립에 가까움. 약한 양의 상관관계
(frozenset({1}), frozenset({8}), 0.10641049325697395, 2.8123428454941988) 상당히 강한 양의 상관관계
(frozenset({8}), frozenset({1}), 0.35467980295566504, 2.812342845494199) 상당히 강한 양의 관관계
(frozenset({12}), frozenset({3}), 0.3221225710014948, 5.3922866107469405) 아주 강한 양의 상관관계
(frozenset({3}), frozenset({12}), 0.16809672386895474, 5.3922866107469405) 아주 강한 양의 상관관계

위 (X->Y, Confidence, Lift)에서의 결과값을 분석하면 아래와 같다.

[def]lift: support를 고려했을 때의 confidence를 계산한 것임. X->Y와 Y->X에서 L(X,Y)와 L(Y,X)의 value는 같음.
L(X,Y)=s(XandY)/(s(X)*s(Y)), L(Y,X)=s(YandX)/(s(Y)*s(X))=L(X,Y)

[def]confidence: X->Y일 때, s(XandY)/s(X). Y->X일 때, s(XandY)/s(Y). 따라서, X->Y와 Y->X는 다를 수 있음.

confidence 값이 높은 association rule을 정리하면 아래와 같다.
8->1: logistic -> regression
2->0: time-series -> r
12->3: classification -> machine-learning
1->0: regression -> r

이중에서도 lift값이 높은 association rule만 추리면 다음과 같다.
8->1: logistic -> regression
12->3: classification -> machine-learning
classfication에 machine-learning approach를 하는 게 대세인가보다.
'''




#R6 테스트용 SQL 코드
'''CREATE VIEW ReputStatMatrix2 AS
        (SELECT derived1.Id, derived1.Reputation, IFNULL(derived2.NumOfPosts,0) AS NumOfPosts, IFNULL(derived3.NumOfComments,0) AS NumOfComments, IFNULL(derived4.NumOfBadges,0) AS NumOfBadges, IFNULL(derived5.TotalView,0) AS TotalView, IFNULL(derived6.Score,0) AS Score, IFNULL(derived7.NumOfAccepted,0) AS NumOfAccepted, IFNULL(derived8.TotalLinks,0) AS TotalLinks, IFNULL(derived10.CreateYM,0) AS CreateYM, IFNULL(derived12. `Like`,0) AS `Like`

        FROM
        (SELECT Id, Reputation
        FROM userInfo
        WHERE Reputation>110) derived1

        /*ColumnName: NumOfPosts; Each User's Number of Posts*/
        LEFT JOIN (
        SELECT userInfo.Id, COUNT(posts.Id) AS NumOfPosts
        FROM userInfo, posts
        WHERE userInfo.Id = posts.OwnerUserId
        GROUP BY userInfo.Id) AS derived2
        ON derived1.Id = derived2.Id

        /*ColumnName: NumOfComments; Each User's Number of Comments*/
        LEFT JOIN (
        SELECT userInfo.Id, COUNT(comments.Id) AS NumOfComments
        FROM userInfo, comments
        WHERE userInfo.Id = comments.UserInfoId
        GROUP BY userInfo.Id) AS derived3
        ON derived1.Id = derived3.Id

        /*ColumnName: NumOfBadges; Each User's Number of Badges*/
        LEFT JOIN (
        SELECT userInfo.Id, COUNT(badges.Id) AS NumOfBadges
        FROM userInfo, badges
        WHERE userInfo.Id = badges.UserInfoId
        GROUP BY userInfo.Id) AS derived4
        ON derived1.Id = derived4.Id

        /*ColumnName: TotalView; Each User's Summation Of Posts' ViewCounts*/
        LEFT JOIN (
        SELECT posts.OwnerUserId, SUM(ViewCount) AS TotalView
        FROM posts, questionPosts
        WHERE posts.Id = questionPosts.PostId
        GROUP BY posts.OwnerUserId) AS derived5
        ON derived1.Id = derived5.OwnerUserId

        /*ColumnName: Score; Each User's Score(Summation of NumOfLike - Summation of NumOfDislike)*/
        LEFT JOIN (
        SELECT posts.OwnerUserId , SUM(`Like`-`Dislike`) AS Score
        FROM posts, (SELECT PostId,
        SUM(case when VoteTypeId=2 then 1 else 0 end) AS `Like`, SUM(case when VoteTypeId=3 then 1 else 0 end) AS `Dislike`
        FROM votes
        GROUP BY PostId) AS derived7
        WHERE posts.Id = derived7.PostId
        GROUP BY posts.OwnerUserId) AS derived6
        ON derived1.Id = derived6.OwnerUserId

        /*ColumnName: NumOfAccepted; Each User's Number of Accepted*/
        LEFT JOIN (
        SELECT posts.OwnerUserId, SUM(IF(answerPosts.Accepted = 1,1,0)) AS NumOfAccepted
        FROM posts, answerPosts
        WHERE posts.Id = answerPosts.PostId
        GROUP BY posts.OwnerUserId) AS derived7
        ON derived1.Id = derived7.OwnerUserId

        /*ColumnName: TotalLinks; Each User's Summation Of Count(RelatedPostId)*/
        LEFT JOIN (
        SELECT posts.OwnerUserId, SUM(NumOfLinks) AS TotalLinks
        FROM posts, (SELECT RelatedPostId,
        COUNT(Id) AS 'NumOfLinks'
        FROM postLinks
        GROUP BY RelatedPostId) AS derived9
        WHERE posts.Id = derived9.RelatedPostId
        GROUP BY posts.OwnerUserId) AS derived8
        ON derived1.Id = derived8.OwnerUserId

        /*ColumnName: CreateYM; Each User's (CreationYear-2000)*12+month*/
        LEFT JOIN (
        SELECT Id, SUM((Year-2000)*12+Month) AS CreateYM
        FROM (SELECT Id, year(userinfo.Creationdate) AS Year,
        month(userInfo.CreationDate) AS Month
        FROM userinfo) AS derived11
        GROUP BY Id) AS derived10
        ON derived1.Id = derived10.Id

        /*ColumnName: Like; Each User's Summation of NumOfLike */
        LEFT JOIN (
        SELECT posts.OwnerUserId , SUM(`Like`) AS `Like`
        FROM posts, (SELECT PostId,
        SUM(case when VoteTypeId=2 then 1 else 0 end) AS `Like`
        FROM votes
        GROUP BY PostId) AS derived13
        WHERE posts.Id = derived13.PostId
        GROUP BY posts.OwnerUserId) AS derived12
        ON derived1.Id = derived12.OwnerUserId
        );'''

#'NumOfPosts','NumOfComments','NumOfBadges','TotalView','Score','NumOfLinked','NumOfAccepted','CreateYM','TotalLinks','Like'
