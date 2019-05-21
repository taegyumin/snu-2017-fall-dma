def requirement2(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
    conn = pymysql.connect(host=host, user=user, password=password) #db='db2017_13', charset='utf8'

    try:
        with conn.cursor() as cursor :
            sql = 'CREATE DATABASE IF NOT EXISTS db2017_13 CHARACTER SET=utf8' #'SET=utf-8' occurs error.
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()

def requirement3(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
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

	            Primary key (Id),
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
	           	TagsId	    INT(11) NOT NULL,

		        Primary key (QuestionId,TagsId),
		        Foreign key (QuestionId) references questionPosts(Id),
		        Foreign key (TagsId) references tags(Id));'''
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

def requirement4(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')
    from datetime import datetime
    import csv

    #csv 파일내 모든 데이터의 타입은 기본적으로 String이다.
    #그러나 우리가 설계한 database내에는 INT, DATETIME등 String이 아닌 타입을 요구하는 attribute들이 존재한다.
    #따라서 csv 파일을 database에 삽입(insert)하는 과정에서 일부 데이터의 형변환(type casting) 내지 전처리가 필요하다.
    #우리 13팀은 이러한 사실에 입각하여, 빠른 시간 내에 알맞게 형변환하여 데이터를 삽입하도록 코드를 작성했다.

    #해당 column의 null이 아닌 data가 integer 제약조건이 걸려있을 경우 String을 Integer로 형변환하였다.
    #이에 대한 내용을 뒤 이어지는 주석문에서는 #String to Integer that is not null이라 표현하였다.

    #데이터의 빈 칸(“”)을 Null을 표현하는 ‘None’으로 변환하였다.
    #이에 대한 내용을 뒤 이어지는 주석문에서는 #empty data to null이라 표현하였다.

    #R4의 전체 코드는 csv file to python, python to database의 크게 두 가지로 나뉜다.
    #csv file to python은, csv file의 데이터를 python 상에 불러오는 과정으로 list 자료형의 변수에 담는다.
    #python to database은, 불러온 데이터들을 python 상에서 database로 최종 삽입하는 과정이다.

    #csv 파일을 불러올 시, directory를 dbproject2_13.py와 동일한 directory로 설정해두었다.
    #따라서 userInfo.csv, posts.csv 등의 csv 파일을 dbproject2_13.py과 동일한 폴더 내에 위치시켜야 한다.


    #----------csv file to python-------------

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
    tempTags = dict()
    f2 = open('dataset/tags.csv','r',encoding='utf-8',errors='replace')
    rdr2 = csv.reader(f2)
    next(rdr2,None)
    for line2 in rdr2:
        for i in [0]: #String to Integer that is not null
            if line2[i] !='':
                line2[i] = int(line2[0])
            else :  #empty data to null
                line2[i] = None
        for i in [1]:  #empty data to null
            if line2[i] =='':
                line2[i] = None
        tempTags[line2[1]] = line2[0]

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
            if j in tempTags:
                tempLine=[line[0],tempTags[j]]
                questionQuoteTags.append(tempLine)
            f2.close()
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


    #----------python to database----------------
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

            cursor.executemany("insert into questionQuoteTags(QuestionId,TagsId) values (%s,%s)",questionQuoteTags)
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

def requirement6(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')

    try:
        with conn.cursor() as cursor :
            sql = '''SELECT  OwnerUserId AS UserId, Reputation, DisplayName, Age, CreationDate, LastAccessDate, WebsiteUrl, Location, AboutMe, TotalView
                    #userInfo의 모든 Column과 User 개인의 총조회수를 의미하는 TotalView Column
                    FROM userInfo,
                    ((SELECT OwnerUserId,TotalView
                    FROM
                    (SELECT OwnerUserId, SUM(ViewCount) AS TotalView
                    # post의 Id와 같은 PostId를 가진 questionPosts의 ViewCount를 OwnerUserId 별로 합산하는 구문
                    FROM posts, questionPosts
                    WHERE posts.Id = questionPosts.PostId
                    GROUP BY OwnerUserId) AS derived1,
                    (SELECT *, case when (userInfo.Age<50 AND userInfo.Age>=10)then (userInfo.Age-(userInfo.Age%10))/10 else 5 end AS AgeRange  /*userInfo의 Column을 가져오되 나이에 따른 AgeRange도 Column에 추가
                    AgeRange는 10대 1, 20대 2, 30대 3, 40대 4, 50대 이상은 5가 나오게 코드를 짬, case when 구문에서 else 이후가 50대 이상을 나타내기 위해서 아래의 WHERE 문에서 익명의 사용자와 NULL값을 제거*/
                    FROM userInfo
                    WHERE Id<>0 AND Age is not null /* 익명의 사용자와 Age가 NULL값인 데이터를 제거하기 위해서 추가한 조건문*/) AS derived2
                    WHERE OwnerUserId = derived2.Id AND AgeRange = 1 # derived1의 OwnerUserId와 derived2의 Id가 같은 값을 갖는  데이터 중에서 10대를 찾기 위한 조건문
                    ORDER BY TotalView DESC  /* 조회수 합으로 내림차순 정렬 후 LIMIT를 사용해 최댓값 하나만 남김*/
                    LIMIT 1)

                    UNION   #앞에서 구한 table은 10대에 관한 데이터 였으므로 앞으로 나올 20대,30대, 40대, 50대 이상을 UNION으로 연결해 하나의 테이블로 만듦.

                    (SELECT OwnerUserId,TotalView    #20대에서 최대 조회수를 가지는 데이터의 OwnerUserId와 TotalView를 구하는 구문
                    FROM
                    (SELECT OwnerUserId, SUM(ViewCount) AS TotalView
                    FROM posts, questionPosts
                    WHERE posts.Id = questionPosts.PostId
                    GROUP BY OwnerUserId) AS derived1,
                    (SELECT *, case when (userInfo.Age<50 AND userInfo.Age>=10)then (userInfo.Age-(userInfo.Age%10))/10 else 5 end AS AgeRange
                    FROM userInfo
                    WHERE Id<>0 AND Age is not null ) AS derived2
                    WHERE OwnerUserId = derived2.Id AND AgeRange = 2
                    ORDER BY TotalView DESC
                    LIMIT 1)

                    UNION

                    (SELECT OwnerUserId, TotalView   #30대에서 최대 조회수를 가지는 데이터의 OwnerUserId와 TotalView를 구하는 구문
                    FROM
                    (SELECT OwnerUserId, SUM(ViewCount) AS TotalView
                    FROM posts, questionPosts
                    WHERE posts.Id = questionPosts.PostId
                    GROUP BY OwnerUserId) AS derived1,
                    (SELECT *, case when (userInfo.Age<50 AND userInfo.Age>=10)then (userInfo.Age-(userInfo.Age%10))/10 else 5 end AS AgeRange
                    FROM userInfo
                    WHERE Id<>0 AND Age is not null ) AS derived2
                    WHERE OwnerUserId = derived2.Id AND AgeRange = 3
                    ORDER BY TotalView DESC
                    LIMIT 1)

                    UNION

                    (SELECT OwnerUserId, TotalView     #40대에서 최대 조회수를 가지는 데이터의 OwnerUserId와 TotalView를 구하는 구문
                    FROM
                    (SELECT OwnerUserId, SUM(ViewCount) AS TotalView
                    FROM posts, questionPosts
                    WHERE posts.Id = questionPosts.PostId
                    GROUP BY OwnerUserId) AS derived1,
                    (SELECT *, case when (userInfo.Age<50 AND userInfo.Age>=10)then (userInfo.Age-(userInfo.Age%10))/10 else 5 end AS AgeRange
                    FROM userInfo
                    WHERE Id<>0 AND Age is not null ) AS derived2
                    WHERE OwnerUserId = derived2.Id AND AgeRange = 4
                    ORDER BY TotalView DESC
                    LIMIT 1)

                    UNION

                    (SELECT OwnerUserId, TotalView    #50대 이상에서 최대 조회수를 가지는 데이터의 OwnerUserId와 TotalView를 구하는 구문
                    FROM
                    (SELECT OwnerUserId, SUM(ViewCount) AS TotalView
                    FROM posts, questionPosts
                    WHERE posts.Id = questionPosts.PostId
                    GROUP BY OwnerUserId) AS derived1,
                    (SELECT *, case when (userInfo.Age<50 AND userInfo.Age>=10)then (userInfo.Age-(userInfo.Age%10))/10 else 5 end AS AgeRange
                    FROM userInfo
                    WHERE Id<>0 AND Age is not null ) AS derived2
                    WHERE OwnerUserId = derived2.Id AND AgeRange = 5
                    ORDER BY TotalView DESC
                    LIMIT 1)) AS U
                    WHERE userInfo.Id = OwnerUserId  #userInfo의 Id와 OwnerUserId가 같은 데이터를 찾아서 UNION을 통해서 묶어둔 테이블과 userInfo의 데이터를 통합할 수 있음
                    ORDER BY Reputation DESC;        #Reputation에 따라 내림차순 정렬
                    '''
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        conn.commit()
    finally:
        conn.close()
    return rows

def requirement7(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')

    try:
        with conn.cursor() as cursor :
            sql = '''SELECT                   # 구문을 이해하기 위해서는 아래 주석부터 읽으시면 편합니다.
                    MAX(`2010`) AS `2010`,    # 데이터 5개에 있는 데이터를 NULL값을 없애고 하나의 데이터로 통합하기 위해서 각 Column의 최댓값을 갖는 하나의 데이터로 만드는 구문이다.
                    MAX(`2011`) AS `2011`,
                    MAX(`2012`) AS `2012`,
                    MAX(`2013`) AS `2013`,
                    MAX(`2014`) AS `2014`
                    FROM ( SELECT
                    (case when Y=2010 then A end) AS `2010`,  /* case when 구문을 이용해서 생성년도 각각을 하나의 Column으로 배정하고 년도에 해당하는 계정 생성수를 하나씩 데이터로 넣는다.
                     이렇게 하면 데이터마다 하나의 년도의 조회수를 포함하고 나머지 년도는 NULL값을 가지는 총 5개의 데이터가 생성된다. */
                    (case when Y=2011 then A end) AS `2011`,
                    (case when Y=2012 then A end) AS `2012`,
                    (case when Y=2013 then A end) AS `2013`,
                    (case when Y=2014 then A end) AS `2014`
                    FROM (SELECT YEAR(CreationDate) as Y, COUNT(*) AS A
                    FROM userInfo
                    GROUP BY Y/*userInfo에서 년도별로 생성된 계정의 수를 COUNT한다. 이 테이블은  년도와 계정의 수를 attribute로 가지는 테이블이 나오므로 우리가 원하는 테이블이 아니다. */) AS derived1) AS derived2;
                    '''
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        conn.commit()
    finally:
        conn.close()
    return rows

def requirement8(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')

    try:
        with conn.cursor() as cursor :
            sql = '''SELECT derived1.PostId, `Like`,`Dislike`, `Like`-`Dislike` AS `Score`
                    FROM (SELECT PostId,
                    SUM(case when VoteTypeId=2 then 1 else 0 end) AS `Like`, SUM(case when VoteTypeId=3 then 1 else 0 end) AS `Dislike` #VoteTypeId를 이용해 `좋아요`와 `싫어요`의 합을 세고 이를 각각의 Column으로 만든다.
                    FROM votes
                    GROUP BY PostId/*각각의 게시물마다 좋아요수와 싫어요수를 알아야 하기 때문에 PostId로 그룹화하였다.*/) AS derived1, (SELECT posts.Id, COUNT(comments.Id) AS `CommentCount`
                    FROM posts, comments              #posts.Id와 comments.PostId가 같은 값을 갖는 데이터들을 Id 별로 COUNT해서 Id마다의 댓글수를 구한다.
                    WHERE posts.Id = comments.PostId
                    GROUP BY posts.Id) AS derived2
                    WHERE derived1.PostId = derived2.Id AND `Like`>=1 AND `CommentCount`>=10
                    ORDER BY `Score` DESC;  # 좋아요가 1이상 댓글수가 10개 이상인 데이터에 대해서만 쿼리를 실행하게 하는 조건문
                    '''
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        conn.commit()
    finally:
        conn.close()
    return rows

def requirement9(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')

    try:
        with conn.cursor() as cursor :
            sql = '''SELECT greatUsers.Id AS UserId, badgeNum AS BadgeAmount, COUNT(*)/COUNT(DISTINCT YEAR(posts.CreationDate)) AS AvgPostCount
                    FROM posts /*평균 게시물 작성수를 알기 위해서 가져와야할 데이터를 포함하고 있는 테이블*/, (
                    SELECT userInfo.Id, COUNT(*) AS badgeNum    #userInfo.Id와 badges.UserInfoId가 같은 데이터 중에서 userInfo.id로 그룹화하여 뱃지의 개수가 50개 이상 가진 데이터만 뽑아내는 구문이다.
                    FROM userInfo, badges
                    WHERE userInfo.Id = badges.UserInfoId
                    GROUP BY userInfo.Id
                    HAVING badgeNum>=50  #우리가 정의한 badgeNum(뱃지의 개수)가 50이상인 데이터만 그룹화한다는 GROUP BY 조건문
                    ) AS greatUsers
                    WHERE posts.OwnerUserId = greatUsers.Id #post와 greatUsers를 조인하기 위해서 OwnerUserId와 greatUsers.Id가 같은 데이터를 지정하는 조건문
                    GROUP BY greatUsers.Id  # 평균 게시물 작성수는 user의 Id에 따라서 각각 나타내야 하므로 greatUsers.Id로 그룹화
                    ORDER BY BadgeAmount DESC; # 획득한 뱃지 수의 내림차순으로 정렬
                    '''
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        conn.commit()
    finally:
        conn.close()
    return rows

def requirement10(host, user, password):
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
    db = MySQLdb.connect(host=host, user=user, password=password)
    conn = pymysql.connect(host=host, user=user, password=password, db='db2017_13', charset='utf8')

    try:
        with conn.cursor() as cursor :
            sql = '''SELECT TagName, numQuote
                    FROM tags, (SELECT TagsId, COUNT(OwnerUserId) AS numQuote
                    FROM (SELECT OwnerUserId, TagsId #posts, questionPosts, questionQuoteTags 테이블을 조인하여 OwnerUserId와 TagsID를 갖는 테이블을 만든 구문
                    FROM posts AS P, questionPosts AS Q, questionQuoteTags AS QT
                    WHERE P.Id = Q.PostId AND Q.Id = QT.QuestionId/*Join을 하기 위한 조건문 */) AS derived1
                    GROUP BY TagsId/* TagsId별로 그룹화함으로써 TagsId별 인용횟수(NumQuote)를 구할 수 있음*/) AS derived2
                    WHERE tags.Id = derived2.TagsId  #TagsId는 어떤 Tag를 나타내는지 알기 어려우므로 tags 테이블과 조인해서 TagName과 numQuote로 나타냄으로써 가독성을 높임
                    ORDER BY numQuote DESC; #우리가 관심있는 부분은 인용이 많이 된 TagName이므로 numQuote로 내림차순 정렬
                    '''
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        conn.commit()
    finally:
        conn.close()
    return rows

# #---------(R2)-(R10) Run--------------------------------
# requirement2('localhost','root','1234')
# requirement3('localhost','root','1234')
# requirement4('localhost','root','1234')
# requirement6('localhost','root','1234')
# requirement7('localhost','root','1234')
# requirement8('localhost','root','1234')
# requirement9('localhost','root','1234')
# requirement10('localhost','root','1234')

# #---------(R2)-(R10) 소요시간 측정 및 결과(.csv) 출력---------
# import time
# import pandas as pd

# #---------(R2): 소요시간 측정 및 결과(.csv) 출력---------
# print('On R2')
# start_time = time.time()
# requirement2('localhost','root','1234')
# print('total time: %.2f'%(time.time() - start_time))

# #--------(R3): 소요시간 측정 및 결과(.csv) 출력---------
# print('On R3')
# start_time = time.time()
# requirement3('localhost','root','1234')
# print('total time: %.2f'%(time.time() - start_time))

# #---------(R4): 소요시간 측정 및 결과(.csv) 출력---------
# print('On R4')
# start_time = time.time()
# requirement4('localhost','root','1234')
# print('total time: %.2f'%(time.time() - start_time))

# #---------(R6): 소요시간 측정 및 결과(.csv) 출력---------
# print('On R6')
# start_time = time.time()
# rows = requirement6('localhost','root','1234')
# print('total time: %.2f'%(time.time() - start_time))
# columns = ['UserId', 'Reputation', 'DisplayName', 'Age', 'CreationDate', 'LastAccessDate', 'WebsiteUrl', 'Location', 'AboutMe', 'TotalView']
# pd.DataFrame([row for row in rows], columns = columns).to_csv('R6.csv', index = None)

# #---------(R7): 소요시간 측정 및 결과(.csv) 출력---------
# print('On R7')
# start_time = time.time()
# rows = requirement7('localhost','root','1234')
# print('total time: %.2f'%(time.time() - start_time))
# columns = ['2010', '2011', '2012', '2013', '2014']
# pd.DataFrame([row for row in rows], columns = columns).to_csv('R7.csv', index = None)

# #---------(R8): 소요시간 측정 및 결과(.csv) 출력---------
# print('On R8')
# start_time = time.time()
# rows = requirement8('localhost','root','1234')
# print('total time: %.2f'%(time.time() - start_time))
# columns = ['PostId', 'Like', 'Dislike', 'Score']
# pd.DataFrame([row for row in rows], columns = columns).to_csv('R8.csv', index = None)

# #---------(R9): 소요시간 측정 및 결과(.csv) 출력---------
# print('On R9')
# start_time = time.time()
# rows = requirement9('localhost','root','1234')
# print('total time: %.2f'%(time.time() - start_time))
# columns = ['UserId', 'BadgeAmount', 'AvgPostCount']
# pd.DataFrame([row for row in rows], columns = columns).to_csv('R9.csv', index = None)

# #---------(R10): 소요시간 측정 및 결과(.csv) 출력--------
# print('On R10')
# start_time = time.time()
# rows = requirement10('localhost','root','1234')
# print('total time: %.2f'%(time.time() - start_time))
# columns = ['TagName', 'NumQuote']
# pd.DataFrame([row for row in rows], columns = columns).to_csv('R10.csv', index = None)
