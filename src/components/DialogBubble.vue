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
    gsap.from(".bubble", { scale: 0.5, duration: 0.5 })

    let animatedText = document.querySelector(".bubble-box");
        animatedText.innerHTML = animatedText.textContent
        .split("")
        .map((char) => {
            if (char === "\n") return "<br>";
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

    <div class="bubble"><img src="../../assets/bubble-arrow.svg" alt="" class="bubble-arrow">
        <div class="bubble-box">{{ dialogContent }}</div>
    </div>

</template>

<style scoped>

.bubble {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.bubble-arrow {
    width: 110px;
    margin-bottom: -10px;
}

.bubble-box {
    font-size: 28px;
    font-weight: 700;
    font-family: 'Gotham-Book';
    text-align: center;
    background-color: #FBF9F5;
    border-radius: 40px;
    padding: 40px 94px;
    width: 700px;
    box-sizing: content-box;
}
</style>
