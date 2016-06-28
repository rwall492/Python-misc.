from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol

class Superhero:
    def __init__(self):
        self.ID = ''
        self.connections = []
        self.distance = 9999
        self.status='un-explored'

    def fromLine(self,line):
        fields = line.split('|')
        if (len(fields) == 4):
            self.ID = fields[0]
            self.connections = fields[1].split(',')
            self.distance = int(fields[2])
            self.status = fields[3]

    def toLine(self):
        connections = ','.join(self.connections)
        return '|'.join((self.ID,connections,str(self.distance),self.status))

class MR_bfs_job(MRJob):
    INPUT_PROTOCOL = RawValueProtocol
    OUTPUT_PROTOCOL = RawValueProtocol#want to ensure input & output are in the same format for iterations

    def configure_options(self):
        super(MR_bfs_job,self).configure_options()
        self.add_passthrough_option('--target',help='ID of character we are searching for')

    def mapper(self,_,line):
        character = Superhero()
        character.fromLine(line)

        if (character.status == 'under-exploration'):
            for friend in character.connections:
                new_character = Superhero()
                new_character.ID = friend
                new_character.distance = int(character.distance) + 1
                new_character.status = 'under-exploration'

                if (self.options.target == friend):
                    counterName = ("Target ID " + friend + " was hit with distance " + str(new_character.distance))
                    self.increment_counter("Degrees of separation ", counterName, 1)
                
                yield friend, new_character.toLine()

            character.status = 'explored'
            
        yield character.ID, character.toLine()

    def reducer(self, key, values):
        edges = []
        distance = 9999
        status = 'un-explored'

        #key is character ID
        #value is whole entry (including character ID)
        for value in values:
            character = Superhero()
            character.fromLine(value)
            
            if (len(character.connections) > 0):
                edges.extend(character.connections)

            if (character.distance < distance):
                distance = character.distance

            if (character.status == 'explored'):
                status = 'explored'

            if (character.status == 'under-exploration' and status == 'un-explored'):
                status = 'under-exploration'

        character = Superhero()
        character.ID = key
        character.distance = distance
        character.status = status
        character.connections = edges

        yield key, character.toLine()

if __name__ == '__main__':
    MR_bfs_job.run()
