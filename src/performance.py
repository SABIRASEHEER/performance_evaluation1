from flask import *
from src.dbconnectionnew import *
from src.emotion import sentiment_score
from src.codep import predict_senti
app = Flask( __name__)
app.secret_key='ffff'
@app.route('/')
def login():
    return render_template('LOGIN.html')

@app.route('/addhr',methods=['post','get'])
def addhr():
    return render_template('ADMIN/ADD_HR.html')

@app.route('/home')
def home():
    return render_template('ADMIN/HOME.html')

@app.route('/managehr')
def managehr():
    qry="SELECT * FROM `hr`"
    res=selectall(qry)
    return render_template('ADMIN/MANAGE_HR.html',val=res)

@app.route('/edithr')
def edithr():
    id = request.args.get('id')
    session['hid'] = id
    qry ="select * from hr where hid=%s"
    res = selectone(qry,id)
    return render_template('ADMIN/edit_hr.html',val=res)

@app.route('/edithr1',methods=['post','get'])
def edithr1():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    email = request.form['textfield6']
    phone = request.form['textfield7']
    gender = request.form['radiobutton']
    qry = "UPDATE hr SET first_name=%s,last_name=%s,place=%s,post=%s,pin=%s,email=%s,phone=%s,gender=%s where hid=%s"
    val = (fname, lname, place, post, pin, email, phone, gender,session['hid'])
    iud(qry, val)
    return '''<script>alert("edited");window.location='/managehr'</script>'''

@app.route('/deletehr')
def deletehr():
    id = request.args.get('id')
    qry = "DELETE FROM `login` WHERE `l_id`=%s"
    iud(qry, id)
    qry1 = "DELETE FROM `hr` WHERE `lid`=%s"
    iud(qry1, id)
    return '''<script> alert ("Deleted");window.location="/managehr"</script>'''

@app.route('/hrreg',methods=['post','get'])
def hrreg():

    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    email = request.form['textfield6']
    phone = request.form['textfield7']
    username = request.form['textfield8']
    password = request.form['textfield9']
    gender = request.form['radiobutton']
    qry="INSERT INTO `login` VALUES(null,%s,%s,'hr')"
    val=(username,password)
    id=iud(qry,val)
    qry="insert into hr values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(str(id),fname,lname,place,post,pin,email,phone,gender)
    iud(qry,val)
    return '''<script>alert("Added");window.location='/managehr'</script>'''

@app.route('/notification',methods=['post','get'])
def notification():
    return render_template('ADMIN/SEND_NOTIFICATION.html')

@app.route('/sendnot',methods=['post','get'])
def sendnot():
    notification = request.form['textarea']
    qry = "insert into notification values(null,%s,curdate())"
    val=(notification)
    iud(qry,val)
    return '''<script>alert("sended");window.location='/notification'</script>'''

@app.route('/reply')
def reply():
    id=request.args.get('id')
    session['cid']=id
    return render_template('ADMIN/SEND_REPLY.html')
@app.route('/reply1',methods=['post'])
def reply1():
   reply=request.form['textarea']
   q="UPDATE `complaint` SET `reply`=%s WHERE `cid`=%s"
   iud(q,(reply,session['cid']))
   return '''<script>alert("reply sended");window.location='viewcomplaint'</script>'''

@app.route('/viewcomplaint')
def viewcomplaint():
    qry="SELECT complaint.*, tm.* FROM complaint JOIN tm ON complaint.lid=tm.lid WHERE complaint.reply='pending' "
    res=selectall(qry)
    return render_template('ADMIN/VIEW_COMPLAINT.html',val=res)

@app.route('/viewperformance1')
def viewperformance1():
    return render_template('ADMIN/view_performance.html')

