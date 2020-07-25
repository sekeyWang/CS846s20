import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import bisect
def f1(df, libraries):
    '''
    f1 is used to analyse LU of a dependency
    '''
#    library = "junit-junit-3.8.1"
    date_time_obj = datetime.datetime.fromisoformat('2016-01-01 00:00:00+00:00')
    for library in libraries:
        l_df = df.loc[(df["dependencies"] == library)] 
        record = []
        for index, row in l_df.iterrows():
        #    print(datetime.datetime.fromisoformat(row['start']))
            start, end = datetime.datetime.fromisoformat(row['start']), datetime.datetime.fromisoformat(row['end'])
            record.append({'date': start, 'label' : 1})
            record.append({'date': end, 'label' : -1})

        record = sorted(record, key=lambda parameter: parameter['date'])
        x, y, lu = [], [], 0
        for r in record:
            if r['date'] > date_time_obj:
                break
            lu += r['label']
            y.append(lu)
            x.append(r['date'])

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%y-%m"))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=300))
        plt.plot(x, y, label = library)
        plt.gcf().autofmt_xdate()
    plt.legend()
    plt.show()

def f2(df):
    '''
    f2 is to analyse the number of projects and dependencies
    '''
    print(len(df['project']))
    print(len(np.unique(df['project'])))
    print(len(np.unique(df['dependencies'])))

def f3(df):
    '''
    f3 is to analyse how many dependency a project has
    '''
    library_numbers = df.groupby(['project']).size()
    plt.boxplot(library_numbers)
    plt.show()

def f4(df):
    '''
    f4 is to analyse how many version does dependency have
    '''
    library_version_name = df['dependencies']
    dependency_name = [x[:x.rfind('-')] for x in df['dependencies']]
    dependency_version = [x[x.rfind('-')+1:] for x in df['dependencies']]
    print(dependency_name[0], dependency_version[0])
    df['name'] = dependency_name
    df['version'] = dependency_version
    name_version = df.groupby(['name', 'version']).size()
    print(name_version.head(5))
    names = name_version.groupby('name').size()
    plt.boxplot(names)
    plt.show()

def f5(df):
    '''
    f5 is to find the Peak LU of each dependency
    '''
    libraries = np.unique(df['dependencies'])
    max_LU_list = []
    for library in libraries:
        l_df = df.loc[(df["dependencies"] == library)] 
        record = []
        for index, row in l_df.iterrows():
            start, end = datetime.datetime.fromisoformat(row['start']), datetime.datetime.fromisoformat(row['end'])
            record.append({'date': start, 'label' : 1})
            record.append({'date': end, 'label' : -1})
        record = sorted(record, key=lambda parameter: parameter['date'])
        LU, max_LU = 0, 0
        for r in record:
            LU += r['label']
            max_LU = max(max_LU, LU)
        max_LU_list.append(max_LU)
    max_LU_list = sorted(max_LU_list)
#    print(max_LU_list)
    y = []
    for i in range(200):
        y.append(bisect.bisect_right(max_LU_list, i) / len(max_LU_list))
    plt.plot(np.arange(200), y)
    plt.xscale('log')
    plt.hlines(0.75, 0, 200)
    plt.vlines(2.8, 0, 1)
#    plt.yticks(['{:,.2%}'.format(x) for x in y])
    plt.show()

def f6(df):
    '''
    f5 is to calculate pre-peak
    '''
    libraries = np.unique(df['dependencies'])
    days = []
    for library in libraries:
        l_df = df.loc[(df["dependencies"] == library)] 
        record = []
        for index, row in l_df.iterrows():
            start, end = datetime.datetime.fromisoformat(row['start']), datetime.datetime.fromisoformat(row['end'])
            record.append({'date': start, 'label' : 1})
            record.append({'date': end, 'label' : -1})
        record = sorted(record, key=lambda parameter: parameter['date'])
        LU, max_LU = 0, 0
        init_date = record[0]['date']
        for r in record:
            LU += r['label']
            if LU > max_LU:
                peak_date = r['date']
            max_LU = max(max_LU, LU)
        post_peak = (peak_date - init_date).days
        days.append(post_peak)
    days = sorted([x for x in days if x != 0])

    y = []
    for i in range(3000):
        y.append(bisect.bisect_right(days, i) / len(days))
    plt.plot(np.arange(3000), y)
    plt.hlines(0.75, 0, 3000)
    plt.vlines(560, 0, 1)
    plt.show()

#    print(days)

if __name__ == "__main__":
    df = pd.read_csv('project_dependency.csv')
    f1(df, ['junit-junit-3.8.1', 'junit-junit-4.10', 'junit-junit-4.11'])