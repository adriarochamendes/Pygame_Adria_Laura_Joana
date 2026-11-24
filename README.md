# Sobrevivência Zumbi

Jogo de sobrevivência com visão de cima, desenvolvido em Python com Pygame. O objetivo é atravessar três fases de 30 segundos, eliminar zumbis e chegar ao fim da partida. Ao acertar um zumbi, uma animação grande de impacto desenha uma mancha irregular e alongada e lança oito riscos avermelhados para trás, na direção oposta à bala. Se um zumbi alcançar o jogador, a partida termina; se o jogador sobreviver às três fases, vence.

## Integrantes

- Ádria Rocha Mendes
- Laura Djehdian Monteiro
- Joana Gregorin Fagundes

## Como instalar e executar

O jogo foi desenvolvido em Python 3 e utiliza a biblioteca Pygame. A dependência está registrada em `requirements.txt` e pode ser instalada com:

```bash
py -m pip install -r requirements.txt
```

## Controles

- *W, A, S, D* ou *setas:* movimentar o personagem.
- *Touchpad:* mover a mira e tocar ou manter pressionado para atirar.
- *Enter:* começar ou jogar novamente.
- *Esc:* sair.

## Fases e pontuação

Cada fase dura 30 segundos. Na fase 1, surge um zumbi por horda a cada 1,6 segundo, com velocidade de referência 90 e limite de oito inimigos simultâneos. Na fase 2, o intervalo cai para 1 segundo, a velocidade de referência sobe para 130 e o limite passa a 14. Na fase 3, surgem dois zumbis por horda a cada 0,65 segundo, com velocidade de referência 175 e limite de 22. As velocidades são ajustadas à resolução do monitor. Cada zumbi eliminado vale um ponto. As cinco melhores pontuações ficam no ranking local, salvo em pontuacoes.txt.

## Recursos e créditos

O jogo utiliza três imagens na pasta assets: o cenário (background.png), o personagem controlado pelo jogador (player.png) e o zumbi (zombie.png). Os efeitos sonoros de disparo, impacto e fim de jogo estão em assets/sounds. As imagens foram geradas com a ferramenta de geração de imagens do ChatGPT (OpenAI). Os efeitos sonoros foram sintetizados para o projeto com código Python, com auxílio do ChatGPT na integração. A animação de impacto é desenhada pelo próprio código, com recursos do Pygame, sem usar uma imagem externa.

## Vídeo do jogo

https://youtu.be/tQuypMHsldo?feature=shared

## Uso de inteligência artificial

O ChatGPT foi utilizado como ferramenta de apoio ao desenvolvimento do projeto. Auxiliou na elaboração do código do jogo, incluindo as telas, a lógica das fases, o ranking e a animação de impacto, além da integração dos recursos gráficos e sonoros. A ferramenta de geração de imagens do ChatGPT foi usada para criar o cenário e os personagens. Os efeitos sonoros foram sintetizados com código Python, também com auxílio do ChatGPT. A interação com a ferramenta será apresentada no anexo solicitado pela disciplina. 