#To use with python3 <<

import string

def decr_rotN(str,typeRot):
    '''
    Decrypt from rotX encryption
    '''
    decrStr=''
    typeRot=int(typeRot)
    str=str.upper()
    arr = [x for x in range(1,26)]
    if typeRot not in arr:
        return 'error typeRot'
    crDic=dict(zip(string.ascii_uppercase, range(1+typeRot,27+typeRot)))
    encrDic=dict(zip(range(1,27),string.ascii_uppercase))
    for x in str:
        for y in crDic:
            if x == ' ':
                decrStr+=' '
                break
            elif x == y:
                tmp=(crDic[y]-typeRot*2)%26
                if tmp == 0:
                    tmp = 26
               # print('crDic[y]=',crDic[y],'y=',y,'tmp=',tmp,'encrDic[tmp]=',encrDic[tmp])
                decrStr+=encrDic[tmp]
    
    return decrStr

def encr_rotN(str,typeRot):
    '''
    Encrypt using rotX encryption
    '''
    encrStr=''
    typeRot=int(typeRot)
    str=str.upper()
    arr = [x for x in range(1,26)]
    if typeRot not in arr:
        return 'error typeRot'
    crDic=dict(zip(range(1,27),string.ascii_uppercase))
    encrDic=dict(zip(string.ascii_uppercase,range(1,27)))
    for x in str:
        for y in encrDic:
            if x == ' ':
                encrStr+=' '
                break
            elif x == y:
                tmp=(encrDic[y]+typeRot)%26
                if tmp == 0:
                    tmp = 26
                encrStr+=crDic[tmp]

    return encrStr

if __name__=='__main__':
    enOrDec=input('Do u want to (E)ncrypt or (D)ecrypt?')
    
    if enOrDec == 'D':
        str=input('Insert string to decrypt:')
        typeRot=input('Insert type of rot (example: 13 means \'rot13\'):')
        decr=decr_rotN(str,typeRot)
        if decr != 'error typeRot':
            print('\n[+] Decrypted word:'+decr)
        else:
            print('\n[-] Type of rot has to be a number between 1 and 25')
    
    elif enOrDec == 'E':
        str=input('Insert string to encrypt:')
        typeRot=input('Insert type of rot (example: 13 means \'rot13\'):')
        encr=encr_rotN(str,typeRot)
        if encr != 'error typeRot':
            print('\n[+] Encrypted word:'+encr)
        else:
            print('\n[-] Type of rot must be a number between 1 and 25')

    else:
        print('[-] Choose a letter between D (Decrypt) or E (Encrypt)\nExit ... ')
