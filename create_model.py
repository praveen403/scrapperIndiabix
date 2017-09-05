import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd = "root")
cur = db.cursor()

pagesJson = {
  "Arithmetic": {
    "dbname": "arithmetic_aptitude",
    "url": "https://www.indiabix.com/aptitude/questions-and-answers/"
  },
  "VerbalAbility": {
    "dbname": "verbal_ability",
    "url": "https://www.indiabix.com/verbal-ability/questions-and-answers/"
  },
  "Logical": {
    "dbname": "logical_reasoning",
    "url": "https://www.indiabix.com/logical-reasoning/questions-and-answers/"
  },
  "VerbalReasoning": {
    "dbname": "verbal_reasoning",
    "url": "https://www.indiabix.com/verbal-reasoning/questions-and-answers/"
  },
  "C": {
    "dbname": "c_programming",
    "url": "https://www.indiabix.com/c-programming/questions-and-answers/"
  },
  "C++Programming": {
    "dbname": "cplus_programming",
    "url": "https://www.indiabix.com/cpp-programming/questions-and-answers/"
  },
  "C#Programming": {
    "dbname": "csharp_programming",
    "url": "https://www.indiabix.com/c-sharp-programming/questions-and-answers/"
  },
  "Java": {
    "dbname": "java_programming",
    "url": "https://www.indiabix.com/java-programming/questions-and-answers/"
  },
  "DatabaseSystems": {
    "dbname": "database_management_system",
    "url": "https://www.indiabix.com/database/questions-and-answers/"
  },
  "ComputerScience": {
    "dbname": "computer_science",
    "url": "https://www.indiabix.com/computer-science/questions-and-answers/"
  },
  "Networking": {
    "dbname": "networking",
    "url": "https://www.indiabix.com/networking/questions-and-answers/"
  },
  "Chemical": {
    "dbname": "chemical_engineering",
    "url": "https://www.indiabix.com/chemical-engineering/questions-and-answers/"
  },
  "Civil": {
    "dbname": "civil_engineering",
    "url": "https://www.indiabix.com/civil-engineering/questions-and-answers/"
  },
  "Electronics": {
    "dbname": "electronic_and_communication",
    "url": "https://www.indiabix.com/electronics-and-communication-engineering/questions-and-answers/"
  },
  "Basic": {
    "dbname": "basic_electronics",
    "url": "https://www.indiabix.com/electronics/questions-and-answers/"
  },
  "Digital": {
    "dbname": "digital_electronics",
    "url": "https://www.indiabix.com/digital-electronics/questions-and-answers/"
  },
  "ElectronicDevices": {
    "dbname": "electronic_devices_and_circuit_theory",
    "url": "https://www.indiabix.com/electronic-devices/questions-and-answers/"
  },
  "Electrical& Electronics": {
    "dbname": "electrical_and_electronics",
    "url": "https://www.indiabix.com/electrical-engineering/questions-and-answers/"
  },
  "Mechanical": {
    "dbname": "mechanical_engineering",
    "url": "https://www.indiabix.com/mechanical-engineering/questions-and-answers/"
  },
  "TechnicalDrawing": {
    "dbname": "technical_drawing",
    "url": "https://www.indiabix.com/technical-drawing/questions-and-answers/"
  },
  "Engineering": {
    "dbname": "engineering_mechanics",
    "url": "https://www.indiabix.com/engineering-mechanics/structural-analysis/006004"
  },
  "Microbiology": {
    "dbname": "microbiology",
    "url": "https://www.indiabix.com/microbiology/questions-and-answers/"
  },
  "Biochemistry": {
    "dbname": "biochemistry",
    "url": "https://www.indiabix.com/biochemistry/questions-and-answers/"
  },
  "Biotechnology": {
    "dbname": "biotechnology",
    "url": "https://www.indiabix.com/biotechnology/questions-and-answers/"
  },
  "Biochemical": {
    "dbname": "biochemical_engineering",
    "url": "https://www.indiabix.com/biochemical-engineering/questions-and-answers/"
  }
}

def createDatabase(databaseName):
    try:
        createDBQuery = 'CREATE DATABASE IF NOT EXISTS '+databaseName
        if cur.execute(createDBQuery):
            print databaseName+'created'
    except Exception as e:
        print e
    createTables(databaseName)

def createTables(databaseName):
    #Question Table
    try:
        questionTableQuery = "CREATE TABLE IF NOT EXISTS "+databaseName+".`question` (`question_id` INT(11) NOT NULL AUTO_INCREMENT,`group_id` INT(11) NOT NULL,`question_no` INT(11) NOT NULL,`question` VARCHAR(2000) NOT NULL,`option_A` VARCHAR(500) NOT NULL,`option_B` VARCHAR(500) NOT NULL,`option_C` VARCHAR(500) NULL DEFAULT NULL,`option_D` VARCHAR(500) NULL DEFAULT NULL,`option_E` VARCHAR(500) NULL DEFAULT NULL,`image_url` VARCHAR(200) NULL DEFAULT NULL, PRIMARY KEY (`question_id`));"
        cur.execute(questionTableQuery)
    except Exception as e:
        print e
    #Answer Table
    try:
        answerTableQuery = "CREATE TABLE IF NOT EXISTS "+databaseName+".`answer` (`answer_id` INT(11) NOT NULL AUTO_INCREMENT,`group_id` INT(11) NOT NULL,`subgroup_id` INT(11) NOT NULL,`question_no` INT(11) NOT NULL,`answer` VARCHAR(5) NOT NULL,`solution` VARCHAR(2000) NOT NULL,PRIMARY KEY (`answer_id`));"
        cur.execute(answerTableQuery)
    except Exception as e:
        print e

def dropTable(databaseName):
    try:
        dropquestionTable = "DROP TABLE IF EXISTS `"+databaseName+"`.`answer`;"
        dropAnswerTable = "DROP TABLE IF EXISTS `"+databaseName+"`.`answer`;"
        cur.execute(dropquestionTable)
        cur.execute(dropAnswerTable)
    except Exception as e:
        print e

def dropDatabase(databaseName):
    try:
        dropdatabase = "DROP DATABASE IF EXISTS "+databaseName
        cur.execute(dropdatabase)
    except Exception as e:
        print e

for i in pagesJson:
    #dropDatabase(pagesJson[i]['dbname'])
    createDatabase(pagesJson[i]['dbname'])
    print "Database " +pagesJson[i]['dbname']+"created"
