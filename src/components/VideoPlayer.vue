<script setup>

import DialogBubble from './DialogBubble.vue';
import ChooseToolScreen from './ChooseToolScreen.vue'
import AssemblageStep from './AssemblageStep.vue';
import PeintureStep from './PeintureStep.vue';
import QRCodeScreen from './QRCodeScreen.vue';

import TimeoutModal from './TimeoutModal.vue'

import { gsap } from 'gsap';

import { ref, onMounted } from 'vue';

const { language, startId } = defineProps({
  language: {
    type: String,
    required: true
  },
  startId: {
    type: Number,
    required: false
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

// Helpers pour récupérer les texts, dialogues et données de vidéos depuis dialogs et texts.

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


const isInactive = ref(false);

let TO1 = setTimeout(()=>{isInactive.value=true}, getText(21, language)*1000);
clearTimeout(TO1);

function stillHere() {
  isInactive.value = false;
  clearTimeout(TO1);
  TO1 = setTimeout(()=>{isInactive.value=true}, getText(21, language)*1000);

}



let currentVideo = startId;

const isPlaying = ref(true);

// Timer pour debug bulles

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

const posLime = 2;
const posLouche = 5;
const posCriterium = 6;

let arm = 1;
const finaleRichard = ref("12111");

// à changer si décalage indices

const idDessinFalse = 1;
const idDessinTrue = 14;

const idCouleeFalse = 28;
const idCouleeTrue = 41;

const idEbarbageFalse = 43;
const idEbarbageTrue = 58;


const idDebutPeintureBras1 = 62;
const idDebutPeintureBras2 = 66;
const idDebutPeintureBras3 = 70;

const idFinPeinture = 74;

let nbErrorDessin = 0;
let nbErrorEbarbage = 0;
let nbErrorCoulee = 0;

function onDessinChoice(n) { resume(n, "dessin"); }
function onCouleeChoice(n) { resume(n, "coulee"); }
function onEbarbageChoice(n) { resume(n, "ebarbage"); }
function onAssemblageChoice(n) { resume(n, "assemblage"); }
function endPeinture(n) { resume(n, "peinture"); }
function onSkipPeintureChoice(n) { resume(n, "skipPeinture"); }

// Reprendre la timeline après une séquence interactive. 
// n = nombre émis par le composant interactif (outil touché pour dessin/ébardage, combinaison choisie pour assemblage/peinture)
async function resume(n, step) {

  clearTimeout(TO1);
  isInactive.value = false;
  isPlaying.value = true;
  animateBubbleOut();
  await delay(1000);
  showBubble.value = false;

  switch (step) {
    case "dessin": await handleDessin(n); break;
    case "coulee": await handleCoulee(n); break;
    case "ebarbage": await handleEbarbage(n); break;
    case "assemblage": await handleAssemblage(n); break;
    case "peinture": await handlePeinture(n); break;
    case "skipPeinture": await handleSkipPeinture(n); break;
  }

  switch (step) {
    case "dessin": showDessin.value = false; break;
    case "coulee": showCoulee.value = false; break;
    case "ebarbage": showEbarbage.value = false; break;
    case "assemblage": showAssemblage.value = false; break;
    case "peinture": showPeinture.value = false; break;
    case "skipPeinture": showPeinture.value = false; break;
  }

  await playSequence();
}


async function handleDessin(n) {
  let videoFalse = 2 * n + idDessinFalse;
  let videoTrue = idDessinTrue;

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
      currentVideo = idDessinTrue-1;
      await playVideo(currentVideo);
      currentVideo = idDessinTrue+1;
    }
  }
}

async function handleCoulee(n) {
  let videoFalse = 2 * n + (n < posLouche ? idCouleeFalse : idCouleeFalse-2);
  let videoTrue = idCouleeTrue;

  if (n == posLouche) {
    currentVideo = videoTrue;
    showCoulee.value = false;

  } else {
    nbErrorCoulee++;
    showCoulee.value = false;
    if (nbErrorCoulee == 1) currentVideo = videoFalse;
    if (nbErrorCoulee == 2) {
      currentVideo = videoFalse;
      await playVideo(videoFalse);
      currentVideo = idCouleeTrue-1;
      await playVideo(currentVideo);
      currentVideo = idCouleeTrue+1;
    }
  }
}

async function handleEbarbage(n) {
  let videoFalse = 2 * n + (n < posLime ? idEbarbageFalse+2 : idEbarbageFalse);
  let videoTrue = idEbarbageTrue;

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
      currentVideo = idEbarbageTrue-1;
      await playVideo(currentVideo);
      currentVideo = idEbarbageTrue+1;
    }
  }
}

