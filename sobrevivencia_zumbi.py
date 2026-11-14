# -*- coding: utf-8 -*-
# Sobrevivência Zumbi - jogo com visão de cima feito em Pygame
# Sprites e cenário criados com ferramenta de IA generativa (ChatGPT ImageGen).
import os
import math
import random
import pygame

# ----------------------------------------------------------------------
# Configurações gerais
# ----------------------------------------------------------------------
# Coordenadas de referência. O jogo usa a resolução real do monitor e escala
# elementos e fontes para desenhá-los diretamente, sem ampliar uma imagem pequena.
LARGURA_BASE = 1280
ALTURA_BASE = 720
LARGURA = LARGURA_BASE
ALTURA = ALTURA_BASE
ESCALA_TELA = 1.0
FPS = 60
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
PASTA_ASSETS = os.path.join(PASTA_PROJETO, 'assets')
ARQUIVO_PONTOS = os.path.join(PASTA_PROJETO, 'pontuacoes.txt')

# Cores (R, G, B)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA_FUNDO = (40, 44, 40)
CINZA_GRADE = (52, 58, 52)
AZUL_JOGADOR = (60, 130, 230)
PELE = (240, 200, 160)
VERDE_ZUMBI = (90, 170, 70)
VERDE_ESCURO = (40, 90, 30)
VERMELHO = (220, 40, 40)
AMARELO_TIRO = (255, 230, 60)
DOURADO = (255, 200, 0)

# Estados do jogo
MENU = 0
NOME = 1
JOGO = 2
VITORIA = 3
FIM = 4
SAIR = 5

# Progressão da partida
NUMERO_FASES = 3
DURACAO_FASE = 30  # segundos por fase

# Parâmetros de jogabilidade (velocidades em pixels por SEGUNDO)
VELOCIDADE_JOGADOR = 250
VELOCIDADE_TIRO = 650
VELOCIDADE_ZUMBI_INICIAL = 80
RAIO_JOGADOR = 31
RAIO_ZUMBI = 70
RAIO_TIRO = 4
INTERVALO_TIRO = 0.18          # segundos mínimos entre tiros
DISTANCIA_SEGURA_SPAWN = 200   # zumbi nunca nasce tão perto do jogador


def px(valor):
    """Converte uma medida de referência para pixels da tela atual."""
    return max(1, round(valor * ESCALA_TELA))


# ----------------------------------------------------------------------
# Classes dos objetos do jogo
# ----------------------------------------------------------------------
class Jogador(pygame.sprite.Sprite):
    """Personagem controlado pelo jogador, desenhado com um sprite."""

    def __init__(self, imagem):
        super().__init__()
        self.posicao = pygame.math.Vector2(LARGURA / 2, ALTURA / 2)
        self.imagem = imagem
        self.raio = px(RAIO_JOGADOR)  # raio usado na colisão
        self.margem_tela = px(84)  # mantém o sprite inteiro dentro da janela
        self.angulo = 0.0  # direção da mira em radianos
        self.tempo_desde_tiro = INTERVALO_TIRO

    def atualizar(self, dt, teclas):
        # WASD ou as setas movimentam o personagem.
        direcao = pygame.math.Vector2(0, 0)
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            direcao.y -= 1
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            direcao.y += 1
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            direcao.x -= 1
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            direcao.x += 1
        if direcao.length() > 0:
            direcao = direcao.normalize()  # diagonal não fica mais rápida
        # Movimento multiplicado por dt => independe do FPS
        self.posicao += direcao * px(VELOCIDADE_JOGADOR) * dt
        # Mantém o jogador dentro da tela
        self.posicao.x = max(self.margem_tela, min(LARGURA - self.margem_tela, self.posicao.x))
        self.posicao.y = max(self.margem_tela, min(ALTURA - self.margem_tela, self.posicao.y))

        # O touchpad controla a posição da mira.
        toque_x, toque_y = pygame.mouse.get_pos()
        self.angulo = math.atan2(toque_y - self.posicao.y,
                                 toque_x - self.posicao.x)
        self.tempo_desde_tiro += dt

    def pode_atirar(self):
        return self.tempo_desde_tiro >= INTERVALO_TIRO

    def atirar(self):
        """Cria um tiro saindo da ponta da arma na direção da mira."""
        self.tempo_desde_tiro = 0
        direcao = pygame.math.Vector2(math.cos(self.angulo), math.sin(self.angulo))
        ponta_arma = self.posicao + direcao * (self.raio + px(12))
        return Tiro(ponta_arma, direcao)

    def desenhar(self, tela):
        # O sprite original aponta para a direita; giramos conforme a mira.
        imagem_rotacionada = pygame.transform.rotate(
            self.imagem, -math.degrees(self.angulo)
        )
        retangulo = imagem_rotacionada.get_rect(
            center=(round(self.posicao.x), round(self.posicao.y))
        )
        tela.blit(imagem_rotacionada, retangulo)


