import sys
import datetime
import sqlite3
import re
from PyQt5 import QtWidgets, uic
from internet import checkinternet
import sendemail

qtCreatorFile = "sd3.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def reminder():
    f = open("date.txt", "r+")
    rdate = f.read()
    emaillist = []
    if checkinternet():
        if rdate != issuedate:
            f.seek(0)
            f.write(issuedate)
            rdate = issuedate
            cur.execute("SELECT (personid) FROM issue WHERE duedate=?", (rdate,))
            idlist = cur.fetchone()
            try:
                for peopleid in idlist:
                    cur.execute('SELECT (email) FROM Person WHERE person_id = ?', (peopleid,))
                    emaillist.append(cur.fetchone()[0])
                sendemail.emailsender(emaillist)
            except:
                pass
    f.close()


def msgsbox(text, title):
    msgbox = QtWidgets.QMessageBox()
    msgbox.setIcon(QtWidgets.QMessageBox.Information)
    msgbox.setText(text)
    msgbox.setWindowTitle(title)
    msgbox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msgbox.exec()


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.enterbookid.hide()
        self.bkidinput.hide()
        self.bkidsubmit.hide()
        self.enterbname.hide()
        self.bname.hide()
        self.bnamesubmit.hide()
        self.bookerror.hide()
        self.copy.hide()
        self.copyinput.hide()
        self.copysubmit.hide()
        self.enterbookid2.hide()
        self.bkidinput2.hide()
        self.bkidsubmit2.hide()
        self.enterbname2.hide()
        self.bnameinput.hide()
        self.bnamesubmit2.hide()
        self.copy2.hide()
        self.copyinput2.hide()
        self.copysubmit2.hide()
        self.smbr.hide()
        self.tblbooks.hide()
        self.clrtable.hide()
        self.enter_email.hide()
        self.emailinput2.hide()
        self.emailsubmit2.hide()
        self.enterphone.hide()
        self.phoneinput.hide()
        self.phonesubmit.hide()
        self.tblissue.hide()
        self.tblmbr.hide()
        self.tblmbrinfo.hide()
        self.smbrinput.hide()
        self.smbrsubmit.hide()

        reminder()
        self.emailsubmit.clicked.connect(self.emailentry)
        self.idsubmit.clicked.connect(self.returnbook)
        self.namesubmit.clicked.connect(self.newmemname)
        self.bkidsubmit3.clicked.connect(self.newbk)
        self.searchbks.clicked.connect(self.sbkslabel)
        self.searchmbr.clicked.connect(self.smbrlabel)
        self.sbkssubmit.clicked.connect(self.searchbooks)
        self.showbks.clicked.connect(self.allbooks)
        self.showmbr.clicked.connect(self.allmbrs)
        self.clrtable.clicked.connect(self.clrtbl)

    def clrtbl(self):
        self.tblbooks.setRowCount(0)
        self.tblissue.setRowCount(0)
        self.tblmbr.setRowCount(0)
        self.tblmbrinfo.setRowCount(0)
        self.clr()

    def allmbrs(self):
        self.clrtbl()
        self.tblmbr.show()
        self.clrtable.show()
        self.tblmbr.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        tabledata = cur.execute('SELECT * From Person').fetchall()
        for row_number, row_data in enumerate(tabledata):
            self.tblmbr.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.tblmbr.setItem(row_number, column_number, cell)

    def allbooks(self):
        self.clrtbl()
        self.tblbooks.show()
        self.clrtable.show()
        self.tblbooks.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        tabledata = cur.execute('SELECT * From Books').fetchall()
        for row_number, row_data in enumerate(tabledata):
            self.tblbooks.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.tblbooks.setItem(row_number, column_number, cell)

    def smbrlabel(self):
        self.sbks.hide()
        self.sbksinput.hide()
        self.sbkssubmit.hide()
        self.smbr.show()
        self.smbrinput.show()
        self.smbrsubmit.show()
        self.smbrsubmit.clicked.connect(self.searchmbrs)

    def searchmbrs(self):
        self.tblbooks.setRowCount(0)
        self.tblissue.setRowCount(0)
        self.tblmbr.setRowCount(0)
        self.tblmbrinfo.setRowCount(0)
        self.tblbooks.hide()
        self.tblissue.hide()
        self.tblmbr.hide()
        self.tblmbrinfo.hide()
        smmbr = self.smbrinput.text()
        if len(smmbr) == 0:
            msgsbox("Invalid Input. Try again!", "Error")
            self.clr()
        else:
            var = re.findall('@(.+)', smmbr)
            if len(var) == 0:
                if smmbr.isnumeric():
                    i, j = 0, int(smmbr)
                    while j > 0:
                        j = j // 10
                        i += 1
                    if i == 10:
                        phoneno = int(smmbr)
                        self.searchmbrphone(phoneno)
                    else:
                        is_personid = cur.execute('SELECT (phoneno) FROM Person Where person_id = ?',
                                                  (smmbr,)).fetchone()
                        if is_personid is not None:
                            self.searchmbrid(smmbr)
                        else:
                            msgsbox("Invalid Input! No such person id found.", "Error")
                            self.clr()
            else:
                email = smmbr
                self.searchmbremail(email)

    def searchmbremail(self, x):
        cur.execute("SELECT (person_id) FROM Person WHERE email = ?", (x,))
        global perid
        perid = cur.fetchone()[0]
        self.searchmbrs2()

    def searchmbrphone(self, x):
        cur.execute("SELECT (person_id) FROM Person WHERE phoneno = ?", (x,))
        global perid
        perid = cur.fetchone()[0]
        self.searchmbrs2()

    def searchmbrid(self, x):
        global perid
        perid = x
        self.searchmbrs2()

    def searchmbrs2(self):
        self.tblbooks.setRowCount(0)
        self.tblissue.setRowCount(0)
        self.tblmbr.setRowCount(0)
        self.tblmbrinfo.setRowCount(0)
        self.tblmbrinfo.show()
        self.clrtable.show()
        self.tblmbrinfo.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        tabledata = cur.execute('SELECT personid,pname,email,phoneno,bname,bookid From Person INNER JOIN issue ON '
                                'Person.person_id = issue.personid INNER JOIN Books ON Books.book_id = issue.bookid '
                                'WHERE Person.person_id=?', (perid,)).fetchall()
        for row_number, row_data in enumerate(tabledata):
            self.tblmbrinfo.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                cell = QtWidgets.QTableWidgetItem(str(data))
                self.tblmbrinfo.setItem(row_number, column_number, cell)

    def sbkslabel(self):
        self.smbr.hide()
        self.smbrinput.hide()
        self.smbrsubmit.hide()
        self.sbks.show()
        self.sbksinput.show()
        self.sbkssubmit.show()
        self.sbkssubmit.clicked.connect(self.searchbooks)

    def searchbooks(self):
        self.tblbooks.setRowCount(0)
        self.tblissue.setRowCount(0)
        self.tblmbr.setRowCount(0)
        self.tblmbrinfo.setRowCount(0)
        self.tblbooks.hide()
        self.tblissue.hide()
        self.tblmbr.hide()
        self.tblmbrinfo.hide()
        sbook = self.sbksinput.text()
        if len(sbook) == 0:
            msgsbox("Invalid Input. Try again!", "Error")
            self.clr()
        else:
            if sbook.isnumeric():
                bkidlist = cur.execute('SELECT (book_id) FROM Books').fetchall()
                f1 = 0
                for i in bkidlist:
                    for j in i:
                        if j == int(sbook):
                            f1 = 1
                            self.tblbooks.setRowCount(0)
                            self.tblissue.setRowCount(0)
                            self.tblmbr.setRowCount(0)
                            self.tblmbrinfo.setRowCount(0)
                            self.tblissue.show()
                            self.clrtable.show()
                            self.tblissue.horizontalHeader().setSectionResizeMode(
                                QtWidgets.QHeaderView.ResizeToContents)
                            tabledata = cur.execute('SELECT personid,pname,bookid,bname,copyno,issuedate,duedate From '
                                                    'issue,Books INNER JOIN Person ON Person.person_id = '
                                                    'issue.personid AND issue.bookid = Books.book_id WHERE bookid=?',
                                                    (j,)).fetchall()
                            for row_number, row_data in enumerate(tabledata):
                                self.tblissue.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                    cell = QtWidgets.QTableWidgetItem(str(data))
                                    self.tblissue.setItem(row_number, column_number, cell)
                            break
                if f1 == 0:
                    msgsbox('No such book found.', 'Error')
                    self.clr()
            elif type(sbook) == str:
                a = None
                tag = None
                sbook = sbook.lower()
                bnamelist = cur.execute('SELECT (bname) FROM Books').fetchall()
                for i in bnamelist:
                    for j in i:
                        j = j.lower()
                        a = j.find(sbook)
                        if a != -1:
                            tag = 1
                            j = j.capitalize()
                            bkid = cur.execute('SELECT (book_id) FROM Books WHERE bname=?', (j,)).fetchone()[0]
                            self.tblbooks.setRowCount(0)
                            self.tblissue.setRowCount(0)
                            self.tblmbr.setRowCount(0)
                            self.tblmbrinfo.setRowCount(0)
                            self.tblissue.show()
                            self.clrtable.show()
                            self.tblissue.horizontalHeader().setSectionResizeMode(
                                QtWidgets.QHeaderView.ResizeToContents)
                            tabledata = cur.execute('SELECT personid,pname,bookid,bname,copyno,issuedate,duedate From '
                                                    'issue,Books INNER JOIN Person ON Person.person_id = '
                                                    'issue.personid AND Books.book_id = issue.bookid WHERE bookid=?',
                                                    (bkid,)).fetchall()
                            for row_number, row_data in enumerate(tabledata):
                                self.tblissue.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                    cell = QtWidgets.QTableWidgetItem(str(data))
                                    self.tblissue.setItem(row_number, column_number, cell)
                            break
                if a == -1 and tag is None:
                    msgsbox('No such book found.', 'Error')
                    self.clr()
            else:
                msgsbox("Invalid Input!", "Error")
                self.clr()

    def newbk(self):
        global book_id
        book_id = self.bkidinput3.text()
        cur.execute('SELECT (bname) FROM Books WHERE book_id=?', (book_id,))
        z = cur.fetchone()
        if z is None:
            self.bkidinput3.setReadOnly(True)
            self.enterbname2.show()
            self.bnameinput.show()
            self.bnamesubmit2.show()
            self.bnamesubmit2.clicked.connect(self.newbk2)
        else:
            msgsbox("Book with this id already exists. Try again!", "Error")
            self.clr()

    def newbk2(self):
        global nbname
        nbname = self.bnameinput.text().capitalize()
        self.bnameinput.setReadOnly(True)
        self.copy2.show()
        self.copyinput2.show()
        self.copysubmit2.show()
        self.copysubmit2.clicked.connect(self.newbk3)

    def newbk3(self):
        copies = self.copyinput2.text()
        self.copyinput2.setReadOnly(True)
        try:
            cur.execute('INSERT INTO Books (book_id, bname, copies) VALUES (?, ?, ?)', (book_id, nbname, copies))
            conn.commit()
            msgsbox("New Book Registered!", "Done")
        except:
            pass
        self.clr()

    def newmemname(self):
        global rowid
        name = self.nameinput.text().capitalize()
        self.nameinput.setReadOnly(True)
        try:
            cur.execute('INSERT INTO Person (pname) VALUES (?)', (name,))
            rowid = cur.lastrowid
            conn.commit()
        except:
            pass
        self.enter_email.show()
        self.emailinput2.show()
        self.emailsubmit2.show()
        self.emailsubmit2.clicked.connect(self.newmememail)

    def newmememail(self):
        email2 = self.emailinput2.text()
        self.emailinput2.setReadOnly(True)
        a = re.findall('@(.+)', email2)
        if len(a) < 1:
            msgsbox("Invalid email address!", "Error")
            cur.execute("DELETE FROM Person WHERE person_id=?", (rowid,))
            conn.commit()
            self.clr()
        else:
            try:
                cur.execute('UPDATE Person SET email=? WHERE person_id=?', (email2, rowid))
                conn.commit()
                self.enterphone.show()
                self.phoneinput.show()
                self.phonesubmit.show()
                self.phonesubmit.clicked.connect(self.newmemphone)
            except:
                pass

    def newmemphone(self):
        phone2 = self.phoneinput.text()
        try:
            i, j = 0, int(phone2)
            while j > 0:
                j = j // 10
                i += 1
            if i == 10:
                phone = int(phone2)
                try:
                    cur.execute('UPDATE Person SET phoneno=? WHERE person_id=?', (phone, rowid))
                    conn.commit()
                    self.phoneinput.setReadOnly(True)
                    msgsbox("New Member Registered!", "Congrats!")
                    self.clr()
                except:
                    self.clr()
            else:
                msgsbox("Invalid Phone Number!", "Error")
                cur.execute("DELETE FROM Person WHERE person_id=?", (rowid,))
                conn.commit()
                self.clr()
        except:
            pass

    def returnbook(self):
        idno = self.idinput.text()
        self.idinput.setReadOnly(True)
        if len(idno) == 0:
            msgsbox('Invalid Input! Try again.', 'Error')
            self.clr()
        else:
            var = re.findall('@(.+)', idno)
            if len(var) == 0:
                if idno.isnumeric():
                    i, j = 0, int(idno)
                    while j > 0:
                        j = j // 10
                        i += 1
                    if i == 10:
                        phoneno = int(idno)
                        self.idphone(phoneno)
                    else:
                        is_personid = cur.execute('SELECT (phoneno) FROM Person Where person_id = ?',
                                                  (idno,)).fetchone()
                        if is_personid is not None:
                            self.idid(idno)
                        else:
                            msgsbox("Invalid Input! No such person id found.", "Error")
                            self.clr()
            else:
                email = idno
                self.idemail(email)

    def idemail(self, x):
        cur.execute("SELECT (person_id) FROM Person WHERE email = ?", (x,))
        global personid
        personid = cur.fetchone()[0]
        self.enterbookid2.show()
        self.bkidinput2.show()
        self.bkidsubmit2.show()
        self.bkidsubmit2.clicked.connect(self.returnbook2)

    def idphone(self, x):
        cur.execute("SELECT (person_id) FROM Person WHERE phoneno = ?", (x,))
        global personid
        personid = cur.fetchone()[0]
        self.enterbookid2.show()
        self.bkidinput2.show()
        self.bkidsubmit2.show()
        self.bkidsubmit2.clicked.connect(self.returnbook2)

    def idid(self, x):
        global personid
        personid = x
        self.enterbookid2.show()
        self.bkidinput2.show()
        self.bkidsubmit2.show()
        self.bkidsubmit2.clicked.connect(self.returnbook2)

    def returnbook2(self):
        bkid2 = self.bkidinput2.text()
        self.bkidinput2.setReadOnly(True)
        try:
            cur.execute('UPDATE issue SET personid=0, issuedate=NULL, duedate=NULL WHERE personid=? AND bookid=?',
                        (personid, bkid2))
            conn.commit()
            cur.execute('SELECT (icopies) FROM Books WHERE book_id=?', (bkid2,))
            value = cur.fetchone()[0] - 1
            cur.execute('UPDATE Books SET icopies=? WHERE book_id=?', (value, bkid2))
            conn.commit()
            msgsbox("Book Returned!", "Done")
            reminder()
            self.clr()
        except:
            self.clr()

    def emailentry(self):
        self.emailinput.setReadOnly(True)
        inputit = self.emailinput.text()
        if len(inputit) == 0:
            msgsbox('Invalid Input! Try again.', 'Error')
            self.clr()
        else:
            var = re.findall('@(.+)', inputit)
            if len(var) == 0:
                try:
                    if inputit.isnumeric():
                        i, j = 0, int(inputit)
                        while j > 0:
                            j = j // 10
                            i += 1
                        if i == 10:
                            phoneno = int(inputit)
                            self.bkidphone(phoneno)
                        else:
                            is_personid = cur.execute('SELECT (phoneno) FROM Person Where person_id = ?',
                                                      (inputit,)).fetchone()
                            if is_personid is not None:
                                self.bkidid(inputit)
                            else:
                                msgsbox("Invalid Input! No such person id found.", "Error")
                                self.clr()
                except:
                    msgsbox("Invalid Input!", "Error")
                    self.clr()
            else:
                email = inputit
                self.bkidemail(email)

    def bkidemail(self, x):
        cur.execute("SELECT (person_id) FROM Person WHERE email = ?", (x,))
        global personid, one
        one = 1
        personid = cur.fetchone()[0]
        self.enterbookid.show()
        self.bkidinput.show()
        self.bkidsubmit.show()
        self.bkidsubmit.clicked.connect(self.bknentry)

    def bkidphone(self, x):
        cur.execute("SELECT (person_id) FROM Person WHERE phoneno = ?", (x,))
        global personid, one
        one = 1
        personid = cur.fetchone()[0]
        self.enterbookid.show()
        self.bkidinput.show()
        self.bkidsubmit.show()
        self.bkidsubmit.clicked.connect(self.bknentry)

    def bkidid(self, x):
        global personid, one
        one = 1
        personid = x
        self.enterbookid.show()
        self.bkidinput.show()
        self.bkidsubmit.show()
        self.bkidsubmit.clicked.connect(self.bknentry)

    def bknentry(self):
        global bkid, one
        if one == 1:
            one = 0
            self.bkidinput.setReadOnly(True)
            bkid = self.bkidinput.text()
            a = cur.execute("SELECT (bname) FROM Books WHERE book_id = ?", (bkid,)).fetchone()
            flag = 0
            if a is not None:
                cur.execute('SELECT (personid) FROM issue WHERE bookid = ?', (bkid,))
                y = cur.fetchall()
                for i in y:
                    for j in i:
                        if j == int(personid):
                            msgsbox("This person already issued this book.", "Error")
                            self.clr()
                            flag = 1
                if flag == 0:
                    cur.execute('SELECT (copyno) FROM issue WHERE bookid = ?', (bkid,))
                    b = cur.fetchall()
                    if len(b) != 0:
                        copy = b[len(b) - 1][0] + 1
                        cur.execute('SELECT (copies) FROM Books WHERE book_id = ?', (bkid,))
                        copies = cur.fetchone()[0]
                        if copy <= copies:
                            try:
                                cur.execute('INSERT INTO issue (personid, bookid, copyno, issuedate, duedate) VALUES '
                                            '(?, ?, ?, ?, ?)', (personid, bkid, copy, issuedate, duedate))
                                conn.commit()
                                cur.execute('SELECT (icopies) FROM Books WHERE book_id=?', (bkid,))
                                value = cur.fetchone()[0] + 1
                                cur.execute('UPDATE Books SET icopies=? WHERE book_id=?', (value, bkid))
                                conn.commit()
                                msgsbox("Book Issued!", "Done")
                                self.clr()
                            except:
                                pass
                        else:
                            cur.execute('SELECT (copyno) FROM issue WHERE personid = 0')
                            copyn = cur.fetchone()[0]
                            if copyn is not None:
                                try:
                                    cur.execute('UPDATE issue SET personid=?, issuedate=?, duedate=? WHERE copyno=?',
                                                (personid, issuedate, duedate, copyn,))
                                    conn.commit()
                                    cur.execute('SELECT (icopies) FROM Books WHERE book_id=?', (bkid,))
                                    value = cur.fetchone()[0] + 1
                                    cur.execute('UPDATE Books SET icopies=? WHERE book_id=?', (value, bkid))
                                    conn.commit()
                                    msgsbox("Book Issued!", "Done")
                                    self.clr()
                                except:
                                    self.clr()
                            else:
                                msgsbox("No more copies of this book available.", "No copies")
                                self.clr()
                    else:
                        copy = 1
                        try:
                            cur.execute(
                                'INSERT INTO issue (personid, bookid, copyno, issuedate, duedate) VALUES (?, ?, ?, ?, '
                                '?)', (personid, bkid, copy, issuedate, duedate))
                            conn.commit()
                            cur.execute('UPDATE Books SET icopies=1 WHERE book_id=?', (bkid,))
                            conn.commit()
                            msgsbox("Book Issued!", "Done")
                            self.clr()
                        except:
                            pass
                else:
                    pass
            else:
                self.bookerror.show()
                self.enterbname.show()
                self.bname.show()
                self.bnamesubmit.show()
                self.bnamesubmit.clicked.connect(self.step)

    def step(self):
        global bookname
        self.bname.setReadOnly(True)
        bookname = self.bname.text().capitalize()
        self.copy.show()
        self.copyinput.show()
        self.copysubmit.show()
        self.copysubmit.clicked.connect(self.final)

    def final(self):
        self.copyinput.setReadOnly(True)
        copies = self.copyinput.text()
        try:
            cur.execute('INSERT INTO Books (bname, book_id, copies, icopies) VALUES (?, ?, ?)',
                        (bookname, bkid, copies, 1))
            conn.commit()
            copy = 1
            cur.execute(
                'INSERT INTO issue (personid, bookid, copyno, issuedate, duedate) VALUES (?, ?, ?, ?, ?)',
                (personid, bkid, copy, issuedate, duedate))
            conn.commit()
            msgsbox("New Book Registered and Book is issued.", "Done")
        except:
            pass
        self.clr()

    def clr(self):
        self.emailinput.setReadOnly(False)
        self.bkidinput.setReadOnly(False)
        self.bname.setReadOnly(False)
        self.bkidinput2.setReadOnly(False)
        self.nameinput.setReadOnly(False)
        self.emailinput2.setReadOnly(False)
        self.phoneinput.setReadOnly(False)
        self.bkidinput3.setReadOnly(False)
        self.bnameinput.setReadOnly(False)
        self.copyinput.setReadOnly(False)
        self.idinput.setReadOnly(False)
        self.bkidinput2.setReadOnly(False)
        self.copyinput2.setReadOnly(False)
        self.emailinput.clear()
        self.bkidinput3.clear()
        self.bnameinput.clear()
        self.nameinput.clear()
        self.emailinput2.clear()
        self.phoneinput.clear()
        self.bkidinput.clear()
        self.bname.clear()
        self.bkidinput2.clear()
        self.copyinput.clear()
        self.idinput.clear()
        self.bkidinput2.clear()
        self.copyinput2.clear()
        self.sbksinput.clear()
        self.enterbookid.hide()
        self.bkidinput.hide()
        self.bkidsubmit.hide()
        self.enterbname.hide()
        self.bname.hide()
        self.bnamesubmit.hide()
        self.bookerror.hide()
        self.copy.hide()
        self.copyinput.hide()
        self.copysubmit.hide()
        self.enterbookid2.hide()
        self.bkidinput2.hide()
        self.bkidsubmit2.hide()
        self.enterbname2.hide()
        self.bnameinput.hide()
        self.bnamesubmit2.hide()
        self.copy2.hide()
        self.copyinput2.hide()
        self.copysubmit2.hide()
        self.tblbooks.hide()
        self.clrtable.hide()
        self.enter_email.hide()
        self.emailinput2.hide()
        self.emailsubmit2.hide()
        self.enterphone.hide()
        self.phoneinput.hide()
        self.phonesubmit.hide()
        self.tblissue.hide()
        self.tblmbr.hide()
        self.tblmbrinfo.hide()


if __name__ == "__main__":
    conn = sqlite3.connect('Library Management.db')
    cur = conn.cursor()
    issuedate = datetime.datetime.now().date()
    duedate = issuedate + datetime.timedelta(days=7)
    issuedate = str(issuedate)
    duedate = str(duedate)
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
