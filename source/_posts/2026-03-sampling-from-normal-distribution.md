---
title: 抽樣常態分佈：Box-Muller Transform
date: 2026-03-20 21:01:48
tags: [機率]
---

數位影像生成一開始就花了兩個禮拜講機率，赫然發現我好久沒用到機率了很多東西都記不清楚了，中計 😔

## 前言

這個禮拜的主題是要怎麼按照一個任意的機率分佈 \\(p_x(x)\\) 抽樣。問題在於，大部分（偽）隨機數產生器只能給你一個 uniform distribution，要把抽到的東西轉換成奇形怪狀的機率分佈是不簡單的。基礎的手段有兩種：

- 如果 \\(P_x(x) = \int_0^x t \mathop{}\\!\mathrm{d}t\\) 和他的反函數 \\(P^{-1}_x(x)\\) 可以算得出來的話，那可以抽一個 \\(u \sim U[0, 1] \\) 之後，做一個轉換 \\(x' = P^{-1}_x(u)\\)，這時候 \\(x'\\) 就會有我們想要的機率分佈。
- 從一個區域 \\( \Omega \supseteq \left\\{ (x, y) \mid 0 \leq y \leq p_x(x) \right\\} \\) 裡面均勻隨機的亂抽一個 \\((x', y')\\)，檢查 \\(0 \leq y' \leq p_x(x')\\) 是不是滿足，是的話就把這個 \\(x'\\) 當這次抽樣的結果，不是的話就再抽一次。直觀上就是把 \\(y = p_x(x)\\) 這個函數畫出來之後開始往平面上射飛鏢直到射中那個函數底下的區域為止。

第一種作法的條件挺嚴格的，要 \\(p_x(x)\\) 可以積分，積完還要可以有好算的反函數。第二種作法的問題是 \\(\Omega\\) 要形狀好看好抽樣，還要完全蓋住 \\(0 \leq y \leq p_x(x)\\)，還要儘可能接近這個區域不然留太多空白會讓每次射飛鏢的成功率變低。有一個很經典的分佈就沒辦法簡單的用這兩種方法：常態分佈要怎麼抽？

$$ p(x) = \frac{1}{\sqrt{2 \pi}} e^{-\frac{x^2}{2}} $$

單純起見這裡只考慮 \\(\mu = 1, \sigma = 1\\) 的 standard normal distribution。首先 \\(\int e^{-t^2} \mathop{}\\!\mathrm{d}t\\) 形狀的東西積不出來所以沒有 \\(P^{-1}_x(x)\\) 可以算；常態分佈的值域 \\(x \in \mathbb{R}\\) 不是有限的，沒辦法找一個形狀單純的區域包住他，所以也不能射飛鏢，除非妥協一下選一個夠遠的地方把常態分佈兩邊的尾巴砍掉。

## Box-Muller Transform

有兩個數學家是這樣說的：我們先均勻隨機抽**兩個**數字 \\(U_1, U_2 \sim U[0, 1]\\)，然後：

$$ R = \sqrt{-2 \ln U_1} \qquad \Theta = 2 \pi U_2 $$
$$ (X, Y) = (R \cos \Theta, R \sin \Theta) $$

這時候 \\(X, Y \sim p(x)\\) 會是兩個獨立的 normal distributed 的變數！

因為第一次看到覺得這個方法實在太神奇了，所以我想把我對他的解讀寫下來。

### 理解 Box-Muller Transform

之所以寫成 \\(R, \Theta\\) 是因為這個變換就是先用極座標抽一個點之後把他寫成直角座標。\\(R\\) 的形狀長得很奇怪，但是找一下他的反函數：

$$ R = \sqrt{-2 \ln U_1} \quad \iff \quad U_1 = e^{-\frac{R^2}{2}} $$

寫成這樣之後和常態分佈的 PDF 像是同一個形狀，好像這個函數還真的跟常態分佈真的有點什麼關聯。

現在想像我們把上面的過程反過來，i.i.d 的抽兩個變數 \\(x, y \sim N(0, 1)\\)，這時候他們的 joint PDF \\(p_{X, Y}(x, y) = p(x) p(y)\\) 大概長得下面這個樣子：

![internal image](/images/2026-03-sampling-normal-distribution/joint-pdf-2-std-normal-distrib.png)

我們想知道的是他換成極座標之後的 joint PDF \\(p_{R, \Theta}\\) 長怎樣？這個 joint PDF 的形狀圓圓的， \\(r\\) 和 \\(\theta\\) 看起來是獨立的，而且 \\(\theta\\) 看起來是 uniformly distributed 的，於是大概可以想見為什麼會有 \\(\Theta = 2 \pi U_2\\)。

我覺得這裡最重要的一件事情是，討論機率密度的時候是不可以 \\(p_{R, \Theta}(r, \theta) = p_{X, Y}(r \cos \theta, r \sin \theta)\\) 的，所有的機率密度都要積分過後變成機率才能比較，所以在 joint PDF 變數代換的時候才會需要乘一個 Jacobian。就像在比較 \\(\textrm{kg}/\textrm{m}^3\\) 和 \\(\textrm{kg}/\textrm{cm}^3\\) 之前要先乘一個單位轉換的係數，Jacobian 就是這個單位轉換。為了把已知的 \\(p_{X, Y}\\) 轉換成未知的 \\(p_{R, \Theta}\\)，我們轉而求 joint CDF：

$$
\begin{aligned}
    P_{R, \Theta}(r_0, \theta_0)
    =& \mathrm{P} \left( 0 \leq R \leq r_0, 0 \leq \Theta \leq \theta_0 \right) \\\\
    =& \iint p(x, y) \mathop{}\\!\mathrm{d}x \mathop{}\\!\mathrm{d}y \\\\
    =& \iint \frac{1}{2 \pi} e^{-\frac{x^2 + y^2}{2}} \mathop{}\\!\mathrm{d}x \mathop{}\\!\mathrm{d}y \\\\
    =& \int_{0}^{\theta_0} \int_{0}^{r_0} \frac{1}{2 \pi} e^{-\frac{r^2}{2}} \cdot r \mathop{}\\!\mathrm{d}r \mathop{}\\!\mathrm{d}\theta \\\\
    =& \frac{\theta_0}{2 \pi} \left(1 - e^{-\frac{r_0^2}{2}}\right)
\end{aligned}
$$

多重積分裡面變數代換要乘 Jacobian 也是一樣的道理，換成積極座標之後多跑出一個 \\(r\\)，一夕之間裡面的積分就變經典的單變數代換了！剩下的就是找出 \\(R\\) 和 \\(\Theta\\) 的 marginal CDF：

$$
\begin{aligned}
    P_{R}(r_0) &= \int_{0}^{2 \pi} \int_{0}^{r_0} \frac{1}{2 \pi} e^{-\frac{r^2}{2}} \cdot r \mathop{}\\!\mathrm{d}r \mathop{}\\!\mathrm{d}\theta = 1 - e^{-\frac{r_0^2}{2}} \\\\
    P_{\Theta}(\theta_0) &= \int_{0}^{\theta_0} \int_{0}^{\infty} \frac{1}{2 \pi} e^{-\frac{r^2}{2}} \cdot r \mathop{}\\!\mathrm{d}r \mathop{}\\!\mathrm{d}\theta = \frac{\theta_0}{2 \pi}
\end{aligned}
$$

這裡順便驗證了 \\(R\\) 和 \\(\Theta\\) 確實是獨立的。因為兩位的 CDF 長得夠好看，所以可以求反函數：

$$
\begin{aligned}
    P_{R}^{-1}(u) &= \sqrt{-2 \ln (1 - u)} \\\\
    P_{\Theta}^{-1}(u) &= 2 \pi u
\end{aligned}
$$

如果 \\(u \sim U[0, 1]\\)，那 \\(v = (1 - u) \sim U[0, 1]\\) 其實是一樣意思。因此 Box-Muller Transform 確實從常態分佈獨立的抽到了兩個數。

## PDF 的變數代換

看懂這個方法之後，我終於能心無罣礙的接受 [課本](https://pbr-book.org/4ed/Monte_Carlo_Integration/Transforming_between_Distributions) 上寫的多變數代換了：

> 假設 \\(X\\) 是一個 \\(d\\) 維的隨機變數，機率密度是 \\(p(x)\\)。現在有一個雙射的 \\(T\\)，拿他來做變換 \\(Y = T(X)\\)，那變換後 \\(Y\\) 的機率密度函數是
> $$ p_T(y) = \frac{p(x)}{|J_T(x)|} $$

之所以會有這個 Jacobian，就是因為 PDF 積成機率之後兩邊要一樣，所以你積分的時候怎麼變數代換這裡就要怎麼乘 Jacobian。

## 後話

當然，要抽常態分佈還有很多種方法，只是這個作法似乎相當 well known，而且我剛好看到而且我覺得很有趣。

我覺得我還是對機率密度的理解不夠深入，可能我的機率思維還有很大一部份停在離散的那邊，所謂的「密度」到底是什麼？我現在覺得思考 PDF 和 CDF 的時候必須要隨時保持積分的概念，理解在連續的世界裡總是要以區間思考，單一個值沒有意義；不應該以機率密度本身去思考，應該要記得 PDF 在一個底面上拿去積分之後才能變真實的機率。

想得越清楚越覺得這些都是顯然的基礎機率觀念，好像我寫了通篇廢話，就當做我的閱讀日記好了。