@app.route('/viewperformance_search',methods=['post'])
def viewperformance_search():
    print(request.form)
    ty=request.form['select']
    fd=request.form['textfield']
    td=request.form['textfield2']
    if ty=="TEAM MEMBER":
        qry="SELECT AVG(`score`) AS scr,`first_name`,`last_name` FROM `tm` JOIN `assign_tm` ON `assign_tm`.`tm_id`=`tm`.`lid` JOIN `report` ON `report`.`wid`=`assign_tm`.`a_tm_id` JOIN `feedback` ON `feedback`.`rid`=`report`.`rid` WHERE `report`.`type`='tm' AND `report`.`date` BETWEEN % s AND % s GROUP BY `tm`.`lid`"
        res=selectall2(qry,(fd,td))
        result=[]
        for i in res:
            if float(i['scr'])>4:
                i['p']="excelent"
            elif float(i['scr']) >3:
                i['p'] = "good"
            elif float(i['scr']) > 2:
                i['p'] = "avarage"
            elif float(i['scr']) > 1:
                i['p'] = "bad"
            else:
                i['p'] = "poor"
            result.append(i)
        return render_template('ADMIN/view_performance.html',val=result)
    else:
        qry = "SELECT AVG(`score`) AS scr,`first_name`,`last_name` FROM `tl` JOIN `assign_tl` ON `assign_tl`.`tl_id`=`tl`.`lid` JOIN `report` ON `report`.`wid`=`assign_tl`.`wid` JOIN `feedback_tl` ON `feedback_tl`.`rid`=`report`.`rid` WHERE `report`.`type`='tl'  AND `report`.`date` BETWEEN %s AND %s GROUP BY `tl`.`lid`"
        res = selectall2(qry, (fd, td))
        result = []
        for i in res:
            if float(i['scr']) > 4:
                i['p'] = "excelent"
            elif float(i['scr']) > 3:
                i['p'] = "good"
            elif float(i['scr']) > 2:
                i['p'] = "avarage"
            elif float(i['scr']) > 1:
                i['p'] = "bad"
            else:
                i['p'] = "poor"
            result.append(i)
        return render_template('ADMIN/view_performance.html', val=result,d1=str(fd),d2=str(td))

@app.route('/viewwork')
def viewwork():
    qry="SELECT hr.*,work.* FROM hr JOIN WORK ON hr.hid=work.hid"
    res=selectall(qry)
    return render_template('ADMIN/VIEW_WORK.html',val=res)

@app.route('/viewworkreport')
def viewworkreport():
    # qry="SELECT hr.*,work.* FROM hr JOIN WORK ON hr.hid=work.hid"
    # res=selectall(qry)
    return render_template('ADMIN/view_work_report.html')

@app.route('/searchbytype',methods=['post','get'])
def searchbytype():
    type=request.form['select']
    if type == 'TEAM LEADER':
        qry="SELECT tl.first_name,tl.last_name,work.work,report.* FROM `tl` JOIN `assign_tl` ON `assign_tl`.`tl_id`=`tl`.`lid` JOIN `work`ON `assign_tl`.`wid`=`work`.`wid` JOIN `report` ON `report`.`wid`=`work`.`wid` group by report.rid"
        res=selectall(qry)
        return render_template('ADMIN/view_work_report.html',val=res)
    else:
        qry = "SELECT tm.first_name,tm.last_name,work.work,report.* FROM `tm` JOIN `assign_tm` ON `assign_tm`.`tm_id`=`tm`.`lid` JOIN `work`ON `assign_tm`.`wid`=`work`.`wid` JOIN `report` ON `report`.`wid`=`work`.`wid` group by report.rid"
        res = selectall(qry)
        return render_template('ADMIN/view_work_report.html', val=res)


@app.route('/addattendance1')
def addattendance1():
    q="SELECT * FROM `tl` WHERE `hid`=%s"
    res=selectall2(q,session['lid'])
    return render_template('HR/add_attendance.html',val=res)

