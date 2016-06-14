

'''
Globals 
'''
setwd("C:/Users/Bill/Desktop/cxcscorecard/datafiles")
stoplistdoc <- "C:/Users/Bill/Desktop/Modeling/RModel"
colnamespath <- "C:/Users/Bill/Desktop/Brandwatch/DataFiles/ColNames.txt"

#modelFile <- "C:/Users/data.csv"
#read.csv(modelFile, header = TRUE , sep = ",")

Sys.setenv(NOAWT=TRUE)
options( java.parameters = "-Xmx7g" )

require(mallet)
library(abind)
library(xlsx)
library(R2PPT)
library(ggplot2)
library(ppls)


'''
Functions
'''
#remove twitter pages (faster processing)
documents <- subset(documents, documents$pageType!="twitter")
rownames(documents) <- seq(length=nrow(documents))



#here is the real topic modeling part
#create topic trainer object
textrows<-gsub("[^[:alnum:]]", " ",df$fullText)
mallet.instances <- mallet.import(as.character(df$id), as.character(textrows), stoplistdoc ,token.regexp = "\\p{L}[\\p{L}\\p{P}]+\\p{L}")
set.seed(2015)
doc.topics.final<-NULL
topic.words.final<-NULL

topic.model <- MalletLDA(num.topics=N)
topic.model$loadDocuments(mallet.instances)
vocabulary <- topic.model$getVocabulary()
word.freqs <- mallet.word.freqs(topic.model)
print("Training ....")
topic.model$train(200)
topic.model$maximize(10)

doc.topics <- mallet.doc.topics(topic.model, smoothed=T, normalized=T)
topic.words <- mallet.topic.words(topic.model, smoothed=T, normalized=T)
  
# Output for Topic %ages
doc.topics.out <- data.frame(doc.topics)
colnames(doc.topics.out)<-paste("topic_",N,"_",1:ncol(doc.topics.out),sep="")

# Output for word probabilities for topics
topic.words.out <- data.frame(t(topic.words))
colnames(topic.words.out)<-paste("topic_",N,"_",1:ncol(topic.words.out),sep="")
rownames(topic.words.out)<-vocabulary
topic.words.final<-abind(topic.words.final,topic.words.out)
doc.topics.final.out <- cbind(documents, doc.topics.out)
model1 <- list(model_name,           #1: Text string of model name
			 topic.model,          #2: Java - Mallet object
			 topic.words.final,    #3: Matrix of words/topic scores
			 word.freqs,           #4: DF of words/Term frequecy/Document frequency
			 documents,            #5: The origional document
			 doc.topics.out,       #6: DF of scores 
			 doc.topics.final.out) #7: DF of origional document with scores (very big, not saved to disk locally)
topicnames <- colnames(model1[[3]])
print("Printing ....")
write.csv(doc.topics.out, file=paste(model_path,"doc_topics",Sys.Date(),".csv", sep=""))
write.csv(topic.words.final, file=paste(model_path,"topic_words",Sys.Date(),".csv", sep=""))

drops <- c("fullText","snippet")
docs2 <- doc.topics.final.out[,!(names(doc.topics.final.out) %in% drops)]

