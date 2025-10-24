<script setup>

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


</script>

<template>
<div class="qr-screen">     

   <div class="bloc-instruction">{{ instruction }}</div>
    <div class="qr-code">Richard N° {{ combination }}</div>
</div>

</template>

<style scoped>
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

.qr-code {
    position: absolute;
    top: 300px;
    font-family: 'Gotham-Bold';
    font-size: 24px;
    right: 200px;

}
</style>
