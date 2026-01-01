---
title: 牙牙學 Vulkan（二）
date: 2025-08-12 05:29:09
tags: [Vulkan, C++]
---

![](/images/2025-08-vulkan-2-buffers.png)

## Buffers

從[上一篇](/2025/08/02/vulkan-1-the-triangle/)到現在差最多的應該是各種 Buffer，有 vertex buffer、index buffer、depth buffer，還有 image 也要有自己的 buffer。除了 depth buffer 以前不用自己造之外，應該所有東西在 OpenGL 就都用過了，但是 vulkan 可以讓你自己決定哪些東西要放在哪裡的記憶體、還有什麼時候要去搬資料這點，我覺得還蠻有趣的。以前 OpenGL 都全部幫你黑盒子做好，現在可以真的看到我的記憶體都在做什麼事情的感覺。

之前在建立 swapchain 的時候就有碰過一點點的 image view，在自己搞過 texture 之後也變得比較清楚 image 和 image view 的角色是什麼。還有在把圖片傳到 GPU 上的時候要轉換 image layout，到這個時候才看懂先前 render loop 裡面在搞 image layout 是在做什麼，還有 barrier 是怎麼用的。

## Windows

另外一個大更新是我換到 Windows 上了。一方面是因為 Ubuntu 奇怪的破病，另外一方面是還是有個遙遠的目標是想做出跨平台，所以決定試試 Windows。但是 Windows 真的破病很多，或者是因為我平常不用 Windows 所以整個系統環境很荒蕪，編輯器之類的各種工具都沒有用得很順手。不過我覺得還是值得再多試一下。

最大的不舒服應該是 build system。Makefile 對我來說還蠻容易理解的，至少我知道我要 build 一個 target 的時候都跑到了哪些指令，我也能自己掌控編譯和連結之類的每一步。但是像 visual studio 很大程度自動化這個過程，讓我沒辦法直接看到他都幫我做了什麼，我要在某個地方加上自己的 dependency 或 build step 也沒有那麼簡單。當然如果我夠會使用 visual studio 的話這些都不是問題，但是我還是覺得要做到同樣的事情 Makefile 可以更簡單直接的完成。

感覺在 linux 上只要我會用指令我就可以隨便做我想做的事情；在 windows 上如果我想做的事情都是內建的那就天下太平，但是只要我想做一點點不一樣的事情我就要準備好坐牢。

還是沒有下定決心征服 cmake 或 premake 之類的。處理 build system 真的還蠻無聊的，我決定維持現狀就好。

## 模型渲染

上面那張圖裡面的模型是從 tutorial 裡偷來的。其實會用各種 buffer 之後渲染模型是最簡單的一步，只要會讀模型檔就好。只是他看起來很酷炫所以當這篇文的封面圖 😋
