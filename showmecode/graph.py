#!/usr/bin/env python3
# -*- coding: utf8 -*-
#test for fugitive tttttt

class EdgeNode(object):
    def __init__(self):
        self.adjvex = None
        self.next = None

class VertexNode(object):
    def __init__(self,data = "#"):
        self.data = data
        self.firstedge = None
    def __str__(self):
        return "Instance of VertexNode %s,%s" % (self.data,self.firstedge)

class Graph(object):
    def __init__(self,vnum,enum):
        self.numVertexes = vnum
        self.numEdges = enum
        self.adjlist = []
        for i in range(1,100):
            self.adjlist.append(VertexNode())

        for i,v in enumerate([1,2,3,4]):
            self.adjlist[i].data = "v" + str(v)
            self.adjlist[i].firstedge = None

        for e in range(0,enum):
            print ("please input the edge number of (vi,vj)")
            p = "v" + str(input())
            q = "v" + str(input())
            m = self._locate(self,p)
            n = self._locate(self,q)
            if m != -1 and n != -1:
                edgei = EdgeNode()
                edgei.adjvex = n
                edgei.next = self.adjlist[m].firstedge
                self.adjlist[m].firstedge = edgei

                edgej = EdgeNode()
                edgej.adjvex = m
                edgej.next = self.adjlist[n].firstedge
                self.adjlist[n].firstedge = edgej

    def _locate(self,g,ch):
        for i in range(0,len(g.adjlist)):
            if ch == g.adjlist[i].data: return i
        return -1

    def printGraph(self,g):
        i = 0
        while (i <= 100 and g.adjlist[i].firstedge):
            print g.adjlist[i].data
            e = g.adjlist[i].firstedge
            while e:
                print e.adjvex
                e = e.next
            i += 1
            print

g1 = Graph(4,6)

g1.printGraph(g1)
