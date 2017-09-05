import requests
import MySQLdb

from bs4 import BeautifulSoup

db = MySQLdb.connect(host="localhost", user="root", passwd = "root", db="practiceOnline")
cur = db.cursor()
baseUrl = 'https://www.indiabix.com'
pageArr = []


def getTopicUrl(url):
    topicUrl = []
    r =requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    topicsIndex =  soup.find_all("div",{"class":"div-topics-index"})
    for totaltopics in topicsIndex:
        topics = totaltopics.find_all("a")
        for topic in topics:
            topicUrl.insert(0,baseUrl + topic.get("href"))
    return topicUrl


def callGetQuestions(topicUrl,i):
    j = 1
    for topic in topicUrl:
        getLinks(topic,i,j)
        j = j+1

def getQuestions(url,i,j):
    print url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    questions = soup.find_all("div",{"class":"bix-div-container"})
    for question in questions:
        questionNo = question.find("td",{"class":"bix-td-qno"}).text.replace('.','')
        questionText = question.find("td",{"class":"bix-td-qtxt"}).text.encode('utf8')
        options = question.find("table",{"class":"bix-tbl-options"}).find_all("td",{"class":"bix-td-option"})
        optionA = options[1].text.encode('utf8')
        optionB = options[3].text.encode('utf8')
        optionC = options[5].text.encode('utf8')
        answer =  question.find("div",{"class":"bix-div-answer"}).find_all("span")
        answerDesc = question.find("div",{"class":"bix-ans-description"}).text
        print questionNo
        if (len(options) > 6):
            optionD = options[7].text.encode('utf8')
            if(len(options)>8):
                optionE = options[9].text.encode('utf8')
                questionsQuery = 'INSERT INTO `questions` ( `group_id`,`subgroup_id`,`question_no`, `question`, `option_A`, `option_B`, `option_C`, `option_D`, `option_E`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cur.execute(questionsQuery, (i, j, questionNo, questionText, optionA, optionB, optionC, optionD, optionE))
            else:
                questionsQuery = 'INSERT INTO `questions` ( `group_id`,`subgroup_id`,`question_no`, `question`, `option_A`, `option_B`, `option_C`, `option_D`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)'
                cur.execute(questionsQuery, (i, j, questionNo, questionText, optionA, optionB, optionC, optionD))
        else:
            questionsQuery = 'INSERT INTO `questions` ( `group_id`,`subgroup_id`,`question_no`, `question`, `option_A`, `option_B`, `option_C`) VALUES ( %s, %s, %s,%s, %s, %s, %s)'
            cur.execute(questionsQuery, (i, j, questionNo, questionText, optionA, optionB, optionC))
        try:
            questionImg = question.find("td",{"class":"bix-td-qtxt"}).find("img",{"class":"nvr-image-opacity"})
            if questionImg.has_attr('src'):
                questionsQuery = 'INSERT INTO `question_images` ( `group_id`,`subgroup_id`, `question_no`, `image_url`) VALUES ( %s, %s, %s, %s)'
                cur.execute(questionsQuery,(i, j, questionNo, baseUrl+questionImg.get('src')))
        except Exception as e:
            print e
        #cur.execute(questionsQuery,(questionText,optionA,optionB,optionC,optionD))
        #print answer[1].text + ' ' + answerDesc
        answerQuery = 'INSERT INTO `answer` ( `group_id`,`subgroup_id`,`question_no`, `answer`, `solution`) VALUES ( %s, %s, %s, %s, %s)'
        cur.execute(answerQuery,(i,j,questionNo, answer[1].text.encode('utf8'), answerDesc.encode('utf-8')))
        db.commit()
        print "Question"+questionNo+"inserted"
        #print questionNo+'.'+questionText
        #print optionA + optionB + optionC + optionD


def getLinks(url, index, j):
    if url != 'https://www.indiabix.com/verbal-ability/comprehension/' and url != 'https://www.indiabix.com/verbal-ability/paragraph-formation/' and url != 'https://www.indiabix.com/verbal-ability/closet-test/' and url != 'http://www.indiabix.com/logical-reasoning/analyzing-arguments/' and url != 'https://www.indiabix.com/logical-reasoning/logical-games/' and url!='https://www.indiabix.com/verbal-reasoning/seating-arrangement/' and url!='https://www.indiabix.com/verbal-reasoning/cube-and-cuboid/' and url!='https://www.indiabix.com/verbal-reasoning/dice/' and url!='https://www.indiabix.com/verbal-reasoning/character-puzzles/' and url!='https://www.indiabix.com/verbal-reasoning/questions-and-answers/':
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        pageCount = soup.find_all("span",{"class":"mx-pager-no"})
        page = soup.find("p",{"class":"mx-pager"})
        pageUrl = page.find("a").get("href").replace(' ','')[:-3]
        pageArr.insert(0,url)
        getQuestions(url, index, j)
        for i in range(2,len(pageCount)+2):
            pageIndex = '00'+ str(i)
            pageIndex = pageIndex[-3:]
            pageArr.insert(i-1,baseUrl+pageUrl+pageIndex)
            getQuestions(baseUrl+pageUrl+pageIndex, index, j)
    #print pageArr


def main():
    group = ['http://www.indiabix.com/microbiology/questions-and-answers/','https://www.indiabix.com/verbal-reasoning/questions-and-answers/','https://www.indiabix.com/non-verbal-reasoning/questions-and-answers/']
    i = 2
    for url in group:
        topicUrl = getTopicUrl(url)
        #print topicUrl
        callGetQuestions(topicUrl, i)
        i = i+1
        #print group
main()
#getQuestions("http://www.indiabix.com/non-verbal-reasoning/analytical-reasoning/007006",1,1)
db.close()