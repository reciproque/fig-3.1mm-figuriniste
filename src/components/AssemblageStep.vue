<script setup>
import { gsap } from 'gsap';

import { onMounted, defineEmits } from 'vue';


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

const emit = defineEmits(['chosenArm']) 

let canClick = true;

function selectArms(n) {
    if (canClick) {
        gsap.from(document.getElementById("circle-"+n), { scale: 0.9, duration: 1, ease: "bounce.out" })
        if(n==1) gsap.to(document.getElementById("arms-"+n), {x:500, duration:0.2})
        if(n==2) gsap.to(document.getElementById("arms-"+n), {x:-800, duration:0.2})
        if(n==3) gsap.to(document.getElementById("arms-"+n), {x:-600,y:-300, duration:0.2})

        setTimeout(() => emit('chosenArm', n), 1500);

    }
    canClick=false;



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

    <div class="arms-choice" id="arms-choice-1">
        <img src="/assets/circle-choice.svg" alt="" class="circle-choice" @click="selectArms(1)" id="circle-1">
        <img src="/assets/bras1.png" alt="" class="arms" id="arms-1">
    </div>

    <div class="arms-choice" id="arms-choice-2">
        <img src="/assets/circle-choice.svg" alt="" class="circle-choice" @click="selectArms(2)" id="circle-2">
        <img src="/assets/bras2.png" alt="" class="arms" id="arms-2">
    </div>


    <div class="arms-choice" id="arms-choice-3">
        <img src="/assets/circle-choice.svg" alt="" class="circle-choice" @click="selectArms(3)" id="circle-3">
        <img src="/assets/bras3.png" alt="" class="arms" id="arms-3">
    </div>


</template>

<style scoped>
.assemblage-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
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

#arms-choice-1 .circle-choice {
    left: -300px;
}

#arms-choice-2 .circle-choice {
    top: -400px;
    left: -300px;
}


#arms-choice-3 .circle-choice {
    top: -280px;
    left: -300px;
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

.arms-choice {
    display: flex;
    justify-content: center;
    align-items: center;
}

#arms-choice-1 {
    top: 730px;
    left: 460px;
}

#arms-choice-2 {
    top:  730px;
    left: 1760px;
}

#arms-choice-3 {
    top: 1030px;
    left: 1560px;
}

/* .arms {
    border: solid 10px #3959D0;
} */

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
