#Blog analysis through Google analytics

#install.packages("RGoogleAnalytics")
library(RGoogleAnalytics)
library(reshape)

#Load my key
load("C:/Users/Bill/Documents/google-analytics/GoogleAnalytics/toekn_file")

#to confirm that your token is valid.
ValidateToken(token)

#Event Tracking Data:
ql = Init(start.date = format(Sys.Date()-120,"%Y-%m-%d"),
			end.date = format(Sys.Date(),"%Y-%m-%d"),
			metrics =  "ga:sessions",
			dimensions = "ga:pageTitle,
			ga:date",
			max.results = 10000,
			table.id = "ga:56928074")

gq = QueryBuilder(ql)

gd = GetReportData(gq, token, paginate_query = F)

#home page not defined
gd[gd$pageTitle=="(not set)","pageTitle"]<-"home"
gd[gd$pageTitle=="home",]

#set date to Date object -- Google Analytics has a wierd date format
#gd[,"date"] <- as.numeric(gd$date)
gd[,"date"] <- as.character(gd$date)
gd[,"Date"] <- as.Date(gd$date, "%Y%m%d")


#Going to filter by days
titles = unique(gd$pageTitle)
#sort by title and date
sorted <-arrange(gd,pageTitle,date)


sorted$wdy <- weekdays(sorted$Date)


#functions to transform data:

#now add a counter that shows the number of days each article ran.
dayCounter <- function(x){
	article <- sorted[sorted$pageTitle==x,]
	firstDate <- article[1,"Date"]
	return(as.numeric((article$Date - firstDate), units="days"))
}

#day of week published
publishDay <- function(x){
	article <- sorted[sorted$pageTitle==x,]
	firstDate <- article[1,"Date"]
	return(rep(weekdays(firstDate),nrow(article)))
}

#Determine if the sessions are sparatic or successive
isSuccessive <- function(x){
	article <- sorted[sorted$pageTitle==x,]
	j = article$dayNumb+1
	return(rep(all(j - c(1:length(j))==max(j - c(1:length(j)))),nrow(article)))
}
#Max number of days out
maxDaysOut <- function(x){
	article <- sorted[sorted$pageTitle==x,]
	return(rep(max(article$dayNumb),nrow(article)))
}

#Median number of days out
medianDaysOut <- function(x){
	article <- sorted[sorted$pageTitle==x,]
	return(rep(median(article$dayNumb),nrow(article)))
}

#indicate if the article was still being viewed after thirty days.
viewedAfterThirtyDays <- function(x){
	article <- sorted[sorted$pageTitle==x,]
	return(rep(any(article$dayNumb > 30),nrow(article)))
}

any(article$dayNumb > 30)

for (title in titles) {
	print(title)
	sorted[sorted$pageTitle==title,"dayNumb"] <- dayCounter(title)
	sorted[sorted$pageTitle==title,"publishDay"] <- publishDay(title)
	sorted[sorted$pageTitle==title,"isSuccessive"] <- isSuccessive(title)
	sorted[sorted$pageTitle==title,"maxDaysOut"] <- maxDaysOut(title)
	sorted[sorted$pageTitle==title,"isSuccessive"] <- isSuccessive(title)
	sorted[sorted$pageTitle==title,"isSuccessive"] <- viewedAfterThirtyDays(title)
}



#plot some figures to see how how they 
hist(sorted$dayNumb, breaks = 60)  
plot(sorted$dayNumb,sorted$sessions)
summary(sorted$dayNumb)
ecdf(sorted$dayNumb)


library(ggplot2)
ggplot(sorted, aes(x=publishDay, y=dayNumb)) + geom_bar(stat="bin")

table(sorted$publishDay,sorted$dayNumb)
