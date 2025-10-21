<script setup>

import { onMounted, defineEmits } from 'vue';

import { gsap } from 'gsap';


const { choiceInstruction, goodAnswer} = defineProps({
    choiceInstruction: {
        type: String,
        required: true
    },
    goodAnswer: {
        type: Number,
        required:true
    }
})

const emit = defineEmits(['touchedTool']) 

// TODO : interfaçage avec Phidget !
// Function qui commence à écouter les touches clavier.
function beginChoiceListening() {
    document.addEventListener('keydown', function (e) {
        if (e.key === "1" || e.key === "2" || e.key === "3" || e.key === "4" || e.key === "5" || e.key === "6") document.getElementById("choix-fleche-" + e.key).style.filter = "invert()";
    });
    document.addEventListener('keyup', function (e) {
        if (e.key === "1" || e.key === "2" || e.key === "3" || e.key === "4" || e.key === "5" || e.key === "6") 
        {
            document.getElementById("choix-fleche-" + e.key).style.filter = "none";
            if (e.key == goodAnswer) document.querySelector(".choice-debug").innerHTML = `Utilisez 1-2-3-4-5-6 sur le clavier <br> Outil touché : ${e.key} <br> (Bonne réponse : ${goodAnswer}) -> VRAI`
            else document.querySelector(".choice-debug").innerHTML = `Utilisez 1-2-3-4-5-6 sur le clavier <br> Outil touché : ${e.key} <br> (Bonne réponse : ${goodAnswer}) -> FAUX`

            emit('touchedTool',  e.key);
        }
    });
}

onMounted(() => { 
    gsap.from(document.querySelector(".choix"), {opacity:0, duration:1})
    beginChoiceListening()
})

</script>

<template>
    <div class="debug choice-debug">Utilisez 1-2-3-4-5-6 sur le clavier <br> Outil touché :  <br> (Bonne réponse) : {{goodAnswer}} </div>

    <div class="choix">
        <div class="instruction">{{choiceInstruction}}</div>
        <div class="arrow-row">
            <img src="/assets/choix-fleche.png" alt="" id="choix-fleche-1">
            <img src="/assets/choix-fleche.png" alt="" id="choix-fleche-2">
            <img src="/assets/choix-fleche.png" alt="" id="choix-fleche-3">
            <img src="/assets/choix-fleche.png" alt="" id="choix-fleche-4">
            <img src="/assets/choix-fleche.png" alt="" id="choix-fleche-5">
            <img src="/assets/choix-fleche.png" alt="" id="choix-fleche-6">
        </div>
        <div class="scrim"><img src="/assets/choix-scrim.svg" alt=""></div>
    </div>

</template>

<style scoped>
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
}

.arrow-row {
    display: flex;
    flex-direction: row;
    gap: 150px;
}


.choice-debug {
    top:0px;
    left:0px;
}

</style>