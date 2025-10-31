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

const emit = defineEmits(['finaleCombination', 'chooseSkipPeinture'])
let finale = '';


function selectColor(n) {

    gsap.from(document.getElementById("color-" + n), { scale: 0.5, duration: 0.2, ease: "bounce.out" })

    if (step.value == 0) peau = n;
    if (step.value == 1) cheveux = n;
    if (step.value == 2) robe = n;
    if (step.value == 3) armoiries = n;

    // TODO : play la vidéo d'animation peinture par dessus

    nextStep();

}

function skipPeinture() {
    emit('chooseSkipPeinture', '1')
}


function nextStep() {

    if (step.value <= 4) {
        setTimeout(() => {
            gsap.from(document.querySelector(".palette-wrapper"), { x: 200, opacity: 0, rotateZ: 20, duration: 1 })
        },
            1000);
    }

    setTimeout(() => { step.value++ }, 1000);

    if (step.value == 3) {
        finale = String(peau) + String(cheveux) + String(robe) + String(armoiries);
        setTimeout(() => { emit('finaleCombination', finale) }, 1000);
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
    <div class="peinture-screen">
        <div class="instruction">{{ instructions[step] }}</div>
        <div v-if="step == 0" class="randomizer-box" @click="skipPeinture()">{{ skipText[0] }}
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
    top: 100px;

}

.peinture-debug {
    top: 0px;
    left: 0px;
}
</style>
