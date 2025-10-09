<script setup>

import DialogBubble from './DialogBubble.vue';

const { language, step } = defineProps({
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


const allDialogs = dialogs.reduce((acc, obj) => {
    return { ...acc, [obj.étape]: [...acc[obj.étape] || [], obj] }
}, {})


import { gsap } from 'gsap';

import { ref, onMounted } from 'vue';

function getText(n, lang) {
    if (lang == "FR") return texts[n]["texte-FR"];
    if (lang == "EN") return texts[n]["texte-EN"];
    if (lang == "DE") return texts[n]["texte-DE"];
}

function getDialog(n, lang) {
    if (lang == "FR") return allDialogs[step][n]["texte-FR"];
    if (lang == "EN") return allDialogs[step][n]["texte-EN"];
    if (lang == "DE") return allDialogs[step][n]["texte-DE"];
}

function getTimecodeStart(n) {
    return allDialogs[step][n]["timecode-start"];
}

function getTimecodeEnd(n) {
    return allDialogs[step][n]["timecode-end"];
}

let nbBubbles = allDialogs[step].length;

let dialogContent = getDialog(0, language)

const showBubble = ref(false)

function animateBubbleOut() {
    const bubble = document.querySelector(".dialog-bubble")
    if (bubble) {
        gsap.to(bubble, { scale: 0, duration: 0.5 })
    }
}

function nextBubble(end, nextStart, n) {
    // Anim fin bubble n
    setTimeout(() => {
        animateBubbleOut()
    }, end)

    // Fin bubble n (1000 entre fin de l'anim et disparition)
    setTimeout(() => {
        showBubble.value = false
    }, end + 1000)

    // Début bubble n + 1 (1000 entre fin de l'anim et apparition)
    setTimeout(() => {
        showBubble.value = true
        dialogContent = getDialog(n + 1, language);
        if (n + 1 == nbBubbles - 1) {
            document.querySelector(".choix").style.display = "flex";
            gsap.from(document.querySelector(".scrim"), { opacity: 0, duration: 0.5 })
            gsap.to(document.querySelector("video"), { opacity: 0, duration: 0.5 })
        }
    }, nextStart)
}

function beginChoiceListening() {
    document.addEventListener('keydown', function (e) {
        if (e.key === "1" || e.key === "2" || e.key === "3" || e.key === "4" || e.key === "5" || e.key === "6") document.getElementById("choix-fleche-" + e.key).style.filter = "invert()";
    });
    document.addEventListener('keyup', function (e) {
        console.log(e.key)
        if (e.key === "1" || e.key === "2" || e.key === "3" || e.key === "4" || e.key === "5" || e.key === "6") document.getElementById("choix-fleche-" + e.key).style.filter = "none";
    });
}

onMounted(() => {
    gsap.from(document.querySelector(".video-screen"), { opacity: 0, duration: 1 })
    const bubble = document.querySelector(".dialog-bubble")
    setTimeout(() => showBubble.value = true, getTimecodeStart(0))
    for (let i = 0; i < nbBubbles - 1; i++) {
        nextBubble(getTimecodeEnd(i), getTimecodeStart(i + 1), i);
    }
    beginChoiceListening();

})

</script>

<template>

    <div class="video-screen"> <video muted autoplay src="../../assets/sample-video.mp4" class="main-video"></video>
        <DialogBubble v-if="showBubble" ref="dialogBubble" class="dialog-bubble" :dialogContent="dialogContent" />

        <!-- TODO : dans un component ? -->
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
