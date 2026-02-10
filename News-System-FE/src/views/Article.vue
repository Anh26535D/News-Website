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
                    </ul>
                </nav>
            </section>
        </header>

        <main v-if="article" class="main-article" role="main">
            <article class="article">
                <h2>{{ article.title }}</h2>
                <p>
                    <small>{{ article.publishedAt }}</small><br />
                    By {{ article.author || 'Unknown' }}
                </p>

                <div class="headline"
                    :style="{ backgroundImage: `url(${article.urlToImage})`, backgroundSize: 'cover', height: '400px' }">
                </div>

                <p class="intro-text">{{ article.content }}</p>
                <p>{{ article.description }}</p>

                <p>
                    Reference:
                    <a :href="article.url" target="_blank" id="reference">
                        {{ article.url }}
                    </a>
                </p>
            </article>

            <aside class="sidebar" role="complementary">
                <h2>Most Read</h2>
                <a href="#" v-for="i in 5" :key="i">
                    <div class="sidebar-headline">
                        <h3>Pariatur laboriosam voluptatum labore tenetur</h3>
                        <p class="exact-time">13:53h</p>
                    </div>
                </a>
            </aside>
        </main>

        <main v-else class="main-article">
            <p>Loading article...</p>
        </main>

        <div class="footer-links">
            <ul class="social-media-links">
                <li><a href="http://twitter.com"><span class="screen-reader-text">Twitter</span></a></li>
                <li><a href="http://facebook.com"><span class="screen-reader-text">Facebook</span></a></li>
            </ul>
            <ul class="main-footer-links">
                <li><a href="#world">World</a></li>
                <li><a href="#politics">Politics</a></li>
            </ul>
            <ul class="our-address">
                <li>Our Address:</li>
                <li>So 1 Dai Co Viet</li>
                <li>Hai Ba Trung, Ha Noi, VN</li>
            </ul>
        </div>

        <footer role="contentinfo">
            <p>2019 &copy; by Frivizn Studio</p>
            <a class="scroll-top" href="#top"></a>
        </footer>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import apiClient from '@/plugins/axios';

const route = useRoute();
const article = ref(null);
let hoverTimer = null;
let scrollTimer = null;

// --- UTILS ---
const getDeviceType = () => {
  const ua = navigator.userAgent;
  if (/Mobile|Android|iP(hone|od)/i.test(ua)) return "mobile";
  return "desktop";
};

const sendTrack = async (eventType, payload) => {
  try {
    await apiClient.post("/track", {
      user_id: localStorage.getItem("user-id"),
      event_type: eventType,
      payload: payload,
      device: getDeviceType(),
      session_id: sessionStorage.getItem("session-id")
    });
  } catch (err) { console.error("Tracking failed", err); }
};

// --- TRACKING LOGIC ---

// 1. Tracking Scroll (Đo độ sâu bài viết người dùng đã đọc)
const handleScrollTrack = () => {
  if (scrollTimer) clearTimeout(scrollTimer);
  scrollTimer = setTimeout(() => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrollPercent = Math.round((scrollTop / scrollHeight) * 100);

    sendTrack("scroll_article_detail", {
      article_id: route.params.id,
      distance_px: Math.round(scrollTop),
      percentage: scrollPercent
    });
  }, 500);
};

// --- DATA INITIALIZATION ---
const fetchArticle = async () => {
  try {
    const response = await apiClient.get(`/news/${route.params.id}`);
    article.value = response.data;
    document.title = article.value.title || "Article Detail";
    
    // Track ngay khi người dùng vào xem bài (View Event)
    sendTrack("view_article", {
      article_id: route.params.id,
      title: article.value.title
    });
  } catch (error) { console.error(error); }
};

onMounted(() => {
  fetchArticle();
  window.addEventListener("scroll", handleScrollTrack);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScrollTrack);
  if (scrollTimer) clearTimeout(scrollTimer);
  if (hoverTimer) clearTimeout(hoverTimer);
});
</script>

<style scoped>
.main-article {
    display: flex;
    gap: 20px;
    padding: 20px;
}

.article {
    flex: 3;
}

.sidebar {
    flex: 1;
}

.headline {
    margin: 20px 0;
    border-radius: 8px;
}
</style>