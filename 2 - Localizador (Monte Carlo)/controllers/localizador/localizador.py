from controller import Robot, Motor, Keyboard
from montecarlo import MonteCarlo

robot = Robot()

timestep = int(robot.getBasicTimeStep())

keyboard = Keyboard()
keyboard.enable(timestep)

# ----- Inicializa o "sensor de luminosidade" -----
# É um sensor de distância infravermelho
lsensor = robot.getDevice('gs1')
lsensor.enable(timestep)

# ----- Inicializa os motores -----
motor_l = robot.getDevice('left wheel motor')
motor_r = robot.getDevice('right wheel motor')
motor_l.setPosition(float('inf'))
motor_r.setPosition(float('inf'))

motor_l.setVelocity(0.0)
motor_r.setVelocity(0.0)


# ----- Funções de controle do robo -----
def robotTurnRight():
    motor_r.setVelocity(-2.197)
    motor_l.setVelocity(2.197)
    robot.step(1000)
    motor_l.setVelocity(0.0)
    robot.step(timestep)

def robotTurnLeft():
    motor_r.setVelocity(2.097)
    motor_l.setVelocity(-2.097)
    robot.step(1000)
    motor_r.setVelocity(0.0)
    robot.step(100)
    

def robotGoForward():
    motor_r.setVelocity(4.13)
    motor_l.setVelocity(4.13)
    robot.step(1000)
    motor_l.setVelocity(0.0)
    motor_r.setVelocity(0.0)
    robot.step(100)        

def robotFollowPath(path, start_angle):
    # ----- Sobe/desce primeiro -----
    
    if(path[0] != 0):
        
        # Baixo ou cima
        if(path[0] > 0):
            angle = 270
        else:
            angle = 90

        # Diferença entre o angulo do robo e do movimento
        delta_ang = start_angle - angle
        
        # Conta quantos vezes tem que virar pra esquerda ou direita
        if (delta_ang < 0):
            esq = -delta_ang//90
            dir = (360+delta_ang)//90
        else:
            esq = (360-delta_ang)//90
            dir = delta_ang//90
        
        # Se tiver calculado uma volta completa, zera os valores
        if (esq == 4 or dir == 4):
            esq = 0
            dir = 0
            
        # Verifica qual o melhor jeito de virar
        if (esq <= dir):
            for n in range(esq):
                robotTurnLeft()
        elif (esq > dir):
            for n in range(dir):
                robotTurnRight()
        
        # Atualiza o angulo do robo
        start_angle = angle
        
        for i in range(abs(path[0])):
            robotGoForward()
        
        
    # ----- Vira para esquerda/direita -----
    
    if(path[1] != 0):
        
        # Direita ou esquerda
        if(path[1] > 0):
            angle = 0
        else:
            angle = 180
            
        # Diferença entre o angulo do robo e do movimento
        delta_ang = start_angle - angle
        
        # Conta quantos vezes tem que virar pra esquerda ou direita
        if (delta_ang < 0):
            esq = -delta_ang//90
            dir = (360+delta_ang)//90
        else:
            esq = (360-delta_ang)//90
            dir = delta_ang//90
        
        # Se tiver calculado uma volta completa, zera os valores
        if (esq == 4 or dir == 4):
            esq = 0
            dir = 0
            
        # Verifica qual o melhor jeito de virar
        if (esq <= dir):
            for n in range(esq):
                robotTurnLeft()
        elif (esq > dir):
            for n in range(dir):
                robotTurnRight()
        
        # Atualiza o angulo do robo
        start_angle = angle
                
        for i in range(abs(path[1])):
            robotGoForward()
            
    return start_angle

# ----- Função para obter a cor do chão abaixo do robô -----
# Retorna 'b' se for preto e 'w' se for branco
def robotGetColor():
    sensor = lsensor.getValue()
    
    if sensor > 350:
        return 'w'
    else:
        return 'b'

# ----- Declarações do algoritmo de localização -----
# Função para printar o mapa de probabilidades
def print_map(map):
    for i in map:
        print("[", end='')
        for j in i:
            print("%.3f "%j, end='')
        print("")
    print("--------------------------------------------------------------")

# Matriz representando as características do mapa
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
       
# Cria o mapa de probabilidades
# Quantidade de linhas e colunas do mapa
x = len(map)
y = len(map[0])
p = 1.0/(x*y)

p_map = [[p for j in range(y)] for i in range(x)]


# Inicia a simulação por um tempo para o robô e os sensores inicializarem
start_angle = 90
robot.step(1000)

# Instancia da localização (passa o mapa com as características)
localize = MonteCarlo(map)

while robot.step(timestep) != -1:

    # Mede a posição atual
    z = robotGetColor()
    
    # Atualiza o mapa de probabilidades com a medição
    p_map = localize.measure(p_map, z)
    
    print_map(p_map) 
    
    # Printa a posição atual mais provável
    pos, prob = localize.where(p_map)
    print("- O robô tem %.1f%% de chance de estar na posição %d - %d"%(prob, pos[0], pos[1]))
    
    # Faz o robo andar
    u = [0, 0]
    
    # Pede para entrar com a nova posição
    print("- Digite quantos quadrados o robô deve andar:")
    print("  (Sinais: - cima/esquerda e + baixo/direita)")

    for i in range(2):        
            if i == 0:
                print("Verticalmente: ")  
                
            else:
                print("Horizontalmente: ")   
                
            key = -1
            
            while key == -1:
                robot.waitForUserInputEvent(robot.EVENT_KEYBOARD, 1000)
                key = keyboard.getKey()   
           
           # 45 é igual ao símbolo -
            if key == 45:                
                key = -1
                
                robot.step(timestep)
                
                while key == -1:
                    robot.waitForUserInputEvent(robot.EVENT_KEYBOARD, 1000)
                    key = keyboard.getKey()
                    
                pos = -((key-48)%10)
            else:
                pos = (key-48)%10
            
            robot.step(timestep)
            
            print(pos)
            
            u[i] = pos
            
    start_angle = robotFollowPath(u, start_angle)
    
    # Atualiza o mapa de probabilidades com o movimento
    p_map = localize.move(p_map, u)
