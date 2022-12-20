from git import Repo

def read_repos(filename):
    with open(filename, 'r') as repos:
        return [repo.rstrip() for repo in repos]

def clone_repo(link, folder):
    try:
        Repo.clone_from(link, folder)
        with open('cloning.log', 'a') as f:
            f.write(link + ' OK\n')
    except Exception as e:
        print(str(e))
        with open('cloning.log', 'a') as f:
            f.write(link + ' FAIL\n')
        


if __name__ == "__main__":
    with open('cloning.log', 'w'):
        pass #creating/cleaning file

    repos = read_repos('repo_names.txt')
    for repo in repos:
        folder_name = '_'.join(repos[0].split('/')[-2:]).replace('.', '_')
        clone_repo(repo, folder_name)
