from os import abort

import numpy as np
from flask import Flask, jsonify, request
import pymysql
import datetime
import base64

app = Flask (__name__)

# conn = pymysql.connect (host="192.169.82.14", user="ahmaliic_tanveer", password="ahmaliic_tanveer", db="ahmaliic_tanveer")

conn = pymysql.connect(host="localhost", user="root", password="",db="slc")

@app.route ("/registerVolunteer", methods=['POST'])
def addVolunteer():
    # conn = pymysql.connect(host="192.169.82.14", user="ahmaliic_tanveer", password="ahmaliic_tanveer",
    #                        db="ahmaliic_tanveer")

    conn = pymysql.connect(host="localhost", user="root", password="", db="slc")

    myCursor = conn.cursor()

    data = request.json
    name = request.json['Name']
    email = request.json['Email']
    password = request.json['Password']
    city = request.json['City']
    phone = request.json['Mobile']
    image = request.json['Image']
    if not data:
        abort(400, 'No data received')

    imgdata = base64.b64decode(image)

    myCursor.execute("select * from volunteer order by id desc limit 1")
    rows = myCursor.fetchall()

    locationforeignKey = 0;
    for j in rows:
        locationforeignKey = j[0]

    filename = 'Volunteer/' + str(locationforeignKey + 1) + '.jpg'
    print(filename)
    with open(filename, 'wb') as f:
        f.write(imgdata)

    sql = "insert into volunteer (name, email, password, city, phone,image) values (%s,%s,%s,%s,%s,%s)"
    myCursor.execute (sql,(name,email,password,city,phone,image))
    conn.commit()
    myCursor.close()

    return jsonify({'Response': "new"})

@app.route ("/authorizeVolunteer", methods=['GET'])
def sendVolunteers():
    # conn = pymysql.connect(host="192.169.82.14", user="ahmaliic_tanveer", password="ahmaliic_tanveer",
    #                        db="ahmaliic_tanveer")

    conn = pymysql.connect(host="localhost", user="root", password="", db="slc")

    volunteerList = []
    myCursor = conn.cursor()
    try:
        myCursor.execute ("select * from volunteer")
        rows = myCursor.fetchall ()


        for i in rows:
        #    imgdata = base64.b64encode(i[6])

            volunteerDictionary = {
                'Id':i[0],
                'Name':i[1],
                'Email':i[2],
                'Password':i[3],
                'City':i[4],
                'Mobile':i[5],
                'Image':i[6]
            }
            volunteerList.append(volunteerDictionary)
        myCursor.close()
        conn.close()

    except:
        import sys
        print("error", sys.exc_info()[0])
        myCursor.close()


    return jsonify(volunteerList)


@app.route ("/updateVolunteer", methods=['POST'])
def updateVolunteer():
    # conn = pymysql.connect(host="192.169.82.14", user="ahmaliic_tanveer", password="ahmaliic_tanveer",
    #                        db="ahmaliic_tanveer")
    conn = pymysql.connect(host="localhost", user="root", password="", db="slc")

    myCursor = conn.cursor()

    data = request.json

    id = request.json['Id']
    name = request.json['Name']
    email = request.json['Email']
    password = request.json['Password']
    city = request.json['City']
    phone = request.json['Mobile']
    image = request.json['Image']

    if not data:
        abort(400, 'No data received')

    imgdata = base64.b64decode(image)

    filename = 'Volunteer/' + str(id) + '.jpg'
    print(filename)
    with open(filename, 'wb') as f:
        f.write(imgdata)


    sql = "update volunteer set name = %s , email = %s, password = %s, city = %s, phone = %s,image = %s where id ="+ str(id);
    myCursor.execute(sql, (name, email, password, city, phone, image))
    conn.commit()
    myCursor.close()

    return jsonify({'Response': "Successfull"})

@app.route ("/getVictimsHistory", methods=['GET'])
def getVictimsHistory():
    # conn = pymysql.connect(host="192.169.82.14", user="ahmaliic_tanveer", password="ahmaliic_tanveer",
    #                        db="ahmaliic_tanveer")

    conn = pymysql.connect(host="localhost", user="root", password="",db="slc")

    missedVictims=[]

    myCursor = conn.cursor()

    try:
        myCursor.execute("select * from searched_victims")
        rows1 = myCursor.fetchall()

        for i in rows1:
            query = "select victim.date,victim.time,victim.path,victim.type,location.address,volunteer.name from search_history join victim on search_history.victimId = victim.id join victim_location on victim.id = victim_location.victimId join location on victim_location.locationId = location.id join volunteer on "+str(i[1])+" = volunteer.id where search_history.id="+str(i[2])
            myCursor.execute(query)
            rows2 = myCursor.fetchall()
            for j in rows2:
                victimsDictionary = {
                'Date': j[0],
                'Time': j[1],
                'Path': j[2],
                'VictimType': j[3],
                'Address': j[4],
                'VolunteerName': j[5]
                 }
                missedVictims.append(victimsDictionary)
        myCursor.close()
        conn.close()

    except:
        import sys
        print("error", sys.exc_info()[0])
        myCursor.close()


    return jsonify(missedVictims)



