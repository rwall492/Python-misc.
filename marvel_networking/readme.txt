This code uses MapReduce to study a network of superheroes from the Marvel Universe.  

0.) The MapReduce code is courtesy of Frank Kane's course "Taming Big Data with MapReduce and Hadoop" from Udemy.  I've mostly added bells and whistles to make the code more handy.
1.) The "data" for this code is in Marvel-graph.txt
    - Each line represents a super-hero and all their immediate connections.
    - The name of each super-hero can be tied to their ID using Marvel-names.txt
2.) The code uses MapReduce to run a breadth-first search (BFS) to determine the minimum number of degrees of separation between two super-heroes
2.) To run the code, use:
    - python marvel_runner.py <starting-hero> <target-hero> <number of iterations>
    - For ease of use, I pipe the output to a text file and grep "Target" from that file afterwards to see the minimum degree of separation
    - <number of iterations> controls the number of BFS "steps" taken by the code to look for connections between the starting and target heroes
