Related-Video
=============
The repository implement a similar video algorithm. A brief description is as follow:

Step1.
By scrapping data from wikipedia, the program build up vocabulary on famous American actors, movies, and television shows.

Step2.
Assigning actors, movies, and tv show tags to each of the 474 youtube videos, if related name appear on the title, 
or the description of the videos. This step is name entity detection

Step3.
Create a measure on the similarity of each pair of videos based on the tags ad the videos category, and selected the top 3 
related videos and write the results to file output.txt

Input Data:
CodeAssignmentDataSet.json

Output Data:
tag.csv           #tagging information for each video
output.txt        #list of top3 related video of each video


Futher work:
Some of the videos also include information of many other fields other than actor, movie, and tv show, such as film awards, 
magzine, film critics, directors, etc. We can use wikipedia data to help the program build up vocabulary on these fields too.
Then we can assign more tags to each of the youtube videos. The more tags we assign, the more information are extracted, and the
better the video clustering algorithm will be.

