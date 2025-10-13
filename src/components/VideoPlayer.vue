<script setup>

import DialogBubble from './DialogBubble.vue';

const { language, step="Dessin 1" } = defineProps({
    language: {
        type: String,
        required: true
    },
    step: {
        type: String,
        required: false,
    }
})

import texts from '../../texts/interface.json'

import dialogs from '../../texts/dialogs.json'

// const allDialogs = dialogs.reduce((acc, obj) => {
//     return { ...acc, [obj.étape]: [...acc[obj.étape] || [], obj] }
// }, {})

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
let currentVideo = 0;

let dialogContent = getDialog(0, language)

const showBubble = ref(false)

function animateBubbleOut() {
    const bubble = document.querySelector(".dialog-bubble")
    if (bubble) {
        gsap.to(bubble, { scale: 0, duration: 0.5 })
    }
}

// function nextVideo(n) {

//     console.log(n);

//     // Désaffiche bulle n 
//     setTimeout(() => {
//         animateBubbleOut()
//     }, getTimecodeEnd(n) - getTimecodeStart(n))

//     setTimeout(() => {
//         showBubble.value = false
//     }, getTimecodeEnd(n) - getTimecodeStart(n) + 1000)

//     // Affiche la bulle n+1 
//     setTimeout(() => {
//         showBubble.value = true
//         dialogContent = getDialog(n + 1, language);
//     }, getTimecodeEnd(n) + getTimecodeStart(n+1) + 1000)
// }

// function nextBubble(end, nextStart, n) {
//     // Anim fin bubble n
//     setTimeout(() => {
//         animateBubbleOut()
//     }, end)

//     // Fin bubble n (1000 entre fin de l'anim et disparition)
//     setTimeout(() => {
//         showBubble.value = false
//     }, end + 1000)

//     // Début bubble n + 1 (1000 entre fin de l'anim et apparition)
//     setTimeout(() => {
//         showBubble.value = true
//         dialogContent = getDialog(n + 1, language);

//         // // si étape "choix"
//         // if (n + 1 == nbVideos - 1) {
//         //     document.querySelector(".choix").style.display = "flex";
//         //     gsap.from(document.querySelector(".scrim"), { opacity: 0, duration: 0.5 })
//         //     gsap.to(document.querySelector("video"), { opacity: 0, duration: 0.5 })
//         // }
//     }, nextStart)
// }

// Debug : touche 1-6 invert flèche 1-6


function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function playSequence() {
    for (let i = 0; i < nbVideos - 1; i++) {
        await playVideo(i);
    }
}

// Fonction pour une "étape" de bulle
async function playVideo(n) {
    console.log(n);

    // Affiche la bulle n
    showBubble.value = true;
    dialogContent = getDialog(n, language);

    const duration = getTimecodeEnd(n) - getTimecodeStart(n);

    // Attends la durée d'affichage de la bulle
    await delay(duration);

    // Lance animation de sortie
    animateBubbleOut();

    // Attends la fin de l'animation de sortie (ex: 1s)
    await delay(1000);

    // Cache la bulle
    showBubble.value = false;

    // Petite pause avant la suivante (optionnel)
    await delay(500);
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

    <!-- TODO : gérer la src de la video selon la step. 1 step = 1 bulle = 1 vidéo ? -->
    <div class="video-screen"> <video loop muted autoplay src="../../assets/sample-video.mp4" class="main-video"></video>
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
</style>
