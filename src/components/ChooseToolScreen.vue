<script setup>

import { onMounted, defineEmits, ref, nextTick, onUnmounted } from 'vue';

import { gsap } from 'gsap';


const { choiceInstruction, goodAnswer } = defineProps({
    choiceInstruction: {
        type: String,
        required: true
    },
    goodAnswer: {
        type: Number,
        required: true
    }
})

const emit = defineEmits(['touchedTool'])

// function beginChoiceListening() {
//     document.addEventListener('keyup', function (e) {
//         if (e.key === "1" || e.key === "2" || e.key === "3" || e.key === "4" || e.key === "5" || e.key === "6") {
//             if (e.key == goodAnswer) document.querySelector(".choice-debug").innerHTML = `Utilisez 1-2-3-4-5-6 sur le clavier <br> Outil touché : ${e.key} <br> (Bonne réponse : ${goodAnswer}) -> VRAI`
//             else document.querySelector(".choice-debug").innerHTML = `Utilisez 1-2-3-4-5-6 sur le clavier <br> Outil touché : ${e.key} <br> (Bonne réponse : ${goodAnswer}) -> FAUX`

//             emit('touchedTool', e.key);
//         }
//     });
// }

onMounted(() => {
    gsap.from(document.querySelector(".choix"), { opacity: 0, duration: 1 })
    // beginChoiceListening()
})

const hiddenInput = ref(null)
const value = ref('')

let locked = false;

function focusInput() {

    nextTick(() => {

        hiddenInput.value?.focus()
    })
}

function validate() {

    // bloque les doubles triggers
    if (locked) return

    const key = value.value.trim()

    if (!['1','2','3','4','5','6'].includes(key)) {

        value.value = ''
        focusInput()

        return
    }

    locked = true

    console.log('tool', key)

    emit('touchedTool', Number(key))

    value.value = ''

    focusInput()

    // délai anti double input
    setTimeout(() => {

        locked = false

    }, 800)
}

function handleTouch() {

    focusInput()
}

onMounted(() => {

    focusInput()

    document.addEventListener('touchstart', handleTouch)
    document.addEventListener('click', handleTouch)
})

onUnmounted(() => {

    document.removeEventListener('touchstart', handleTouch)
    document.removeEventListener('click', handleTouch)
})

</script>

<template>

        <input
        ref="hiddenInput"
        v-model="value"
        @keyup.enter="validate"
        style="
            position:absolute;
            opacity:0;
            pointer-events:none;
        "
    />
    <div class="debug choice-debug">Utilisez 1-2-3-4-5-6 sur le clavier <br> Outil touché : <br> (Bonne réponse) :
        {{ goodAnswer }} </div>

    <div class="choix">
        <div class="instruction">{{ choiceInstruction }}</div>
        <div class="arrow-row">
            <img src="/assets/main.png" alt="" class="main">
        </div>
        <div class="scrim"><img src="/assets/choix-scrim.svg" alt=""></div>

        <!-- <div class="touch-tools">
            <div class="touch-tools">
                                <img src="/assets/outils/06_Palette.png" alt="" class="outil" @click="simulateKeyPress('4')"
                    @touchend.prevent="simulateKeyPress('6')">

                                   <img src="/assets/outils/05_Lime.png" alt="" class="outil" @click="simulateKeyPress('2')"
                    @touchend.prevent="simulateKeyPress('5')">

                                    <img src="/assets/outils/03_Moule.png" alt="" class="outil" @click="simulateKeyPress('3')"
                    @touchend.prevent="simulateKeyPress('3')">

                                    <img src="/assets/outils/02_Ebauchoir.png" alt="" class="outil" @click="simulateKeyPress('1')"
                    @touchend.prevent="simulateKeyPress('2')">


                <img src="/assets/outils/04_Louche.png" alt="" class="outil" @click="simulateKeyPress('5')"
                    @touchend.prevent="simulateKeyPress('4')">

                <img src="/assets/outils/01_Criterium.png" alt="" class="outil" @click="simulateKeyPress('6')"
                    @touchend.prevent="simulateKeyPress('1')">

 

            </div>
        </div> -->
    </div>

</template>

<style scoped>
.touch-tools {
    display: flex;
    flex-direction: row;
    justify-content: center;
    width: 100%;
    position: absolute;
    bottom: 0;
}

.outil {
    width: 300px;
    cursor: pointer;
}

.choix {
    display: flex;
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
    opacity: 20%;
}

.arrow-row {
    animation: floating 2s infinite;
}


.choice-debug {
    top: 0px;
    left: 0px;
}

.main {
    animation: main-anim 10s infinite linear;
}

@keyframes main-anim {
    0% {
        opacity: 0;
        transform: translateX(-500px);
    }

    10% {
        opacity: 100%;
    }

    90% {
        opacity: 100%;
    }

    100% {
        opacity: 0;
        transform: translateX(500px);
    }

}

@keyframes floating {
    0% {
        transform: translateY(80px);
    }

    50% {
        transform: translateY(50px);
    }

    100% {
        transform: translateY(80px);
    }
}
</style>