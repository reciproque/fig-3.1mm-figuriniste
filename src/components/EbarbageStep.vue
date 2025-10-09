<script setup>
import texts from '../../texts/interface.json'

const { language = "FR", step } = defineProps({
    language: {
        type: String,
        required: true
    },
    selectedArms: {
        type: Number,
        required: false,
    }
})

function getText(n, lang) {
    if (lang == "FR") return texts[n]["texte-FR"];
    if (lang == "EN") return texts[n]["texte-EN"];
    if (lang == "DE") return texts[n]["texte-DE"];
}

</script>

<template>
    <div class="ebarbage-screen">
        <div class="instruction">{{ getText(8, language) }}</div>
        <div class="randomizer-box">{{ getText(9, language) }}
            <br>
            <em>{{ getText(10, language) }}</em>
        </div>

    </div>
    <img src="../../assets/circle-head.svg" alt="" class="circle-head">
    <img src="../../assets/sample-armless-richard.png" alt="" class="richard">

    <div class="arms-choice" id="arms-choice-1">
        <img src="../../assets/circle-choice.svg" alt="" class="circle-choice">
        <img src="../../assets/sample-arm1.png" alt="" class="arms" id="arms-1">
    </div>

    <div class="arms-choice" id="arms-choice-2">
        <img src="../../assets/circle-choice.svg" alt="" class="circle-choice">
        <img src="../../assets/sample-arm1.png" alt="" class="arms" id="arms-2">
    </div>


    <div class="arms-choice" id="arms-choice-3">
        <img src="../../assets/circle-choice.svg" alt="" class="circle-choice">
        <img src="../../assets/sample-arm1.png" alt="" class="arms" id="arms-3">
    </div>


</template>

<style scoped>
.ebarbage-screen {
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
    top: 114px;
    left: 624px;

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

#arms-choice-1 {
    top: 300px;
    left: 200px;
}

#arms-choice-2 {
    top: 170px;
    right: 500px;
}

#arms-choice-3 {
    bottom: 480px;
    right: 700px;
}

.arms {
    top: -95px;
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
    font-family: 'Gotham';
    font-style: normal;
    font-size: 22px;
    font-weight: 500;
}
</style>
