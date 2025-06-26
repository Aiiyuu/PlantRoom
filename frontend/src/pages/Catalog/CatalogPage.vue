<template>
    <div class="catalog flex flex-col">
        <p class="mb-8 " v-for="i in 25" :key="i">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Earum, id, totam. Accusamus ad alias beatae
            blanditiis culpa cum cupiditate debitis distinctio dolor dolorem dolorum earum eligendi enim eveniet ex id
            iusto laborum minima modi nam necessitatibus nemo nesciunt, nostrum nulla, officia officiis quas quibusdam,
            recusandae sequi sit suscipit ullam voluptas voluptatum? Ab architecto atque culpa deserunt doloremque earum
            error expedita hic id, itaque labore magni maiores minima nobis odit possimus quasi sapiente vero. Ab
            accusamus aliquam assumenda autem consectetur corporis culpa delectus fugiat in incidunt labore laudantium
            neque nostrum officia, omnis optio quasi repellendus sapiente sed soluta, ullam, ut voluptas!</p>
    </div>
</template>

<script lang="ts" setup>
import {useInventoryStore} from "@/stores/inventory"
import Plant from '@/types/PlantInterface'
</script>

<style lang="scss" scoped>
.catalog {
    @apply w-full min-h-screen p-8 md:px-16 flex justify-between;
}
</style>