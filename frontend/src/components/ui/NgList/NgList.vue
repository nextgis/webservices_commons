<template>
  <v-list class="ng-list"
    v-bind="$attrs"
    v-model="innerValue"
    v-on="$listeners">
    <slot name="prepend"></slot>
    <v-list-item v-for="(item, index) in items"
      class="ng-list__item"
      :key="index"
      :href="item.href"
      :target="item.target || '_self'">
      <v-list-item-title>{{item.title}}</v-list-item-title>
    </v-list-item>
    <slot name="append"></slot>
  </v-list>
</template>

<script>
export default {

  name: 'NgList',
  props: {
    items: {
      type: Array,
      default: []
    }
  },
  data() {
    return {

    };
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
  .ng-list{
    &__item:hover{
      color: var(--v-primary-base);
    }
  }
</style>
