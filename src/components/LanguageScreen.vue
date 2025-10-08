<script setup>
defineProps({

})

import texts from '../../assets/interface.json'

import { gsap } from 'gsap';

import { onMounted } from 'vue';

function getText(n, lang) {
  if (lang=="FR") return texts[n]["texte-FR"];
  if (lang=="EN") return texts[n]["texte-EN"];
  if (lang=="DE") return texts[n]["texte-DE"];
}

let lang = "FR";

function select(selectedLang) {
  lang = selectedLang;
  gsap.from(document.getElementById(selectedLang), {scale:0.9, duration:1, ease:"bounce.out"})
} 

onMounted(() => {
  gsap.from(document.querySelector("h1"), {opacity:0, duration:3})
  gsap.from(document.querySelectorAll("h2"), {opacity:0, duration:3})

  gsap.from(document.querySelector(".paraph-lang"), {opacity:0, duration:3, delay:1})
  gsap.from(document.getElementById("FR"), {opacity:0, duration:4, delay:0.5})
  gsap.from(document.getElementById("EN"), {opacity:0, duration:4, delay:0.75})
  gsap.from(document.getElementById("DE"), {opacity:0, duration:4, delay:1})

})


</script>

<template>
  <div class="language-screen">
  <h1>{{ getText(0, lang) }}</h1> <br>
  <h2>{{ getText(1, lang) }}</h2> <br>
  <h2>{{ getText(2, lang) }}</h2> 
  <div class="flags-row">
    <div class="flag" id="FR"><img src="../../assets/fr.png" alt="" @click="select('FR')"></div>
    <div class="flag" id="EN"><img src="../../assets/en.png" alt="" @click="select('EN')"></div>
    <div class="flag" id="DE"><img src="../../assets/de.png" alt="" @click="select('DE')"></div>
  </div>
  <div class="paraph-lang"><span>{{ getText(3, lang) }}</span></br>
    <span>{{ getText(4, lang) }}</span> </br>
    <span>{{ getText(5, lang) }}</span> </br>
  </div></div>

</template>

<style scoped>
.language-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.flag {
  cursor: pointer;
}

.flags-row {
  display: flex;
  flex-direction: row;
  padding-top: 80px;
  padding-bottom: 80px;
  gap: 96px;
}

.paraph-lang {
  font-family: 'Gotham-Book';
  text-transform: uppercase;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 32px;
}
</style>
