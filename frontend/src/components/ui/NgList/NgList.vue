<template>
  <v-list class="ng-list"
    v-bind="$attrs"
    v-model="innerValue"
    v-on="$listeners">
    <v-list-item v-for="(item, index) in items"
      class="ng-list__item"
      :key="index"
      :href="item.href">
      <v-list-item-title>{{item.title}}</v-list-item-title>
    </v-list-item>
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
};
</script>

<style lang="scss" scoped>
  .ng-list{
    &__item:hover{
      color: var(--v-primary-base);
    }
  }
</style>
