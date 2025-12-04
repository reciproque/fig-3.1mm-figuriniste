<script setup>

import { gsap } from 'gsap';

import { onMounted } from 'vue';

import { defineEmits, ref } from 'vue'


const { instructions } = defineProps({
  instructions: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['language-selected'])

let canClick = true;
function selectLanguage(lang) {
  showVoile.value = false;
  clearTimeout(TOvoile);

  if (canClick) {
    document.getElementById(lang).style.animation = "none"
    gsap.from(document.getElementById(lang), { scale: 0.9, duration: 1, ease: "bounce.out" })
    setTimeout(() => emit('language-selected', lang), 800);
  }
  
  canClick = false;
}

// Animation de début (fade in)
onMounted(() => {
  gsap.from(document.querySelector("h1"), { opacity: 0, duration: 3 })
  gsap.from(document.querySelectorAll("h2"), { opacity: 0, duration: 3 })
  gsap.from(document.querySelectorAll("span"), { opacity: 0, duration: 3, delay: 1 })
  gsap.from(document.getElementById("FR"), { opacity: 0, duration: 4, delay: 0.5 })
  gsap.from(document.getElementById("EN"), { opacity: 0, duration: 4, delay: 0.75 })
  gsap.from(document.getElementById("DE"), { opacity: 0, duration: 4, delay: 1 })

})

const showVoile = ref(false);

let TOvoile = setTimeout(()=>{showVoile.value=true}, 600*1000);

function clickOnVoile() {
  showVoile.value = false;
  clearTimeout(TOvoile);
  TOvoile = setTimeout(()=>{showVoile.value=true}, 600*1000);
}


</script>

<template>
  <div v-if="showVoile" class="voile" @mousedown="clickOnVoile">
    <img src="/assets/main-touch.png" alt="">
  </div>
  <div class="language-screen">
    <h1>{{ instructions[0] }}</h1>
    <h2>{{ instructions[1] }}</h2>
    <h2>{{ instructions[2] }}</h2>
    <div class="flags-row">
      <div class="flag"><img src="/assets/en.png" id="EN" alt="" @click="selectLanguage('EN')"><br><span>{{
        instructions[4] }}</span></div>
              <div class="flag"><img src="/assets/fr.png" id="FR" alt="" @click="selectLanguage('FR')"><br><span>{{
        instructions[3] }}</span></div>
      <div class="flag"><img src="/assets/de.png" id="DE" alt="" @click="selectLanguage('DE')"><br><span>{{
        instructions[5] }}</span></div>
    </div>
  </div>

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
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

#FR {
    animation: flags 8s infinite ;
}

#EN {
    animation: flags 8s 0.4s infinite ;
}

#DE {
    animation: flags 8s 0.8s infinite;
}

@keyframes flags {
  0% {
    transform: scale(1);
  }

  25% {
    transform: scale(1.2);
  }

  50% {
    transform: scale(1);
  }

  100% {
    transform: scale(1);
  }
  
}

.flag img {
  width: 350px;

}

.flags-row {
  display: flex;
  flex-direction: row;
  padding-top: 180px;
  padding-bottom: 80px;
  gap: 96px;
  font-family: 'Gotham-Book';
  text-transform: uppercase;
  font-size: 32px;
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

span {
  font-size: 23px;
  margin: 10px 70px;
}

.voile {
  cursor: pointer;
  position: absolute;
  z-index: 100;
  width: 1920px;
  height: 1080px;
  background-color: #0e0e0b9c;
}

.voile img {
  width: 300px;
  position: absolute;
  right: 500px;
  bottom: -40px;
  animation: main 5s infinite;
  filter: invert();
}

@keyframes main {
  0% {
    transform: scale(1.1);
  }
  50% {
    transform: scale(1);
  }
  100% {
    transform: scale(1.1);
  }
}
</style>
