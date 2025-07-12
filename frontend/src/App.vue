<template>
  <div id="app">
    <ChatInterface />
  </div>
</template>

<script setup>
import ChatInterface from './components/ChatInterface.vue';
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, 
               Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

#app {
  height: 100vh;
  width: 100vw;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

#app::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 25% 25%, rgba(61, 167, 205, 0.1) 0%, transparent 20%),
    radial-gradient(circle at 75% 75%, rgba(52, 168, 83, 0.1) 0%, transparent 20%);
  z-index: 0;
}

#app > * {
  position: relative;
  z-index: 1;
}
</style>