<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue';

const generateRandomString = (length) => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
};

const initIdentifiers = () => {
  if (!localStorage.getItem('user-id')) {
    const unixTime = Date.now();
    const agent = navigator.userAgent.replace(/\s+/g, '-').substring(0, 50);
    const randomStr = generateRandomString(10);

    const userId = `${unixTime}-${agent}-${randomStr}`;
    localStorage.setItem('user-id', userId);
    console.log('Created new user-id:', userId);
  }

  if (!sessionStorage.getItem('session-id')) {
    const sessionId = generateRandomString(32);
    sessionStorage.setItem('session-id', sessionId);
    console.log('Created new session-id:', sessionId);
  }
};

onMounted(() => {
  initIdentifiers();
})
</script>

<style></style>