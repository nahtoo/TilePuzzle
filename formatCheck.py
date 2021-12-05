import sys
import re

def formatCheck(file):
    success = True
    with open(file, 'r') as f:
        output = f.readlines()
        if len(output)!= 1:
            print('Failure: output file should only contain ONE line')
            success = False
            #exit(-1)

        res = output[0].strip('\n')
        if len(re.sub('[LDRU,]', '', res)) !=0:
            print("Failure: invalid characters in '{}'".format(re.sub('[LDRU,]', '', res)))
            print("Failure: only 'L' 'D' 'R' 'U' ',' are valid characters. No blanks.")
            success = False
            #exit(-1)

        moves = res.split(',')
        for m in moves:
            if(len(m) != 1):
                print("Failure: 'L' 'D' 'R' 'U' must be separated by ','. No extra ','.")
                success = False
                break
                #exit(-1)
    if success:
        print('Success: format check passed')
    else:
        print('Failure: format check failed')


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Error: invalid arguments!')
        print('usage: python formatCheck.py <output_file>')
        exit(-1)

    output_file = sys.argv[1]
    formatCheck(output_file)