class Zumbi(pygame.sprite.Sprite):
    """Zumbi que persegue o jogador e usa um sprite girado na direção dele."""

    def __init__(self, posicao, velocidade, imagem):
        super().__init__()
        self.posicao = pygame.math.Vector2(posicao)
        self.velocidade = velocidade
        self.imagem = imagem
        self.raio = px(33)  # raio usado na colisão
        self.direcao = pygame.math.Vector2(1, 0)

    def atualizar(self, dt, posicao_jogador):
        vetor = posicao_jogador - self.posicao
        if vetor.length() > 0:
            self.direcao = vetor.normalize()
        self.posicao += self.direcao * self.velocidade * dt

    def desenhar(self, tela):
        angulo = math.degrees(math.atan2(self.direcao.y, self.direcao.x))
        imagem_rotacionada = pygame.transform.rotate(self.imagem, -angulo)
        retangulo = imagem_rotacionada.get_rect(
            center=(round(self.posicao.x), round(self.posicao.y))
        )
        tela.blit(imagem_rotacionada, retangulo)


class Tiro(pygame.sprite.Sprite):
    """Projétil amarelo que anda em linha reta."""

    def __init__(self, posicao, direcao):
        super().__init__()
        self.posicao = pygame.math.Vector2(posicao)
        self.direcao = direcao
        self.raio = px(RAIO_TIRO)

    def atualizar(self, dt):
        self.posicao += self.direcao * px(VELOCIDADE_TIRO) * dt
        # Remove o tiro quando ele sai da tela
        margem = px(10)
        if not (-margem < self.posicao.x < LARGURA + margem and -margem < self.posicao.y < ALTURA + margem):
            self.kill()

    def desenhar(self, tela):
        rastro = self.posicao - self.direcao * px(10)
        pygame.draw.line(tela, (255, 150, 0), rastro, self.posicao, px(3))
        pygame.draw.circle(tela, AMARELO_TIRO, self.posicao, self.raio)