@app.route ("/getRecoveredVictims", methods=['GET'])
def getRecoveredVictims():
    # conn = pymysql.connect(host="192.169.82.14", user="ahmaliic_tanveer", password="ahmaliic_tanveer",
    #                        db="ahmaliic_tanveer")

    conn = pymysql.connect(host="localhost", user="root", password="",db="slc")

    missedVictims=[]

    myCursor = conn.cursor()

    try:
        myCursor.execute("select * from victim")
        rows1 = myCursor.fetchall()
        victimIds=[]
        for i in rows1:
            if(i[5]=="recovered"):
                victimIds.append(i[0])
        for s in victimIds:
            query = "select victim.date,victim.time,victim.path,location.address,volunteer.name from victim join victim_location on victim.id = victim_location.victimId join location on victim_location.locationId = location.id join added_victims on victim.id = added_victims.victimId join volunteer on added_victims.volunteerId = volunteer.id  where victim.id="+str(s)

            myCursor.execute(query)
            rows2 = myCursor.fetchall()
            print(rows2)
            for j in rows2:
                print(j[0])
                victimsDictionary = {
                'Date': j[0],
                'Time': j[1],
                'Path': j[2],
                'Address': j[3],
                'VolunteerName': j[4]
                 }
                missedVictims.append(victimsDictionary)
        myCursor.close()
        conn.close()

    except:
        import sys
        print("error", sys.exc_info()[0])
        myCursor.close()


    return jsonify(missedVictims)




@app.route ("/saveRequest", methods=['POST'])
def saveRequest():
    # conn = pymysql.connect(host="192.169.82.14", user="ahmaliic_tanveer", password="ahmaliic_tanveer",
    #                        db="ahmaliic_tanveer")

    conn = pymysql.connect(host="localhost", user="root", password="", db="slc")

    myCursor = conn.cursor()

    data = request.json

    image = request.json['Image']
    id = request.json['VolunteerId']
    date = request.json['Date']
    type = request.json['Type']
    time = request.json['Time']
    lattitude = request.json['Lattitude']
    address = request.json['Address']

    if not data:
        abort(400, 'No data received')

    myCursor.execute("select * from victim order by id desc limit 1")
    rows = myCursor.fetchall()

    locationforeignKey = 0;
    for j in rows:
        locationforeignKey = j[0]

    imgdata = base64.b64decode(image)
    filename='History/'+str(locationforeignKey+1)+ '.jpg'
    #filename = 'Pictures/2.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)

    from face_match_demo import getFace
    import cv2
    img1 = cv2.imread(filename)
    face = getFace(img1)

    points = np.matrix
    points = face[0]['embedding']
    pointsToString = str(points)
    #print(pointsToString)

    sql = "insert into victim (date, time, path, points,type) values (%s,%s,%s,%s,%s)"
    sql1 = "insert into location (lattitude, address) values (%s,%s)"
    myCursor.execute(sql, (date, time,image,pointsToString,type))
    myCursor.execute(sql1, (lattitude, address))

    myCursor.execute("select * from victim order by id desc limit 1")
    rows = myCursor.fetchall()
    victimforeignKey = 0;
    for i in rows:
        victimforeignKey = i[0]

    myCursor.execute("select * from location order by id desc limit 1")
    rows = myCursor.fetchall()

    locationforeignKey = 0;
    for j in rows:
        locationforeignKey = j[0]

    sql2 = "insert into victim_location (victimId, locationId) values (%s,%s)"
    sql3 = "insert into search_history (victimId) values (%s)"

    myCursor.execute(sql2, (victimforeignKey, locationforeignKey))
    myCursor.execute(sql3, (victimforeignKey))

    myCursor.execute("select * from search_history order by id desc limit 1")
    rowss = myCursor.fetchall()

    historyforeignKey = 0;
    for j in rowss:
        historyforeignKey = j[0]

    sql3 = "insert into searched_victims (volunteerId,searchHistoryId) values (%s,%s)"

    myCursor.execute(sql3, (id, historyforeignKey))

    conn.commit()

    myCursor.close()

    return jsonify({'Response': "Successfull"})


