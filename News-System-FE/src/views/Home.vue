<template>
  <div class="content-wrap">
    <header role="banner">
      <section class="nav-section">
        <div class="logo">
          <router-link to="/" title="Five Mem">Five Mem</router-link>
        </div>
        <nav class="nav-menu" role="navigation">
          <ul class="nav-links">
            <li><a href="/" title="Home">Home</a></li>
            <li>
              <input type="text" id="searchInput" placeholder="Search" v-model="searchQuery"
                @keydown.enter="handleSearch">

              <h2 v-if="gIndex === 0">
                {{ isSearching ? "List result search for you" : "List news for you" }}
              </h2>
            </li>
          </ul>
        </nav>
      </section>
    </header>

    <main class="main" role="main">
      <div class="top-news">
        <section v-if="latestNews" class="latest-news">
          <div class="headline-lastest-news"
            :style="{ backgroundImage: `url(${latestNews.urlToImage})`, backgroundSize: 'cover' }"
            @mouseenter="startHoverLatest(latestNews)" @mouseleave="cancelHover">
            <p>Hot New</p>
            <a :href="latestNews.url">
              <h1>{{ latestNews.title }}</h1>
            </a>
          </div>
        </section>

        <section class="top-stories">
          <h2>Latest stock news</h2>
          <div class="tradingview-widget-container" ref="tradingView" @mouseenter="startHoverTradingView"
            @mouseleave="cancelHover">
            <div class="tradingview-widget-container__widget"></div>
            <div class="tradingview-widget-copyright">
              <a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank">
                <span class="blue-text">Track all markets on TradingView</span>
              </a>
            </div>
          </div>
        </section>
      </div>

      <div class="main-content-list">
        <section v-for="(group, gIndex) in groupedNews" :key="gIndex" class="world">
          <h2 v-if="gIndex === 0">List news for you</h2>
          <h2 v-else></h2>
          <div v-for="(story, sIndex) in group" :key="story._id" :class="['story', `story-${sIndex + 1}`]"
            @mouseenter="startHover(story)" @mouseleave="cancelHover">
            <router-link :to="`/article/${story._id}`">
              <div class="story-img">
                <img :src="story.urlToImage" :alt="story.description" />
              </div>
              <div class="story-headline">
                <h3>{{ story.title }}</h3>
                <p class="exact-time">{{ story.publishedAt }}</p>
              </div>
            </router-link>
          </div>
        </section>
      </div>

      <div class="load-more-wrapper">
        <button id="btnMore" @click="handleLoadMore">More ...</button>
      </div>
    </main>

    <div class="footer-links">
      <ul class="social-media-links">
        <li>
          <a href="http://twitter.com"><span class="screen-reader-text">Twitter</span></a>
        </li>
        <li>
          <a href="http://facebook.com"><span class="screen-reader-text">Facebook</span></a>
        </li>
        <li>
          <a href="http://linkedin.com"><span class="screen-reader-text">LinkedIn</span></a>
        </li>
        <li>
          <a href="http://youtube.com"><span class="screen-reader-text">YouTube</span></a>
        </li>
        <li>
          <a href="http://instagram.com"><span class="screen-reader-text">Instagram</span></a>
        </li>
      </ul>

      <ul class="main-footer-links">
        <li><a href="#world" title="World">World</a></li>
        <li><a href="#politics" title="Politics">Politics</a></li>
        <li><a href="#business" title="Business">Business</a></li>
        <li><a href="#sport" title="Sport">Sport</a></li>
        <li>
          <a href="#entertainment" title="Entertainment">Entertainment</a>
        </li>
        <li><a href="#science" title="Science">Science</a></li>
        <li><a href="#travel" title="Travel">Travel</a></li>
        <li><a href="#health" title="Health">Health</a></li>
        <li><a href="#style" title="Style">Style</a></li>
        <li><a href="#weather" title="Weather">Weather</a></li>
        <li><a href="#video" title="Video">Video</a></li>
      </ul>

      <ul class="info-links">
        <li>
          <a href="#terms-of-use" title="Terms of Use">Terms of Use</a>
        </li>
        <li>
          <a href="#privacy-policy" title="Privacy Policy">Privacy Policy</a>
        </li>
        <li><a href="#about-us" title="About Us">About Us</a></li>
        <li>
          <a href="#advertising" title="Advertising">Advertising</a>
        </li>
        <li><a href="#sitemap" title="Sitemap">Sitemap</a></li>
      </ul>

      <ul class="our-address">
        <li>Our Address:</li>
        <li>So 1 Dai Co Viet</li>
        <li>Hai Ba Trung, Ha Noi, VN</li>
        <li>12345678910</li>
      </ul>
    </div>

    <footer role="contentinfo">
      <p>2019 &copy; by Frivizn Studio</p>
      <a class="scroll-top" href="#top"></a>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from "vue";