class EfeitoImpacto:
    """Mancha de impacto grande e partículas lançadas contra o sentido da bala."""

    DURACAO = 0.42

    def __init__(self, posicao, direcao_bala):
        self.posicao = pygame.math.Vector2(posicao)
        self.tempo = 0.0
        vetor_bala = pygame.math.Vector2(direcao_bala)
        if vetor_bala.length() > 0:
            self.direcao_recuo = -vetor_bala.normalize()
        else:
            self.direcao_recuo = pygame.math.Vector2(-1, 0)
        self.lateral = pygame.math.Vector2(
            -self.direcao_recuo.y, self.direcao_recuo.x
        )

        # Pontos assimétricos formam uma mancha alongada para trás do impacto.
        self.contorno = [
            (-6, -4), (-3, -11), (3, -8), (8, -16), (14, -10),
            (21, -14), (25, -7), (34, -9), (31, -2), (43, 2),
            (34, 7), (38, 13), (26, 11), (20, 17), (14, 10),
            (8, 14), (5, 7), (-2, 9), (1, 3), (-7, 2)
        ]

        # Riscos de comprimentos diferentes saem em um leque na direção oposta.
        self.particulas = []
        for angulo in (-58, -42, -27, -11, 8, 25, 43, 61):
            direcao = self.direcao_recuo.rotate(angulo)
            distancia = random.uniform(35, 72)
            tamanho = random.uniform(2.5, 5.5)
            comprimento = random.uniform(8, 17)
            self.particulas.append((direcao, distancia, tamanho, comprimento))

    def atualizar(self, dt):
        self.tempo += dt

    def terminou(self):
        return self.tempo >= self.DURACAO

    def desenhar(self, tela):
        progresso = min(self.tempo / self.DURACAO, 1.0)
        crescimento = min(self.tempo / 0.09, 1.0)
        escala_mancha = (0.72 + 0.48 * crescimento) * (1 - 0.2 * progresso)
        centro = (round(self.posicao.x), round(self.posicao.y))

        # A forma cresce rapidamente e depois escurece enquanto desaparece.
        pontos = []
        for distancia, deslocamento_lateral in self.contorno:
            ponto = (
                self.posicao
                + self.direcao_recuo * round(distancia * escala_mancha * ESCALA_TELA)
                + self.lateral * round(deslocamento_lateral * escala_mancha * ESCALA_TELA)
            )
            pontos.append((round(ponto.x), round(ponto.y)))
        escurecimento = max(0.0, (progresso - 0.2) / 0.8)
        cor_mancha = (
            round(148 - 48 * escurecimento),
            round(31 - 13 * escurecimento),
            round(27 - 10 * escurecimento)
        )
        pygame.draw.polygon(tela, cor_mancha, pontos)
        pygame.draw.circle(tela, (72, 18, 18), centro, px(5 * (1 - 0.35 * progresso)))

        # As partículas percorrem trajetórias diferentes e não formam um círculo.
        for direcao, distancia_maxima, tamanho_inicial, comprimento_inicial in self.particulas:
            distancia = px(distancia_maxima * progresso)
            ponta = self.posicao + direcao * distancia
            comprimento = px(comprimento_inicial * (1 - 0.45 * progresso))
            inicio = ponta - direcao * comprimento
            cor = (155, 35, 29) if progresso < 0.65 else (112, 29, 26)
            largura = max(1, px(tamanho_inicial * (1 - 0.55 * progresso)))
            pygame.draw.line(
                tela, cor, (round(inicio.x), round(inicio.y)),
                (round(ponta.x), round(ponta.y)), largura
            )
            pygame.draw.circle(
                tela, (175, 43, 32), (round(ponta.x), round(ponta.y)),
                max(1, px(tamanho_inicial * (1 - 0.55 * progresso)))
            )


class Botao:
    """Botão do menu, selecionável pelo touchpad ou pelo teclado."""

    def __init__(self, texto, centro, cor):
        self.texto = texto
        self.retangulo = pygame.Rect(0, 0, px(300), px(55))
        self.retangulo.center = centro
        self.cor = cor

    def desenhar(self, tela, fonte):
        sobre_botao = self.retangulo.collidepoint(pygame.mouse.get_pos())
        cor = tuple(min(255, c + 35) for c in self.cor) if sobre_botao else self.cor
        pygame.draw.rect(tela, cor, self.retangulo, border_radius=10)
        pygame.draw.rect(tela, BRANCO, self.retangulo, px(2), border_radius=px(10))
        superficie = fonte.render(self.texto, True, BRANCO)
        tela.blit(superficie, superficie.get_rect(center=self.retangulo.center))

    def foi_clicado(self, evento):
        return (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
                and self.retangulo.collidepoint(evento.pos))