import smtplib,requests,bs4,mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

if(True):
    print("Program started")
    mydb=mysql.connector.connect(host="localhost",user="root",password="",database="user")
    
    r=requests.get("http://mmmut.ac.in/")
    r.raise_for_status()
    mySoup=bs4.BeautifulSoup(r.text,features="html.parser")
    elems=mySoup.select('#ctl00_DataList1 span')
    elemText=[]
    for x in elems:
        if(x.span):
            if(x.a):
                elemText.append([(x.span.string),(x.a.get('href'))])
            else:
                elemText.append([(x.span.string),''])

		
    mycursor=mydb.cursor()
    mycursor.execute("select * from data")
    res=mycursor.fetchall()
    res_set=set()
    for x in res:
        res_set.add(x[0])
    for elem in elemText:
        if(elem[0] not in res_set):
            s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security 
            s.starttls() 
# Authentication 
            s.login("sender_gmail_id", "password")
            text="New Notice-> "+elem[0]
            html="<h3>New Notice-> </h3><h4>"+elem[0]+"</h4>"
            if(elem[1]!=''):
                if('http' in elem[1]):
                    html+='<br/><h4><a href="'+elem[1]+'">Click here</a> to download.</h4>'
                else:
                    html+='<br/><h4><a href="'+'http://mmmut.ac.in/'+elem[1]+'">Click here</a> to download.</h4>'

            mycursor.execute("select * from emailList");
            emaillist=mycursor.fetchall()
            for i in emaillist:
                message = MIMEMultipart("alternative")
                message["Subject"] = "New Notice on mmmut.ac.in"
                message["From"] = "sender_gmail_id"
                part1 = MIMEText(text, "plain")
                part2 = MIMEText(html, "html")
                message["To"] =i[0]
                message.attach(part1)
                message.attach(part2)
                s.sendmail("sender_gmail_id",i[0], message.as_string())
            print(elem[0])
            s.quit()
    if(len(elemText)):
        mycursor.execute("truncate table data")
        mycursor.execute("commit")
    for elem in elemText:
        sqlString='insert into data values("'+elem[0]+'")'
        mycursor.execute(sqlString)
        mycursor.execute("commit")
    


    
    elems=mySoup.select('#ctl00_DataList2 span')
    elemText=[]
    for x in elems:
        if(x.span):
            if(x.a):
                elemText.append([(x.span.string),(x.a.get('href'))])
            else:
                elemText.append([(x.span.string),''])
    
    
    mycursor=mydb.cursor()
    mycursor.execute("select * from notice")
    res=mycursor.fetchall()
    res_set=set()
    for x in res:
        res_set.add(x[0])
    
    for elem in elemText:
        if(elem[0] not in res_set):
            s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security 
            s.starttls() 
# Authentication 
            s.login("sender_gmail_id", "password")
            text="New Notice-> "+elem[0]
            html="<h3>New Notice-> </h3><h4>"+elem[0]+"</h4>"
            if(elem[1]!=''):
                if('http' in elem[1]):
                    html+='<br/><h4><a href="'+elem[1]+'">Click here</a> to download.</h4>'
                else:
                    html+='<br/><h4><a href="'+'http://mmmut.ac.in/'+elem[1]+'">Click here</a> to download.</h4>'

            mycursor.execute("select * from emailList");
            emaillist=mycursor.fetchall()
            for i in emaillist:
                message = MIMEMultipart("alternative")
                message["Subject"] = "New Notice on mmmut.ac.in"
                message["From"] = "sender_gmail_id"
                part1 = MIMEText(text, "plain")
                part2 = MIMEText(html, "html")
                message["To"] =i[0]
                message.attach(part1)
                message.attach(part2)
                s.sendmail("sender_gmail_id",i[0], message.as_string())
            print(elem[0])
            s.quit()
    if(len(elemText)):
        mycursor.execute("truncate table notice")
        mycursor.execute("commit")
    for elem in elemText:
        sqlString='insert into notice values("'+elem[0]+'")'
        mycursor.execute(sqlString)
        mycursor.execute("commit")
print("Ended")