async function handleAssemblage(n) {
  showAssemblage.value = false;
  console.log("Bras choisi : " + n);
  arm = n;
  if (arm==1) {
    currentVideo = idDebutPeintureBras1;
  }
  if (arm==2) {
    currentVideo = idDebutPeintureBras2;
  }
  if (arm==3) {
    currentVideo = idDebutPeintureBras3;
  }

  for (let i=1; i<=2; i++) {
    await playVideo(currentVideo);
    currentVideo++;
  }
}

async function handlePeinture(n) {
  showPeinture.value = false;
  finaleRichard.value = String(arm) + String(n);
  currentVideo = idFinPeinture;

}

async function handleSkipPeinture() {
  currentVideo = idFinPeinture;
  showPeinture.value = false;
  finaleRichard.value = arm + "2111";
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
      isPlaying.value = true;
    }

  }
}

const showDessin = ref(false);
const showCoulee = ref(false);
const showEbarbage = ref(false);
const showAssemblage = ref(false);
const showPeinture = ref(false);
const showQR = ref(false);

function launchInteractiveStep(step) {
  showDessin.value = false;
  showCoulee.value = false;
  showEbarbage.value = false;
  showAssemblage.value = false;
  showQR.value = false;

  TO1 = setTimeout(()=>{isInactive.value=true}, getText(21, language)*1000)

  switch (step) {
    case "dessin": showDessin.value = true; break;
    case "coulee": showCoulee.value = true; break;
    case "ebarbage": showEbarbage.value = true; break;
    case "assemblage": showAssemblage.value = true; break;
    case "peinture": showPeinture.value = true; break;
    case "qrcode": {
      showQR.value = true;
      break;
    }
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
  currentVideoId.value = currentVideoId.value === 1 ? 2 : 1;
  await videoToShow.play();
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

    <TimeoutModal v-if="isInactive"
    @click="stillHere"

    :interface="[getText(19, language), getText(20, language), getText(23, language)]" 
    :timer2="getText(22, language)"/>


  <div class="video-screen" v-if="dialogs && texts">


    <video v-if="!showPeinture" crossorigin="anonymous" class="main-video" id="video1"
      :style="{ opacity: currentVideoId === 1 ? 1 : 0 }" muted></video>

    <video v-if="!showPeinture" crossorigin="anonymous" class="main-video" id="video2"
      :style="{ opacity: currentVideoId === 2 ? 1 : 0 }" muted></video>

    <DialogBubble v-if="showBubble" ref="dialogBubble" class="dialog-bubble" :dialogContent="dialogContent" />

    <!-- Dessin -->
    <ChooseToolScreen v-if="showDessin" :choiceInstruction="getText(6, language)" :goodAnswer='posCriterium'
      @touchedTool="onDessinChoice" />

    <!-- Coulee -->
    <ChooseToolScreen v-if="showCoulee" :choiceInstruction="getText(7, language)" :goodAnswer='posLouche'
      @touchedTool="onCouleeChoice" />

    <!-- Ebarbage -->
    <ChooseToolScreen v-if="showEbarbage" :choiceInstruction="getText(8, language)" :goodAnswer='posLime'
      @touchedTool="onEbarbageChoice" />

    <!-- Assemblage -->
    <AssemblageStep v-if="showAssemblage" :instruction="getText(9, language)"
      :skipText="[getText(10, language), getText(11, language)]" @chosenArm="onAssemblageChoice" />

    <!-- Peinture -->
    <PeintureStep v-if="showPeinture"
      :instructions="[getText(14, language), getText(15, language), getText(16, language), getText(17, language)]"
      :skipText="[getText(12, language), getText(13, language)]" :bras="arm" @chooseSkipPeinture="onSkipPeintureChoice"
      @action="stillHere"
      @finaleCombination="endPeinture"
       />

    <img v-if="currentVideo==idFinPeinture || currentVideo==idFinPeinture+1 " class="richard" :src="'richards/resultats/' + finaleRichard + '.png'" alt="">

    <!-- QRCode -->
    <QRCodeScreen v-if="showQR" :instruction="getText(18, language)" :combination="finaleRichard" />
  </div>

</template>

<style scoped>

.richard {
  position: absolute;
  z-index: 100;
  top: 90px;
}

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
