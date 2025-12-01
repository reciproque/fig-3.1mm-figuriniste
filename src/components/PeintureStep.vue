<script setup>

import { gsap } from 'gsap';

import { ref, onMounted, defineEmits } from 'vue';

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
    },
    bras: {
        type: Number,
        required: false
    }
})

const step = ref(0);
const stepText = ref(0);
const showBox = ref(true);

const emit = defineEmits(['action', 'finaleCombination', 'chooseSkipPeinture'])
let finale = '';

let canClick = true;

function selectColor(n) {
    if (canClick) {
            canClick = false;

    gsap.from(document.getElementById("color-" + n), { scale: 0.5, duration: 0.2, ease: "bounce.out" })
    
    

    if (step.value == 0){
        peau = n;
        showBox.value = false;

    } 
    if (step.value == 1) {
        cheveux = n;
    }
    if (step.value == 2) {
        robe = n;
    }
    if (step.value == 3) {
        armoiries = n;
}
    
    const image = document.createElement("img");
    image.className = "animation-peinture";
    image.id = step.value;
    image.src = `assets/videos-pinceaux/${step.value}/${n}.gif`;
    document.querySelector(".anim-wrapper").appendChild(image);
    document.querySelector(".anim-wrapper").style.display = "block"


    if (step.value >0) {
        document.querySelector(".anim-wrapper").removeChild(document.getElementById(step.value-1))
    }        
    
    gsap.to(document.querySelector(".palette-wrapper"), { x: 200, opacity: 0, rotateZ: 20, duration: 1, delay:0.5 })


    setTimeout(()=>{nextStep()},2000);

    }


}

function skipPeinture() {
    emit('chooseSkipPeinture', '1')
}


function nextStep() {

    emit('action');

    if (step.value <= 4) {

        gsap.to(document.querySelector(".palette-wrapper"), { x: 0, opacity: 1, rotateZ: 0, duration: 1, delay:3})
        setTimeout(()=>{stepText.value++},3000);

    }

    let stepDelay = 2000;

    if (step.value == 0){
        stepDelay = 1000;
        setTimeout(()=>{document.querySelector(".anim-wrapper").style.display = "none"}, 4000);
    } 
    if (step.value == 1) {
        stepDelay = 200;
        setTimeout(()=>{document.querySelector(".anim-wrapper").style.display = "none"}, 4000);

    }
    if (step.value == 2) {
        stepDelay = 600;
        setTimeout(()=>{document.querySelector(".anim-wrapper").style.display = "none"}, 4000);

    }
    if (step.value == 3) {
        stepDelay = 600;
        setTimeout(()=>{document.querySelector(".anim-wrapper").style.display = "none"}, 4000);

}

    setTimeout(() => { 
        step.value++;  
        canClick=true; }, stepDelay);
 

    if (step.value == 3) {
        finale = String(peau) + String(cheveux) + String(robe) + String(armoiries);

        gsap.to(document.querySelector(".palette-wrapper"), { x: 0, opacity: 1, rotateZ: 0, duration: 1, delay:3})


        setTimeout(() => { emit('finaleCombination', finale) }, 3000);
    }
}

onMounted(() => {
    gsap.from(document.querySelector(".palette-wrapper"), { x: 200, opacity: 0, rotateZ: 20, duration: 1 })
})

</script>

