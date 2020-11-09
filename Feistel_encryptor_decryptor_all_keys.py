def encrypt(file,round,key):
    '''
Method to encrypt a plaintext using
a Feistel cipher (S,L,T).
N.B. : this method works only with a plaintext of one word.
>>> INSTRUCTIONS <<<
Message length lu = lx = 2l = 32 ; key length lk = 32 ;
Round function: the j-th bit of the output block wi in the i-th round, denoted
wi(j) is
f : wi(j) ={
    yi(j) XOR ki(4j - 3) ; 1 <= j <= l/2
    yi(j) XOR ki(4j - 2l) ; l/2 < j <= l
    }
subkey generation: the j-th bit of the subkey ki for the i-th round, denoted ki(j) is
gi : ki(j) = k(((5i + j - 1) mod lk) + 1) ; i = 1,..,n
    '''
    print('\nENCRYPTION'+'--------------'*2+'\n')
    words=[]
    for line in file:
        words.append(line)
    lk = 32 #key-length
    plain = bin(int(words[0],16))[2:]
    if( len(plain)<lk ): #pad zeros
        plain = '0'*(lk-len(str(plain)))+str(plain)
    y1 = int(plain[0:int(len(plain)/2)],2) #"left" part of plain. TODO if len(plain) is odd? Control
    y1 = bin(y1)[2:]
    z1 = int(plain[int(len(plain)/2):],2) #"right" part of the number

    if( len(y1)<int(len(plain)/2) ):
        y1 = '0'*(int(len(plain)/2)-len(y1))+y1

    key = int(key,16)
    round = int(round)
    # remark: '&' (AND), '|' (OR), '^' (XOR) operators work bitwise
    if ( len(bin(key)[2:])<lk ):
        key = '0'*(lk - len(bin(key)[2:]))+bin(key)[2:]
    else:
        key = bin(key)[2:]
    
    subkeys=[0] #the first index is occupied by a 0 value in order to have congruence with the next indexes (also for the other arrays)
    ys = [0,y1] #array with the various yi ; i=1,..,nr.rounds
    zs = [0,str(bin(z1)[2:])] #array with zi
    ws = [0] #arr with wi
    vs = [0] #ar with vi
    j=1
    i=1
    tmp=''
    tmpRound=round
    #since to generate the subkeys i only need k,lk and the nr. of rounds, before
    #I generate the subkeys i will need

    #SUBKEY GENERATION
    while(round!=0):
        for b in key:
            index_key =(((5*i+j-1)%lk)+1)
            bit = int((key)[index_key-1],2) #-1 because the index start from 1 instead of 0
            tmp+=str(bit)
            j+=1
        subkeys.append(tmp)
        #reset values for next subkey
        tmp=''
        i+=1
        j=1
        round-=1
    #at the end of the while-loop, i'll have k1 in subkeys[1], .., kn in subkeys[n]

    round = tmpRound
    i = 1
    j = 1

    while(round!=0):

        # >>> ROUND function <<<
        while(j<=lk/2):
            if( (j>=1) and (j<=lk/4) ):
                tmp += str( int(str(ys[i])[j-1],2) ^ int(subkeys[i][4*j-3-1],2) )
                j+=1
            else: # j>lk/4 and j<=lk/2
                tmp += str( int(str(ys[i])[j-1],2) ^ int(subkeys[i][4*j-lk-1],2) )
                j+=1
        ws.append(tmp)
        tmp=""

        #>>> LINEAR operation <<<
        tmp = bin(int(ws[i],2) ^ int(zs[i],2))[2:]
        if( len(str(tmp))<16 ):
            tmp = '0'*(16-len(str(tmp)))+str(tmp)
        vs.append(tmp)
        tmp=''
        #>>> TRANSPOSITION <<<
        ys.append(vs[i])
        zs.append(ys[i])

        #update values
        i+=1
        j=1
        round-=1
    #END WHILE

    encr_val = int(str(zs[i])+str(ys[i]),2)
    print('[+] Encrypted value :',hex(encr_val))
    return subkeys,encr_val

#################################################

def decrypt(plain,round,subkeys):

    print('\nDECRYPTION'+'--------------'*2+'\n')

    lk = 32 #key-length
    plain = str(bin(plain)[2:])
    if( len(plain)<lk ): #pad zeros
        plain = '0'*(lk-len(str(plain)))+str(plain)
    y1 = int(plain[0:int(len(plain)/2)],2) #"left" part of plain. TODO if len(plain) is odd? Control
    y1 = bin(y1)[2:]
    z1 = int(plain[int(len(plain)/2):],2) #"right" part of the number
    z1 = bin(z1)[2:]
    if( len(y1)<int(len(plain)/2) ):
        y1 = '0'*(int(len(plain)/2)-len(y1))+y1
    if( len(z1)<int(len(plain)/2) ):
        z1 = '0'*(int(len(plain)/2)-len(z1))+z1
    round = int(round)
    # remark: '&' (AND), '|' (OR), '^' (XOR) operators work bitwise

    #the first index is occupied by a 0 value in order to have congruence with the indexes of the lab
    ys = [0,y1] #array with the various yi ; i=1,..,nr.rounds
    zs = [0,z1] #array with zi
    ws = [0] #arr with wi
    vs = [0] #ar with vi
    j=1
    i=1
    tmp=''
    tmpRound=round
    '''
    what I need to do in decryption, is reversing the order of the subkeys
    and then reiterate the process of the previous one, so reiterate the same
    order for encryption. Remember that in my version, in order to have congruence
    with the indexes of the lab, there is a 0 in the first index (index 0).
    '''
    #REVERSE subkeys' order
    subkeys = subkeys[::-1][0:len(subkeys)-1]
    subkeys.insert(0,0)

    round = tmpRound
    i = 1
    j = 1

    while(round!=0):

        # >>> ROUND function <<<
        while(j<=lk/2):
            if( (j>=1) and (j<=lk/4) ):
                tmp += str( int(str(ys[i])[j-1],2) ^ int(subkeys[i][4*j-3-1],2) )
                j+=1
            else: # j>lk/4 and j<=lk/2
                tmp += str( int(str(ys[i])[j-1],2) ^ int(subkeys[i][4*j-lk-1],2) )
                j+=1
        ws.append(tmp)
        tmp=""

        #>>> LINEAR operation <<<
        tmp = bin(int(ws[i],2) ^ int(zs[i],2))[2:]
        if( len(str(tmp))<16 ):
            tmp = '0'*(16-len(str(tmp)))+str(tmp)
        vs.append(tmp)
        tmp=''

        #>>> TRANSPOSITION <<<
        ys.append(vs[i])
        zs.append(ys[i])

        #update values
        i+=1
        j=1
        round-=1
    #END WHILE

    decr_val = int(str(zs[i])+str(ys[i]),2)
    print('[+] Decrypted value :',hex(decr_val))




if __name__=='__main__':
    file_name = input('Enter file name : ')
    round = input('Enter number of rounds : ')
    key = input('Enter the key-value (HEX number with 0x) : ')
    out=True
    while(out):
        if key[0:2] != '0x':
            key=input('Enter HEX key-value PRE-PENDING \'0x\': ')
        else:
            out=False
    with open(file_name) as file:
        res = encrypt(file,round,key) #N.B.: remember that the very first value is a casual value
                                          # (0) to have consistency with the indexes of the lab
                                      #res[0]->subkeys ; res[1]->encrypted_value to decipher
        if res != None:
            decrypt(res[1],round,res[0])
