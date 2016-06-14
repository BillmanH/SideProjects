#Blog analysis through Google analytics

#install.packages("RGoogleAnalytics")
library(RGoogleAnalytics)
library(reshape)

#Load my key
load("C:/Users/Bill/Documents/google-analytics/GoogleAnalytics/toekn_file")

#to confirm that your token is valid.
ValidateToken(token)

#Event Tracking Data:
ql = Init(start.date = format(Sys.Date()-30,"%Y-%m-%d"),
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



#now add a counter that shows the number of days each article ran.
dayCounter <- function(x){
  article <- sorted[sorted$pageTitle==x,]
  firstDate <- article[1,"Date"]
  return(as.numeric((article$Date - firstDate), units="days"))
}

for (title in titles) {
  sorted[sorted$pageTitle==title,"dayNumb"] <- dayCounter(title)
}


#plot some figures to see how how they 
hist(sorted$dayNumb, breaks = 60)  
#not a curve at all, some articles have short lives and some have long lives with few in the middle
plot(sorted$dayNumb,sorted$sessions)
summary(sorted$dayNumb)


