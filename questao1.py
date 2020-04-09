import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
print("Use 'q' para sair e 'p' para pausar\n")


# Exibe a imagem recebida na posição posX,posY, com o label indicado e redimensionada usando o fator fornecido
def exibir(img, label, fator, posX, posY):
    alt, larg = img.shape[:2]
    nova_dimensao = (int(larg*fator), int(alt*fator))
    redimen = cv2.resize(img, nova_dimensao, 0,0)
    labelWindow = label + str(redimen.shape)
    cv2.namedWindow(labelWindow) # Cria uma janela com o nome labelWindow
    cv2.moveWindow(labelWindow, posX, posY)  # Move a janela pra posição indicada
    cv2.imshow(labelWindow, redimen)

# Retorna apenas os N contornos de maior COMPRIMENTO 
def maiores_contornos(contornos, N): # Modificação da função N_Maiores_Contornos() criada por nós e usada na Entrega2
    # N não pode ser maior que o número de contornos
    if len(contornos) < N:
        return []
    
    # Usa uma cópia pra não alterar o original
    contornos = contornos.copy()
    A, M = [0]*N, [None]*N
    maior_i= -1
    
    # Pega os N maiores da lista
    for n in range( N ):
        for i in range( len(contornos) ):
            # comp = cv2.arcLength(contornos[i],1 )      
            comp = Maior_Comprimento_Contorno(contornos[i])
            if comp > A[n]:
                maior_i = i
                A[n],M[n] = comp,contornos[i]
        # Remove o maior da lista
        if (maior_i > -1) and (maior_i < len(contornos)):
            contornos.pop(maior_i) 

    # Nenhum contorno pode ser None
    for m in M:
        if m is None:
            return []
    return M

# Retorna o maior comprimento (vertical ou horizontal) de um contorno
def Maior_Comprimento_Contorno(contorno):
    Bx, By = tuple(contorno[contorno[:,:,1].argmax()][0]) # Ponto de baixo extremo do contorno
    Cx, Cy = tuple(contorno[contorno[:,:,1].argmin()][0]) # Ponto de cima  extremo do contorno
    Dx, Dy = tuple(contorno[contorno[:,:,0].argmax()][0]) # Ponto direito  extremo do contorno
    Ex, Ey = tuple(contorno[contorno[:,:,0].argmin()][0]) # Ponto esquerdo extremo do contorno
    compX = abs(Ex-Dx)
    compY = abs(Cx-Bx)
    if (compX > compY):
        return compX
    return compY

# Retorna o ponto do centro de um contorno
def center_of_contour(cont):
    """ Retorna uma tupla (cx, cy) que desenha o centro do contorno"""
    M = cv2.moments(cont)
    # Usando a expressão do centróide definida em: https://en.wikipedia.org/wiki/Image_moment
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (int(cX), int(cY))

# Retorna tupla com os 4 pontos mais extremos do contorno fornecido (Ymin, Ymax, Xmin, Xmax) = (Cima, Baixo, Esq., Dir.)
    # Lembre-se: o eixo Y no OpenCV cresce para baixo
def pontos_extremos_contorno(contorno):
    C = tuple(contorno[contorno[:,:,1].argmin()][0]) # cima 
    B = tuple(contorno[contorno[:,:,1].argmax()][0]) # baixo
    E = tuple(contorno[contorno[:,:,0].argmin()][0]) # mais a esquerda
    D = tuple(contorno[contorno[:,:,0].argmax()][0]) # direita
    return (C,B,E,D)

# Retorna a imagem recebida sem a parte de cima da imagem (para eliminar ruídos dos objetos acima)
def tira_parte_cima(img, fator):
    alt, larg = img.shape[:2]
    altMin= alt*(fator)
    img_cortada = img[int(altMin):alt, 0:larg]
    return img_cortada

