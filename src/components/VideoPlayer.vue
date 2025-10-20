<script setup>

import DialogBubble from './DialogBubble.vue';
import ChooseToolScreen from './ChooseToolScreen.vue'
import AssemblageStep from './AssemblageStep.vue';
import PeintureStep from './PeintureStep.vue';

const { language } = defineProps({
  language: {
    type: String,
    required: true
  }
})

const currentVideoId = ref(1);

const dialogs = ref({});
const texts = ref({});
const nbVideos = ref(0);

onMounted(async () => {
  try {
    const dialogsRes = await fetch('texts/dialogs.json');
    dialogs.value = await dialogsRes.json();
    console.log('✔ dialogs loaded:', dialogs.value);

    const textsRes = await fetch('texts/interface.json');
    texts.value = await textsRes.json();
    console.log('✔ texts loaded:', texts.value);

    nbVideos.value = Object.keys(dialogs.value).length - 1;
    await playSequence();

  } catch (err) {
    console.error('Erreur de chargement des fichiers JSON', err);
  }
});


import { gsap } from 'gsap';

import { ref, onMounted } from 'vue';

function getText(n, lang) {
  const entry = texts.value?.[n];
  if (!entry) return '';

  if (lang === "FR") return entry["texte-FR"] || '';
  if (lang === "EN") return entry["texte-EN"] || '';
  if (lang === "DE") return entry["texte-DE"] || '';

  return '';
}

function getDialog(n, lang) {
  const entry = dialogs.value?.[n];
  if (!entry) return '';

  if (lang === "FR") return entry["texte-FR"] || '';
  if (lang === "EN") return entry["texte-EN"] || '';
  if (lang === "DE") return entry["texte-DE"] || '';

  return '';
}

function getVideo(n) {
  const entry = dialogs.value?.[n];
  return entry?.["nomenclature-video"] || '';
}

function getDuration(n) {
  const entry = dialogs.value?.[n];
  return entry?.["duration"] ?? 0;
}

function getTimecodeStart(n) {
  const entry = dialogs.value?.[n];
  return entry?.["timecode-start"] != null ? entry["timecode-start"] * 1000 : 0;
}

function getTimecodeEnd(n) {
  const entry = dialogs.value?.[n];
  return entry?.["timecode-end"] != null ? entry["timecode-end"] * 1000 : 0;
}



let currentVideo = 0;

const isPlaying = ref(true);

// Timer pour debug
const timer = ref(0);
let timerInterval = null;


let dialogContent = getDialog(0, language)

const showBubble = ref(false)

