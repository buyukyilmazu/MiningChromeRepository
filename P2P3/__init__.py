import github
import operator
import datetime
import matplotlib.pyplot as plt

accounts = {"social": TOKEN,}

token = accounts["social"]
client = github.Github(token, per_page=100)

screen_name = "scheib"
repository_name = "chromium"

user = client.get_user(screen_name)
repo = user.get_repo(repository_name)

while (True):
    first_commit_date = raw_input("Please give the date of first commit (Format: YYYY-MM-DD): ")
    try:
        datetime.datetime.strptime(first_commit_date, '%Y-%m-%d')
        break
    except:
        print "Incorrect data format, should be YYYY-MM-DD"

user_list = dict()

#to find commits which are at spesific time intervals
for commit in repo.get_commits():
    if commit.commit is not None:
        authorOfCommit = commit.commit.author
        if str(authorOfCommit.date) > first_commit_date:
            if authorOfCommit.name in user_list:
                user_list[authorOfCommit.name] += 1
            else:
                user_list[authorOfCommit.name] = 1
        else:
            break

#to find total commits
total_commit = 0
for i in user_list.values():
    total_commit += i

#calculating %80 of total commit
top_developer = (total_commit * 80) / 100


#user list sorted by number of commit descending
user_list = sorted(user_list.items(), key=operator.itemgetter(1), reverse=True)

flag = 0

#to print top developer's name
for i in range(len(user_list)):
    flag += user_list[i][1]
    if flag >= top_developer:
        break
    else:
        print user_list[i][0]

user_list = dict(user_list)

plt.bar(range(len(user_list)), user_list.values(), align='center')
plt.xticks(range(len(user_list)), user_list.keys())
plt.show()