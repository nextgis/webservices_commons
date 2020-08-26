<template>
  <v-card class="ng-sheet" :class="sizeClasses"
    v-bind="$attrs"
    :style="cssStyles">
    <slot></slot>
  </v-card>
</template>

<script>
export default {

  name: 'NgSheet',
  props: {
    xl: {type: Boolean},
    lg: {type: Boolean},
    sm: {type: Boolean},
    xs: {type: Boolean},
    bgSrc: {type: String},
    bgPosition: {type: String}
  },
  data() {
    return {

    };
  },
  computed: {
    sizeClasses(){
      return{
        'ng-size--xs': this.xs,
        'ng-size--sm': this.sm,
        'ng-size--default':!this.xs && !this.sm && !this.lg && !this.xl,
        'ng-size--lg': this.lg,
        'ng-size--xl': this.xl,
      }
    },
    cssStyles() {
      //console.log(this.bgSrc);
      return {
        'background-image': this.bgSrc ? `url("${this.bgSrc}")` : 'none',
        'background-position': this.bgPosition || 'center center'
      }
    },
  },
  mounted() {
  }
};
</script>

<style lang="scss" scoped>
  .ng-sheet{

    background-image: var(--bg-image);

    &.ng-size--xl{
      padding: 32px;
    }
    &.ng-size--lg{
      padding: 24px;
    }

    &.ng-size--default{
      padding: 16px;
    }

    &.ng-size--sm{
      padding: 12px;
    }
    &.ng-size--xs{
      padding: 8px;
    }
  }
</style>
