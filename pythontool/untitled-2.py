import string
import random


class ss:
    info = ''
    lenth = 0
    username = 'ch3ck'
    password = ''
    email = ''

    def __init__(self, username, password, info, email, lenth):
        self.email = email
        self.info = info
        self.lenth = lenth
        self.username = username
        self.password = password

    def show(self):
        print "username:" + self.username
        print "password:" + self.password
        print "info:" + self.info
        print "email:" + self.email
        print "lenth:" + self.lenth

    def check(self, username, info):
        if username == self.username:
            return True
        elif info in self.info:
            return True
        else:
            return False


class passwd:
    info = ''
    lenth = 0
    username = 'ch3ck'
    password = ''
    email = ''

    def show(self):
        print "username:" + self.username
        print "password:" + self.password
        print "info:" + self.info
        print "email:" + self.email
        print "email:" + self.lenth

    def write(self):
        filename = "password.txt"
        with open(filename, 'a') as f:
            f.write("username:" + self.username + "\n")
            f.write("password:" + self.password + "\n")
            f.write("info:" + self.info + "\n")
            f.write("email:" + self.email + "\n")
            f.write("email:" + self.lenth + "\n")
            f.write("\n================================================\n")

    def getPass(self):
        self.username = raw_input('input the username:')
        self.info = raw_input('input the info about the password:')
        self.lenth = raw_input('input the lenth:')
        self.email = raw_input('input the email')
        choice = raw_input('1.printable chars\n2.number and up\n')
        if choice == 1:
            table = string.printable[:-6]
        else:
            table = string.printable[:-38]
        for i in range(int(self.lenth)):
            x = random.randint(0, len(table) - 1)
            self.password += table[x]

    def search(self):
        url = raw_input('input the info:')
        user = raw_input('input the username:')
        filename = "password.txt"
        with open(filename) as f:
            result = f.readlines()
        i = 0
        while True:
            if i >= len(result) - 4:
                break
            s = ss(result[i][9:-1], result[i + 1][9:-1], result[i + 2][5:-1], result[i + 3][6:-1], result[i + 4][6:-1])
            if s.check(user, url):
                s.show()
            i = i + 6


if __name__ == '__main__':
    user = passwd()
    sss = raw_input('1.check\n2.add\n')
    if sss == 1:
        user.search()
    else:
        user.getPass()
        user.write()
        user.show()
