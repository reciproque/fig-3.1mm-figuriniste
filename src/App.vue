<script setup>

import { ref, onMounted } from 'vue'
import LanguageScreen from './components/LanguageScreen.vue'
import VideoPlayer from './components/VideoPlayer.vue'


// Chargement des dialogues et textes d'interface depuis Json

const dialogs = ref({});
const texts = ref({});

onMounted(async () => {
  try {
    const dialogsRes = await fetch('texts/dialogs.json');
    dialogs.value = await dialogsRes.json();

    const textsRes = await fetch('texts/interface.json');
    texts.value = await textsRes.json();
  } catch (error) {
    console.error('Erreur lors du chargement des fichiers JSON : ', error);
  }
});

//

// Langue globale du programme

const selectedLanguage = ref(null)

function onLanguageSelected(lang) {
  selectedLanguage.value = lang
}

//

</script>

<template>
  <div class="screen">

    <LanguageScreen v-if="!selectedLanguage" @language-selected="onLanguageSelected"
    :instructions="[texts?.[0]?.['texte-FR'], texts?.[1]?.['texte-FR'], texts?.[2]?.['texte-FR'], texts?.[3]?.['texte-FR'], texts?.[4]?.['texte-FR'], texts?.[5]?.['texte-FR']]" />
    <VideoPlayer v-else :language="selectedLanguage" />

    <div class="debug debug-versions" v-if="dialogs && Object.keys(dialogs).length && texts && Object.keys(texts).length" >    
      Numéro de versions<br>
      Build du 22/10/2025 à 18h10<br>
      Interface : {{ texts[Object.keys(texts).length-1]["texte-FR"] }} <br>
      Dialogues : {{ dialogs[Object.keys(dialogs).length-1]["texte-FR"] }} <br>
    
    </div>

</div>

    <!-- TODO : modale inactivité et reload -->

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
  font-size: 38px;
  color: white;
  font-family: 'Gotham-Black';
  font-weight: 300;
  filter: drop-shadow(0 0 29px rgba(0, 0, 0, 0.5));
  text-align: center;
}

.debug {
  /* display: none; */
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