@app.route('/add_attendance1',methods=['post','get'])
def add_attendance1():
    leader = request.form['select']
    intime= request.form['textfield']
    outtime = request.form['textfield2']
    date = request.form['textfield3']
    attendance = request.form['radiobutton']
    qry="INSERT INTO attendance VALUES(NULL,%s,%s,%s,%s,%s)"
    val=(attendance,leader,date,intime,outtime)
    iud(qry,val)
    return'''<script>alert("atendance marked");window.location='/addattendance1'</script>'''


@app.route('/addfeedback')
def addfeedback():
    session['rid']=request.args.get('id')

    return render_template('HR/add_feedback.html')

@app.route('/add_feedback',methods=['post','get'])
def add_feedback():
    feedback=request.form['textarea']
    s=sentiment_score(feedback)
    s=predict_senti(feedback)[1]
    qry="INSERT INTO feedback_tl VALUES(NULL,%s,%s,%s,CURDATE())"
    val=(session['rid'],feedback,s)
    iud(qry,val)
    return '''<script>alert('added');window.location='/addfeedback'</script>'''


@app.route('/addtl',methods=['post','get'])
def addtl():
    return render_template('HR/add_tl.html')

@app.route('/add_tl',methods=['post','get'])
def add_tl():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    email = request.form['textfield6']
    phone = request.form['textfield7']
    username = request.form['textfield8']
    password = request.form['textfield9']
    gender = request.form['radiobutton']
    qry = "INSERT INTO `login` VALUES(null,%s,%s,'team_leader')"
    val = (username, password)
    id = iud(qry, val)
    qry = "insert into tl values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (str(id),session['lid'], fname, lname, place, post, pin, email, phone, gender)
    iud(qry, val)
    return '''<script>alert("Added");window.location='/viewtl'</script>'''


@app.route('/addwork',methods=['post'])
def addwork():
    return render_template('HR/add_work.html')


@app.route('/addwork1',methods=['get','post'])
def addwork1():
    work = request.form['textfield']
    dateofsub = request.form['textfield2']
    qry="INSERT INTO WORK VALUES(NULL,%s,CURDATE(),%s,'pending',%s)"
    val=(work,session['lid'],dateofsub)
    iud(qry,val)
    return '''<script>alert("added");window.location='/addwork'</script>'''

@app.route('/assigntl')
def assigntl():
    qry="select * from work where hid=%s"
    res=selectall2(qry,session['lid'])
    qry1="select * from tl "
    res1=selectall(qry1)
    return render_template('HR/assign_tl.html',val=res,val1=res1)

@app.route('/assigntl1',methods=['post','get'])
def assigntl1():
    work=request.form['select']
    tl=request.form['select2']
    qry="INSERT INTO assign_tl VALUES(NULL,%s,%s,CURDATE(),'pending')"
    val=(work,tl)
    iud(qry,val)
    return '''<script>alert("added");window.location='/assigntl'</script>'''


@app.route('/attendancetl')
def attendancetl():
    qry="SELECT COUNT(*) AS twd,SUM(`attendance`) AS tpd,(SUM(`attendance`)/COUNT(*))*100 AS per,`tl`.`first_name`,`last_name` FROM `tl` JOIN `attendance` ON `attendance`.`lid`=`tl`.`lid` GROUP BY `tl`.`lid` "
    res=selectall(qry)
    return render_template('HR/attendance_tl.html',val=res)

@app.route('/blocktl')
def blocktl():
    qry="SELECT login.*,tl.* FROM login JOIN tl ON login.l_id=`tl`.`lid`"
    res=selectall(qry)
    return render_template('HR/block_tl.html',val=res)

@app.route('/blocktl1')
def blocktl1():
    id=request.args.get('id')
    qry="update login set type='blocked' where l_id=%s"
    iud(qry,id)
    return '''<script>alert('blocked');window.location='/blocktl'</script>'''

@app.route('/unblock')
def unblock():
    id = request.args.get('id')
    qry = "update login set type='team_leader' where l_id=%s"
    iud(qry, id)
    return '''<script>alert('unblocked');window.location='/blocktl'</script>'''

