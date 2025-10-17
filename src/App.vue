<script setup>

import { ref } from 'vue'
import LanguageScreen from './components/LanguageScreen.vue'
import VideoPlayer from './components/VideoPlayer.vue'

import texts from '../public/texts/interface.json'
import dialogs from '../public/texts/dialogs.json'



// Langue globale du programme
const selectedLanguage = ref(null)

function onLanguageSelected(lang) {
  selectedLanguage.value = lang
}

</script>

<template>
  <div class="screen">

    <!-- TODO : gérer le passage d'une step à l'autre + étapes interactives -->
    <LanguageScreen v-if="!selectedLanguage" @language-selected="onLanguageSelected" />
    <VideoPlayer v-else :language="selectedLanguage" />

    <div class="debug debug-versions">    
    Numéro de versions<br>
    Build du 17/10/2025 à 16:30 <br>
    Interface : {{ texts[Object.keys(texts).length-1]["texte-FR"] }} <br>
    Dialogues : {{ dialogs[Object.keys(dialogs).length-1]["texte-FR"] }}</div>

    <!-- TODO : modale inactivité et reload -->
    <!-- <VideoPlayer :language='"FR"' /> -->

  </div>
</template>

<style>
@font-face {
  font-family: 'Gotham-Black';
  src: url('/assets/Gotham-Black.otf') format("opentype");
}

@font-face {
  font-family: 'Gotham-Book';
  src: url('/assets/Gotham-Book.otf') format("opentype");
}

.screen {
  background-image: url('/public/assets/background.png');
  background-size: cover;
  width: 1920px;
  height: 1080px;
  margin: 0;
  padding: 0;
  position: absolute;
  top: 0;
  left: 0;
  color: #ffffff;
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
  font-family: 'Gotham-Black';
  font-weight: 300;
  filter: drop-shadow(0 0 29px rgba(0, 0, 0, 0.5));
  text-align: center;
}

.debug {
  color: white;
  position: absolute;
  padding: 10px;
  background-color: rgba(255, 184, 184, 0.3);
  z-index: 1000;

}

.debug-versions {
  bottom:0px;
  left:0px;
}
</style>
