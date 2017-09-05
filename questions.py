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
        questionText = question.find("td",{"class":"bix-td-qtxt"}).text
        options = question.find("table",{"class":"bix-tbl-options"}).find_all("td",{"class":"bix-td-option"})
        optionA = options[1].text
        optionB = options[3].text
        optionC = options[5].text
        answer =  question.find("div",{"class":"bix-div-answer"}).find_all("span")
        answerDesc = question.find("div",{"class":"bix-ans-description"}).text
        print questionNo
        try:
            questionImg = question.find("td",{"class":"bix-td-qtxt"}).find("img",{"class":"nvr-image-opacity"})
            if (len(options) > 6):
                optionD = options[7].text
                if(len(options)>8):
                    optionE = options[9].text
                    questionsQuery = 'INSERT INTO `questions` ( `group_id`,`subgroup_id`, `question`, `option_A`, `option_B`, `option_C`, `option_D`, `option_E`, `image_url`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    cur.execute(questionsQuery, (i, j, questionText.encode('utf8'), optionA, optionB, optionC, optionD, optionE,baseUrl+questionImg.get('src')))
                else:
                    questionsQuery = 'INSERT INTO `questions` ( `group_id`,`subgroup_id`, `question`, `option_A`, `option_B`, `option_C`, `option_D`, `image_url`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)'
                    cur.execute(questionsQuery, (i, j, questionText, optionA, optionB, optionC, optionD,baseUrl+questionImg.get('src')))
            else:
                questionsQuery = 'INSERT INTO `questions` ( `group_id`,`subgroup_id`, `question`, `option_A`, `option_B`, `option_C`, `image_url`) VALUES ( %s, %s, %s, %s, %s, %s, %s)'
                cur.execute(questionsQuery, (i, j, questionText, optionA, optionB, optionC,baseUrl+questionImg.get('src')))
        except Exception as e:
            print e
        answerQuery = 'INSERT INTO `answer` ( `group_id`,`subgroup_id`,`question_id`, `answer`, `solution`) VALUES ( %s, %s, %s, %s, %s);'

        #cur.execute(questionsQuery,(questionText,optionA,optionB,optionC,optionD))
        #print answer[1].text + ' ' + answerDesc
        cur.execute(answerQuery,(i,j,questionNo, answer[1].text, answerDesc.encode('utf-8')))
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
    group = ['https://www.indiabix.com/verbal-reasoning/questions-and-answers/','https://www.indiabix.com/non-verbal-reasoning/questions-and-answers/']
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