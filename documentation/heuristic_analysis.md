---
title: Analysis of heuristics for a special variant of the isolation board game
author: by Rene Kretzschmar
geometry: margin=2.5cm
papersize: a4
header-includes:
    - \usepackage{caption}
    - \usepackage{multirow}
---

# Synopsis

I tried a lot of ideas, played pen and paper games, searched for patterns - and the following strategies turned out to perform best.

## Custom Score: Looking ahead and blocking during end game
My first and best strategy takes the current legal moves and expands each of them by applying all valid move directions to it. The resulting list is then filtered by checking if these are legal moves. The same is done with the opponent moves, so I get two counts of look ahead moves $L_{own}$ and $L_{opp}$.

Then I calculate the moves that would block the opponent's moves and do the same for the moves that would block the player using $L_{opp}$, so I get two more counts of blocking moves $B_{own}$ and $B_{opp}$.

Because blocking does makes sense especially during the end game, I calculate a board occupation factor $O_b$. 

The score value $S_b$ of the current board is then calculated like this:

\begin{align}
S_b & = ( L_{own} - L_{opp} + O_b(B_{own} - B_{opp}) )
\end{align}

## Custom Score 2: Counting legal moves and blocking during the end game

Like the improved base heuristic I simply count the players and the opponents moves and get two counts $M_{own}$ and $M_{opp}$. Then I calculate the moves that would block the opponent's moves and get $B_{own}$. And like before, because blocking does makes sense especially during the end game, I calculate a board occupation factor $O_b$.

The score value $S_{b_2}$ of the current board is then calculated like this:

\begin{align}
S_{b_2} & = ( M_{own} - M_{opp} + O_b B_{own} )
\end{align}

## Custom Score 3: Counting legal moves and moving towards the center during end game

Like before I count the players and the opponents moves and get two counts $M_{own}$ and $M_{opp}$. Then I take the player position and calculate the distance to the center $C_{own}$. I do the same for the opponent and get $C_{opp}$. When I played pen and paper games I found out, that it is better to occupy the edge position during the beginning of the game and the center during end game. So I calculate the board occupation factor $O_b$ and take that into account.

 The score value $S_{b_3}$ of the current board is then calculated like this:

\begin{align}
S_{b_3} & = ( M_{own} - M_{opp} + \frac{1}{O_b} (C_{own} - C_{opp}) )
\end{align}

## Results

Table \ref{table:run1} shows the results of the first tournament with 5 games against each opponent. The results of the first strategy and the third are very similar and the others are somehow in the same range. So I ran another tournament with 10 games against each opponent. Table \ref{table:run2} shows the results. The second run shows that the first strategy is slightly more successfull than the third, but not significantly enough. So I ran another tournament, this time 100 games against each opponent. Table \ref{table:run3} shows the results.

Now the first strategy really stands out, while all others are in the same range. The second and the third are only slightly better than the base _Improved_ heuristic.

## Conclusion
I decided to go with the _Looking ahead and blocking during end game_ strategy, because it is the most suffisticated heuristic and is actually the only one, that implements it's own unique strategy. The others do basically the same like the _Improved_ one and only add one particular aspect, that does not seem to have a massive impact in both cases. My hope here was, that the inexpensive calculations of the second and third strategy might serve to their advantage. Less computation time during the heuristics calculation means potentially more time to traverse deeper into the game tree. The first strategy does four potentially expensive list operations, but they seem to be implemented very efficiently in python, so it seems it had no impact. But that needs further research, which is out of scope of this analysis.

In general - instead of guessing a good heuristic, today the score evaluation function could also be a deep neural network that learns from game plays against the basic heuristics and different versions of itself in a re-inforced manner.

## Result Tables

