<script setup>

import { gsap } from 'gsap';

import { onMounted } from 'vue';

defineProps({
    dialogContent: {
        type: String,
        required: false,
    }
})

onMounted(() => {

    gsap.from(".bubble", { y: -50, duration: 0.5 })

    let animatedText = document.querySelector(".bubble-box");

    // Espaces insécables et sauts de ligne
    animatedText.innerHTML = animatedText.textContent.replace(/ (\?|!)/g, '\u00A0$1')
        .split("")
        .map((char) => {
            if (char === "\n") return "<br>";
            if (char === '\u00A0') return  `<span style="font-family:auto">${char}</span>`;
            return `<span>${char}</span>`;
        })
        .join("");


    gsap.from(animatedText.querySelectorAll("span"), {
        opacity: 0,
        y: 50,
        duration: 0.1,
        stagger: 0.02,
    });
})

</script>

<template>

    <div class="bubble" v-show="dialogContent"><img src="/assets/bubble-arrow.svg" alt="" class="bubble-arrow">
        <div class="bubble-box">{{ dialogContent }}</div>
    </div>

</template>

<style scoped>
.bubble {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 891px;
}

.bubble-arrow {
    width: 110px;
    margin-bottom: -20px;
}

/* TODO : taille de la bulle adaptée au texte */

.bubble-box {
    font-size: 30px;
    font-weight: 700;
    font-family: 'Gotham-Bold';
    text-align: center;
    color: #493C38;
    background-color: #FBF9F5;
    border-radius: 40px;
    padding: 40px 94px;
    line-height: 110%;
    max-width: 703px;
    letter-spacing: -2%;
    box-sizing: content-box;
}
</style>
