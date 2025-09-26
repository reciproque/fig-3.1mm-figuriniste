<script setup>
import LanguageScreen from './components/LanguageScreen.vue'
</script>

<template>
  <div class="screen">
    <LanguageScreen/>

  </div>
</template>

<style>
@font-face {
  font-family: 'Gotham-Black';
  src: url('../assets/Gotham-Black.otf') format("opentype");
}

@font-face {
  font-family: 'Gotham-Book';
  src: url('../assets/Gotham-Book.otf') format("opentype");
}

.screen {
  background-image: url('../assets/background.png');
  background-size: cover;
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  position: absolute;
  top: 0;
  left: 0;
  color: #493C38;
}

</style>
