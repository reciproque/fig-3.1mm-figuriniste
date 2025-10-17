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

import texts from '../../public/texts/interface.json'
import dialogs from '../../public/texts/dialogs.json'

import { gsap } from 'gsap';

import { ref, onMounted } from 'vue';

function getText(n, lang) {
    if (lang == "FR") return texts[n]["texte-FR"];
    if (lang == "EN") return texts[n]["texte-EN"];
    if (lang == "DE") return texts[n]["texte-DE"];
}

function getDialog(n, lang) {
    if (lang == "FR") return dialogs[n]["texte-FR"];
    if (lang == "EN") return dialogs[n]["texte-EN"];
    if (lang == "DE") return dialogs[n]["texte-DE"];
}

function getVideo(n) {
    return dialogs[n]["nomenclature-video"];

}

function getDuration(n) {
    return dialogs[n]["duration"];
}

function getTimecodeStart(n) {
    return dialogs[n]["timecode-start"] * 1000;
}

function getTimecodeEnd(n) {
    return dialogs[n]["timecode-end"] * 1000;
}

let nbVideos = Object.keys(dialogs).length -1;

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

async function resume() {
    isPlaying.value = true;

    animateBubbleOut();
    await delay(1000);
    showBubble.value = false;

    currentVideo++;          

    await playSequence();          
}


async function playSequence() {
  for (let i = currentVideo; i < nbVideos; i++) {
    currentVideo = i;

    // Précharge la vidéo suivante si elle existe
    if (i + 1 < nbVideos) {
      const nextSrc = import.meta.env.BASE_URL + 'assets/videos/' + String(getVideo(i + 1));
      await preloadVideo(nextSrc);
    }

    await playVideo(i);

    if (dialogs[i]["end"] == "skip") {
      isPlaying.value = true;
    } else if (dialogs[i]["end"] == "pause") {
      isPlaying.value = false;
      if (currentVideo == nbVideos - 1) {
        isPlaying.value = true;
        break;
      }
      pauseVideoPlayer();
      break;
    }
  }
}

function playVideoPlayer() {
    document.getElementById("main-video").play();
}

function pauseVideoPlayer() {
    document.getElementById("main-video").pause();
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

  const duration = getTimecodeEnd(n) - getTimecodeStart(n);

  // Timer debug
  timer.value = 1;
  timerInterval = setInterval(() => {
    timer.value++;
  }, 1000);

  await delay(duration);

  clearInterval(timerInterval);

  // NE ferme la bulle QUE si pas une pause
  if (dialogs[n]["end"] !== "pause") {
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


onMounted(() => {

    // Démarre la séquence
    playSequence();
});


</script>

<template>


    <div class="debug bubble-debug">video n° {{ currentVideo }} <br> <span class="timer">{{ timer }}</span><br> isPlaying : {{
        isPlaying }} ({{ dialogs[currentVideo]["end"] }}) <br> durée : {{ getDuration(currentVideo) }} <br>
        timecode-start : {{ getTimecodeStart(currentVideo) / 1000 }} <br> timecode-end : {{
            getTimecodeEnd(currentVideo) /1000 }} </div>


    <div class="video-screen">
        <button v-if="!isPlaying" id="play" @click="resume()">Continuer</button>

        <!-- <video crossorigin="anonymous" class="main-video" id="main-video"></video> -->

  <video
    crossorigin="anonymous"
    class="main-video"
    id="video1"
    :style="{ opacity: currentVideoId === 1 ? 1 : 0 }"
    muted
  ></video>
  <video
    crossorigin="anonymous"
    class="main-video"
    id="video2"
    :style="{ opacity: currentVideoId === 2 ? 1 : 0 }"
    muted
  ></video>

        <DialogBubble v-if="showBubble" ref="dialogBubble" class="dialog-bubble" :dialogContent="dialogContent" />

        <!-- <ChooseToolScreen :choiceInstruction="getText(6, language)" :goodAnswer='6'/> -->

        <!-- <AssemblageStep :instruction="getText(8, language)" :skipText="[getText(9, language), getText(10, language)]" />      -->

        <!-- <PeintureStep :instructions="[getText(13, language), getText(14, language), getText(15, language), getText(16, language)]" :skipText="[getText(11, language), getText(12, language)]"/> -->

    </div>

</template>

<style scoped>

button {
    position: absolute;
    top:500px;
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

 
.main-video{
    position: absolute;
    top: 0;
    left: 0;
    transition: opacity 0.5s ease;
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