@app.route('/home1')
def home1():
    return render_template('hr_index.html')

@app.route('/managework')
def managework():
    qry="select * from work where hid=%s"
    res=selectall2(qry,session['lid'])
    return render_template('HR/manage_work.html',val=res)

@app.route('/editwork')
def editwork():
    id = request.args.get('id')
    session['wid'] = id
    qry = "select * from work where wid=%s"
    res = selectone(qry, id)
    return render_template('HR/editwork.html',val=res)

@app.route('/edit_work',methods=['post'])
def edit_work():
    work = request.form['textfield']
    dateofsub = request.form['textfield2']
    qry = "UPDATE WORK SET `work`=%s,`submission_date`=%s WHERE wid=%s"
    val = (work, dateofsub,session['wid'])
    iud(qry, val)
    return '''<script>alert("updated");window.location='/managework'</script>'''

@app.route('/deletework')
def deletework():
    id = request.args.get('id')
    qry = "DELETE FROM `work` WHERE `wid`=%s"
    iud(qry, id)
    return '''<script> alert ("Deleted");window.location="/managework"</script>'''

@app.route('/updatehr')
def updatehr():
    qry="SELECT * FROM hr WHERE `lid`=%s"
    res=selectone(qry,session['lid'])
    return render_template('HR/update_hr.html',val=res)

@app.route('/updateprofile', methods=['post', 'get'])
def updateprofile():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    email = request.form['textfield6']
    phone = request.form['textfield7']
    gender=request.form['radiobutton']
    qry = "UPDATE hr SET first_name=%s,last_name=%s,place=%s,post=%s,pin=%s,email=%s,phone=%s,gender=%s WHERE lid=%s"
    val = ( fname, lname, place, post, pin, email, phone, gender,session['lid'])
    iud(qry, val)
    return '''<script>alert("updated");window.location='/updatehr'</script>'''

@app.route('/viewnot1')
def viewnot1():
    qry="select * from notification"
    res=selectall(qry)
    return render_template('HR/view_not.html',val=res)

@app.route('/viewperformance2')
def viewperformance2():
    return render_template('HR/view_performance.html')

@app.route('/viewperformance_search1',methods=['post'])
def viewperformance_search1():
    print(request.form)
    ty=request.form['select']
    fd=request.form['textfield']
    td=request.form['textfield2']
    if ty=="TEAM MEMBER":
        qry="SELECT AVG(`score`) AS scr,`first_name`,`last_name` FROM `tm` JOIN `assign_tm` ON `assign_tm`.`tm_id`=`tm`.`lid` JOIN `report` ON `report`.`wid`=`assign_tm`.`a_tm_id` JOIN `feedback` ON `feedback`.`rid`=`report`.`rid` WHERE `report`.`type`='tm' AND `report`.`date` BETWEEN %s AND %s AND `tm`.`lid` IN(SELECT `lid` FROM `tm` WHERE `tl_id` IN(SELECT `lid` FROM `tl` WHERE `hid`=%s)) GROUP BY `tm`.`lid`"
        res=selectall2(qry,(fd,td,session['lid']))
        result=[]
        for i in res:
            if float(i['scr'])>4:
                i['p']="excelent"
            elif float(i['scr']) >3:
                i['p'] = "good"
            elif float(i['scr']) > 2:
                i['p'] = "avarage"
            elif float(i['scr']) > 1:
                i['p'] = "bad"
            else:
                i['p'] = "poor"
            result.append(i)
        return render_template('HR/view_performance.html',val=result)
    else:
        qry = "SELECT AVG(`score`) AS scr,`first_name`,`last_name` FROM `tl` JOIN `assign_tl` ON `assign_tl`.`tl_id`=`tl`.`lid` JOIN `report` ON `report`.`wid`=`assign_tl`.`wid` JOIN `feedback_tl` ON `feedback_tl`.`rid`=`report`.`rid` WHERE `report`.`type`='tl'  AND `report`.`date`  BETWEEN %s AND %s AND `tl`.`lid` IN (SELECT `lid` FROM `tl` WHERE `hid`=%s) GROUP BY `tl`.`lid`"
        res = selectall2(qry, (fd, td,session['lid']))
        result = []
        for i in res:
            if float(i['scr']) > 4:
                i['p'] = "excelent"
            elif float(i['scr']) > 3:
                i['p'] = "good"
            elif float(i['scr']) > 2:
                i['p'] = "avarage"
            elif float(i['scr']) > 1:
                i['p'] = "bad"
            else:
                i['p'] = "poor"
            result.append(i)
        return render_template('ADMIN/view_performance.html', val=result,d1=str(fd),d2=str(td))

