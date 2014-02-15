Related-Video
=============
The repository implement a similar video algorithm. A brief description is as follow:

Input Data:
CodeAssignmentDataSet.json

Output Data:
tag.csv           #tagging information for each video
output.txt        #list of top 3 related video of each video

Get Started:
Choose a directory to the input data and output data. Make sure the computer has internet accees, because the program 
needs to fetch data from wikipedia website. Run the 'tag.py' from the Command Line, and follow the message to type in
the complete directory. It takes about 6 minutes for the program to run. After that, you will find the tagging information
in 'tag.csv' and list of top 3 related video of each video


Step1.
By scrapping data from wikipedia, the program build up vocabulary on famous American actors, movies, and television shows.

Step2.
Assigning actors, movies, and tv show names as tags to each of the 474 youtube videos. Scan through all names on the built
up vocabulary on actors, movies, and tv shows. If a name or the its trimed version appear on the title, or the description
of the videos, it will be added as a tag of this video. Sometimes, one short movie name can be part of a longer movie name.
On this situation, only the longested name will be treated as the tag. This step is name entity detection procedure

Step3.
Create a measure on the similarity of each pair of videos based on the tags ad the videos category, and selected the top 3 
related videos and write the results to file output.txt




Futher work:
Some of the videos also include information of many other fields other than actor, movie, and tv show, such as film awards, 
magzine, film critics, directors, etc. We can use wikipedia data to help the program build up vocabulary on these fields too.
Then we can assign more tags to each of the youtube videos. The more tags we assign, the more information are extracted, and the
better the video clustering algorithm will be.

Another possible improvement is detecting words with high TD-IDF score of each video, and use them as tags. The key idea of 
the algorithm is extrating important features for each video, and compare how much in common for each pair of video. 

