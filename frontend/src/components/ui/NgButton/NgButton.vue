<template>
  <v-btn class="ng-button" v-bind="$attrs">
    <v-icon v-if="iconName && iconPosition==='left'"
      class="ng-button__icon ng-button__icon--left">{{ iconName }}</v-icon>
    <slot></slot>
    <v-icon v-if="iconName && iconPosition==='right'"
      class="ng-button__icon ng-button__icon--right">{{ iconName }}</v-icon>
  </v-btn>
</template>

<script>
export default {
  name: 'NgButton',
  props: {
    iconName: { type: String },
    iconPosition: { type: String }
  },
  data() {
    return {

    };
  },
};
</script>

<style lang="scss" scoped>
  .ng-button{
    font-family: $heading-font-family;

    &.v-size--x-large{
      padding-left: 32px;
      padding-right: 32px;
    }

    &__icon{
      opacity: .8;

      &--left{
        margin-left: -4px;
        margin-right: 4px;
      }

      &--right{
        margin-left: 4px;
        margin-right: -4px;
      }
    }

    &:not(.v-btn--depressed):not(.v-btn--flat){
      box-shadow: 0 1px 2px rgba(0, 0, 0, .24)
    }
  }
</style>
