import numpy
import math
from numpy import matrix
from numpy import linalg
from itertools import *

gamma = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
def indexof(letter):
    for i in range(0,len(gamma)):
        if letter == gamma[i]:
            return i
    return -1

def clean(text):
    cln = text.lower()
    for ch in text:
        if ch not in gamma:
            cln = cln.replace(ch,'')
    return cln

def dot_product(mat, vec):
    p = len(gamma)
    res = []
    for row in mat:
        if len(row)!=len(vec):
            raise ValueError("Size of mat is different from size of vec")
        res_i = 0
        for i in range(0,len(row)):
            res_i = res_i + row[i]*vec[i]
        res.append(res_i%p)
    return res

def modMatInv(A,p):       # Finds the inverse of matrix A mod p
  n=len(A)
  A=matrix(A)
  adj=numpy.zeros(shape=(n,n))
  for i in range(0,n):
    for j in range(0,n):
      adj[i][j]=((-1)**(i+j)*int(round(linalg.det(minor(A,j,i)))))%p
  return (modInv(int(round(linalg.det(A))),p)*adj)%p

def modInv(a,p):          # Finds the inverse of a mod p, if it exists
  for i in range(1,p):
    if (i*a)%p==1:
      return i
  raise ValueError(str(a)+" has no inverse mod "+str(p))
  
def divide(v1, v2):
	print("So i am dividing "+str(v1)+" for "+str(v2))
	return numpy.divide(v1,v2)

def minor(A,i,j):    # Return matrix A with the ith row and jth column deleted
  A=numpy.array(A)
  minor=numpy.zeros(shape=(len(A)-1,len(A)-1))
  p=0
  for s in range(0,len(minor)):
    if p==i:
      p=p+1
    q=0
    for t in range(0,len(minor)):
      if q==j:
        q=q+1
      minor[s][t]=A[p][q]
      q=q+1
    p=p+1
  return minor
