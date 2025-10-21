<script setup>
import { gsap } from 'gsap';

import { onMounted } from 'vue';


defineProps({
    instruction: {
        type: String,
        required: false
    },
    skipText: {
        type: Object,
        required: false
    }
})

function selectArms(n) {
    gsap.to(document.getElementById("circle-"+n), {opacity:0, duration:0.2})
    if(n==1) gsap.to(document.getElementById("arms-"+n), {x:500,y:80, duration:0.2})
    if(n==2) gsap.to(document.getElementById("arms-"+n), {x:-700,y:220, duration:0.2})
    if(n==3) gsap.to(document.getElementById("arms-"+n), {x:-500,y:-220, duration:0.2})

}

onMounted(() => {
    gsap.from(document.querySelector(".assemblage-screen"), { opacity: 0, duration: 1})


})

</script>

<template>
    <div class="assemblage-screen">     
        <div class="instruction">{{ instruction }}</div>
        <div class="randomizer-box" @click="selectArms(1)">{{ skipText[0] }}
            <br>
            <em>{{ skipText[1] }}</em>
        </div>

    </div>
    <img src="/assets/circle-head.svg" alt="" class="circle-head">
    <img src="/assets/sample-armless-richard.png" alt="" class="richard">

    <div class="arms-choice" id="arms-choice-1">
        <img src="/assets/circle-choice.svg" alt="" class="circle-choice" @click="selectArms(1)" id="circle-1">
        <img src="/assets/sample-arm1.png" alt="" class="arms" id="arms-1">
    </div>

    <div class="arms-choice" id="arms-choice-2">
        <img src="/assets/circle-choice.svg" alt="" class="circle-choice" @click="selectArms(2)" id="circle-2">
        <img src="/assets/sample-arm2.png" alt="" class="arms" id="arms-2">
    </div>


    <div class="arms-choice" id="arms-choice-3">
        <img src="/assets/circle-choice.svg" alt="" class="circle-choice" @click="selectArms(3)" id="circle-3">
        <img src="/assets/sample-arm3.png" alt="" class="arms" id="arms-3">
    </div>


</template>

<style scoped>
.assemblage-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.circle-head {
    position: absolute;
    top: 224px;
    left: 749px;
}

.richard {
    position: absolute;
    top: 114px;
    left: 624px;

}

.instruction {
    margin-top: 85px;
}

.arms {
    pointer-events: none;
}

.circle-choice {
    cursor: pointer;
}

.arms-choice {
    transition: 0.4s;
}

.arms-choice,
.arms,
.circle-choice {
    position: absolute;
}

.arms-choice:hover {
    filter: invert();
    transition: 0.4s;

}

#arms-choice-1 {
    top: 300px;
    right: 1700px;
}

#arms-choice-2 {
    top: 170px;
    right: 500px;
}

#arms-choice-3 {
    top: 600px;
    right: 700px;
}

.arms {
    top: -95px;
}

.randomizer-box {
    position: absolute;
    bottom: 0;
    background-color: #F5F7FB;
    padding: 32px 40px;
    color: #3959D0;
    text-align: center;
    font-size: 24px;
    font-weight: 300;
    border-radius: 40px 40px 0 0;
    cursor: pointer;
    transition: 0.4s;
}

.randomizer-box:hover {
    scale: 1.02;
    transition: 0.4s;

}

em {
    font-family: 'Gotham-Black';
    font-style: normal;
    font-size: 22px;
    font-weight: 500;
}
</style>
