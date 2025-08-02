---
title: 牙牙學 Vulkan（一）用七百行畫一個三角形
date: 2025-08-02 07:23:54
tags: [C++]
---

我終於第一次不嘴砲真的去寫 vulkan 了！

## 牙牙學 Vulkan

我開始學程式大概很長一段時間都是為競賽服務，不過總是有個願望是開發個什麼厲害的東西。

依稀有一個模糊的印象，很久很久以前我認知範圍內最複雜的電腦遊戲是 minecraft，於是我學程式的最高願望（競賽另論）是寫 minecraft 模組，但是僅止於翻幾下 java 語法，沒有實際嘗試，可能部份也是因為那時候沒辦法常常摸電腦。

後來學 C++ 的時候認識 [The Cherno](https://www.youtube.com/@TheCherno) 和他的 [OpenGL 系列](https://www.youtube.com/playlist?list=PLlrATfBNZ98foTJPJ_Ev03o2oq3-GGOS2)，才知道原來在電腦螢幕上畫畫是普通人做得到的事情，學程式的願望清單加入了一個「自己寫出 minecraft」，但是還是沒有找到一個動力去甚至是把教學看完。那時候知識範圍可能僅限這個系列的前十五集，程度差不多停留在會畫一個三角形。像矩陣之類的數學工具還不夠熟悉所以看沒有懂，還被四元數恐嚇。

我真的很喜歡 The Cherno 這個頻道，我從他的 C++ 系列第一次知道現代 C++ 和各種 computer graphics 101。他本人甚至跟一個兩三個人的團隊在自己開發遊戲引擎。我會知道 Vulkan 也是從這裡看到的。

總之時間來到今年三月要寫計算機圖形作業一，終於找到一個足夠強的動力讓我去真的把 OpenGL 給學會了，至少我現在可以說我會做一般來說最一般的那些圖形渲染。五月和王淇一組做 [計算機圖形 final project](https://github.com/littlecube8152/icg-term-project)，我們要搞光線追蹤，但是 OpenGL 就是不行，我們又沒人會 CUDA（這東東還真有點難搞），後來是用 OpenGL compute shaders 做平行化，只能說有加速但不多。或者說其實跟 CPU ray tracing 比起來快很多了，只是這個 approach 加上我們寫出來的完全沒在管優化問題的 shader，應該離硬體性能上限差很遠很遠。在這途中王淇嘗試過要不要用 Vulkan 開真正的硬體加速的光線追蹤，但是 Vulkan 入門難度實在是太可怕了，後來連一個三角形都沒有畫出來就放棄了。

現在暑假還剩一個月，終於被我逮到機會真的嘗試看看 Vulkan 了。

學 Vulkan 的過程我感覺我根本就是兩三歲的小小孩在學講話，那些寫 tutorial 的專業開發者們說一句我就做一句，左邊看一看「懂了知道了」，右邊複製貼上「啊怎麼不會動，破防」，感覺離真正做出有任何原創價值的東西還有很遠很遠。這個牙牙學 Vulkan 系列大概會是我的里程碑和感想，不知道可以更新多久。

## 畫一個三角形

Vulkan 的前置設定給非常多選項可以選，換句話說就是真的真的真的很麻煩，尤其是體驗過 legacy OpenGL 之後。似乎有廣為流傳的說法說你要寫好幾百上千行才能用 Vulkan 畫出一個三角形，雖然行數不是很絕對的評斷指標，各種 coding style 或模組化思維之類的差異可能會讓一個三角形從五百多行到快一千行不等，不過還是可以證明他特別 verbose。畫出這個三角形花了我至少半個禮拜。

![](/images/2025-08-vulkan-1-the-triangle.png)

Vulkan 的 API 是純 C 的形式。我一開始是看 [Vulkan Tutorial](https://vulkan-tutorial.com/Introduction)，他用的就是這種 C-style 的寫法，所有資源要自己 allocate/free 的那種。看到一半聽王淇說有 [Khronos Vulkan Tutorial](https://docs.vulkan.org/tutorial/latest/00_Introduction.html)，才知道原來 Vulkan SDK 裡面還有附贈 [Vulkan-Hpp](https://github.com/KhronosGroup/Vulkan-Hpp/tree/main) 幫你把那些資源和 API call 包成很多好看好寫的 class，裡面的 RAII 版本整個好用不少，所以打掉重練了一下。

不過後面那個 tutorial 是抄前面那個的（只是改成 `vulkan_raii`），他看起來又只想改一小部份，不少地方程式碼和文字說明對不上，如果完全不知道 C-style 寫法的話沒辦法懂他在講什麼也無從抄起，在修理的過程偶爾還要去看看 [vulkan registry](https://registry.khronos.org/vulkan/specs/latest/man/html/)。我甚至有點懷疑只湊程式碼片段不小改一下或參考一下完整的 sample code 是沒辦法編譯或跑不動的。我覺得我不小心走到最棒的路線是我知道 C-style API 長怎樣、那些 API call 通常是個什麼流程、讀過 registry，然後實際使用是包裝好的 Vulkan-Hpp RAII module。

## 錯誤處理

畫三角形的時候遇到一個比較頭痛的問題是錯誤處理。Vulkan API call 一般還你一個 `VkResult` enum 代表成功或失敗原因之類的（用純 C 的話大概也只有這種辦法？），在 Vulkan-Hpp 裡面錯誤會變 exception 被 throw 回來。但是我單純的沒有很喜歡 try-catch，比較喜歡 `std::expected` 那種的，但是開 Vulkan-Hpp 的 `VULKAN_HPP_NO_EXCEPTIONS` 的話又會有各種破病，像是錯誤不會被 throw 而是直接被 assert 掉（？？？）之類的。總之我 [左看看](https://github.com/KhronosGroup/Vulkan-Hpp/issues/1498) [右看看](https://github.com/KhronosGroup/Vulkan-Hpp/pull/1474) 都沒有解決，最後還是乖乖 try-catch。

像這種「錯誤處理到底應該怎麼做」的問題，感覺現在我沒有辦法找到答案的根本原因就是開發經驗還太少了，或者說我太菜了，就先隨便吧。

比較好笑的是這一段錯誤處理在 tutorial 的 sample code 裡面完全沒有出現，不知道是不是 library 版本問題。至少在我的版本上編譯的話那份 sample code 應該是不會 work =w=

## Cmake 和 make

原本 build system 是想用 cmake 的，但是我怎麼搞就是搞不懂到底怎麼正確使用 cmake，像是怎麼處理外部 dependency 之類的問題，或者說我根本上的沒有懂 cmake 的運作原理到底是什麼。只是他實在不是我想處理的重點，而且處理 build system 還真有點無聊，所以我還是落敗了。

後來乖乖回去用 make，makefile 的規則對我來說還是比較好懂一點，至少我能知道 makefile 哪一行會什麼時候被怎麼拿出來跑，之類的。

處理 build system 的時候還額外學會一些生活小技能（像是 g++ 可以 `-MMD` 產生 `.cpp` 檔的 header dependencies 之類的，極有用），應該算是額外收穫。

## 下一步

一說是 Vulkan 會 setup 之後，後面的事情就不會這麼坐牢了，多寫一點什麼就可以多看到一點什麼；不過一看 tutorial 後面還有二十篇我整個都不好了。我覺得我至少想學會到 compute pipeline 和 ray tracing pipeline 之類的，然後再看看想做一點什麼實際應用，其實也沒有明確的目標，也許是重寫我們的計圖 final project 或者其他，再說。

不過其實也不排除我下禮拜或是開學後就又不動這個計畫了，不知道下一篇牙牙學 Vulkan 什麼時候可以寫出來。

## Reference

各種我有頻繁用到、或覺得很有用、或覺得也許會有用的東西。其實其貌不揚的 Vulkan Registry 讓我有點意外，這個東西居然比我想像中好看．好讀．好用多了。

- [Vulkan Tutorial (by Alexander Overvoorde)](https://vulkan-tutorial.com/Introduction)
- [Khronos Vulkan Tutorial](https://docs.vulkan.org/tutorial/latest/00_Introduction.html)
- [VulkanGuide](https://vkguide.dev/)
- [Vulkan Registry](https://registry.khronos.org/vulkan/specs/latest/man/html/)
- [Vulkan-Hpp GitHub repository](https://github.com/KhronosGroup/Vulkan-Hpp/tree/main)