import apiClient from "@/plugins/axios";
const latestNews = ref(null);
const listNews = ref([]);
const searchQuery = ref("");
const skip = ref(0);
const isSearching = ref(false);

let hoverTimer = null; // Biến dùng để lưu bộ đếm thời gian
let scrollTimer = null;

const handleScrollTrack = () => {
  // Xóa timer cũ, chỉ gửi khi người dùng dừng cuộn 500ms
  if (scrollTimer) clearTimeout(scrollTimer);

  scrollTimer = setTimeout(async () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrollPercent = Math.round((scrollTop / scrollHeight) * 100);

    const trackBody = {
      user_id: localStorage.getItem("user-id"),
      event_type: "scroll_page",
      payload: {
        distance_px: Math.round(scrollTop),
        percentage: scrollPercent,
        current_url: window.location.href
      },
      device: getDeviceType(),
      session_id: sessionStorage.getItem("session-id")
    };

    try {
      // Chỉ gửi nếu người dùng đã cuộn được một khoảng đáng kể (ví dụ > 100px)
      if (scrollTop > 100) {
        await apiClient.post("/track", trackBody);
        console.log(`Tracked scroll: ${scrollPercent}%`);
      }
    } catch (error) {
      console.error("Failed to send scroll tracking:", error);
    }
  }, 500); // Đợi người dùng dừng cuộn 500ms mới gửi tin
};

// Hàm bổ trợ để xác định device
const getDeviceType = () => {
  const ua = navigator.userAgent;
  if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) return "tablet";
  if (/Mobile|Android|iP(hone|od)|IEMobile|BlackBerry|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/i.test(ua)) return "mobile";
  return "desktop";
};

// --- Logic Tracking Hover ---

const startHoverLatest = (news) => {
  // Xóa timer hiện tại nếu có
  if (hoverTimer) clearTimeout(hoverTimer);

  // Khởi tạo timer 300ms
  hoverTimer = setTimeout(async () => {
    const trackBody = {
      user_id: localStorage.getItem("user-id"),
      event_type: "hover_latest_news", // Định danh riêng cho tin nóng
      payload: {
        article_id: news._id || "latest_headline", // ID của tin hoặc fallback
        article_data: {
          title: news.title,
          url: news.url,
          is_headline: true
        }
      },
      device: getDeviceType(),
      session_id: sessionStorage.getItem("session-id")
    };

    try {
      await apiClient.post("/track", trackBody);
      console.log("Tracked hover for Latest News:", news.title);
    } catch (error) {
      console.error("Failed to send Latest News tracking:", error);
    }
  }, 300);
};



const startHover = (story) => {
  // Nếu đang có một timer chạy, xóa nó đi để tránh trùng lặp
  if (hoverTimer) clearTimeout(hoverTimer);

  // Khởi tạo timer 300ms
  hoverTimer = setTimeout(async () => {
    const trackBody = {
      user_id: localStorage.getItem("user-id"),
      event_type: "hover_article",
      payload: {
        article_id: story._id,
        article_data: {
          title: story.title,
          publishedAt: story.publishedAt,
          url: story.url
          // Bạn có thể thêm các field khác từ object story vào đây
        }
      },
      device: getDeviceType(),
      session_id: sessionStorage.getItem("session-id")
    };

    try {
      // Gửi API track về BE
      await apiClient.post("/track", trackBody);
      console.log("Tracked hover for article:", story._id);
    } catch (error) {
      console.error("Failed to send tracking:", error);
    }
  }, 300); // 300ms theo yêu cầu
};

const cancelHover = () => {
  if (hoverTimer) {
    clearTimeout(hoverTimer);
    hoverTimer = null;
  }
};