@app.route ("/addVictim", methods=['POST'])
def addVictim():
    global generateMessageVictimId;
    notificationList= {}
    if request.method == 'POST':
        global locationforeignKey

        # conn = pymysql.connect(host="192.169.82.14", user="ahmaliic_tanveer", password="ahmaliic_tanveer",
        #                        db="ahmaliic_tanveer")
        conn = pymysql.connect(host="localhost", user="root", password="", db="slc")

        myCursor = conn.cursor()


        now = datetime.datetime.now()

        data = request.json
        if not data:
            abort(400, 'No data received')


        image = request.json['Image']
        id = request.json['VolunteerId']
        date = request.json['Date']
        type = request.json['Type']
        time = request.json['Time']
        lattitude = request.json['Lattitude']
        address = request.json['Address']
        imgdata = base64.b64decode(image)

        myCursor.execute("select * from victim order by id desc limit 1")
        rows = myCursor.fetchall()

        locationforeignKey = 0;
        for j in rows:
            locationforeignKey = j[0]

        filename = 'Record/'+str(locationforeignKey+1)+ '.jpg'
        print(filename)
        with open(filename, 'wb') as f:
            f.write(imgdata)


        from face_match_demo import getFace
      #  from other_matching_model import getFace as g
        from face_match_demo import detect_face
        from face_match_demo import getEmbedding
        import face_match_demo
        import cv2
        #
        #
        img1 = cv2.imread(filename)
        face = getFace(img1)
        #
        if face:
            points = np.matrix
            points = face[0]['embedding']
            #print(points)
            pointsToString = str(points)

            sql = "insert into victim (date, time, path, points,type) values (%s,%s,%s,%s,%s)"
            sql1 = "insert into location (lattitude, address) values (%s,%s)"

            myCursor.execute(sql, (date, time,image,pointsToString,type))
            myCursor.execute(sql1, (lattitude, address))

            myCursor.execute("select * from victim order by id desc limit 1")
            rows = myCursor.fetchall()
            victimforeignKey=0;
            for i in rows:
                victimforeignKey=i[0]

            myCursor.execute("select * from location order by id desc limit 1")
            rows = myCursor.fetchall()

            locationforeignKey = 0;
            for j in rows:
                locationforeignKey = j[0]

            sql2 = "insert into victim_location (victimId, locationId) values (%s,%s)"
            sql3 = "insert into added_victims (volunteerId, victimId) values (%s,%s)"

            myCursor.execute(sql2, (victimforeignKey, locationforeignKey))
            myCursor.execute(sql3, (id, victimforeignKey))

            #
            missedVictims=[]
            myCursor.execute("select * from search_history")
            rows = myCursor.fetchall()
            for i in rows:
                missedVictims.append(i[1])


            for j in missedVictims:
                myCursor.execute("select * from victim where id = " + str(j))
                rows1 = myCursor.fetchall()
                for k in rows1:

                    if(k[5]=="searched"):
                        matrix = np.matrix
                        matrix = np.matrix(k[4])
                        dist = np.sqrt(np.sum(np.square(np.subtract(points, matrix))))
                        if dist <= 1.10:
                            print("Generate message to ")
                            #print(k[0])
                            query = "select victim.date,victim.time,victim.path,location.address,volunteer.name,volunteer.phone from search_history join victim on search_history.victimId = victim.id join victim_location on victim.id = victim_location.victimId join location on victim_location.locationId = location.id join searched_victims on search_history.id = searched_victims.searchHistoryId join volunteer on searched_victims.volunteerId = volunteer.id   where search_history.victimId = " + str(k[0])
                         #   myCursor.execute("select victim.date,victim.time,victim.path,location.address,volunteer.name, volunteer.phone from search_history join searched_victims on search_history.id = searched_victims.searchHistoryId join volunteer on searched_victims.volunteerId = volunteer.id   where victimId = " + str(k[0]))
                            myCursor.execute(query)
                            rows2 = myCursor.fetchall()
                            for l in rows2:
                                # print(l[0])
                                # print(l[1])
                              #  print(l[2])
                              #   print(l[3])
                              #   print(l[4])
                              #   print(l[5])

                                myCursor.execute("select * from volunteer where id = "+str(id))
                                rows5=myCursor.fetchall()
                                uploadedName=''
                                uploadedPhone=""
                                for x in rows5:
                                    uploadedName = x[1]
                                    uploadedPhone=x[5]

                                generateMessageVictimId=k[0]
                                print(l[5]+'\n'+l[4]+'\n'+'Missed Child Id: '+str(k[0])+'\n'+'Current Location: '+address+ '\n' +'Current date: '+date+'\n'+'Current Time: '+ time+'\n'+'Added by: '+ uploadedName)

                                notificationList={
                                    'Date': date,
                                    'Time': time,
                                    'Path': l[2],
                                    'Address': address,
                                    'VolunteerName': l[4],
                                    'VolunteerPhone': l[5],
                                    'UploadedName':uploadedName,
                                    'UploadedPhone':uploadedPhone
                                }
            conn.commit()

            if(bool(notificationList)):
                sql = "update victim set date = %s,time = %s, type = %s where id =" + str(generateMessageVictimId);
                myCursor.execute(sql, (date,time,"recovered"))



                # sql2 = "select volunteer.id from search_history join searched_victims on search_history.id searched_victims.searchHistoryId join volunteer on searched_victims.volunteerId = volunteer.id where victimId = "+str(generateMessageVictimId);
                # myCursor.execute(sql2)
                # r = myCursor.fetchall()
                # searchedVolunteerId ="";
                # for k in r:
                #     searchedVolunteerId=str(k[0])


                conn.commit()

                myCursor.close()

                return jsonify({'Response': '2','Message': 'Generate Notification','data':notificationList})
            else:
                return jsonify({'Response': '1','Message': 'Successfull','data':notificationList})
        else:
             return jsonify({'Response': '0','Message': 'Invalid Image','data':notificationList})




