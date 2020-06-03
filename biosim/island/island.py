class Island:
    def __init__(self, map):
        self.map = map

    def make_a_map(self):
        '''
        Makes a map and puts a cell in each position

        :return:
        Full map
        '''
        kart = []
        geo = [list(rader) for rader in
               self.map.replace(" ", "").split("\n")]

        for row in geo:
            temp_kart = []
            for cellene in row:
                if cellene == "J":
                    temp_kart.append(Jungle())  # osv

            kart.append(temp_kart)