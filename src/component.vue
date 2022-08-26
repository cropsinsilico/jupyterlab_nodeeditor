<template>
    <input :type="type || 'text'" :readonly="readonly" :value="value" @input="onChange($event)" @mousedown.stop />
</template>

<script setup lang="ts">
import { defineProps } from "vue";

const props = defineProps<{
    initial: number,
    readonly: boolean,
    emitter: any,
    ikey: string,
    type: string,
    change?: (value: number | string) => void,
    getData?: (ikey: string) => number,
    putData?: (ikey: string, value: number | string) => void
}>();

</script>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({

    data(): { value: number } {
        return {
            value: this.initial || 0,
        }
    },
    methods: {
        parse(value: any): number {
            return this.type === 'number' ? +value : value;
        },
        onChange(e: InputEvent) {
            const target = <HTMLInputElement>e.target;
            this.value = this.parse(target);
            this.update();
        },
        update() {
            if (this.ikey) {
                this.putData(this.ikey, this.value)
                this.change(this.value);
            }
            this.emitter.trigger('process');
        }
    },
    mounted() {
        this.value = this.getData(this.ikey);
    },
    initial: 0,
    type: 'number',
    value: 0
});
</script>


<style lang="sass" scoped>
input
  width: 100%
  border-radius: 30px
  background-color: white
  padding: 2px 6px
  border: 1px solid #999
  font-size: 110%
  width: 170px
</style>