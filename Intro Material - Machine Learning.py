'''
Summary of Native Bayes:
first machine learning
uses bayes rule
Laplaccia smoother
Bag of words
'''
from collections import Counter
from __future__ import division
import numpy as np

dictionary = ["offer",
"is",
"secret",
"click",
"secret",
"link",
"secret",
"sport",
"link",
"play",
"sport",
"today",
"went",
"play",
"sport",
"secret",
"sport",
"event",
"sport",
"sport",
"costs",
"money"]

'''What is the probabilty that a message will be in the spam bucket.
SSSHHHHH or 11100000

p(s) = pi
p(Yi) = {pi if Yi = S,
		1-pi if Yi = H}
		
p(Yi) = pi^Yi * (1-pi)^1-Yi


Bayes network:
(spam) -> w1
		-> w2
		-> w3

p("secret"|spam)=1/3
p("secret"|ham)=

assuming a vocabulary of 12, how many parameters do we need to specify 

#this quesiton made no sense
23
One for prior:
1 for p(spam)
plus two dictionary distribution:
p(wi|spam)
p(wi|HAM)
'''




#using maximum likelyhood estimator what is the probability that M is spam?
m = "sports"

spam = [
"offer is secret",
"click secret link",
"secret sports link"]

ham = [
"play sports today",
"went play sports",
"secret sports event",
"sports is today",
"sports costs money"]

spam = [x.split(" ") for x in spam]		
ham = [x.split(" ") for x in ham]				

#building some dictionaries:
spam_words = Counter()

for mail in spam:
	for word in mail:
		spam_words[word]+=1

ham_words = Counter()

for mail in ham:
	for word in mail:
		ham_words[word]+=1

p_of_m_in_spam = spam_words[m]/sum(spam_words.values())
p_spam = len(spam)/len(spam+ham)
p_of_m_in_ham = ham_words[m]/sum(ham_words.values())
p_ham = len(ham)/len(spam+ham)


p_of_m_is_spam = (p_of_m_in_spam)*(p_spam)/((p_of_m_in_spam)*(p_spam)+(p_of_m_in_ham)*(p_ham))


#using maximum likelyhood estimator what is the probability that M is spam?
m = "secret is secret".split(" ")
p_of_m_in_spam = 1
for word in m:
	p_of_m_in_spam = p_of_m_in_spam*(spam_words[word]/sum(spam_words.values()))
p_of_m_in_ham = 1
for word in m:
	p_of_m_in_ham = p_of_m_in_ham*(ham_words[word]/sum(ham_words.values()))

p_spam = len(spam)/len(spam+ham)
p_ham = len(ham)/len(spam+ham)

p_of_m_is_spam = (p_of_m_in_spam)*(p_spam)/((p_of_m_in_spam)*(p_spam)+(p_of_m_in_ham)*(p_ham))


#using maximum likelyhood estimator what is the probability that M is spam?
m = "today is secret".split(" ")
p_of_m_in_spam = 1
for word in m:
	p_of_m_in_spam = p_of_m_in_spam*(spam_words[word]/sum(spam_words.values()))
p_of_m_in_ham = 1
for word in m:
	p_of_m_in_ham = p_of_m_in_ham*(ham_words[word]/sum(ham_words.values()))

p_spam = len(spam)/len(spam+ham) #the prior for spamness
p_ham = len(ham)/len(spam+ham)

p_of_m_is_spam = (p_of_m_in_spam)*(p_spam)/((p_of_m_in_spam)*(p_spam)+(p_of_m_in_ham)*(p_ham))
#the outcome is zero because we are 'overfitting'

'''
Laplace Smothing
ML p(x) = count(x)/N
LS(k) = (count(x)+k)/(N+k[x])
'''
k = 1
nclasses = 2


p_spams = []
nMessages = 1
nSpam = 1
p_spams.append((nSpam+k)/(nMessages+(k*nclasses)))

nMessages = 10
nSpam = 6
p_spams.append((nSpam+k)/(nMessages+(k*nclasses)))

nMessages = 100
nSpam = 60
p_spams.append((nSpam+k)/(nMessages+(k*nclasses)))

#using the Laplace smoothing for following
k = 1
nwords = 12
ncategories = 2
p_of_m_in_spam = (spam_words["today"]+k)/(sum(spam_words.values())+(k*nwords))
p_spam = (len(spam)+k)/(len(spam+ham)+(k*ncategories))
p_of_m_in_ham = (ham_words["today"]+k)/(sum(ham_words.values())+(nwords))
p_ham = (len(ham)+k)/(len(spam+ham)+(k*ncategories))
answers = [p_spam,p_ham,p_of_m_in_spam,p_of_m_in_ham]


#using the Laplace smoothing for following
m = "today is secret"
a = (len(spam)+k)/(len(spam+ham)+(k*ncategories))
for i in m.split(" "):
	a = a*(spam_words[i]+k)/(sum(spam_words.values())+(k*nwords))
b = (len(ham)+k)/(len(spam+ham)+(k*ncategories))
for i in m.split(" "):
	b = b*(ham_words[i]+k)/(sum(ham_words.values())+(k*nwords))

answer = a/(a+b)

'''
linear regression - section
'''
x = [3,6,4,5]
y = [0,-3,-1,-2]

data = [(x[i],y[i]) for i in range(len(x))]

#change in x over change in y
slope = (data[1][0] - data[0][0]) / (data[1][1] - data[0][1])


'''
0 = slope*x + b
-b+y = slope*x
-b+0 = slope*3
'''
b = -1*(slope*3)

x = np.array(x)
y = np.array(y)

#calculating the slope:
w1 = ((len(x)*sum(x*y)) - (sum(x)*sum(y)))/(len(x)*(sum(x**2))-(sum(x)**2))
w0 = (1/len(x)*sum(y)) - ((w1/len(x))*sum(x))

#quiz:
x = [2,4,6,8]
y = [2,5,5,8]

