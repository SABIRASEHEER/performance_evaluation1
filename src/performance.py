from flask import *
from src.dbconnectionnew import *
from src.emotion import sentiment_score
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
    ty=request.form['select']
    fd=request.form['textfield']
    td=request.form['textfield2']
    if ty=="TEAM MEMBER":
        qry="SELECT AVG(`score`) AS scr,`first_name`,`last_name` FROM `tm` JOIN `assign_tm` ON `assign_tm`.`tm_id`=`tm`.`lid` JOIN `report` ON `report`.`wid`=`assign_tm`.`a_tm_id` JOIN `feedback` ON `feedback`.`rid`=`report`.`rid` WHERE `report`.`type`='tm' AND `report`.`date` BETWEEN % s AND % s GROUP BY `tm`.`lid`"
        res=selectall2(qry,(fd,td))
        return render_template('ADMIN/view_performance.html',val=res)

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
        qry="SELECT tl.first_name,tl.last_name,work.work,report.* FROM `tl` JOIN `assign_tl` ON `assign_tl`.`tl_id`=`tl`.`lid` JOIN `work`ON `assign_tl`.`wid`=`work`.`wid` JOIN `report` ON `report`.`wid`=`work`.`wid`"
        res=selectall(qry)
        return render_template('ADMIN/view_work_report.html',val=res)
    else:
        qry = "SELECT tm.first_name,tm.last_name,work.work,report.* FROM `tm` JOIN `assign_tm` ON `assign_tm`.`tm_id`=`tm`.`lid` JOIN `work`ON `assign_tm`.`wid`=`work`.`wid` JOIN `report` ON `report`.`wid`=`work`.`wid`"
        res = selectall(qry)
        return render_template('ADMIN/view_work_report.html', val=res)



@app.route('/addfeedback')
def addfeedback():

    return render_template('HR/add_feedback.html')\

@app.route('/add_feedback',methods=['post','get'])
def add_feedback():
    feedback=request.form['textarea']
    s=sentiment_score(feedback)
    qry="INSERT INTO feedback VALUES(NULL,%s,%s,%s,CURDATE())"
    val=(session['lid'],feedback,s)
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
    qry="SELECT attendance.*,tl.* FROM attendance JOIN tl ON attendance.lid=tl.lid"
    res=selectall(qry)
    return render_template('HR/attendance_tl.html',val=res)

@app.route('/blocktl')
def blocktl():
    qry="select * from tl"
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
    return render_template('HR/home.html')

@app.route('/managework')
def managework():
    qry="select * from work where hid=%s"
    res=selectall2(qry,session['lid'])
    return render_template('HR/manage_work.html',val=res)

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


@app.route('/addfeedback1')
def addfeedback1():
    id=request.args.get('id')
    session['rid']=id

    return render_template('TL/add_feedback.html')

@app.route('/addfeedback_1',methods=['post','get'])
def addfeedback_1():
    feedback = request.form['textarea']
    s = sentiment_score(feedback)
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
    return render_template('TL/block_tm.html')

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



@app.route('/verifyatt')
def verifyatt():
    return render_template('TL/verify_att.html')

@app.route('/viewnot2')
def viewnot2():
    qry="select * from notification"
    res=selectall(qry)
    return render_template('TL/view_not.html',val=res)

@app.route('/viewperformance3')
def viewperformance3():
    return render_template('TL/view_performance.html')

@app.route('/viewreport1')
def viewreport1():
    qry = "SELECT tm.*,assign_tm.`wid`,report.*,work.* FROM `work` JOIN `report` ON `report`.`wid`=`work`.`wid` JOIN `assign_tm` ON `assign_tm`.`wid`=`work`.`wid` JOIN `tm` ON `tm`.`lid`=`assign_tm`.`tm_id` WHERE `tm`.`tl_id`=%s"
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

@app.route('/viewatt')
def viewatt():
    return render_template('TM/view_att.html')

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


