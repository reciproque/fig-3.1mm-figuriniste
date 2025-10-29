<script setup>

import DialogBubble from './DialogBubble.vue';
import ChooseToolScreen from './ChooseToolScreen.vue'
import AssemblageStep from './AssemblageStep.vue';
import PeintureStep from './PeintureStep.vue';
import QRCodeScreen from './QRCodeScreen.vue';

import { gsap } from 'gsap';

import { ref, onMounted } from 'vue';

const { language, startId } = defineProps({
  language: {
    type: String,
    required: true
  },
  startId: {
    type: Number,
    required:false
  }
})

const currentVideoId = ref(1);

// Chargement des dialogues et textes d'interface depuis Json

const dialogs = ref({});
const texts = ref({});
const nbVideos = ref(0);

onMounted(async () => {
  try {
    const dialogsRes = await fetch('texts/dialogs.json');
    dialogs.value = await dialogsRes.json();

    const textsRes = await fetch('texts/interface.json');
    texts.value = await textsRes.json();

    nbVideos.value = Object.keys(dialogs.value).length - 1;
    await playSequence();

  } catch (err) {
    console.error('Erreur de chargement des fichiers JSON : ', err);
  }
});

//


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


let currentVideo = startId;

const isPlaying = ref(true);

// Timer pour debug

const timer = ref(0);
let timerInterval = null;


// Gestion bulles de dialogue

let dialogContent = getDialog(0, language)
const showBubble = ref(false)

