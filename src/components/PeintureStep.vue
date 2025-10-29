<script setup>

import { gsap } from 'gsap';

import { ref, onMounted, defineEmits } from 'vue';

let bras = 3;

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

const step = ref(0);

const emit = defineEmits(['finaleCombination', 'nextStep', 'chooseSkipPeinture']) 
let finale = '';


function selectColor(n) {

    gsap.from(document.getElementById("color-"+n), { scale: 0.5, duration: 0.2, ease: "bounce.out" })
    
    if (step.value==0) peau = n;
    if (step.value==1) cheveux = n;
    if (step.value==2) robe = n;
    if (step.value==3) armoiries = n;

    //TODO : play la vidéo adéquate et afficher la couleur peinte... 
    
    nextStep();

    document.querySelector(".peinture-debug").innerHTML = `ETAPE : ${step.value} 
    <br> Peau : ${peau} 
    <br> Cheveux : ${cheveux} 
    <br> Robe/Bouclier : ${robe} 
    <br> Cote de maille/Armoiries : ${armoiries} 
    `;

}

function skipPeinture() {
    emit('chooseSkipPeinture', '1')
}


// TODO : nextStep doit aussi changer la vidéo de fond...

function nextStep() {
    
    // setTimeout(() => {
    //     gsap.from(document.querySelector(".palette"), { x: 200, rotateZ: 20, duration: 1 })}, 
    //     500);

    //emit('nextStep', 1);
    setTimeout(()=>{step.value++},1000);


    document.querySelector(".peinture-debug").innerHTML = `ETAPE : ${step.value} 
    <br> Peau : ${peau} 
    <br> Cheveux : ${cheveux} 
    <br> Robe/Bouclier : ${robe} 
    <br> Cote de maille/Armoiries : ${armoiries} 
    `;
    console.log(step.value);

    if (step.value==3) {
        finale = String(peau) + String(cheveux) + String(robe) + String(armoiries);
        //emit('finaleCombination', finale);
    }
}

onMounted(() => {
    gsap.from(document.querySelector(".palette-wrapper"), { x: 200, rotateZ: 20, duration: 1 })
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

        <img class="white-richard" :src="'assets/figurine-blanche-bras'+bras+'.png'" alt="">

        <img v-if="step>=1" class="peau" :src="'richards/bras'+bras+'/peau/'+peau+'.png'" alt="">
        <img v-if="step>=2" class="cheveux" :src="'richards/bras'+bras+'/cheveux/'+cheveux+'.png'" alt="">
        <img v-if="step>=3" class="robe" :src="'richards/bras'+bras+'/robe/'+robe+'.png'" alt="">
        <img v-if="step>=4"class="armoiries" :src="'richards/bras'+bras+'/armoiries/'+armoiries+'.png'" alt="">



        
        <div class="palette-wrapper">
            <img class="palette" src="/assets/palette.png" alt="">

        <!-- Peau -->
        <div class="step-0" v-if="step==0">
            <img src="/assets/peinture-1-1.png" alt="" class="color" id="color-1"  @click="selectColor(1)">
            <img src="/assets/peinture-1-2.png" alt="" class="color" id="color-2"  @click="selectColor(2)">
            <img src="/assets/peinture-1-3.png" alt="" class="color" id="color-3"  @click="selectColor(3)">
        </div>

        <!-- Cheveux -->
        <div class="step-1" v-if="step==1">
            <img src="/assets/peinture-2-1.png" alt="" class="color" id="color-1"  @click="selectColor(1)">
            <img src="/assets/peinture-2-3.png" alt="" class="color" id="color-2"  @click="selectColor(2)">
            <img src="/assets/peinture-2-2.png" alt="" class="color" id="color-3"  @click="selectColor(3)">
        </div>

        <!-- Robe -->
        <div class="step-2" v-if="step==2">
            <img src="/assets/peinture-3-1.png" alt="" class="color" id="color-1"  @click="selectColor(1)">
            <img src="/assets/peinture-3-2.png" alt="" class="color" id="color-2"  @click="selectColor(2)">
            <img src="/assets/peinture-3-3.png" alt="" class="color" id="color-3"  @click="selectColor(3)">
        </div>

        <!-- Armoiries -->
        <div class="step-2" v-if="step==3">
            <img src="/assets/peinture-4-1.png" alt="" class="color" id="color-1"  @click="selectColor(1)">
            <img src="/assets/peinture-4-2.png" alt="" class="color" id="color-2"  @click="selectColor(2)">
            <img src="/assets/peinture-4-3.png" alt="" class="color" id="color-3"  @click="selectColor(3)">
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

.white-richard, .peau, .cheveux, .robe, .armoiries {
    position: absolute;
    pointer-events: none;
    top:100px;

}

.peinture-debug {
    top:0px;
    left:0px;
}


</style>