print("Evaluating and Scoring ....")
for(i in 1:length(rownames(docs2))){
docs2$highestTopicValue[i] <- max(docs2[i,topicnames])
if(length(topicnames[which(docs2[i,topicnames]==docs2$highestTopicValue[i])])==1){
  docs2$bestTopic[i] <- topicnames[which(docs2[i,topicnames]==docs2$highestTopicValue[i])]
} else {
  docs2$bestTopic[i] <- "No Topic"
}
print(length(docs2$fullText)-i)

  
write.xlsx(docs2, paste(model_name,"/","/out_",model_name,Sys.Date(),".xlsx", sep=""))



make_new_stop_list <- function(model1,threshold=.4){
  #stoplist <- make_new_stop_list(model1,threshold=.4)
  #plot the words to see if you need to add stop words AND at what level you should cut them off. 
  word.freqs <- model1[[4]]
  documents <- model1[[5]]
  word.freqs$sum <- word.freqs$doc.freq / dim(documents)[1]
  plot(word.freqs$sum)
  temp.list <-word.freqs[order(word.freqs$sum,decreasing=TRUE),]
  plot(temp.list$sum)
  stoplist <- as.data.frame(temp.list[temp.list$sum > threshold,]$words)
  write.table(stoplist, file = paste(model1[[1]],"/","stoplist.csv",sep=""), append = FALSE, quote = TRUE, sep = ",")
  #mallet can only read a text file from file, not a dataframe (because it is run in Java, not R), so I am returning the path as opposed to the stoplist.
  path <- paste(getwd(),"/",model1[[1]],"/","stoplist.csv",sep="")
  return(path)
}

model_meta_data <- function(model1){
  docs3 <- model1[[6]]
  topicnames <- colnames(model1[[3]])
  print ("Getting global means and variance...")
  globalMeans <- colMeans(docs3[,topicnames])
  globalVar <- apply(docs3[,topicnames], 2, var)
  
  docs2 <- model1[[7]]
  for(i in 1:length(rownames(docs2))){
    docs2$highestTopicValue[i] <- max(docs2[i,topicnames])
    if(length(topicnames[which(docs2[i,topicnames]==docs2$highestTopicValue[i])])==1){
      docs2$bestTopic[i] <- topicnames[which(docs2[i,topicnames]==docs2$highestTopicValue[i])]
    } else {
      docs2$bestTopic[i] <- "No Topic"
    }
    print(length(docs2$fullText)-i)
  }
  
  return(list(globalMeans,  
              globalVar,
              docs2))
}

score_new_docs_against_model <- function(model1,newFileName,remove_twitter=T,dropText=T,docType="*.csv") {
  model_file <- choose.files(default = "", caption = "Select the file that will train your model",
                             multi = F, filters = docType,
                             index = nrow(Filters)
  )
  mySep <- ","
  if (docType=="*.txt"){mySep <- "\t"}
  if (model_file!="") {
    doc1 <-read.csv(model_file, header = TRUE , sep = mySep)
  } else {
    print("No file was selected. Program Terminated.")
    return (NULL)
  }
  
  topic.words.final <- model1[[3]]
  topicnames <- colnames(topic.words.final)
  topicResults <- NULL
  
  print(dim(doc1))
  if('twitter' %in% colnames(doc1)){
    if(remove_twitter){
      doc1 <- subset(doc1, doc1$pageType!="twitter")
      rownames(doc1) <- seq(length=nrow(doc1))
    }
  }
  print (paste("NumRows",length(rownames(doc1))))
  
  for(i in 1:length(doc1$fullText)){
    print(paste("Length of row ",length(doc1$fullText)-i,sep=""))
    text <- doc1$fullText[i]
    wordList <- tolower(strsplit(gsub("[^[:alnum:] ]", "", text), " +")[[1]])
    newIndex <- wordList[wordList %in% rownames(topic.words.final)]
    shortDF <- topic.words.final[rownames(topic.words.final) %in% newIndex,]
    if(class(shortDF) != "numeric"){
      topicValues <- NULL
      for(j in 1:length(colnames(topic.words.final))){
        topicValues <- c(topicValues,sum(shortDF[,topicnames[j]]))
      }
    } else {
      topicValues <- rep(0,length(topicnames))
      names(topicValues) <- topicnames
    }
    topicResults <- rbind(topicResults,topicValues)
  }
  #merge the results back into your document:
  colnames(topicResults) <- topicnames
  rownames(topicResults) <- 1:length(rownames(doc1))
  #adding those results back to the origional document.
  docs2 <- cbind(doc1,topicResults)
  
  if(dropText) {
    drops <- c("fullText","snippet")
    docs2 <- docs2[,!(names(docs2) %in% drops)]
  }
  #pick top documents from model
  for(i in 1:length(rownames(docs2))){
    docs2$highestTopicValue[i] <- max(docs2[i,topicnames])
    if(length(topicnames[which(docs2[i,topicnames]==docs2$highestTopicValue[i])])==1){
      docs2$bestTopic[i] <- topicnames[which(docs2[i,topicnames]==docs2$highestTopicValue[i])]
    } else {
      docs2$bestTopic[i] <- "No Topic"
    }
    print(length(docs2$fullText)-i)
  }
  write.table(docs2, file = paste(model1[[1]],"_VS_",newFileName,".csv",sep=""), row.names = F, append = FALSE, quote = TRUE, sep = ",")
  return (docs2)
}

#get list of character vector of topic names where the name is the top five words in that topic.
get_good_names <- function(model1){
  wordDF <- model1[[3]]
  goodnames <- NULL
  for (i in 1:length(colnames(wordDF))){
    wordList <- head(sort(wordDF[,i], decreasing = T))
    newTitle <- paste(names(wordList),sep=" ",collapse=" ")
    goodnames <- c(goodnames,newTitle)
  }
  names(goodnames) <- colnames(wordDF)
  return (goodnames)
}

#Normalizes the content score so that the values add up to one. 
get_distributed_scores <- function(model1,newdoc){
  topicnames <- colnames(model1[[6]])
  testDF <- newdoc[,topicnames]
  evenScores <- NULL
  for(i in 1:length(rownames(testDF))){
    scores <- testDF[i,topicnames]
    normalized <- (scores)/(sum(scores))
    evenScores <- rbind(evenScores,normalized)
  }
  newdoc[,topicnames] <- evenScores
  return (newdoc)
}

#This is where your final score is calcualted
#NOTE: High == more different, low == more similar
calcualte_similarity_to_mention <- function(model1,meta_data,scoredDF){
  topicnames <- colnames(model1[[6]])
  
  average_scores <- meta_data[[1]]
  splitScore <- (average_scores - scoredDF[,topicnames])
  absScore <- abs((average_scores - scoredDF[,topicnames]))
  splitScore$RelScore <- rowSums(absScore)
  scorcard <- cbind(scoredDF,splitScore)
  return(scorcard)
}


doc.topics.final.out<-cbind(as.character(documents$full.text),doc.topics.final)
topic.words.final.out<-as.data.frame(topic.words.final)
topic.words.final.out$Total<-rowSums(topic.words.final.out)

topic.words.final.out<-topic.words.final.out[order(topic.words.final.out$Total,decreasing=TRUE),]
month<-"March"
write.csv(doc.topics.final.out[1:10000,], file=paste("doc.topics",month,Sys.Date(),".csv", sep=""), quote=TRUE)
write.csv(topic.words.final.out[1:10000,], file=paste("topic.words",month,Sys.Date(),".csv", sep=""))
write.csv(doc.topics.final.out, file=paste("doc.topicsFull",month,Sys.Date(),".csv", sep=""))





'''
execution
'''

#refer to run file


'''
Graphing
'''
#big DF that has all of the data together
modelDF <- model1[[6]]
modelDF <- subset(modelDF, modelDF$pageType!="twitter")
drops <- c("snippet")
modelDF <- modelDF[,!(names(modelDF) %in% drops)]
rownames(modelDF) <- seq(length=nrow(modelDF))


#MetadataGraph
par(mai=c(1,1.75,1,1))
p <- barplot(normalize.vector(meta_data[[2]]),
             main="Varience of topicality in model",
             horiz=TRUE,
             names.arg = topicnames,
             las=1)

barplot(model1[[6]])
ggplot(model1[[6]],aes(x="pageType"))

ggplot(as.data.frame(normalize.vector(meta_data[[2]])),
       aes(x=normalize.vector(meta_data[[2]]))) + geom_histogram(binwidth=)

p <- ggplot(mtcars, aes(wt, mpg))
format(meta_data[[2]], scientific = FALSE)


