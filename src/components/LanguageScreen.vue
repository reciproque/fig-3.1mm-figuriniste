<script setup>
defineProps({
  msg: {
    type: String,
    required: false,
  },
})

import { gsap } from 'gsap';

import { onMounted } from 'vue'

onMounted(() => {
gsap.from(document.querySelector("h1"), {opacity:0, duration:3})
gsap.from(document.querySelector(".paraph-lang"), {opacity:0, duration:3, delay:1})
gsap.from(document.getElementById("fr"), {opacity:0, duration:4, delay:0.5})
gsap.from(document.getElementById("en"), {opacity:0, duration:4, delay:0.75})
gsap.from(document.getElementById("de"), {opacity:0, duration:4, delay:1})

})


</script>

<template>
  <div class="language-screen">
  <h1>Le métier du figuriniste</h1>
  <div class="flags-row">
    <div class="flag" id="fr"><img src="../../assets/fr.png" alt=""></div>
    <div class="flag" id="en"><img src="../../assets/en.png" alt=""></div>
    <div class="flag" id="de"><img src="../../assets/de.png" alt=""></div>
  </div>
  <div class="paraph-lang"><span>Choisissez votre langue</span></br>
    <span>Choose your language</span> </br>
    <span>Wählen Sie Ihre Sprache</span> </br>
  </div></div>

</template>

<style scoped>
.language-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

h1 {
  font-size: 80px;
  font-family: 'Gotham-Black';
  text-transform: uppercase;
  font-weight: 800;
  padding-top: 180px;

}

.flag {
  cursor: pointer;
}

.flags-row {
  display: flex;
  flex-direction: row;
  padding-top: 160px;
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