@app.route('/viewreport')
def viewreport():
    qry="SELECT tl.*,assign_tl.`wid`,report.*,work.* FROM `work` JOIN `report` ON `report`.`wid`=`work`.`wid` JOIN `assign_tl` ON `assign_tl`.`wid`=`work`.`wid` JOIN `tl` ON `tl`.`lid`=`assign_tl`.`tl_id` WHERE `tl`.`hid`=%s"
    res=selectall2(qry,session['lid'])
    return render_template('HR/view_report.html',val=res)

@app.route('/viewtl')
def viewtl():
    qry="select * from tl"
    res=selectall(qry)
    return render_template('HR/view_tl.html',val=res)

@app.route('/delete_tl')
def delete_tl():
    id=request.args.get('id')
    qry="DELETE FROM `login` WHERE `l_id`=%s"
    iud(qry,id)
    qry1="DELETE FROM `tl` WHERE `lid`=%s"
    iud(qry1,id)
    return '''<script> alert ("Deleted");window.location="/viewtl"</script>'''

@app.route('/edit_tl')
def edit_tl():
    id = request.args.get('id')
    session['tl_id'] = id
    qry = "select * from tl where lid=%s"
    res = selectone(qry, id)
    # print(res,"OOOOOOOOO")
    return render_template('HR/edit_tl.html',val=res)

@app.route('/edittl',methods=['post'])
def edittl():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    email = request.form['textfield6']
    phone = request.form['textfield7']
    gender = request.form['radiobutton']
    qry = "UPDATE tl SET first_name=%s,last_name=%s,place=%s,post=%s,pin=%s,email=%s,phone=%s,gender=%s where lid=%s"
    val = (fname, lname, place, post, pin, email, phone, gender, session['tl_id'])
    iud(qry, val)
    return '''<script>alert("edited");window.location='/viewtl'</script>'''

@app.route('/addattendance2')
def addattendance2():
    q="SELECT * FROM `tm` WHERE `tl_id`=%s"
    res=selectall2(q,session['lid'])
    return render_template('TL/add_attendance.html',val=res)

@app.route('/add_attendance2',methods=['post','get'])
def add_attendance2():
    member = request.form['select']
    intime= request.form['textfield']
    outtime = request.form['textfield2']
    date = request.form['textfield3']
    attendance = request.form['radiobutton']
    qry="INSERT INTO attendance VALUES(NULL,%s,%s,%s,%s,%s)"
    val=(attendance,member,date,intime,outtime)
    iud(qry,val)
    return'''<script>alert("atendance marked");window.location='/addattendance2'</script>'''

@app.route('/addfeedback1')
def addfeedback1():
    id=request.args.get('id')
    name=request.args.get('name')
    print(name)
    session['rid']=id

    return render_template('TL/add_feedback.html',name=name)

@app.route('/addfeedback_1',methods=['post','get'])
def addfeedback_1():
    feedback = request.form['textarea']
    s = sentiment_score(feedback)
    s = predict_senti(feedback)[1]
    qry = "INSERT INTO feedback VALUES(NULL,%s,%s,%s,CURDATE())"
    val = ( session['rid'],feedback,s)
    iud(qry, val)
    return '''<script>alert('added');window.location='/addfeedback1'</script>'''


