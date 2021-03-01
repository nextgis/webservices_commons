<template>
  <v-tabs class="ng-tabs"
    v-bind="$attrs"
    v-model="innerValue"
    v-on="$listeners">
    <v-tabs-slider></v-tabs-slider>
    <v-tab class="ng-tabs__item" v-for="item in items"
      ripple :key="item.key" :href="item.href"> {{ item.text }}
    </v-tab>
  </v-tabs>
</template>

<script>
export default {
  name: 'NgTabs',
  props: {
    items: { type: Array },
    value: { type: String }
  },
  computed: {
    innerValue: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      }
    }
  }
};
</script>

<style lang="scss" scoped>
  .ng-tabs{
    font-family: $heading-font-family;

    .ng-tabs__item{
      border-bottom: 0;
    }
  }
</style>