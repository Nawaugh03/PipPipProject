import tweepy


class TweetManager:
    def __init__(self):
        consumer_key = "9Vtlzmn3FYY9z5KKZx5RsnfG7"
        consumer_secret = "K9MAfLBjUiSDEzsOl9A7QWPzP7eBRLmn74pmZBKLDQwcs00bn6"
        access_token = "1042132884742701056-rmvBaiu8yw1R6F27tk0r2MMFAjrb0t"
        access_token_secret = "39xDtA2Of0UEvlJoGiOsACwPv7vy1s29I7hrJlT9zo0dJ"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.content = []
        self.getTwitterUser()
        #self.AddTwitterMessagestofile();

    def AddTwitterMessagestofile(self):
        with open("Messages.txt", 'w') as mf:
            for i in range(len(self.content)):
                mf.write(self.content[i])
            
    def getTwitterUser(self): #This function collect users from list and their recent tweets.
        with open("Followers.txt") as infile:
            for line in infile:
                if "**" in line:
                    pass
                elif '@' in line:
                    line = line.lower()
                    line=line.replace('\n','')
                    line=line.split(":")
                    line.append(self.GetRecentTweet(line[1]))
                    self.content.append(line)

    def AddtoFile(self):
        with open('Followers.txt','w') as wf:
            wf.write("**Name:TwitterUsername**\n")
            for words in self.content:
                wf.write(str(words[0])+":"+words[1].lower()+"\n")

    def GetRecentTweet(self,user):
        a=""
        cursor = tweepy.Cursor(self.api.user_timeline, id=user, tweet_mode="extended").items(1)
        for i in cursor:
            a=i.full_text
        return a

    def CheckTweetUpdate(self,Tweet,pos):
        if(Tweet!=self.content[pos][2]):
            return True
        return False
    
    def CheckUpdates(self):#Check if there is an new tweet in the Q user.
        for i in range(len(self.content)):
            #print(self.content[i][2])
            #print(self.GetRecentTweet(self.content[i][1]))
            if (self.CheckTweetUpdate(self.GetRecentTweet(self.content),i)):
                return True
            #if self.content[i][2] in self.GetRecentTweet(self.content[i][1]):
            #    print(self.content[i][2]!=self.GetRecentTweet(self.content[i][1]))
            #    return False
        return False

    

    def SetNotifications(self):
        UpdatedUsers = []
        for i in range(len(self.content)):
            CurrentUser=self.content[i][1]
            A=self.GetRecentTweet(CurrentUser)
            #if(self.CheckTweetUpdate(A,i))==True:
            UpdatedUsers.append([CurrentUser,A])
        return UpdatedUsers

    def RemoveUser(self,UserName):
        tempContent=[]
        for items in self.content:
            if items[1]==UserName:
                self.RemovefromFile(items[1])
            else:
                tempContent.append(items)
        self.content=tempContent

    def RemovefromFile(self, UserName):
        lines=[]
        with open("Followers.txt",'r') as f:
            lines=f.readlines()
        with open("Followers.txt","w") as f:
            for line in lines:
                if UserName.lower() in line:
                    pass
                else:
                    f.write(line)
    def AddUser(self,Usernames=""):
        a=""
        Msg=""
        if not '@' in Usernames:
            Usernames='@'+Usernames
        Usernames.replace(" ", "")
        Users=Usernames.split(",")
        for i in Users:
            if i=="":
                Msg+="Error: Requires Usename\n"
            else:
                if(self.GetRecentTweet(i)==False):
                    Msg+="Error: invalid Username: "+ i+"\n"
                elif self.FindUsername(i):
                    Msg+=str(i)+" already in storage\n"
                else:
                    a=self.GetRecentTweet(i)
                    user=self.api.get_user(screen_name=i)
                    id=user.name
                    self.content.append([id,i,a])
                    self.AddtoFile()
                    Msg+=str(i)+" Added\n"
        return Msg

    def FindUsername(self,Username):
        temp=[]
        with open("Followers.txt") as w:
            temp=w.readlines()
        for i in temp:
            if Username in i:
                return True
        return False

    def ReadContent(self):
        return self.content
'''
#use the following to read tweets
consumer_key = "9Vtlzmn3FYY9z5KKZx5RsnfG7"
consumer_secret = "K9MAfLBjUiSDEzsOl9A7QWPzP7eBRLmn74pmZBKLDQwcs00bn6"
access_token = "1042132884742701056-rmvBaiu8yw1R6F27tk0r2MMFAjrb0t"
access_token_secret = "39xDtA2Of0UEvlJoGiOsACwPv7vy1s29I7hrJlT9zo0dJ"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
cursor= tweepy.Cursor(api.user_timeline, id="@elonmusk", tweet_mode="extended").items(1)
for i in cursor:
    print(i.full_text)
'''