# Retorna o coeficiente angular da reta que corta o ponto mais alto e o mais baixo do contorno
def coef_ang(contorno):
    Cx, Cy = tuple(contorno[contorno[:,:,1].argmin()][0]) # cima 
    Bx, By = tuple(contorno[contorno[:,:,1].argmax()][0]) # baixo
    if (Cx != Bx):
        m = (Cy-By)/(Cx-Bx)
        return round(m,2)


# Recebe 4 pontos: P1, P2, Q1 e Q2 e retorna a posição do ponto de fuga (F)
def ponto_de_fuga(P1,P2,Q1,Q2):
    (P1x,P1y), (P2x,P2y) = P1, P2
    (Q1x,Q1y), (Q2x,Q2y) = Q1, Q2
    
    # Coeficiente angulares:
    mP = (P1y-P2y)/(P1x-P2x)
    mQ = (Q1y-Q2y)/(Q1x-Q2x)
    
    Fx = (P1y -Q1y +mQ*Q1x -mP*P1x)/(mQ-mP)
    Fy = Q1y + mQ*(Fx-Q1x)
    F = (int(Fx), int(Fy))
    return F

# 0) DEFINIR AS CONSTANTES USADAS
    # Intervalo de cores usado no InRange
hsvi = np.array([0, 0, 225], dtype=np.uint8)
hsvf = np.array([90, 25, 255], dtype=np.uint8)
    # Constantes relacionadas à captura
cap = cv2.VideoCapture('videos/1.mp4') 





while(True):
    ret, frame = cap.read()

# 1) MANIPULAÇÕES NA IMAGEM
    # Converte o frame pra HSV e pra cinza
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # i) Retira 25% da parte de cima da imagem e cria uma cópia da imagem em escala de cinza
    img_cortada = tira_parte_cima(frame, 0.25)
    cortado_gray = cv2.cvtColor(img_cortada, cv2.COLOR_BGR2GRAY)

# ii) Limiarizar
    retorno, limiarizado = cv2.threshold(cortado_gray, 220, 255, cv2.THRESH_BINARY)

# iii) Identificar os contornos e desenha eles na imagem
    contornos, hierarquia = cv2.findContours(limiarizado.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
    maiores = maiores_contornos(contornos, 2)
 
    if (len(maiores) == 2):
        # cv2.drawContours(img_cortada, maiores[0], -1, [0,255,0], 3);
        m0 = coef_ang(maiores[0])
        m1 = coef_ang(maiores[1])
        
        cm0 = center_of_contour(maiores[0])
        cm1 = center_of_contour(maiores[1])

        deltaY = frame.shape[0] - img_cortada.shape[0]
        xC0, yC0 = cm0[0], cm0[1]+deltaY
        xC1, yC1 = cm1[0], cm1[1]+deltaY

        h0 = yC0 - m0*xC0
        h1 = yC1 - m1*xC1

        intercept_x0 = (int(-h0/m0),0)
        intercept_x1 = (int(-h1/m1),0)

        cv2.line(frame, (xC0,yC0), intercept_x0, [255,0,0],5)
        cv2.line(frame, (xC1,yC1), intercept_x1, [255,0,0],5)


        pf = ponto_de_fuga((xC0,yC0),intercept_x0,(xC1,yC1),intercept_x1)
        cv2.circle(frame, pf, 10, (200, 0, 255), -1)

        print(pf)



# 2) EXIBE O(S) FRAME(S)
    exibir(frame, 'Frame', 0.50, 0, 0)


# 3) TRATA TECLAS PRESSIONADAS
    tecla = cv2.waitKey(1)     # Aguarda T ms por uma tecla 

    if tecla == ord('p'): # A tecla 'p' pausa no frame exibido
        print('\nPausado pelo usuário \nPressione qualquer tecla para continuar \n')
        cv2.waitKey()
        continue

    if tecla == ord('q'): # A tecla 'q' finaliza o loop
        print('\nFinalizado pelo usuário\n')
        break

cap.release()
cv2.destroyAllWindows()