@app.route('/addtm',methods=['post','get'])
def addtm():
    return render_template('TL/add_tm.html')

@app.route('/add_tm',methods=['post','get'])
def add_tm():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    email = request.form['textfield6']
    phone = request.form['textfield7']
    username = request.form['textfield8']
    password = request.form['textfield9']
    gender = request.form['radiobutton']
    qry = "INSERT INTO `login` VALUES(null,%s,%s,'team_member')"
    val = (username, password)
    id = iud(qry, val)
    qry = "insert into tm values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (str(id), session['lid'], fname, lname, place, post, pin, email, phone, gender)
    iud(qry, val)
    return '''<script>alert("Added");window.location='/managetm'</script>'''


@app.route('/assigntm')
def assigntm():
    qry = "select * from work where hid=%s"
    res = selectall2(qry, session['lid'])
    print(res)
    qry1 = "select * from tm "
    res1 = selectall(qry1)
    return render_template('TL/assign_tm.html',val=res,val1=res1)

@app.route('/assign_tm',methods=['post','get'])
def assign_tm():
    work = request.form['select']
    tm = request.form['select2']
    qry = "INSERT INTO assign_tm VALUES(NULL,%s,%s,CURDATE(),'pending')"
    val = (work, tm)
    iud(qry, val)
    return '''<script>alert("added");window.location='/assigntm'</script>'''

@app.route('/assignedwork')
def assignedwork():
    qry="select * from work"
    res=selectall(qry)

    return render_template('TL/assigned_work.html',val=res)

@app.route('/blocktm')
def blocktm():
    qry = "SELECT login.*,tm.* FROM login JOIN tm ON login.l_id=`tm`.`lid`"
    res = selectall(qry)
    return render_template('TL/block_tm.html',val=res)

@app.route('/block_tm')
def block_tm():
    id = request.args.get('id')
    qry = "update login set type='blocked' where l_id=%s"
    iud(qry, id)
    return '''<script>alert('blocked');window.location='/blocktm'</script>'''


@app.route('/unblocktm')
def unblocktm():
    id = request.args.get('id')
    qry = "update login set type='team_member' where l_id=%s"
    iud(qry, id)
    return '''<script>alert('unblocked');window.location='/blocktm'</script>'''


@app.route('/home2')
def home2():
    return render_template('TL/home.html')

@app.route('/managetm')
def managetm():
    qry = "select * from tm"
    res = selectall(qry)
    return render_template('TL/manage_tm.html',val=res)

@app.route('/edittm')
def edittm():
    id=request.args.get('id')
    session['tid']=id
    qry="select * from tm where lid=%s"
    res=selectone(qry,id)
    return render_template('TL/edit_tm.html',val=res)

@app.route('/edit_tm',methods=['post','get'])
def edit_tm():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    email = request.form['textfield6']
    phone = request.form['textfield7']
    gender = request.form['radiobutton']
    qry = "UPDATE tm SET first_name=%s,last_name=%s,place=%s,post=%s,pin=%s,email=%s,phone=%s,gender=%s where lid=%s"
    val = ( fname, lname, place, post, pin, email, phone, gender,session['tid'])
    iud(qry, val)
    return '''<script>alert("Added");window.location='/managetm'</script>'''

@app.route('/deletetm')
def deletetm():
    id = request.args.get('id')
    qry = "DELETE FROM `login` WHERE `l_id`=%s"
    iud(qry, id)
    qry1 = "DELETE FROM `tm` WHERE `lid`=%s"
    iud(qry1, id)
    return '''<script> alert ("Deleted");window.location="/managetm"</script>'''


