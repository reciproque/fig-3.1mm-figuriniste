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

let arm1init = [-670, 350];
let arm2init = [540, 115];
let arm3init = [330, 640];

let arm1final = [-233.5, 487.5];
let arm2final = [-274.5, 153.5];
let arm3final = [-268, 445];

let canClick = true;

function startDrag(e, n) {
    e.preventDefault();

    const arm = document.getElementById("arms-" + n);
    arm.style.position = "absolute";

    document.getElementById("circle-"+n).style.opacity = "0.5";

    function moveAt(event) {
        let x, y;

        if (event.type.startsWith('touch')) {
            const touch = event.touches[0];
            x = touch.pageX;
            y = touch.pageY;
        } else {
            x = event.clientX;
            y = event.clientY;
        }

        let xOffset;
        let yOffset;

        if (n==1) {
            xOffset = 227/2;
            yOffset = 455/2;
        }

        if (n==2) {
            xOffset = 217/2;
            yOffset = 405/2;
        }
        if (n==3) {
            xOffset = 226/2;
            yOffset = 208*2;
        }

        arm.style.left = (x - 1920/2 - xOffset) + "px";
        arm.style.top = (y - 1080/2 + yOffset) + "px";

    }

    function stopDrag() {
        document.getElementById("circle-"+n).style.opacity = "1";

        document.removeEventListener('mousemove', moveAt);
        document.removeEventListener('mouseup', stopDrag);
        document.removeEventListener('touchmove', moveAt);
        document.removeEventListener('touchend', stopDrag);

        let xfinal = Number(arm.style.left.replace(/px$/, ''));

        // RICHARD OK
        if (xfinal >= -400 && xfinal <= 100) {
            canClick = false;
            if (n==1) {
                arm.style.left = arm1final[0]+"px";
                arm.style.top = arm1final[1]+"px";
            }
            if (n==2) {
                arm.style.left = arm2final[0]+"px";
                arm.style.top = arm2final[1]+"px";
            }
            if (n==3) {
                arm.style.left = arm3final[0]+"px";
                arm.style.top = arm3final[1]+"px";
            }

        setTimeout(() => emit('chosenArm', n), 50);
        }
        // Retour position initiale
        else {
            if (n==1) {
                arm.style.left = arm1init[0]+"px";
                arm.style.top = arm1init[1]+"px";
            }
            if (n==2) {
                arm.style.left = arm2init[0]+"px";
                arm.style.top = arm2init[1]+"px";
            }
            if (n==3) {
                arm.style.left = arm3init[0]+"px";
                arm.style.top = arm3init[1]+"px";
            }
        }
    }
    if (canClick) {

        document.addEventListener('mousemove', moveAt);
        document.addEventListener('mouseup', stopDrag);
        document.addEventListener('touchmove', moveAt);
        document.addEventListener('touchend', stopDrag);
        
        moveAt(e);
    }
}

onMounted(() => {
    gsap.from(document.querySelector(".assemblage-screen"), { opacity: 0, duration: 1 })
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

    <div class="debug-hitbox"></div>

    <div class="arms-choice" id="arms-choice-1">
        <img src="/assets/circle-choice.svg" alt="" class="circle-choice"id="circle-1">
        <img src="/assets/bras1.png" alt="" class="arms" id="arms-1"  @touchstart="startDrag($event, 1)" @mousedown="startDrag($event, 1)" >
    </div>

    <div class="arms-choice" id="arms-choice-2">
        <img src="/assets/circle-choice.svg" alt="" class="circle-choice"  id="circle-2">
        <img src="/assets/bras2.png" alt="" class="arms" id="arms-2" @touchstart="startDrag($event, 2)" @mousedown="startDrag($event, 2)">
    </div>


    <div class="arms-choice" id="arms-choice-3">
        <img src="/assets/circle-choice.svg" alt="" class="circle-choice" id="circle-3">
        <img src="/assets/bras3.png" alt="" class="arms" id="arms-3"  @touchstart="startDrag($event, 3)" @mousedown="startDrag($event, 3)">
    </div>


</template>

<style scoped>
.debug-hitbox {
    position: absolute;
    top: 300px;
    width: 400px;
    height: 700px;
}

.assemblage-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.instruction {
    margin-top: 85px;
}

.arms {
    position: absolute;
}

.circle-choice {
    cursor: pointer;

}

#arms-1 {
   left: -670px;
   top: 350px;
}

#circle-1 {
   left: -750px;
   top : 350px;
}

#arms-2 {
   left: 540px;
   top: 115px;
}

#circle-2 {
   left: 480px;
   top: 120px;
}

#arms-3 {
   left: 330px;
   top: 640px;
}

#circle-3 {
   left: 250px;
   top: 530px;
}

.arms-choice,
.arms,
.circle-choice {
    position: absolute;
    -webkit-user-drag: none;
    user-select: none;
    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
}

.arms-choice {
    display: flex;
    justify-content: center;
    align-items: center;
}

.randomizer-box {
    display: none;
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
