from zipfile import *

def extractFile(File, password):
    try:
        File.extractall(pwd = password)
        return password
    except:
        return

def main():
    zFile = ZipFile('evil.zip')
    passFile = open('dictionary.txt')
    for line in passFile.readlines():
        password = line.strip('\n')
        guess = extractFile(zFile,password)
        if guess:
            print '[+] Password = ' + password + '\n'
            exit(0)
if __name__ == '__main__':
    main()