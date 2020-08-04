import os
import sys
import maven
import git
import csv
import pandas as pd

#lib_name_version_list = []
#with open('LU_metricsLMP.csv', 'r') as f1:
#    reader = csv.DictReader(f1)
#    for row in reader:
#        lib_name_version_list.append(row['Domain_Libname_Version'])

github_url = []
with open('Projects2019.csv', 'r') as f2:
    reader = csv.DictReader(f2)
    for row in reader:
        github_url.append(row['url'])

open("unavailable_proj.txt", 'w')
f_unavailable_proj = open("unavailable_proj.txt", 'a')
f_first_row = open("project_dependency2019.csv", "w")
f_first_row.write("\"project\",\"dependencies\",\"start\",\"end\"\n")
f_first_row.close()

username, password = '', ''
for id_url, url in enumerate(github_url):
    local_repo = 'projects/' + url.split('/')[-1]
    splited = url.split('//')
    m_url = splited[0] + "//" + username + ":" + password + "@" + splited[1]
    print(id_url + 1, len(github_url), m_url)
    try:
        repo = git.Repo.clone_from(m_url, local_repo)
        new_df = pd.DataFrame(columns=['project', 'dependencies', 'start', 'end'])
        commits = list(repo.iter_commits('master'))

        for idx, commit in enumerate(reversed(commits)):
            repo.git.checkout(commit)
    #        print(idx + 1, len(commits), commit.committed_datetime)
            poms = []
            for dirname in os.walk(local_repo):
                maven.pom_visitor(poms, dirname[0], dirname[2])
            for pom in poms:
                artifactId = pom['artifact'].artifactId
    #            print(artifactId)
                dependency_artifact = pom['dependencies']
                for artifact in dependency_artifact:
                    lib_name_version = "%s-%s-%s" % (artifact.groupId, artifact.artifactId, artifact.version)
#                    if lib_name_version in lib_name_version_list:
    #                    print(artifactId, lib_name_version, commit.committed_datetime)
                    if new_df.loc[(new_df["project"] == artifactId) & (new_df["dependencies"] == lib_name_version)].shape[0] > 0:
                        new_df.loc[(new_df["project"] == artifactId) & (new_df["dependencies"] == lib_name_version), 'end'] = commit.committed_datetime
                    else:
                        new_df = new_df.append([{"project": artifactId, "dependencies": lib_name_version, 
                                        "start": commit.committed_datetime, "end": commit.committed_datetime}])
        new_df.to_csv('project_dependency.csv', mode='a', header=False, index=False)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        f_unavailable_proj.write(url + '\n')
        continue