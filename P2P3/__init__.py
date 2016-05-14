import github
import operator
import datetime
import matplotlib.pyplot as plt
import networkx as NX

accounts = {"social": '95a5b5a8a29b5144ff088c657410f6f87f525c73',}

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

commit_list = []

count = 0
for commit in repo.get_commits():
    if commit.commit is not None:
        authorOfCommit = commit.commit.author
        if str(authorOfCommit.date) > first_commit_date:
            commit_list.append([authorOfCommit.name])
            commit_list[count].append(str(authorOfCommit.date))
            count += 1
        else:
            break

G = NX.DiGraph()
for commit in repo.get_commits():
    authorOfCommit = commit.commit.author
    if str(authorOfCommit.date) > first_commit_date:
        for parent in commit.parents:
            G.add_edge(parent.sha, commit.sha)
    else:
        break
print G.number_of_nodes(), G.number_of_edges()



NX.draw(G, cmap = plt.get_cmap('jet'), node_color = 'b')
plt.show()