function animateBubbleOut() {
  const bubble = document.querySelector(".dialog-bubble")
  if (bubble) {
    gsap.to(bubble, { opacity: 0, duration: 0.2 })
  }
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Reprendre la timeline après une séquence interactive. 
// n = nombre émis par le composant interactif (outil touché pour dessin/ébardage, combinaison choisie pour assemblage/peinture)
const posLime = 2;
const posCriterium = 6;

let arm = 1;
const finaleRichard = ref("11111");

let nbErrorDessin = 0;
let nbErrorEbarbage = 0;

function onDessinChoice(n) { resume(n, "dessin"); }
function onEbarbageChoice(n) { resume(n, "ebarbage"); }
function onAssemblageChoice(n) { resume(n, "assemblage"); }
function onPeintureChoice(n) { resume(n, "peinture"); }
function onSkipPeintureChoice(n) { resume(n, "skipPeinture"); }


async function resume(n, step) {

  isPlaying.value = true;
  animateBubbleOut();
  await delay(1000);
  showBubble.value = false;

  switch(step) {
    case "dessin": await handleDessin(n); break;
    case "ebarbage": await handleEbarbage(n); break;
    case "assemblage": await handleAssemblage(n); break;
    case "peinture": await handlePeinture(n); break;
    case "skipPeinture": await handleSkipPeinture(n); break;

  }

  switch(step) {
    case "dessin": showDessin.value = false; break;
    case "ebarbage": showEbarbage.value = false; break;
    case "assemblage": showAssemblage.value = false; break;
    case "peinture": showPeintureForAnim.value = false; break;
    case "skipPeinture": showPeintureForAnim.value = false; break;

  }

  await playSequence();
}


async function handleDessin(n) {
  let videoFalse = 2 * n + 1;
  let videoTrue = 14;

  if (n == posCriterium) {
    currentVideo = videoTrue;
    showDessin.value = false;
  } else {
    nbErrorDessin++;
    showDessin.value = false;

    if (nbErrorDessin == 1) currentVideo = videoFalse;
    if (nbErrorDessin == 2) {
      currentVideo = videoFalse;
      await playVideo(videoFalse);
      currentVideo = 13;
      await playVideo(currentVideo);
      currentVideo = 15;
    }
  }
}

async function handleEbarbage(n) {
  let videoFalse = 2 * n + (n < 2 ? 34 : 32);
  let videoTrue = 47;

  if (n == posLime) {
    currentVideo = videoTrue;
    showEbarbage.value = false;

  } else {
    nbErrorEbarbage++;
    showEbarbage.value = false;
    if (nbErrorEbarbage == 1) currentVideo = videoFalse;
    if (nbErrorEbarbage == 2) {
      currentVideo = videoFalse;
      await playVideo(videoFalse);
      currentVideo = 46;
      await playVideo(currentVideo);
      currentVideo = 48;
    }
  }
}

async function handleAssemblage(n) {
  console.log("Bras choisi : " + n);
  arm = n;
  currentVideo = 52;
}

async function handlePeinture(n) {
  currentVideo++;
  if (n%2==0) showPeintureForAnim.value = false;
  if (n%2==1) showPeintureForAnim.value = true;

  if(currentVideo==63) {
    showPeinture.value = false; 
    finaleRichard.value = String(arm) + String(n);
  }
}

async function handleSkipPeinture() {
  currentVideo = 63;
  showPeinture.value = false; 
  showPeintureForAnim.value = false;
  finaleRichard.value = arm + "1111";
}




async function playSequence() {
  for (let i = currentVideo; i < nbVideos.value; i++) {
    currentVideo = i;
    await playVideo(i);

    const end = dialogs.value?.[i]?.["end"];

    if (end === "skip") {
      isPlaying.value = true;
    }
    else if (end === "pause") {
      isPlaying.value = false;

      if (currentVideo === nbVideos.value) {
        isPlaying.value = true;
        break;
      }
      launchInteractiveStep(dialogs.value?.[i]?.["pause"]);
      break;
    }
    else {
      console.warn(`Champ "end" manquant ou non reconnu pour la vidéo ${i}:`, end);
      isPlaying.value = true;
    }

  }
}

const showDessin = ref(false);
const showEbarbage = ref(false);
const showAssemblage = ref(false);
const showPeinture = ref(false);
const showQR = ref(false);

const showPeintureForAnim = ref(false);

function launchInteractiveStep(step) {
  showDessin.value = false;
  showEbarbage.value = false;
  showAssemblage.value = false;
  showPeintureForAnim.value = false;
  showQR.value = false;

  switch (step) {
    case "dessin": showDessin.value = true; break;
    case "ebarbage": showEbarbage.value = true; break;
    case "assemblage": showAssemblage.value = true; break;
    case "peinture": showPeinture.value = true; showPeintureForAnim.value = true; break;
    case "qrcode": showQR.value = true; break;
  }

}



async function playVideo(n) {
  
  // Echange de load entre video1 et video2 pour passage imperceptible de l'une à l'autre
  const videoToShow = currentVideoId.value === 1 ? document.getElementById('video2') : document.getElementById('video1');
  const nextVideoSrc = import.meta.env.BASE_URL + 'assets/videos/' + String(getVideo(n));
  videoToShow.src = nextVideoSrc;
  await videoToShow.load();
  await new Promise(resolve => {
    videoToShow.oncanplaythrough = () => resolve();
  });
  videoToShow.currentTime = 0;
  await videoToShow.play();
  currentVideoId.value = currentVideoId.value === 1 ? 2 : 1;
  //

  await delay(getTimecodeStart(n));

  // Afficher la bulle
  showBubble.value = true;
  dialogContent = getDialog(n, language);

  const duration = getTimecodeEnd(n) - getTimecodeStart(n);

  // Timer debug
  timer.value = 1;
  timerInterval = setInterval(() => {
    timer.value++;
  }, 1000);

  await delay(duration);

  clearInterval(timerInterval);

  // Ferme la bulle que si pas une pause
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

  <div class="debug bubble-debug">
    video n° {{ currentVideo }} <br> 
    <span class="timer">{{ timer }}</span><br> 
    isPlaying : {{ isPlaying }} <br> 
    durée : {{ getDuration(currentVideo) }} <br>
    timecode-start : {{ getTimecodeStart(currentVideo) / 1000 }} <br> 
    timecode-end : {{ getTimecodeEnd(currentVideo) / 1000 }} 
  </div>


  <div class="video-screen" v-if="dialogs && texts">
    <!-- <button v-if="!isPlaying" id="play" @click="resume(0)">Continuer</button> -->

    <video  v-if="!showPeinture" crossorigin="anonymous" class="main-video" id="video1" :style="{ opacity: currentVideoId === 1 ? 1 : 0 }"
      muted></video>

    <video v-if="!showPeinture" crossorigin="anonymous" class="main-video" id="video2" :style="{ opacity: currentVideoId === 2 ? 1 : 0 }"
      muted></video>

    <DialogBubble v-if="showBubble" ref="dialogBubble" class="dialog-bubble" :dialogContent="dialogContent" />

    <!-- Dessin -->
    <ChooseToolScreen v-if="showDessin" 
      :choiceInstruction="getText(6, language)" 
      :goodAnswer='posCriterium'
      @touchedTool="onDessinChoice" />

    <!-- Ebarbage -->
    <ChooseToolScreen v-if="showEbarbage" 
      :choiceInstruction="getText(7, language)" 
      :goodAnswer='posLime'
      @touchedTool="onEbarbageChoice"  />

    <!-- Assemblage -->
    <AssemblageStep v-if="showAssemblage" 
      :instruction="getText(8, language)"
      :skipText="[getText(9, language), getText(10, language)]"
      @chosenArm="onAssemblageChoice" />

    <!-- Peinture -->
     <div v-show="showPeintureForAnim">
    <PeintureStep v-if="showPeinture"
      :instructions="[getText(13, language), getText(14, language), getText(15, language), getText(16, language)]"
      :skipText="[getText(11, language), getText(12, language)]" 
      @chooseSkipPeinture="onSkipPeintureChoice"
      @finaleCombination="onPeintureChoice"
      @nextStep="onPeintureChoice"/></div>

    <!-- TODO: QRCode -->
    <QRCodeScreen v-if="showQR"
      :instruction="getText(17, language)"
      :combination="finaleRichard"/>
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
