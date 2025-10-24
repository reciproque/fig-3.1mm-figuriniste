<script setup>

import { gsap } from 'gsap';

import { ref, onMounted, defineEmits } from 'vue';

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

const emit = defineEmits(['finaleCombination']) 
let finale = '';


function selectColor(n) {

    gsap.from(document.getElementById("color-choice-"+n), { scale: 0.5, duration: 0.2, ease: "bounce.out" })
    
    if (step.value==0) peau = n;
    if (step.value==1) cheveux = n;
    if (step.value==2) robe = n;
    if (step.value==3) armoiries = n;

    //TODO : play la vidéo adéquate et afficher la couleur peinte... 
    
    step.value++;
    nextStep();

    document.querySelector(".peinture-debug").innerHTML = `ETAPE : ${step.value} 
    <br> Peau : ${peau} 
    <br> Cheveux : ${cheveux} 
    <br> Robe/Bouclier : ${robe} 
    <br> Cote de maille/Armoiries : ${armoiries} 
    `;

}

function skipPeinture() {
    emit('finaleCombination', '1111')
}


// TODO : nextStep doit aussi changer la vidéo de fond...

function nextStep() {
    
    // setTimeout(() => {
    //     gsap.from(document.querySelector(".palette"), { x: 200, rotateZ: 20, duration: 1 })}, 
    
    //     500);


    document.querySelector(".peinture-debug").innerHTML = `ETAPE : ${step.value} 
    <br> Peau : ${peau} 
    <br> Cheveux : ${cheveux} 
    <br> Robe/Bouclier : ${robe} 
    <br> Cote de maille/Armoiries : ${armoiries} 
    `;

    if (step.value==4) {
        finale = String(peau) + String(cheveux) + String(robe) + String(armoiries);
        setTimeout(() => emit('finaleCombination', finale), 500);
    }
}

onMounted(() => {
    // gsap.from(document.querySelector(".palette"), { x: 200, rotateZ: 20, duration: 1 })
    // gsap.from(document.querySelector(".assemblage-screen"), { opacity: 0, duration: 1})
})

</script>

<template>
    <div class="debug peinture-debug">
    ETAPE : {{ step }}
    <br>Peau : {{ peau }}
    <br> Cheveux :  {{ cheveux }}
    <br> Robe/Bouclier :  {{ robe }}
    <br> Cote de maille/Armoiries : {{ armoiries }}</div>
    <div class="peinture-screen">
        <div class="instruction">{{ instructions[step] }}</div>
        <div v-if="step==0" class="randomizer-box" @click="skipPeinture()">{{ skipText[0] }}
            <br>
            <em>{{ skipText[1] }}</em>
        </div>

        <div class="palette">
            <!-- <img src="/assets/palette.png" alt=""> -->
            <div class="color-choice" id="color-choice-1">
                <img src="/assets/circle-choice-paint.svg" alt="" class="circle-choice" @click="selectColor(1)"
                    id="circle-1">
                <img src="" alt="" class="color" id="color-1">
            </div>

            <div class="color-choice" id="color-choice-2">
                <img src="/assets/circle-choice-paint.svg" alt="" class="circle-choice" @click="selectColor(2)"
                    id="circle-2">
                <img src="" alt="" class="color" id="color-2">
            </div>

            <div class="color-choice" id="color-choice-3">
                <img src="/assets/circle-choice-paint.svg" alt="" class="circle-choice" @click="selectColor(3)"
                    id="circle-3">
                <img src="" alt="" class="color" id="color-3">
            </div>



        </div>
    </div>

</template>

<style scoped>
.peinture-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
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
    border: solid 3px red;
    scale: 0.9;
}

.color-choice:hover {
    filter: invert();
    transition: 0.4s;

}

#color-choice-1 {
    top: 560px;
    right: 300px;
}

#color-choice-2 {
    top: 720px;
    right: 410px;
}

#color-choice-3 {
    top: 900px;
    right: 400px;
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

/* .palette {
    position: absolute;
    right: 0;
} */


.peinture-debug {
    top:0px;
    left:0px;
 
}
</style>
