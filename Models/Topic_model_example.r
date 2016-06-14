
# A new, a vast, and a powerful language is developed
# for the future use of analysis, in which to wield its
# truths so that these may become of more speedy and 
# accurate practical application for the purposes of 
# mankind than the means hitherto in our possession have
# rendered possible. 
#  - Ada Lovelace


#This changes R's java paramaters so that it can handle larger datafiles
options( java.parameters = "-Xmx7g" )
#setup the workspace
# Set working directory
dir <- "C:/Users/Bill/Desktop/" # adjust to suit
setwd(dir)

#you will need these libraries:
require(mallet)
library(abind)
library(XLConnect)



#load the file from BW:
#using the 'fulltext' export excel sheet
#note: the excel sheet has 8 empty rows that are not part of the table
df <- readWorksheet(loadWorkbook("text.xlsx"),startRow = 8,sheet=1)


dim(df) #should be 137 columns
df$id<-df$Resource.Id
df$full.text<-df$Full.Text

#here are some cleaning examples you will probably want to customize this part a lot.
for (j in 1:nrow(df)) {
  df$full.text[j] <- gsub("http://t.co/.*", "",df$full.text[j])
}
textrows<-gsub("Ã¢", "",df$full.text)
textrows<-gsub("[^[:alnum:]]", " ",textrows)
# Use the first pared set of df
# textrows<-gsub("[^[:alnum:]]", " ",df.pared.1$text.m)
length(textrows)

#---Modeling---
mallet.instances <- mallet.import(as.character(df$id),
                                  as.character(textrows),
                                  "StopList_en.txt",
                                  token.regexp = "\\p{L}[\\p{L}\\p{P}]+\\p{L}")
set.seed(2015)

numTopics <- 50 #how many topics do you want in this model.
topic.model <- MalletLDA(numTopics)
topic.model$loadDocuments(mallet.instances)

## Get the vocabulary, and some statistics about word frequencies.
## These may be useful in further curating the stopword list.
vocabulary <- topic.model$getVocabulary()
word.freqs <- mallet.word.freqs(topic.model)

## Optimize hyperparameters every 20 iterations,
## after 50 burn-in iterations.
topic.model$setAlphaOptimization(20, 50)

## Now train a model. Note that hyperparameter optimization is on, by default.
## We can specify the number of iterations. Here we'll use a large-ish round number.
topic.model$train(200)

## Run through a few iterations where we pick the best topic for each token,
## rather than sampling from the posterior distribution.
topic.model$maximize(10)

## Get the probability of topics in documents and the probability of words in topics.
## By default, these functions return raw word counts. Here we want probabilities,
## so we normalize, and add "smoothing" so that nothing has exactly 0 probability.
doc.topics <- mallet.doc.topics(topic.model, smoothed=T, normalized=T)
topic.words <- mallet.topic.words(topic.model, smoothed=T, normalized=T)

# Output for Topic 
doc.topics.out <- data.frame(doc.topics)
colnames(doc.topics.out)<-paste("topic_",1:ncol(doc.topics.out),sep="")

# Output for word probabilities for topics
topic.words.out <- data.frame(t(topic.words))
colnames(topic.words.out)<-paste("topic_",1:ncol(topic.words.out),sep="")
rownames(topic.words.out)<-vocabulary

#final tables:
doc.topics.out<-cbind(df$id,as.character(df$full.text),doc.topics.out)

topic.words.final.out<-as.data.frame(topic.words.out)
topic.words.final.out$Total<-rowSums(topic.words.final.out)

#save your files often!!
write.csv(topic.words.final.out[1:10000,], file=paste("topic.words",Sys.Date(),".csv", sep=""))
write.csv(doc.topics.out, file=paste("doc.topicsFull",Sys.Date(),".csv", sep=""))