function animateBubbleOut() {
  const bubble = document.querySelector(".dialog-bubble")
  if (bubble) {
    gsap.to(bubble, { scale: 0, duration: 0.5 })
  }
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const replaceToolName = ref(false);
const replaceToolNameNumber = ref(0);

async function resume(n) {
  isPlaying.value = true;
  animateBubbleOut();
  await delay(1000);
  showBubble.value = false;

  console.log(n);

  if (showDessin) {
    let goodAnswer = 6;
    showDessin.value = false;
    if (n == goodAnswer) {
      replaceToolName.value = false;
      currentVideo = 5;
    }
    else {
      replaceToolName.value = true;
      replaceToolNameNumber.value = n;
      currentVideo = 3;
    }
  }
  else {
    replaceToolName.value = false;
    currentVideo++;
  }
  await playSequence();
}

async function playSequence() {
  for (let i = currentVideo; i < nbVideos.value; i++) {
    currentVideo = i;

    // Précharge la vidéo suivante si elle existe
    if (i + 1 < nbVideos.value) {
      const nextSrc = import.meta.env.BASE_URL + 'assets/videos/' + String(getVideo(i + 1));
      await preloadVideo(nextSrc);
    }

    await playVideo(i);

    const end = dialogs.value?.[i]?.["end"];

    if (end === "skip") {
      isPlaying.value = true;
    }
    else if (end === "pause") {
      isPlaying.value = false;

      if (currentVideo === nbVideos.value- 1) {
        isPlaying.value = true;
        break;
      }

      // TODO : choisir en fonction du champ "pause"
      launchInteractiveStep("dessin");
      break;
    }
    else {
      console.warn(`⚠️ Champ "end" manquant ou non reconnu pour la vidéo ${i}:`, end);
      // Par défaut : continuer
      isPlaying.value = true;
    }

  }
}

const showDessin = ref(false);
const showEbarbage = ref(false);
const showAssemblage = ref(false);
const showPeinture = ref(false);
const showQR = ref(false);


function launchInteractiveStep(step) {
  console.log(step);

  switch (step) {
    case "dessin":
      showDessin.value = true;
      break;
    case "ebarbage":
      showEbarbage.value = true;
      break;
    case "assemblage":
      showAssemblage.value = true;
      break;
    case "peinture":
      showPeinture.value = true;
      break;
    case "qrcode":
      showQR.value = true;


    default:
      break;
  }
}

// Précharge une vidéo et retourne la vidéo invisible quand elle est prête
function preloadVideo(src) {
  return new Promise((resolve, reject) => {
    const video = document.createElement('video');
    video.src = src;
    video.preload = 'auto';
    video.style.display = 'none';
    document.body.appendChild(video);

    video.addEventListener('canplaythrough', () => {
      resolve(video);
    });

    video.addEventListener('error', (e) => {
      reject(e);
    });
  });
}


async function playVideo(n) {
  const videoToShow = currentVideoId.value === 1 ? document.getElementById('video2') : document.getElementById('video1');
  const videoToHide = currentVideoId.value === 1 ? document.getElementById('video1') : document.getElementById('video2');

  const nextVideoSrc = import.meta.env.BASE_URL + 'assets/videos/' + String(getVideo(n));

  // Précharge la vidéo dans la vidéo cachée
  videoToShow.src = nextVideoSrc;
  await videoToShow.load();

  // Attend que la vidéo soit prête
  await new Promise(resolve => {
    videoToShow.oncanplaythrough = () => resolve();
  });

  // Lance la vidéo cachée
  videoToShow.currentTime = 0;
  await videoToShow.play();

  currentVideoId.value = currentVideoId.value === 1 ? 2 : 1;

  await delay(getTimecodeStart(n));

  // Affiche la bulle
  showBubble.value = true;
  dialogContent = getDialog(n, language);

  if (replaceToolName.value == true) {
    let outil = getText(17 + Number(replaceToolNameNumber.value), language);
    dialogContent = dialogContent.replace("[[cet outil]]", outil);
  }

  const duration = getTimecodeEnd(n) - getTimecodeStart(n);

  // Timer debug
  timer.value = 1;
  timerInterval = setInterval(() => {
    timer.value++;
  }, 1000);

  await delay(duration);

  clearInterval(timerInterval);

  // NE ferme la bulle QUE si pas une pause
  if (dialogs.value?.[n]["end"] !== "pause") {
    animateBubbleOut();
    await delay(1000);
    showBubble.value = false;
  }

  // Attend la fin de la vidéo affichée
  await new Promise((resolve) => {
    if (videoToShow.ended) {
      resolve();
    } else {
      videoToShow.addEventListener("ended", resolve, { once: true });
    }
  });
}




</script>

<template>


  <div class="debug bubble-debug">video n° {{ currentVideo }} <br> <span class="timer">{{ timer }}</span><br> isPlaying
    : {{
      isPlaying }} <br> durée : {{ getDuration(currentVideo) }} <br>
    timecode-start : {{ getTimecodeStart(currentVideo) / 1000 }} <br> timecode-end : {{
      getTimecodeEnd(currentVideo) / 1000 }} </div>


  <div class="video-screen" v-if="dialogs && texts">
    <button v-if="!isPlaying" id="play" @click="resume(0)">Continuer</button>

    <!-- <video crossorigin="anonymous" class="main-video" id="main-video"></video> -->

    <video crossorigin="anonymous" class="main-video" id="video1" :style="{ opacity: currentVideoId === 1 ? 1 : 0 }"
      muted></video>

    <video crossorigin="anonymous" class="main-video" id="video2" :style="{ opacity: currentVideoId === 2 ? 1 : 0 }"
      muted></video>

    <DialogBubble v-if="showBubble" ref="dialogBubble" class="dialog-bubble" :dialogContent="dialogContent" />

    <!-- Dessin -->
    <ChooseToolScreen v-if="showDessin" :choiceInstruction="getText(6, language)" :goodAnswer='6'
      @numberChosen="resume" />

    <!-- Ebarbage -->
    <ChooseToolScreen v-if="showEbarbage" :choiceInstruction="getText(6, language)" :goodAnswer='6' />

    <!-- Assemblage -->
    <AssemblageStep v-if="showAssemblage" :instruction="getText(8, language)"
      :skipText="[getText(9, language), getText(10, language)]" />

    <!-- Peinture -->
    <PeintureStep v-if="showPeinture"
      :instructions="[getText(13, language), getText(14, language), getText(15, language), getText(16, language)]"
      :skipText="[getText(11, language), getText(12, language)]" />

  </div>

</template>

<style scoped>
button {
  position: absolute;
  top: 500px;
}

#play {
  z-index: 100;
  position: absolute;
  font-size: xx-large;
}

.dialog-bubble {
  position: absolute;
  top: 10px;
  z-index: 10;
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

video {
  outline: none;
}


.main-video {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
}


.video-screen {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
}

.bubble-debug {
  top: 0px;
  right: 0px;
}

.timer {
  font-size: xx-large;
  font-weight: 700;
}
</style>
