"""
Crowdsourcing to analyze belief systems underlying social issues
Prepare directories of Ding et al. 2015 financial news data for modeling
J. Hunter Priniski and Keith Holyoak
"""
import shutil
import os

#create structured dataset for Reuters dataset

root = os.getcwd()
path = 'financial-news-dataset-master/ReutersNews106521/'

# move all files into TextFiles directory.
destination = 'financial-news-dataset-master/TextFiles'

#covert each file to a .txt file
for dir in os.listdir(path):

    if os.path.isdir(path + dir):

        path_dir = path + dir

        for file in os.listdir(path_dir):

            path_file = path_dir + '/' + file

            if not os.path.isfile(path_file):
                continue

            head, tail = os.path.splitext(path_file)

            if not tail:
                src = os.path.join(root, path_file)
                dst = os.path.join(root, path_file + '.txt')

                if not os.path.exists(dst):
                    os.rename(src, dst)
                    shutil.move(path_file + '.txt', destination)


    else:
        continue