const startHoverTradingView = () => {
  // Xóa timer cũ nếu có
  if (hoverTimer) clearTimeout(hoverTimer);

  // Khởi tạo timer 300ms
  hoverTimer = setTimeout(async () => {
    const trackBody = {
      user_id: localStorage.getItem("user-id"),
      event_type: "hover_tradingview", // Định danh loại sự kiện
      payload: {
        widget_name: "Hotlists",
        market: "US Stock",
        current_url: window.location.href
      },
      device: getDeviceType(),
      session_id: sessionStorage.getItem("session-id")
    };

    try {
      await apiClient.post("/track", trackBody);
      console.log("Tracked hover for TradingView");
    } catch (error) {
      console.error("Failed to send TradingView tracking:", error);
    }
  }, 300);
};

const groupedNews = computed(() => {
  const groups = [];
  for (let i = 0; i < listNews.value.length; i += 3) {
    groups.push(listNews.value.slice(i, i + 3));
  }
  return groups;
});

const initData = async () => {
  try {
    const [listRes, latestRes] = await Promise.allSettled([
      apiClient.get("/news/common-articles"),
      apiClient.get("/news/lastest")
    ]);

    if (listRes.status === 'fulfilled' && listRes.value.status === 200) {
      listNews.value = listRes.value.data;
    } else {
      console.error("Lỗi tải list news:", listRes.reason);
    }

    if (latestRes.status === 'fulfilled' && latestRes.value.status === 200) {
      latestNews.value = latestRes.value.data;
    } else {
      console.error("Lỗi tải latest news:", latestRes.reason);
    }

  } catch (error) {
    console.error("Lỗi hệ thống:", error);
  }
};

const handleSearch = async () => {
  const value = searchQuery.value.trim();

  if (value.length !== 0) {
    skip.value = 0;
    isSearching.value = true;

    // --- Logic Tracking Search ---
    const searchTrackBody = {
      user_id: localStorage.getItem("user-id"),
      event_type: "search_action", // Đã đổi tên event cho đúng ngữ cảnh
      payload: {
        query: value
      },
      device: getDeviceType(),
      session_id: sessionStorage.getItem("session-id")
    };

    try {
      const [searchRes] = await Promise.all([
        apiClient.get("/news/search", { params: { q: value, skip: skip.value } }),
        apiClient.post("/track", searchTrackBody) // Gửi tracking POST
      ]);

      listNews.value = searchRes.data;
      console.log("Search tracked and data loaded for:", value);
    } catch (error) {
      console.error("Search or tracking error:", error);
    }
    // ----------------------------

  } else {
    isSearching.value = false;
    skip.value = 0;
    await initData();
  }
};

const handleLoadMore = async () => {
  skip.value += 9;
  const value = searchQuery.value.trim();

  try {
    let response;
    if (value.length !== 0) {
      // Đang trong chế độ tìm kiếm
      response = await apiClient.get("/news/search", {
        params: { q: value, skip: skip.value }
      });
    } else {
      response = await apiClient.get("/news/common-articles", {
        params: { skip: skip.value }
      });
    }

    if (response.data && response.data.length > 0) {
      listNews.value = [...listNews.value, ...response.data];
    } else {
      alert("No more news to load!");
    }
  } catch (error) {
    console.error("Load more error:", error);
  }
};

const initTradingView = () => {
  const script = document.createElement("script");
  script.type = "text/javascript";
  script.src =
    "https://s3.tradingview.com/external-embedding/embed-widget-hotlists.js";
  script.async = true;
  script.innerHTML = JSON.stringify({
    colorTheme: "light",
    dateRange: "12M",
    exchange: "US",
    showChart: true,
    locale: "en",
    width: "400",
    height: "600",
    isTransparent: false,
  });
  document.querySelector(".tradingview-widget-container").appendChild(script);
};

onMounted(async () => {
  await initData();
  initTradingView();
  window.addEventListener("scroll", handleScrollTrack);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScrollTrack);
  if (scrollTimer) clearTimeout(scrollTimer);
});

</script>

<style scoped>
.load-more-wrapper {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding-bottom: 2rem;
  font-size: large;
}

#btnMore {
  border-radius: 10px;
  background-color: #0866ff;
  color: #fff;
  padding: 8px 16px;
  border: none;
  cursor: pointer;
}

.headline-lastest-news {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 20px;
}
</style>