<template>
    <div class="debug peinture-debug">
        ETAPE : {{ step }}
        <br>Bras : {{ bras }}
        <br>Peau : {{ peau }}
        <br> Cheveux : {{ cheveux }}
        <br> Robe/Bouclier : {{ robe }}
        <br> Cote de maille/Armoiries : {{ armoiries }}
    </div>

    <div class="anim-wrapper"></div>

    <div class="peinture-screen">
        <div class="instruction">{{ instructions[stepText] }}</div>
        <div v-if="showBox" class="randomizer-box" @click="skipPeinture()">{{ skipText[0] }}
            <br>
            <em>{{ skipText[1] }}</em>
        </div>

        <img class="white-richard" :src="'assets/figurine-blanche-bras' + bras + '.png'" alt="">

        <img v-if="step >= 1" class="peau" :src="'richards/bras' + bras + '/peau/' + peau + '.png'" alt="">
        <img v-if="step >= 2" class="cheveux" :src="'richards/bras' + bras + '/cheveux/' + cheveux + '.png'" alt="">
        <img v-if="step >= 3" class="robe" :src="'richards/bras' + bras + '/robe/' + robe + '.png'" alt="">
        <img v-if="step >= 4" class="armoiries" :src="'richards/bras' + bras + '/armoiries/' + armoiries + '.png'" alt="">

        <div class="palette-wrapper" v-if="step < 4">
            <img class="palette" src="/assets/palette.png" alt="">

            <!-- Peau -->
            <div class="step-0" v-if="step == 0">
                <img src="/assets/peinture-1-1.png" alt="" class="color" id="color-1" @click="selectColor(1)">
                <img src="/assets/peinture-1-2.png" alt="" class="color" id="color-2" @click="selectColor(2)">
                <img src="/assets/peinture-1-3.png" alt="" class="color" id="color-3" @click="selectColor(3)">
            </div>

            <!-- Cheveux -->
            <div class="step-1" v-if="step == 1">
                <img src="/assets/peinture-2-1.png" alt="" class="color" id="color-1" @click="selectColor(1)">
                <img src="/assets/peinture-2-3.png" alt="" class="color" id="color-2" @click="selectColor(2)">
                <img src="/assets/peinture-2-2.png" alt="" class="color" id="color-3" @click="selectColor(3)">
            </div>

            <!-- Robe -->
            <div class="step-2" v-if="step == 2">
                <img src="/assets/peinture-3-1.png" alt="" class="color" id="color-1" @click="selectColor(1)">
                <img src="/assets/peinture-3-2.png" alt="" class="color" id="color-2" @click="selectColor(2)">
                <img src="/assets/peinture-3-3.png" alt="" class="color" id="color-3" @click="selectColor(3)">
            </div>

            <!-- Armoiries -->
            <div class="step-2" v-if="step == 3">
                <img src="/assets/peinture-4-1.png" alt="" class="color" id="color-1" @click="selectColor(1)">
                <img src="/assets/peinture-4-2.png" alt="" class="color" id="color-2" @click="selectColor(2)">
                <img src="/assets/peinture-4-3.png" alt="" class="color" id="color-3" @click="selectColor(3)">
            </div>
        </div>
    </div>

</template>

<style scoped>

.anim-wrapper {
    position: absolute;
    width: 1920px;
    height: 1080px;
    top: 0;
    z-index: 100;
    pointer-events: none;
    display: flex;
}

.animation-peinture  img {
    image-rendering: optimizeSpeed;
    z-index: 1000;
    position: absolute;
}

.peinture-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.instruction {
    margin-top: 85px;
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
    z-index: 10;
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



.palette-wrapper {
    position: absolute;
    width: 1920px;
    height: 1080px;
}

.palette {
    position: absolute;
    pointer-events: none;
}

.color {
    position: absolute;
    cursor: pointer;
    z-index: 10;
    transition: 0.4s;

}

.color:hover {
    scale: 1.1;
    transition: 0.4s;

}

#color-1 {
    top: 400px;
    right: 400px;
}

#color-2 {
    top: 590px;
    right: 400px;
}

#color-3 {
    top: 760px;
    right: 300px;
}

.white-richard,
.peau,
.cheveux,
.robe,
.armoiries {
    position: absolute;
    pointer-events: none;
    top: 90px;
}

@keyframes appear {
    0% {
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
    
}

.peau,
.cheveux,
.robe,
.armoiries {
    opacity: 1;

    animation: appear 1s 1;
}

.peinture-debug {
    top: 0px;
    left: 0px;
}
</style>