@app.route('/updatereport')
def updatereport():
    qry = "SELECT work.*,assign_tl.* FROM WORK JOIN assign_tl ON work.wid=assign_tl.wid WHERE `assign_tl`.`tl_id`=%s "
    res = selectall2(qry, session['lid'])

    return render_template('TL/update_report.html',val=res)

@app.route('/update_report',methods=['post','get'])
def update_report():
    report = request.files['file']

    status = request.form['textfield']
    work = request.form['select']
    qry = " INSERT INTO report VALUES(NULL,%s,%s,CURDATE(),%s,'tl')"
    val = (work, report, status)
    iud(qry, val)
    return '''<script>alert('updated');window.location='/updatereport'</script>'''


@app.route('/myatt',methods=['post','get'])
def myatt():
    qry="SELECT tl.*,`attendance`.* FROM tl JOIN `attendance` ON `attendance`.`lid`=`tl`.`lid` WHERE `tl`.`lid`=%s"
    res=selectall2(qry,session['lid'])
    return render_template('TL/my_att.html',val=res)


@app.route('/verifyatt',methods=['post','get'])
def verifyatt():
    qry="SELECT COUNT(*) AS twd,SUM(`attendance`) AS tpd,(SUM(`attendance`)/COUNT(*))*100 AS per,`tm`.`first_name`,`last_name` FROM `tm` JOIN `attendance` ON `attendance`.`lid`=`tm`.`lid` GROUP BY `tm`.`lid` "
    res = selectall(qry)
    return render_template('TL/verify_att.html',val=res)


@app.route('/viewnot2')
def viewnot2():
    qry="select * from notification"
    res=selectall(qry)
    return render_template('TL/view_not.html',val=res)

@app.route('/viewperformance3')
def viewperformance3():
    print(request.form)
    qry="SELECT AVG(`score`) AS scr,`first_name`,`last_name` FROM `tm` JOIN `assign_tm` ON `assign_tm`.`tm_id`=`tm`.`lid` JOIN `report` ON `report`.`wid`=`assign_tm`.`a_tm_id` JOIN `feedback` ON `feedback`.`rid`=`report`.`rid` WHERE `report`.`type`='tm'  AND tm.`tl_id`=%s GROUP BY `tm`.`lid` "
    res=selectall2(qry,session['lid'])
    result = []
    for i in res:
        if float(i['scr']) > 4:
            i['p'] = "excelent"
        elif float(i['scr']) > 3:
            i['p'] = "good"
        elif float(i['scr']) > 2:
            i['p'] = "avarage"
        elif float(i['scr']) > 1:
            i['p'] = "bad"
        else:
            i['p'] = "poor"
        result.append(i)
    return render_template('TL/view_performance.html',val=result)

@app.route('/viewreport1')
def viewreport1():

    qry = "SELECT tm.*,assign_tm.`wid`,report.*,work.* FROM `work`  JOIN `assign_tm` ON `assign_tm`.`wid`=`work`.`wid` JOIN `tm` ON `tm`.`lid`=`assign_tm`.`tm_id` JOIN `report` ON `report`.`wid`=`assign_tm`.`a_tm_id` WHERE `report`.`type`='tm' and `tm`.`tl_id`=%s"
    res = selectall2(qry, session['lid'])
    return render_template('TL/view_report.html',val=res)

@app.route('/home3')
def home3():
    return render_template('TM/home.html')

@app.route('/sendcomplaint')
def sendcomplaint():
    return render_template('TM/send_complaint.html')

@app.route('/sendcomp',methods=['post','get'])
def sendcomp():
    complaint= request.form['textarea']
    qry=" INSERT INTO complaint VALUES(NULL,%s,%s,CURDATE(),'pending')"
    val=(session['lid'],complaint)
    iud(qry,val)
    return '''<script>alert('sended');window.location='/sendcomplaint'</script>'''

@app.route('/updatereport1')
def updatereport1():
    qry = "SELECT work.*,assign_tm.* FROM WORK JOIN assign_tm ON work.wid=assign_tm.wid WHERE `assign_tm`.`tm_id`=%s "
    res=selectall2(qry,session['lid'])
    return render_template('TM/update_report.html',val=res)

