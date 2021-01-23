'''
map = [['b', 'w', 'w', 'b', 'b', 'b', 'b', 'w', 'w', 'b', 'b', 'b'],
       ['w', 'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b', 'b', 'w', 'b'],
       ['b', 'w', 'b', 'w', 'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b'],
       ['w', 'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b', 'b', 'w', 'b'],
       ['w', 'b', 'w', 'b', 'b', 'w', 'w', 'b', 'w', 'b', 'b', 'w'],
       ['b', 'b', 'w', 'w', 'w', 'b', 'b', 'b', 'w', 'w', 'w', 'b'],
       ['b', 'w', 'w', 'b', 'b', 'b', 'b', 'w', 'w', 'b', 'b', 'b'],
       ['w', 'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b', 'b', 'w', 'b'],
       ['b', 'w', 'b', 'w', 'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b'],
       ['w', 'b', 'b', 'b', 'w', 'b', 'w', 'b', 'b', 'b', 'w', 'b'],
       ['w', 'b', 'w', 'b', 'b', 'w', 'w', 'b', 'w', 'b', 'b', 'w'],
       ['b', 'b', 'w', 'w', 'w', 'b', 'b', 'b', 'w', 'w', 'w', 'b']]
'''

class MonteCarlo():
    def __init__(self, map, pmes = 0.95, pmove = 0.9):
        self.pmes = pmes
        self.pmove = pmove

        self.map = map

        # Linhas e colunas do mapa
        self.map_x = len(map)
        self.map_y = len(map[0])

    '''
        Atualiza o mapa de probabilidades
        a partir de uma medição feita
    '''
    def measure(self, p_map, z):
        
        soma = 0
        
        for i in range(self.map_x):
            for j in range(self.map_y):
                # Se a medição for igual a do quadrado analisado,
                # multiplica pela probabilidade de medição correta
                if self.map[i][j] == z:
                    p_map[i][j] *= self.pmes
                else:
                    p_map[i][j] *= (1.0-self.pmes)

                # Já aproveita para somar as probabilidades
                soma += p_map[i][j]
        print(soma)
        # Normaliza as probabilidades
        for i in range(self.map_x):
            for j in range(self.map_y):
                p_map[i][j] /= soma

        return p_map

    '''
        Atualiza o mapa de probabilidades
        a partir de um movimento
    '''
    def move(self, p_map, u):
        # Cria um mapa zerado
        new_map = [[0 for i in range(self.map_y)] for j in range(self.map_x)]

        u_x = u[0]
        u_y = u[1]
        
        for i in range(self.map_x):
            for j in range(self.map_y):
                # Adiciona a probabilide da posição atual
                # à probabilidade da posição atual + movimento

                # Obtem o índice da nova posição após o movimento
                p_x, p_y = self.adequate([i, j], u)
                
                new_map[p_x][p_y] += p_map[i][j]*self.pmove

                # Adiciona as probabilidade de se mover a mais
                # ou a menos nos 4 quadrados adjascentes
                pwmove = (1 - self.pmove)/4.0

                for w_u in [[-1,0], [1,0], [0,-1], [0,1]]:
                    wp_x, wp_y = self.adequate([p_x, p_y], w_u)
                    
                    new_map[wp_x][wp_y] += p_map[i][j]*pwmove
                    
        return new_map


    '''
        Adequa a posição do movimento para ficar
        dentro do tamanho do mapa
    '''
    def adequate(self, pos, u):
        p_x = pos[0] + u[0]
        p_y = pos[1] + u[1]

        p_x = max(0, p_x)
        p_y = max(0, p_y)

        p_x = min(self.map_x - 1, p_x)
        p_y = min(self.map_y - 1, p_y)

        return p_x, p_y

    '''
        Informa a primeira posição mais provável do
        robô estar junto com a probabilidade em %
    '''
    def where(self, p_map):
        pos = [0, 0]
        max = p_map[0][0]

        for i in range(self.map_x):
            for j in range(self.map_y):
                if(p_map[i][j] > max):
                    max = p_map[i][j]
                    pos = [i,j]
            
        return pos, max*100