@app.route ("/searchVictim", methods=['POST','GET'])
def searchVictim():
    conn = pymysql.connect(host="localhost", user="root", password="", db="slc")

    # conn = pymysql.connect(host="192.169.82.14", user="ahmaliic_tanveer", password="ahmaliic_tanveer",
    #                        db="ahmaliic_tanveer")

    myCursor = conn.cursor()

    now = datetime.datetime.now()

    data = request.json
    image = request.json['Image']

    if not data:
        abort(400, 'No data received')

    matchedVictims = []




    imgdata = base64.b64decode(image)

    myCursor.execute("select * from victim order by id desc limit 1")
    rows = myCursor.fetchall()

    locationforeignKey = 0;
    for j in rows:
        locationforeignKey = j[0]

    filename = 'Searched/' + str(locationforeignKey + 1) + '.jpg'
    print(filename)
    with open(filename, 'wb') as f:
        f.write(imgdata)

    from face_match_demo import getFace
    from face_match_demo import detect_face
    from face_match_demo import getEmbedding
    import face_match_demo
    import cv2

    img1 = cv2.imread(filename)
    face = getFace(img1)
    if face:
        points = np.matrix
        points = face[0]['embedding']
        myCursor.execute("select * from victim")
        rows = myCursor.fetchall()

        victimIds = []
        matchingVictimIds=[]

        for i in rows:
            if(i[5]=="begging"):
                victimIds.append(i[0])

        for j in victimIds:
            myCursor.execute("select * from victim where id = " + str(j))
            rows1 = myCursor.fetchall()
            for k in rows1:
                matrix = np.matrix
                matrix=np.matrix(k[4])
                dist = np.sqrt(np.sum(np.square(np.subtract(points, matrix))))


                if dist <= 1.10:
                    matchingVictimIds.append(k[0])
                    print(dist)
                    print(k[0])
                    query = "select victim.date,victim.time,victim.path,location.address,location.lattitude,volunteer.name from victim join victim_location on victim.id = victim_location.victimId join location on victim_location.locationId = location.id join added_victims on victim.id = added_victims.victimId join volunteer on added_victims.volunteerId = volunteer.id where victim.id = "+ str(k[0])
                    myCursor.execute(query)
                    rows2 = myCursor.fetchall()
                    for x in rows2:
                        print(x[0])
                        print(x[1])
                        print(x[3])
                        print(x[4])

                        victimsDictionary = {
                            'Date': x[0],
                            'Time': x[1],
                            'Image': x[2],
                            'Address': x[3],
                            'Lattitude': x[4],
                            'VolunteerName': x[5]
                        }
                        matchedVictims.append(victimsDictionary)


        # imgdata = base64.b64decode(image)
        # filename = 'Images/SLC_'+str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+'.jpg'
        # with open(filename, 'wb') as f:
        #     f.write(imgdata)


        conn.commit()

        myCursor.close()
        if not matchedVictims:
            return jsonify({'Response': 0, 'Message': 'No Data Found', 'data': matchedVictims})
        else:
            return jsonify({'Response': 1, 'Message': 'Data Found', 'data':matchedVictims})

    else:
        return jsonify({'Response': 2, 'Message': 'Invalid Image', 'data': matchedVictims})





if __name__ == '__main__':
    app.run (host="192.168.42.65",debug=True)


