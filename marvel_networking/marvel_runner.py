import subprocess
import sys

iter = 0
start = 2459
end = 100
num_tries = 10

if (len(sys.argv) == 4):
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    num_tries = int(sys.argv[3])

with open("iters/BFS-iteration-0.txt",'w') as out:
    with open("Marvel-graph.txt") as f:
        for line in f:
            fields = line.split()
            heroID = fields[0]
            n_connections = len(fields) - 1
            connections = fields[-n_connections:]

            color = 'un-explored'
            distance = 9999

            if (int(heroID) == start):
                color = 'under-exploration'
                distance = 0

            if (heroID != ''):
                edges = ','.join(connections)
                s_out = '|'.join((heroID,edges,str(distance),color))
                out.write(s_out)
                out.write('\n')

        f.close()
    out.close()

for x in range(0,num_tries):
    str_iter = 'python marvel_bfs_iter.py --target=' + str(end) + ' iters/BFS-iteration-' + str(iter) + '.txt 1> iters/BFS-iteration-' + str(iter + 1) + '.txt'
    subprocess.call(str_iter,shell=True)

    iter += 1
