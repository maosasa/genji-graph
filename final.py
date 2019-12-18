#源氏物語第１部系図
#婚姻関係を双方向の有向グラフ（無向グラフ）で表し、親子関係を親から子への有向グラフで表す。
#実血縁関係を偽っている場合（薫や冷泉帝）は、表向きの血縁関係のみグラフに表す。
'''
1 右大臣
2 弘徽殿
3 朧月夜
4 左大臣
5 頭中将
6 葵上
7 夕顔
8 玉鬘
9 桐壺帝
10 桐壺更衣
11 朱雀帝
12 女三宮
13 柏木
14 雲居雁
15 薫
16 夕霧
17 光源氏
18 明石上
19 明石姫君
20 六条御息所
21 斎宮
22 花散里
23 先帝
24 藤壺中宮
25 兵部卿宮
26 紫上
27 冷泉帝
'''

name = ["","右大臣","弘徽殿","朧月夜","左大臣","頭中将","葵上","夕顔","玉鬘","桐壺帝","桐壺更衣","朱雀帝","女三宮","柏木","雲居雁","薫","夕霧","光源氏","明石上","明石姫君","六条御息所","斎宮","花散里","先帝","藤壺中宮","兵部卿宮","紫上","冷泉帝"]

graph='''27
1 2
1 3
2 9
2 11
3 17
4 5
4 6
5 7
5 8
5 13
5 14
6 16
6 17
7 5
7 8
7 17
9 2
9 10
9 11
9 17
9 24
10 9
10 17
11 12
12 17
12 15
12 13
13 12
13 15
17 3
17 6
17 7
17 12
17 16
17 18
17 19
17 20
17 22
17 24
17 26
17 27
18 17
18 19
20 17
20 21
22 17
23 24
23 25
24 9
24 17
24 27
25 26
26 17'''

class DiGraph:
    def __init__(self,g):
        lines = g.split("\n")
        self.size = int(lines[0])
        self.list = [[] for i in range(self.size+1)]
        for s in lines[1:]:
            d1,d2 = s.split(" ")
            self.connect1(int(d1),int(d2)) # ここをconnect1にすればOK
    def connect1(self, x, y):
        self.list[x].append(y) # xの隣接リストにyを追加する。
    def to_s(self):
        s = []
        for i in range(len(self.list)):
            for j in self.list[i]:
                s.append([i, j]) # [i,j]が隣接した頂点
        return s
    def trav(self,frm,to):#全てのルート
        print(name[frm],"から",name[to],"までの全ての経路")
        self.fmap = [None for i in range(len(self.list))]
        self.travx(frm, frm, to)
        print("")
    def trav2(self, frm, to):#幅優先探索
        print(name[frm],"から",name[to],"までの最短の経路")
        self.fmap = [None for i in range(self.size+1)]
        q = []             # Pythonの配列を待ち行列(queue)のように使う
        d = frm
        while d != to:
            for u in self.married(d):
                if u != frm: # frmに戻ってしまわないようにする.
                    if self.fmap[u] == None:
                        self.fmap[u] = [d,0]#婚姻関係なら0を付け足しておく
                        q.append(u)
            for u in self.parent(d):
                if u != frm: # frmに戻ってしまわないようにする.
                    if self.fmap[u] == None:
                        self.fmap[u] = [d,1]#親なら1を付け足しておく
                        q.append(u)
            for u in self.children(d):
                if u != frm: # frmに戻ってしまわないようにする.
                    if self.fmap[u] == None:
                        self.fmap[u] = [d,2]#子なら2を付け足しておく
                        q.append(u)
            if len(q) == 0:
                break
            d = q.pop(0) # qの先頭を取り出し(qからは除き)
        if d == to:                # 目的地に到着していたら、
            self.trace(to,frm)          # 経路を示す。
        print("")
    def travx(self, frm, d, to):
        if d == to:
            self.trace(to,frm)
            return # toに到達したら戻る
        for u in self.married(d):
            if u != frm: # frmに戻ってしまわないようにする.
                if self.fmap[u] == None:
                    self.fmap[u] = [d,0]#婚姻関係なら0を付け足しておく
                    self.travx(frm,u,to)
                    self.fmap[u] = None # uを元に戻して他の可能性を調べる。
        for u in self.parent(d):
            if u != frm: # frmに戻ってしまわないようにする.
                if self.fmap[u] == None:
                    self.fmap[u] = [d,1]#親なら1を付け足しておく
                    self.travx(frm,u,to)
                    self.fmap[u] = None # uを元に戻して他の可能性を調べる。
        for u in self.children(d):
            if u != frm: # frmに戻ってしまわないようにする.
                if self.fmap[u] == None:
                    self.fmap[u] = [d,2]#子なら2を付け足しておく
                    self.travx(frm,u,to)
                    self.fmap[u] = None # uを元に戻して他の可能性を調べる。
    def trace(self, frm, to):
        last = frm
        a = []
        frm=self.fmap[frm]
        while frm[0] != to :
            a.append(frm)
            frm = self.fmap[frm[0]]
        a.append(frm)
        rltn=""
        for i in (reversed(a)):
            if i[1]==0: rltn="配偶者"
            if i[1]==1: rltn="親"
            if i[1]==2: rltn="子"
            print(name[i[0]],"の",rltn,"である",end="")
        print(name[last])

    def relation(self,d):#dの持つ親族関係を全て示す
        print(name[d],"の血縁関係")
        print("婚姻関係: ",end="")
        for i in self.married(d):
            print(name[i],end=" ")
        print("")
        print("親: ",end="")
        for i in self.parent(d):
            print(name[i],end="")
        print("")
        print("子: ",end="")
        for i in self.children(d):
            print(name[i],end=" ")
        print("")
        print("")
    def married(self,d):#dの持つ婚姻関係があればリストに追加
        marriedlist = []
        for u in self.list[d]:
            if d in self.list[u]:
                marriedlist.append(u)
        return marriedlist
    def parent(self,d):#dの親がいればリストに追加
        parentlist = []
        for u in range(1,self.size+1):
            if d in self.list[u] and u not in self.list[d]:
                parentlist.append(u)
        return parentlist
    def children(self,d):#dの子がいればリストに追加
        childrenlist = []
        for u in self.list[d]:
            if d not in self.list[u]:
                childrenlist.append(u)
        return childrenlist


def test():
    g=DiGraph(graph)
    #g.trav(24,26)#任意の2人の血縁関係（誰を経由しているか）を示す
    #g.trav2(24,26)#任意の2人の血縁関係の最短経路を示す
    #g.relation(17)#任意の1人について、直接の婚姻関係、親子関係を示す
    g.trav2(5,23)
    g.relation(7)
test()

