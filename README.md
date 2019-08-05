# olx_crawler
Realiza pesquisas na OLX.

***Utilização***

O programa pode receber argumentos através do argv na forma de:

python main.py pesquisa

Ou através de um input do usuário caso o mesmo não forneça argumentos através do argv.

***Remoção de outliers***

A pesquisa é realizada utilizando o sistema próprio da OLX, o crawler então entra em cada um dos anuncios e os salva, seguindo para os anuncios recomendados dentro da página de cada um deles. Os resultados são salvos em um pandas dataframe o qual é então filtrado para remover anuncios que não possuam preço e também para realizar a remoção de anuncios cujos preços variam certa porcentagem da mediana. Por exemplo:

Título | Preço
-------|------
A      | 10
B      | 20
C      | 25
D      | 50

A mediana é de 22.5
O produto D de valor 50 será removido pois varia mais de 100% da mediana, o valor pode ser mudado editando os parâmetros no arquivo main.py ou mesmo desativado setando remove_outliers para False no arquivo main.py

