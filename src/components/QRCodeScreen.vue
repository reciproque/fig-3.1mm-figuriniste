<script setup>

import { gsap } from 'gsap';

import { onMounted } from 'vue';


defineProps({
    instruction: {
        type: String,
        required: false
    },
    combination: {
        type: String,
        required: false
    }
})

function reloadApp() {
    location.reload();
}

onMounted(() => {
    gsap.from(document.querySelector(".star"), { opacity: 0, delay: 0, scale: 0.95, duration: 1 })
    gsap.from(document.querySelector(".shadow"), { opacity: 0, delay: 0.1, scale: 0.95, duration: 1 })
    //gsap.from(document.querySelector(".richard"), { opacity: 0, delay: 0.2, scale: 0.95, duration: 1 })
    gsap.from(document.querySelector(".light"), { opacity: 0, delay: 0.7, scale: 0.95, duration: 1 })

    gsap.from(document.querySelector(".qr-wrapper"), { opacity: 0, delay: 0.8, scale: 0.95, duration: 1 })

    gsap.from(document.querySelector(".bloc-instruction"), { opacity: 0, delay: 0, duration: 1 })

})


</script>

<template>
    <div class="retry" @click="reloadApp()">↺ Recommencer</div>

    <div class="qr-screen">

        <div class="bloc-instruction">{{ instruction }}</div>
        <div class="debug combination-txt">Richard N° {{ combination }}</div>

        <div class="qr-wrapper">
            <div class="circle"></div>
            <img class="qr-code" :src="'richards/qrcodes/' + combination + '.png'" alt="">
        </div>

        <img class="richard" :src="'richards/resultats/' + combination + '.png'" alt="">
        <div class="shadow"></div>
        <img class="star" src="/assets/star.png" alt="">
        <img class="light" src="/assets/light.png" alt="">


    </div>

</template>

<style scoped>
.retry {
    z-index: 100;
    position: absolute;
    font-family: 'Gotham-Bold';
    background-color: #F5F7FB;
    padding: 32px 40px;
    color: #0E0E0B;
    text-align: center;
    font-size: 24px;
    font-weight: 300;
    top: 400px;
    left: 100px;
    border-radius: 50px;
    cursor: pointer;
    transition: 0.4s;

}

.retry:hover {
    scale: 1.1;
    transition: 0.4s;
}

.qr-screen {
    z-index: 20;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.bloc-instruction {
    font-family: 'Gotham-Bold';
    position: absolute;
    bottom: 0;
    background-color: #F5F7FB;
    padding: 32px 40px;
    color: #0E0E0B;
    text-align: center;
    font-size: 24px;
    font-weight: 300;
    border-radius: 40px 40px 0 0;
}

.combination-txt {
    position: absolute;
    top: 300px;
    font-family: 'Gotham-Bold';
    font-size: 24px;
    right: 200px;
}

.qr-wrapper {
    position: absolute;
    top: 400px;
    right: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.qr-code {
    position: absolute;

}

.circle {
    width: 400px;
    height: 400px;
    background-color: rgb(255, 255, 255);
    border-radius: 200px;
}

.richard {
    position: absolute;
    top: 90px;
    /* animation: richard 5s infinite; */
}

@keyframes richard {
    0% {
        rotate: 2deg;
    }

    50% {
        rotate: -2deg;
    }

    100% {
        rotate: 2deg;
    }

}

.shadow {
    z-index: -30;
    width: 300px;
    height: 400px;
    background-color: hsla(0, 0%, 100%, 0.5);
    border-radius: 50px;
    filter: blur(200px);
    position: absolute;
    top: 400px;
}

.star {
    z-index: -10;
    position: absolute;
    top: 200px;
    animation: star 60s infinite linear;
    -webkit-mask: linear-gradient(135deg,#000c 40%,#000,#000c 60%) 100% 100%/250% 250%;
    mask: linear-gradient(135deg,#000c 40%,#000,#000c 60%) 100% 100%/250% 250%;
}


.light {
    z-index: -31;
    position: absolute;
    opacity: 0.1;
    filter: blur(5px);

    animation: star 120s infinite linear;

}

@keyframes star {
    0% {
        rotate: 0deg;
        
    }

    25% {
    -webkit-mask-position: 0 0;
      mask-position: 0 0;
    }

    100% {
        rotate: 360deg;
    }

}
</style>
