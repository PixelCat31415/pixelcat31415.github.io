---
title: 牙牙學 Vulkan（三）
date: 2026-01-27 03:09:34
tags: [Vulkan, C++]
---

又放假了，所以回頭來學畫畫。這個專案的進度龜速，因為我學期間基本沒空搞其他東西，再加上我確實的學藝不精寫程式效率奇差，都常常覺得怎麼我搞了這麼久還在這裡 😔（more on this later）

## 前情提要

半年前的 [上一篇](https://pixelcat31415.github.io/2025/08/12/vulkan-2-buffers/) 的進度大概是會畫一個任意的模型。理論上到這裡就可以很暴力的畫出任意我想畫的東西了，所以扣除效能問題之外根本就可以寫一個完整的會動的遊戲了；但是大問題是原本的程式碼整個塞在同一個有 1200 行的檔案裡面，擴展性基本是零，所以這是一個我必須要第一個處理的問題。

## 重寫（幾乎）

其實也不是說一個檔案寫很長就很糟糕，是在說原本我只有一個 class 裝下一切所有的東西，包含：

```c++
GLFWwindow* window_;
vk::raii::Context context_;
vk::raii::Instance instance_;
vk::raii::DebugUtilsMessengerEXT debug_messenger_;
vk::raii::SurfaceKHR surface_;
vk::raii::PhysicalDevice physical_device_;
vk::raii::Device device_;
uint32_t queue_family_index_;
vk::raii::Queue device_queue_;
uint32_t swapchain_image_count_;
uint32_t parallel_rendering_count_;
vk::raii::SwapchainKHR swapchain_;
std::vector<vk::Image> swapchain_images_;
std::vector<vk::raii::ImageView> swapchain_image_views_;
vk::Format swapchain_image_format_;
vk::Extent2D swapchain_extent_;
vk::raii::Pipeline graphics_pipeline_;
vk::raii::DescriptorSetLayout descriptor_set_layout_;
vk::raii::PipelineLayout graphics_pipeline_layout_;
vk::raii::CommandPool graphics_command_pool_;
vk::raii::CommandPool transfer_command_pool_;
std::vector<vk::raii::CommandBuffer> command_buffers_;
std::vector<vk::raii::Semaphore> present_finished_semaphores_;
std::vector<vk::raii::Semaphore> render_finished_semaphores_;
std::vector<vk::raii::Fence> draw_fences_;
uint32_t semaphore_index_ = 0;
uint32_t frame_index_ = 0;
bool swapchain_outdated_ = false;
vk::raii::Buffer vertex_buffer_;
vk::raii::DeviceMemory vertex_buffer_memory_;
vk::raii::Buffer index_buffer_;
vk::raii::DeviceMemory index_buffer_memory_;
std::vector<vk::raii::Buffer> uniform_buffers_;
std::vector<vk::raii::DeviceMemory> uniform_buffers_memory_;
std::vector<void*> uniform_buffers_mapping_;
vk::raii::DescriptorPool descriptor_pool_;
std::vector<vk::raii::DescriptorSet> descriptor_sets_;
vk::raii::Image texture_image_;
vk::raii::DeviceMemory tetxure_image_memory_;
vk::raii::ImageView texture_image_view_;
vk::raii::Sampler texture_sampler_;
vk::Format depth_format_;
std::vector<vk::raii::Image> depth_image_;
std::vector<vk::raii::DeviceMemory> depth_image_memory_;
std::vector<vk::raii::ImageView> depth_image_views_;
```

其實還蠻好笑的，根本就是實質意義的全域變數。基於各種所有你想得到的原因我把這個宇宙 class 裡面的東西拆成很多個部份，像是有一個類裝跟 swapchain 有關的東西，或是像實做一個類包裝 buffer 和對應的 device memory，之類的。

必須說剛開始的時候我根本不知道我該怎麼做才能讓他足夠分離、足夠精簡、又足夠好用、讓我以後可以輕鬆的擴展或使用，所以我去問 LLM 了。我問他我如果想為了 3D 遊戲寫一個 renderer，一般來說這種東西會有哪些元件和 expose 哪些介面，讓我思考一下我該怎麼實做；LLM 的回答我沒有很滿意，他講了一大段但是我感覺要不是在講我已經知道的不然就是說得很模糊，感覺有可能其實連我都不知道我的問題是什麼，我不知道我該知道什麼才能幫助我往「寫一個適合 3D 遊戲的渲染引擎」的目標前進。

但是 LLM 說了一句讓我印象很深的話是「我應該從『誰擁有一項資源』的角度思考」。我以前寫程式的思維模式都是 procedural 的，像是我應該用什麼順序照著做這些事情，對我來說物件一直都像是 service/functionality provider 而不是 resource holder，所以我覺得這句話對我來說特別重要，那是一個根本上思維模式層級的問題。我根據我的理解把整個程式在架構上重寫了一次，現在看起來還算順眼，之後大概可以開始預謀用這個 renderer 做點什麼事情了。

## 知識牆

我原本的目標是寫一個小遊戲，但是要寫遊戲總要有某種概念上的遊戲引擎吧？像是輸入要怎麼處理、要怎麼抽象化遊戲內的實體和渲染機制，等等的，要是只寫一個遊戲而用很暴力的方式隨便處理的話那就無聊了，要是能寫一個完整一些的遊戲引擎的話應該會是有趣的嘗試，所以現在姑且把一個遊戲引擎當做目標。

我覺得最大的障礙就是我確實的知識不足了。當我說出「我要寫一個遊戲引擎」的時候我甚至不知道一個完整的遊戲引擎應該要有哪些部份，幾乎沒用過遊戲引擎，唯一經驗是去年 challenge 用 godot 做的小遊戲，我覺得在這個條件下我對我自己做出的任何 design desicion 都沒有任何信心。思而不學則殆。

總之現在的話也許會想先不真的寫程式，去到處看看關於遊戲引擎的書、教學、甚至是上手用用看，直到我覺得我又準備好了的那天。

## 其他閒話

不可避免的開始思考有沒有可能我有機會進入遊戲引擎或圖形渲染開發一類的工作，不過我猜大概是沒有，這種領域的門檻看起來都好高，我覺得我能不能作為 software developer 混一口飯吃搞不好都是個問題了。我一直覺得作為一個寫程式的人有一個自己作為興趣的專案是一件讓我很嚮往的事情，他不會成為一個世界頂尖的或突破性的發明，我沒有要改變世界，我自己覺得開心就是唯一的最高目標，希望我能堅持這個願望很多年。

下一次更新這個系列會是什麼時候呢？
