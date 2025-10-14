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

import texts from '../../texts/interface.json'
import dialogs from '../../texts/dialogs.json'

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

function getDuration(n) {
    return dialogs[n]["duration"];
}

function getTimecodeStart(n) {
    return dialogs[n]["timecode-start"] * 1000;
}

function getTimecodeEnd(n) {
    return dialogs[n]["timecode-end"] * 1000;
}

let nbVideos = Object.keys(dialogs).length;

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

    currentVideo++;          // avance bien à la vidéo suivante

    playSequence();          // c’est playVideo() qui jouera la vidéo
}


async function playSequence() {
    for (let i = currentVideo; i < nbVideos; i++) {
        currentVideo = i;
        await playVideo(i);

        if (dialogs[i]["end"] == "skip") {
            isPlaying.value = true;

        }
        else if (dialogs[i]["end"] == "pause") {
            isPlaying.value = false;
            if (currentVideo == nbVideos - 1) {
                isPlaying.value = true;
                break
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


// Fonction pour une "étape" de bulle
async function playVideo(n) {
    const video = document.getElementById("main-video");

    // Change la source
    //video.src = `../../assets/video-${n % 4}.mp4`;
    video.src = "../../assets/sample-video.mp4"

    // Recharge et joue la vidéo (important !)
    await video.load();
    await video.play();

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
}


onMounted(() => {
    //gsap.from(document.querySelector(".video-screen"), { opacity: 0, duration: 1 });


    // Démarre la séquence
    playSequence();
});


</script>

<template>


    <div class="bubble-debug">video n° {{ currentVideo }} <br> <span class="timer">{{ timer }}</span><br> isPlaying : {{
        isPlaying }} ({{ dialogs[currentVideo]["end"] }}) <br> durée : {{ getDuration(currentVideo) }} <br>
        timecode-start : {{ getTimecodeStart(currentVideo) / 1000 }} <br> timecode-end : {{
            getTimecodeEnd(currentVideo) /1000 }} </div>


    <div class="video-screen">
        <button v-if="!isPlaying" id="play" @click="resume()">Continuer</button>

        <video loop muted autoplay src="../../assets/sample-video.mp4" class="main-video" id="main-video"></video>

        <DialogBubble v-if="showBubble" ref="dialogBubble" class="dialog-bubble" :dialogContent="dialogContent" />

        <!-- <ChooseToolScreen :choiceInstruction="getText(6, language)" :goodAnswer='6'/> -->

        <!-- <AssemblageStep :instruction="getText(8, language)" :skipText="[getText(9, language), getText(10, language)]" />      -->

        <!-- <PeintureStep :instructions="[getText(13, language), getText(14, language), getText(15, language), getText(16, language)]" :skipText="[getText(11, language), getText(12, language)]"/> -->

    </div>

</template>

<style scoped>
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
    width: 100vw;
}

.video-screen {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0;
}

.bubble-debug {
    position: absolute;
    top: 0px;
    right: 0px;
    background-color: rgba(255, 0, 0, 0.3);
    padding: 10px;
}

.timer {
    font-size: xx-large;
    font-weight: 700;
}
</style>
