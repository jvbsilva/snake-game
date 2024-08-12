joguinho de snake para treinar POO

![Início do jogo](inicio.png)

![Durante o jogo](jogo_em_andamento.png)

Features implementadas até agora:
- Jogo inicia com 5 pySnakes e 5 comidas.
- O valor dos pontos recebidos quando o usuário come uma comida é igual ao valor da velocidade naquele instante.
- A cada pySnake eliminada a velocidade do jogo aumenta.
- As pySnakes irão evitar contato com o usuário bem como com as outras pySnakes e com elas próprias.
- Se o usuário sair do grid ou tocar alguma pySnake ou nele mesmo o jogo acaba.
- As pySnakes são eleminadas pelos mesmos motivos que levam o jogador a ser eliminado.
- Se todas as pySnakes morrerem o jogo continua apenas com o usuário e a valocidade será constante a partir de então.
- A pontuação atual bem como o valor máximo já alcançado é exibido no painel lateral.

Ideias de próximas features:
- Tela de menu onde será possível escolher o número de pySnakes, o número de comidas e a velocidade inicial.
- A pontuação de cada comida levará em conta o número de pySnakes, o número de comidas e a velocidade inicial.
- Implementar uma verificação de autenticidade para o valor armazenado no arquivo best_score.txt