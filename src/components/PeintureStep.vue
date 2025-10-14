<script setup>
import texts from '../../texts/interface.json'

import { gsap } from 'gsap';

import { ref, onMounted } from 'vue';

const step = ref(0);

const paintColors = ref(["black", "yellow", "white"]);

let peau = 1;
let cheveux = 1;
let robe = 1;
let armoiries = 1;

defineProps({
    instructions: {
        type: Object,
        required: false
    },
    skipText: {
        type: Object,
        required: false
    }
})


function selectColor(n) {

    gsap.from(document.getElementById("color-choice-"+n), { scale: 0.5, duration: 0.2, ease: "bounce.out" })
    
    if (step.value==0) peau = n;
    if (step.value==1) cheveux = n;
    if (step.value==2) robe = n;
    if (step.value==3) armoiries = n;
    
    step.value++;
    nextStep();

    document.querySelector(".peinture-debug").innerHTML = `ETAPE : ${step.value} 
    <br> Peau : ${peau} 
    <br> Cheveux : ${cheveux} 
    <br> Robe/Bouclier : ${robe} 
    <br> Cote de maille/Armoiries : ${armoiries} 
    `;

}

function nextStep() {
    
    setTimeout(() => {
        gsap.from(document.querySelector(".palette"), { x: 200, rotateZ: 20, duration: 1 })}, 
    
        500);


    document.querySelector(".peinture-debug").innerHTML = `ETAPE : ${step.value} 
    <br> Peau : ${peau} 
    <br> Cheveux : ${cheveux} 
    <br> Robe/Bouclier : ${robe} 
    <br> Cote de maille/Armoiries : ${armoiries} 
    `;
}

onMounted(() => {
    gsap.from(document.querySelector(".palette"), { x: 200, rotateZ: 20, duration: 1 })
    // gsap.from(document.querySelector(".assemblage-screen"), { opacity: 0, duration: 1})

})

</script>

<template>
    <div class="peinture-debug">
    ETAPE : {{ step }}
    <br>Peau : {{ peau }}
    <br> Cheveux :  {{ cheveux }}
    <br> Robe/Bouclier :  {{ robe }}
    <br> Cote de maille/Armoiries : {{ armoiries }}</div>
    <div class="assemblage-screen">
        <div class="instruction">{{ instructions[step] }}</div>
        <div v-if="step==0" class="randomizer-box" @click="selectColor(1)">{{ skipText[0] }}
            <br>
            <em>{{ skipText[1] }}</em>
        </div>

        <div class="palette">
            <img src="/assets/palette.png" alt="">
            <div class="color-choice" id="color-choice-1">
                <img src="/assets/circle-choice-paint.svg" alt="" class="circle-choice" @click="selectColor(1)"
                    id="circle-1">
                <img src="/assets/paint-black.png" alt="" class="color" id="color-1">
            </div>

            <div class="color-choice" id="color-choice-2">
                <img src="/assets/circle-choice-paint.svg" alt="" class="circle-choice" @click="selectColor(2)"
                    id="circle-2">
                <img src="/assets/paint-yellow.png" alt="" class="color" id="color-2">
            </div>

            <div class="color-choice" id="color-choice-3">
                <img src="/assets/circle-choice-paint.svg" alt="" class="circle-choice" @click="selectColor(3)"
                    id="circle-3">
                <img src="/assets/paint-white.png" alt="" class="color" id="color-3">
            </div>



        </div>
    </div>

    <img src="/assets/circle-head.svg" alt="" class="circle-head">
    <img src="/assets/sample-white-richard.png" alt="" class="richard">



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
    top: 173px;
    left: 711px;
}

.instruction {
    margin-top: 85px;
}

.color {
    pointer-events: none;
}

.circle-choice {
    cursor: pointer;
}

.color-choice {
    display: flex;
    align-items: center;
    justify-content: center;
    transition: 0.4s;
}

.color-choice,
.color,
.circle-choice {
    position: absolute;
}

.color-choice:hover {
    filter: invert();
    transition: 0.4s;

}

#color-choice-1 {
    top: 300px;
    left: 370px;
}

#color-choice-2 {
    top: 511px;
    left: 306px;
}

#color-choice-3 {
    top: 724px;
    left: 370px;
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

.palette {
    position: absolute;
    right: 0;
}

.peinture-debug {
    position: absolute;
    top:0px;
    left:0px;
    background-color: rgba(255, 0, 0, 0.3);
    padding: 10px;
}
</style>