@app.route('/update_report1',methods=['post','get'])
def update_report1():
    report=request.files['file']

    status=request.form['textfield']
    work=request.form['select']
    qry=" INSERT INTO report VALUES(NULL,%s,%s,CURDATE(),%s,'tm')"
    val=(work,report,status)
    iud(qry,val)
    return '''<script>alert('updated');window.location='/updatereport1'</script>'''

@app.route('/viewattendance',methods=['post'])
def viewattendance():
    fd=request.form['textfield']
    td=request.form['textfield2']
    qry1="SELECT tm.*,`attendance`.* FROM tm JOIN `attendance` ON `attendance`.`lid`=`tm`.`lid` WHERE `tm`.`lid`=%s AND `attendance`.`date` BETWEEN %s AND %s"
    res1=selectall2(qry1,(session['lid'],fd,td))
    qry2="SELECT SUM(`attendance`)as `sum` FROM `attendance` WHERE `lid`=%s AND `date` BETWEEN %s AND %s"
    res2=selectone(qry2,(session['lid'],fd,td))
    qry3 = "SELECT ROUND((SUM(`attendance`)/COUNT(`attendance`))*100) AS per FROM `attendance` WHERE `lid`=%s AND `date` BETWEEN %s AND %s"
    res3 = selectone(qry3, (session['lid'],fd,td))
    return render_template('TM/view_att.html',val1=res1,sd=fd,ed=td,val2=res2,val3=res3)

@app.route('/viewatt')
def viewatt():
    qry1 = "SELECT tm.*,`attendance`.* FROM tm JOIN `attendance` ON `attendance`.`lid`=`tm`.`lid` WHERE `tm`.`lid`=%s "
    res1 = selectall2(qry1,session['lid'])

    qry2 = "SELECT SUM(`attendance`)as `sum` FROM `attendance` WHERE `lid`=%s "
    res2 = selectone(qry2, session['lid'])
    print(res2)
    qry3="SELECT ROUND((SUM(`attendance`)/COUNT(`attendance`))*100) AS per FROM `attendance` WHERE `lid`=%s "
    res3=selectone(qry3,session['lid'])

    return render_template('TM/view_att.html',val=res1,val2=res2,val3=res3)

@app.route('/viewnot3')
def viewnot3():
    qry="select * from notification"
    res=selectall(qry)
    return render_template('TM/view_not.html',val=res)

@app.route('/viewreply')
def viewreply():
    qry="select * from complaint"
    res=selectall(qry)
    return render_template('TM/view_reply.html',val=res)

@app.route('/viewwork1')
def viewwork1():
    qry="  SELECT work.*,assign_tm.* FROM WORK JOIN assign_tm ON work.wid=assign_tm.wid WHERE `assign_tm`.`tm_id`=%s "
    res=selectall2(qry,session['lid'])
    return render_template('TM/view_work.html',val=res)








@app.route('/login_code',methods=['get','post'])
def login_code():
    username=request.form['textfield']
    password=request.form['textfield2']
    qry="select * from login where username=%s and password=%s"
    val=(username,password)
    res=selectone(qry,val)
    if res is None:
        return '''<script> alert("invalid");window.location="/"</script>'''
    elif res['type']=='admin':
        session['lid']=res['l_id']
        return redirect('/home')
    elif res['type']=='hr':
        session['lid']=res['l_id']

        return redirect('/home1')
    elif res['type']=='team_leader':
        session['lid']=res['l_id']

        return redirect('/home2')
    elif res['type']=='team_member':
        session['lid']=res['l_id']

        return redirect('/home3')
    else:
        return '''<script> alert ("invalid");window.location="/"</script>'''

@app.route('/login_index',methods=['post','get'])
def login_index():
    return render_template('login_index.html')


app.run(debug = True)



