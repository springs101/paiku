import random
import itertools
import copy
import numpy as np
import os, sys


def chulipai():
    pokers = []
    poker11 = []
    for i in ['hx', 'ht', 'fk', 'ch']:
        for j in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']:  # 1:A 11:J 12:Q 13:K
            poker11.append(i)
            poker11.append(j)
            pokers.append(poker11)
            poker11 = []

    dawang = ['bigboss', '0']
    xiaowang = ['littleboss', '0']
    pokers.append(dawang)
    pokers.append(xiaowang)
    return pokers


def player_ku(playid, list1, objlist=None, oblist1=None):
    list_temp = copy.deepcopy(list1)
    if not (objlist is None):
        for val in objlist:
            list_temp.remove(val)

    if not (oblist1 is None):
        for val1 in oblist1:
            list_temp.remove(val1)

    playlist = itertools.combinations(list_temp, 17)
    # for val2 in playlist:
    #     print("play" + playid + ":" + val2)

    return playlist


def random_left(list1, objlist=None, oblist1=None, oblist2=None):
    resarray = []
    list_temp = copy.deepcopy(list1)
    if not (objlist is None):
        for val in objlist:
            list_temp.remove(val)

    if not (oblist1 is None):
        for val2 in oblist1:
            list_temp.remove(val2)

    if not (oblist2 is None):
        for val3 in oblist2:
            list_temp.remove(val3)

    return list_temp


def is_containboom(objlist):
    data = np.asarray(objlist)
    data = data[data[:, 1].argsort()]

    # print(data)

    [rows, cols] = data.shape
    for i in range(rows):
        if i < (rows - 2):
            if (int(data[i, 1]) == 0) & (int(data[(i + 1), 1]) == 0):
                return True
        if i < (rows - 4):
            if (data[i, 1] == data[(i + 1), 1]) & (data[(i + 1), 1] == data[(i + 2), 1]) & \
                    (data[(i + 2), 1] == data[(i + 3), 1]) & (data[(i + 3), 1] == data[(i + 4), 1]):
                return True

    return False


def is_landui(objlist):
    data = np.asarray(objlist)
    data = data[data[:, 1].argsort()]

    # print(data)

    [rows, cols] = data.shape
    for i in range(rows):
        if i < (rows - 7):
            if data[i, 1] == 0:
                continue
            if (data[i, 1] == data[(i + 1), 1]) & (data[(i + 2), 1] == data[(i + 3), 1]) & \
                    (data[(i + 4), 1] == data[(i + 5), 1]):
                if (int(data[i, 1]) + 1 == int(data[(i + 2), 1])) & (int(data[i, 1]) + 2 == int(data[(i + 4), 1])):
                    return True
    return False


def is_huiji(objlist):
    data = np.asarray(objlist)
    data = data[data[:, 1].argsort()]

    # print(data)

    [rows, cols] = data.shape
    for i in range(rows):
        if i < (rows - 7):
            if (data[i, 1] == data[(i + 1), 1]) & (data[(i + 1), 1] == data[(i + 2), 1]) \
                    & (data[(i + 3), 1] == data[(i + 4), 1]) & (data[(i + 4), 1] == data[(i + 5), 1]):
                if (int(data[i, 1]) != 2) & (int(data[(i + 3), 1]) != 2):
                    return True
    return False


def is_record(player1, player2, player3):
    player1_sel = False
    player2_sel = False
    player3_sel = False
    if is_containboom(player1) | is_landui(player2) | is_huiji(player3):
        player1_sel = True
    if is_containboom(player2) | is_landui(player2) | is_huiji(player2):
        player2_sel = True
    if is_containboom(player3) | is_landui(player3) | is_huiji(player3):
        player3_sel = True

    if player1_sel & player2_sel & player3_sel:
        return True

    return False


if __name__ == '__main__':
    print("start!!")
    poker1 = chulipai()
    new_s = []
    new_v = []
    new_k = []
    random.shuffle(poker1)
    iCount = 0
    ifileCont = 0
    ictrlcount1 = 0
    ictrlcount2 = 0
    ictrlcount3 = 0
    li = {}
    # b = random.sample(poker1, 17)
    b = itertools.combinations(poker1, 17)
    for s in b:
        if ictrlcount1 > 1:
            ictrlcount1 = 0
            continue
        play2 = player_ku(2, poker1, s)
        for v in play2:
            if ictrlcount2 > 1:
                ictrlcount2 = 0
                ictrlcount1 += 1
                break
            play3 = player_ku(3, poker1, v, s)
            for k in play3:
                new_s = list(s)
                new_v = list(v)
                new_k = list(k)
                leftlist = random_left(poker1, s, v, k)
                leftlist = list(leftlist)
                isR = is_record(new_s, new_v, new_k)
                if not isR:
                    continue
                if ictrlcount3 > 2:
                    ictrlcount3 = 0
                    ictrlcount2 += 1
                    break
                ictrlcount3 += 1
                with open('d:\paiku' + str(ifileCont), 'ab+') as f:
                    numpy_s = np.asarray(new_s)
                    numpy_v = np.asarray(new_v)
                    numpy_k = np.asarray(new_k)
                    numpy_left = np.asarray(leftlist)
                    f.write('\nplayer1\n'.encode())
                    np.savetxt(f, numpy_s, delimiter=',', fmt='%s')
                    f.write('\nplayer2\n'.encode())
                    np.savetxt(f, numpy_v, delimiter=',', fmt='%s')
                    f.write('\nplayer3\n'.encode())
                    np.savetxt(f, numpy_k, delimiter=',', fmt='%s')
                    f.write('\nleftthree\n'.encode())
                    np.savetxt(f, numpy_left, delimiter=',', fmt='%s')
                    iCount += 1
                    if iCount >= 20000:
                        ifileCont += 1
                        if ifileCont >= 50:
                            sys.exit(1)
                        iCount = 0
                        print("++++++++++++file" + str(iCount))

                    f.write("====================================".encode())

    print("------------------------end!!---------------------------------------------")