\begin{center}
\begin{tabular}{ |l|l|c|c|c|c|c|c|c|c| }
\hline
\# & Opponent & \multicolumn{2}{ |c| }{AB Improved} & \multicolumn{2}{ |c| }{AB Custom} & \multicolumn{2}{ |c| }{AB Custom 2} & \multicolumn{2}{ |c| }{AB Custom 3}\\
\hline
& & Won & Lost & Won & Lost & Won & Lost & Won & Lost\\
\hline
    1 & Random & 7 & 3 & 9  &   1  &   9  &   1  &   9  &   1\\
    2 & MM Open & 6  &   4   &  7  &   3  &   5  &   5 &    7  &   3\\
    3 & MM Center & 9  &   1   &  8  &   2   &  9  &   1  &  10  &   0\\
    4 & MM Improved & 8  &   2  &   6  &   4  &   6  &   4  &   7  &   3\\
    5 & AB Open & 5  &   5   &  5  &   5   &  5  &   5   &  6  &   4\\
    6 & AB Center & 5  &   5  &   7  &   3   &  6  &   4  &   5  &   5\\
    7 & AB Improved &   6  &   4  &   6  &   4   &  6  &   4  &   4  &   6\\
\hline
& Win Rate: & \multicolumn{2}{ |c| }{65.7\%} & \multicolumn{2}{ |c| }{68.6\%} & \multicolumn{2}{ |c| }{65.7\%} & \multicolumn{2}{ |c| }{68.6\%}\\
\hline
\end{tabular}
\captionof{table}{Tournament with 5 games against each opponent}
\label{table:run1}
\end{center}

\begin{center}
\begin{tabular}{ |l|l|c|c|c|c|c|c|c|c| }
\hline
\# & Opponent & \multicolumn{2}{ |c| }{AB Improved} & \multicolumn{2}{ |c| }{AB Custom} & \multicolumn{2}{ |c| }{AB Custom 2} & \multicolumn{2}{ |c| }{AB Custom 3}\\
\hline
& & Won & Lost & Won & Lost & Won & Lost & Won & Lost\\
\hline
    1   &    Random    &  13  &   7 &   18  &   2  &  18  &   2  &  15  &   5\\
    2    &   MM Open   &  13  &   7  &  13  &   7  &  11  &   9  &  13  &   7\\
    3    &  MM Center   & 15  &   5  &  17  &   3  &  18  &   2  &  15  &   5\\
    4   &  MM Improved  & 15  &   5  &  13  &   7  &  14  &   6  &  16  &   4\\
    5   &    AB Open    & 11  &   9  &  13  &   7  &  10  &  10  &  11  &   9\\
    6   &   AB Center   & 11  &   9  &  13  &   7  &  12  &   8  &  15  &   5\\
    7   &  AB Improved   & 8  &  12  &  12  &   8  &   7  &  13  &  11  &   9\\
\hline
& Win Rate: & \multicolumn{2}{ |c| }{61.4\%} & \multicolumn{2}{ |c| }{70.7\%} & \multicolumn{2}{ |c| }{64.3\%} & \multicolumn{2}{ |c| }{68.6\%}\\
\hline
\end{tabular}
\captionof{table}{Tournament with 10 games against each opponent}
\label{table:run2}
\end{center}

\begin{center}
\begin{tabular}{ |l|l|c|c|c|c|c|c|c|c| }
\hline
\# & Opponent & \multicolumn{2}{ |c| }{AB Improved} & \multicolumn{2}{ |c| }{AB Custom} & \multicolumn{2}{ |c| }{AB Custom 2} & \multicolumn{2}{ |c| }{AB Custom 3}\\
\hline
& & Won & Lost & Won & Lost & Won & Lost & Won & Lost\\
\hline
1   &    Random     & 161 &  39  &  170 &  30 &   163 &  37  &  169 &  31\\
2   &    MM Open    & 124 &  76  &  146 &  54 &   124 &  76  &  139 &  61\\
3   &   MM Center   & 145 &  55  &  164 &  36 &   150 &  50  &  144 &  56\\
4   &  MM Improved  & 121 &  79  &  149 &  51 &   138 &  62  &  124 &  76\\
5   &    AB Open    & 106 &  94  &  112 &  88 &   102 &  98  &  102 &  98\\
6   &   AB Center   & 109 &  91  &  119 &  81 &   109 &  91  &  102 &  98\\
7   &  AB Improved  & 105 &  95  &  109 &  91 &   91  &  109 &  98  &  102\\
\hline
& Win Rate: & \multicolumn{2}{ |c| }{62.2\%} & \multicolumn{2}{ |c| }{69.2\%} & \multicolumn{2}{ |c| }{62.6\%} & \multicolumn{2}{ |c| }{62.7\%}\\
\hline
\end{tabular}
\captionof{table}{Tournament with 100 games against each opponent}
\label{table:run3}
\end{center}