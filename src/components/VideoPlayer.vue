<script setup>

import DialogBubble from './DialogBubble.vue';

const { language} = defineProps({
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

function getTimecodeStart(n) {
    return dialogs[n]["timecode-start"]*1000;
}

function getTimecodeEnd(n) {
    return dialogs[n]["timecode-end"]*1000;
}

let nbVideos = 39;

let currentVideo = 1;

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

async function playSequence() {
    for (let i = 0; i < nbVideos; i++) {
        currentVideo = i+1;
        await playVideo(i);
        // TODO : play next video si end='skip', pauser et afficher séquence choix si end='choix-...'
    }
}

// Fonction pour une "étape" de bulle
async function playVideo(n) {

    //TODO: pas de modulo quand on aura toutes les vidéos
    document.querySelector("video").src = `../../assets/video-${n%4}.mp4`;

    // Affiche la bulle n
    showBubble.value = true;
    dialogContent = getDialog(n, language);

    const duration = getTimecodeEnd(n) - getTimecodeStart(n);

    // Timer pour debug
    timer.value = 1;
    timerInterval = setInterval(() => {
        timer.value++;
    }, 1000);

    // Attends la durée d'affichage de la bulle
    await delay(duration);

    // Timer pour debug
    clearInterval(timerInterval);

    // Lance animation de sortie
    animateBubbleOut();

    // Attends la fin de l'animation de sortie (ex: 1s)
    await delay(1000);

    // Cache la bulle
    showBubble.value = false;

    // Petite pause avant la suivante (optionnel)
    //await delay(500);
}

onMounted(() => {
    gsap.from(document.querySelector(".video-screen"), { opacity: 0, duration: 1 });

    // Démarre la séquence
    playSequence();
});



function beginChoiceListening() {
    document.addEventListener('keydown', function (e) {
        if (e.key === "1" || e.key === "2" || e.key === "3" || e.key === "4" || e.key === "5" || e.key === "6") document.getElementById("choix-fleche-" + e.key).style.filter = "invert()";
    });
    document.addEventListener('keyup', function (e) {
        if (e.key === "1" || e.key === "2" || e.key === "3" || e.key === "4" || e.key === "5" || e.key === "6") document.getElementById("choix-fleche-" + e.key).style.filter = "none";
    });
}



// onMounted(() => {
//     gsap.from(document.querySelector(".video-screen"), { opacity: 0, duration: 1 })
//     const bubble = document.querySelector(".dialog-bubble")
    
//     setTimeout(() => showBubble.value = true, getTimecodeStart(0))

//     for (let i = 0; i < nbVideos - 1 ; i++) {
//         nextVideo(i)
//     }

//     beginChoiceListening();

// })

</script>

<template>

    <div class="bubble-debug">video  n° {{ currentVideo }} <br> <span class="timer">{{ timer }}</span><br> start : {{ getTimecodeStart(currentVideo) }} <br> end : {{ getTimecodeEnd(currentVideo) }} </div>

    <div class="video-screen"> 
        <video loop muted autoplay src="../../assets/video-0.mp4" class="main-video"></video>
        <DialogBubble v-if="showBubble" ref="dialogBubble" class="dialog-bubble" :dialogContent="dialogContent" />

        <!-- TODO : dans un component ? -->
        <!-- TODO : gérer le passage à une séquence "choisis un outil" un param json. "Stop" ou "Continue" ? -->
        <div class="choix">
            <div class="instruction">{{ getText(6, language) }}</div>
            <div class="arrow-row">
                <img src="../../assets/choix-fleche.png" alt="" id="choix-fleche-1">
                <img src="../../assets/choix-fleche.png" alt="" id="choix-fleche-2">
                <img src="../../assets/choix-fleche.png" alt="" id="choix-fleche-3">
                <img src="../../assets/choix-fleche.png" alt="" id="choix-fleche-4">
                <img src="../../assets/choix-fleche.png" alt="" id="choix-fleche-5">
                <img src="../../assets/choix-fleche.png" alt="" id="choix-fleche-6">
            </div>
            <div class="scrim"><img src="../../assets/choix-scrim.svg" alt=""></div>
        </div>

    </div>

</template>

<style scoped>
.choix {
    display: none;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: absolute;
    bottom: 0;
    margin: 0;
    gap: 30px;
}

.scrim {
    height: fit-content;
    margin: 0;
    vertical-align: bottom;
    margin-bottom: -10px;
}

.arrow-row {
    display: flex;
    flex-direction: row;
    gap: 150px;
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
    top:100px;
    right: 100px;
    background-color: rgba(255, 255, 255, 0.3);
    padding: 10px;

}

.timer {
    font-size: xx-large;
    font-weight: 700;
}
</style>
