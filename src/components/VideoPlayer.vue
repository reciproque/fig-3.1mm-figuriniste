<script setup>

import DialogBubble from './DialogBubble.vue';

defineProps({

    msg: {
        type: String,
        required: false,
    },
})

import texts from '../../assets/dialogues-01-dessin.json'

import { gsap } from 'gsap';

import { ref, onMounted } from 'vue';

function getText(n, lang) {
    if (lang == "FR") return texts[n]["texte-FR"];
    if (lang == "EN") return texts[n]["texte-EN"];
    if (lang == "DE") return texts[n]["texte-DE"];
}

function getTimecodeStart(n) {
   return texts[n]["timecode-start"];
}

function getTimecodeEnd(n) {
   return texts[n]["timecode-end"];
}


let lang = "FR";
let dialogContent = getText(0, lang)

const showBubble = ref(true)

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
    }, end+1000)

    // Début bubble n + 1 (1000 entre fin de l'anim et apparition)
    setTimeout(() => {
        showBubble.value = true
        dialogContent = getText(n + 1, lang);
    }, nextStart)
}

onMounted(() => {
    const bubble = document.querySelector(".dialog-bubble")
    for (let i=0; i<2; i++) {
        nextBubble(getTimecodeEnd(i), getTimecodeStart(i+1), i);

    }
    // nextBubble(getTimecodeEnd(0), getTimecodeStart(1), 0);
    // nextBubble(getTimecodeEnd(1),  getTimecodeStart(2), 1);
})

</script>

<template>

    <div class="video-screen"> <video muted autoplay src="../../assets/sample-video.mp4" class="main-video"></video>
        <DialogBubble v-if="showBubble" ref="dialogBubble" class="dialog-bubble" :dialogContent="dialogContent" />
    </div>


</template>

<style scoped>

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
}
</style>
