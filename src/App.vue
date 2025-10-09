<script setup>

import { ref } from 'vue'
import LanguageScreen from './components/LanguageScreen.vue'
import VideoPlayer from './components/VideoPlayer.vue'
import EbarbageStep from './components/EbarbageStep.vue'


// Langue globale du programme
const selectedLanguage = ref(null)

function onLanguageSelected(lang) {
  selectedLanguage.value = lang
}

</script>

<template>
  <div class="screen">

    <!-- <LanguageScreen v-if="!selectedLanguage" @language-selected="onLanguageSelected" /> -->
    <!-- TODO : gérer le passage d'une step à l'autre + étapes interactives -->
    <!-- <VideoPlayer v-else :language="selectedLanguage" step="Dessin 1" /> -->
    <EbarbageStep/>

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
  width: 1920px;
  height: 1080px;
  margin: 0;
  padding: 0;
  position: absolute;
  top: 0;
  left: 0;
  color: #493C38;
  overflow: hidden;
}

h1 {
  font-size: 80px;
  font-family: 'Gotham-Black';
  text-transform: uppercase;
  font-weight: 800;
  padding-top: 120px;

}

h2 {
  font-size: 50px;
  font-family: 'Gotham-Black';
  text-transform: uppercase;
  font-weight: 800;
}

.instruction {
  font-size: 50px;
  color: white;
  font-family: 'Gotham';
  font-weight: 700;
  filter: drop-shadow(0 0 29px rgba(0, 0, 0, 0.5));
  text-align: center;
}
</style>
